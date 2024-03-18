from constants.qr_pay import Provider, AdditionalData, Consumer, Merchant, QRProvider, QRProviderGUID, FieldID, ProviderFieldID, VietQRService, VietQRConsumerFieldID, AdditionalDataID

class QRPay:
    def __init__(self, content):
        self.content = content
        self.isValid = True
        self.provider = Provider()
        self.consumer = Consumer()
        self.merchant = Merchant()
        self.additionalData = AdditionalData()
        self.category = ''
        self.tipAndFeeType = ''
        self.tipAndFeeAmount = ''
        self.tipAndFeePercent = ''
        self.city = ''
        self.zipCode = ''
    @staticmethod
    def crc16ccitt(s):
        crc = 0xFFFF
        for char in s:
            crc ^= ord(char) << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
        return crc & 0xFFFF

    def build(self):
        version = QRPay.genFieldData(FieldID['VERSION'], getattr(self, 'version', '01'))
        initMethod = QRPay.genFieldData(FieldID['INIT_METHOD'], getattr(self, 'initMethod', '11'))
        guid = QRPay.genFieldData(ProviderFieldID['GUID'], self.provider.guid)
        providerDataContent = f"{QRPay.genFieldData(VietQRConsumerFieldID['BANK_BIN'], self.consumer.bankBin)}{QRPay.genFieldData(VietQRConsumerFieldID['BANK_NUMBER'], self.consumer.bankNumber)}" if self.provider.guid == QRProviderGUID['VIETQR'] else (self.merchant.id if self.provider.guid == QRProviderGUID['VNPAY'] else '')
        provider = QRPay.genFieldData(ProviderFieldID['DATA'], providerDataContent)
        service = QRPay.genFieldData(ProviderFieldID['SERVICE'], self.provider.service)
        providerData = QRPay.genFieldData(self.provider.fieldId, guid + provider + service)
        fields = [
            [FieldID['CATEGORY'], self.category],
            [FieldID['CURRENCY'], getattr(self, 'currency', '704')],
            [FieldID['AMOUNT'], self.amount],
            [FieldID['TIP_AND_FEE_TYPE'], self.tipAndFeeType],
            [FieldID['TIP_AND_FEE_AMOUNT'], self.tipAndFeeAmount],
            [FieldID['TIP_AND_FEE_PERCENT'], self.tipAndFeePercent],
            [FieldID['NATION'], getattr(self, 'nation', 'VN')],
            [FieldID['MERCHANT_NAME'], self.merchant.name],
            [FieldID['CITY'], self.city],
            [FieldID['ZIP_CODE'], self.zipCode]
        ]
        additionalDataFields = [
            [AdditionalDataID['BILL_NUMBER'], self.additionalData.billNumber],
            [AdditionalDataID['MOBILE_NUMBER'], self.additionalData.mobileNumber],
            [AdditionalDataID['STORE_LABEL'], self.additionalData.store],
            [AdditionalDataID['LOYALTY_NUMBER'], self.additionalData.loyaltyNumber],
            [AdditionalDataID['REFERENCE_LABEL'], self.additionalData.reference],
            [AdditionalDataID['CUSTOMER_LABEL'], self.additionalData.customerLabel],
            [AdditionalDataID['TERMINAL_LABEL'], self.additionalData.terminal],
            [AdditionalDataID['PURPOSE_OF_TRANSACTION'], self.additionalData.purpose],
            [AdditionalDataID['ADDITIONAL_CONSUMER_DATA_REQUEST'], self.additionalData.dataRequest]
        ]
        categoryFields = ''.join(QRPay.genFieldData(id, value) for id, value in fields)
        additionalDataContent = ''.join(QRPay.genFieldData(id, value) for id, value in additionalDataFields)
        additionalData = QRPay.genFieldData(FieldID['ADDITIONAL_DATA'], additionalDataContent)
        content = f"{version}{initMethod}{providerData}{categoryFields}{additionalData}{FieldID['CRC']}04"
        crc = QRPay.genCRCCode(content)
        return content + crc

    @staticmethod
    def initQR(options, providerType):
        if providerType.lower() not in ['vietqr', 'vnpay']:
            raise TypeError('Chỉ có 2 loại đó là: vietqr, vnpay')
        qr = QRPay(None)
        isVietQR = providerType.lower() == 'vietqr'
        qr.provider.fieldId = FieldID['VIETQR'] if isVietQR else FieldID['VNPAYQR']
        qr.provider.guid = QRProviderGUID['VIETQR'] if isVietQR else QRProviderGUID['VNPAY']
        qr.provider.name = QRProvider['VIETQR'] if isVietQR else QRProvider['VNPAY']
        if isVietQR:
            qr.provider.service = options.get('service', VietQRService['BY_ACCOUNT_NUMBER'])
            qr.consumer.bankBin = options['bankBin']
            qr.consumer.bankNumber = options['bankNumber']
        else:
            qr.merchant.id = options.get('merchantId', '')
            qr.merchant.name = options.get('merchantName', '')
        qr.amount = options.get('amount', '')
        qr.additionalData.purpose = options.get('description', options.get('purpose', ''))
        qr.additionalData.billNumber = options.get('billNumber', '')
        qr.additionalData.mobileNumber = options.get('mobileNumber', '')
        qr.additionalData.store = options.get('store', '')
        qr.additionalData.terminal = options.get('terminal', '')
        qr.additionalData.loyaltyNumber = options.get('loyaltyNumber', '')
        qr.additionalData.reference = options.get('reference', '')
        qr.additionalData.customerLabel = options.get('customerLabel', '')
        return qr

    @staticmethod
    def verifyCRC(content):
        checkContent = content[:-4]
        crcCode = content[-4:].upper()
        genCrcCode = QRPay.genCRCCode(checkContent)
        return crcCode == genCrcCode

    @staticmethod
    def genCRCCode(content):
        return format(QRPay.crc16ccitt(content), '04X')

    @staticmethod
    def sliceContent(content):
        id = content[:2]
        length = int(content[2:4])
        value = content[4:4 + length]
        nextValue = content[4 + length:]
        return id, length, value, nextValue

    @staticmethod
    def genFieldData(id, value):
        fieldId = id if id is not None else ''
        fieldValue = value if value is not None else ''
        idLen = len(fieldId)
        if idLen != 2 or len(fieldValue) <= 0:
            return ''
        length = str(len(fieldValue)).zfill(2)
        return f"{fieldId}{length}{fieldValue}"
