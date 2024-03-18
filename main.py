from constants.qr_pay import (
    Provider,
    AdditionalData,
    Consumer,
    Merchant,
    QRProvider,
    QRProviderGUID,
    FieldID,
    ProviderFieldID,
    VietQRService,
    VietQRConsumerFieldID,
    AdditionalDataID,
)


class QRPay:
    def __init__(self, content=None):
        self.content = content
        self.isValid = True
        self.provider = Provider()
        self.consumer = Consumer()
        self.merchant = Merchant()
        self.additionalData = AdditionalData()
        self.category = ""
        self.tipAndFeeType = ""
        self.tipAndFeeAmount = ""
        self.tipAndFeePercent = ""
        self.city = ""
        self.zipCode = ""

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
        version = self.genFieldData(FieldID["VERSION"], getattr(self, "version", "01"))
        initMethod = self.genFieldData(
            FieldID["INIT_METHOD"], getattr(self, "initMethod", "11")
        )

        provider_data_content = ""
        if self.provider.guid == QRProviderGUID["VIETQR"]:
            provider_data_content = self.genFieldData(
                VietQRConsumerFieldID["BANK_BIN"], self.consumer.bankBin
            ) + self.genFieldData(
                VietQRConsumerFieldID["BANK_NUMBER"], self.consumer.bankNumber
            )
        elif self.provider.guid == QRProviderGUID["VNPAY"]:
            provider_data_content = self.merchant.id

        provider_data = self.genFieldData(
            self.provider.fieldId,
            self.genFieldData(ProviderFieldID["GUID"], self.provider.guid)
            + self.genFieldData(ProviderFieldID["DATA"], provider_data_content)
            + self.genFieldData(ProviderFieldID["SERVICE"], self.provider.service),
        )

        fields = {
            FieldID["CATEGORY"]: self.category,
            FieldID["CURRENCY"]: getattr(self, "currency", "704"),
            FieldID["AMOUNT"]: self.amount,
            FieldID["TIP_AND_FEE_TYPE"]: self.tipAndFeeType,
            FieldID["TIP_AND_FEE_AMOUNT"]: self.tipAndFeeAmount,
            FieldID["TIP_AND_FEE_PERCENT"]: self.tipAndFeePercent,
            FieldID["NATION"]: getattr(self, "nation", "VN"),
            FieldID["MERCHANT_NAME"]: self.merchant.name,
            FieldID["CITY"]: self.city,
            FieldID["ZIP_CODE"]: self.zipCode,
        }

        category_fields = "".join(
            self.genFieldData(id, value) for id, value in fields.items()
        )

        additional_data_fields = {
            AdditionalDataID["BILL_NUMBER"]: self.additionalData.billNumber,
            AdditionalDataID["MOBILE_NUMBER"]: self.additionalData.mobileNumber,
            AdditionalDataID["STORE_LABEL"]: self.additionalData.store,
            AdditionalDataID["LOYALTY_NUMBER"]: self.additionalData.loyaltyNumber,
            AdditionalDataID["REFERENCE_LABEL"]: self.additionalData.reference,
            AdditionalDataID["CUSTOMER_LABEL"]: self.additionalData.customerLabel,
            AdditionalDataID["TERMINAL_LABEL"]: self.additionalData.terminal,
            AdditionalDataID["PURPOSE_OF_TRANSACTION"]: self.additionalData.purpose,
            AdditionalDataID[
                "ADDITIONAL_CONSUMER_DATA_REQUEST"
            ]: self.additionalData.dataRequest,
        }

        additional_data_content = "".join(
            self.genFieldData(id, value) for id, value in additional_data_fields.items()
        )
        additional_data = self.genFieldData(
            FieldID["ADDITIONAL_DATA"], additional_data_content
        )
        content = f"{version}{initMethod}{provider_data}{category_fields}{additional_data}{FieldID['CRC']}04"
        crc = self.genCRCCode(content)
        return content + crc

    @staticmethod
    def initQR(options, provider_type):
        provider_type_lower = provider_type.lower()
        if provider_type_lower not in ["vietqr", "vnpay"]:
            raise TypeError("Chỉ có 2 loại đó là: vietqr, vnpay")
        qr = QRPay()
        qr.provider.fieldId = FieldID[
            "VIETQR" if provider_type_lower == "vietqr" else "VNPAYQR"
        ]
        qr.provider.guid = QRProviderGUID[
            "VIETQR" if provider_type_lower == "vietqr" else "VNPAY"
        ]
        qr.provider.name = QRProvider[
            "VIETQR" if provider_type_lower == "vietqr" else "VNPAY"
        ]
        if provider_type_lower == "vietqr":
            qr.provider.service = options.get(
                "service", VietQRService["BY_ACCOUNT_NUMBER"]
            )
            qr.consumer.bankBin = options["bankBin"]
            qr.consumer.bankNumber = options["bankNumber"]
        else:
            qr.merchant.id = options.get("merchantId", "")
            qr.merchant.name = options.get("merchantName", "")
        qr.amount = options.get("amount", "")
        qr.additionalData.purpose = options.get(
            "description", options.get("purpose", "")
        )
        qr.additionalData.billNumber = options.get("billNumber", "")
        qr.additionalData.mobileNumber = options.get("mobileNumber", "")
        qr.additionalData.store = options.get("store", "")
        qr.additionalData.terminal = options.get("terminal", "")
        qr.additionalData.loyaltyNumber = options.get("loyaltyNumber", "")
        qr.additionalData.reference = options.get("reference", "")
        qr.additionalData.customerLabel = options.get("customerLabel", "")
        return qr

    @staticmethod
    def verifyCRC(content):
        check_content = content[:-4]
        crc_code = content[-4:].upper()
        gen_crc_code = QRPay.genCRCCode(check_content)
        return crc_code == gen_crc_code

    @staticmethod
    def genCRCCode(content):
        return format(QRPay.crc16ccitt(content), "04X")

    @staticmethod
    def genFieldData(identifier, value):
        field_id = identifier if identifier is not None else ""
        field_value = value if value is not None else ""
        id_len = len(field_id)
        if id_len != 2 or len(field_value) <= 0:
            return ""
        length = str(len(field_value)).zfill(2)
        return f"{field_id}{length}{field_value}"
