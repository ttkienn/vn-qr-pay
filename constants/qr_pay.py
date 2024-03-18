class Provider:
    def __init__(self):
        self.fieldId = None
        self.name = None
        self.guid = None
        self.service = None

class AdditionalData:
    def __init__(self):
        self.billNumber = None
        self.mobileNumber = None
        self.store = None
        self.loyaltyNumber = None
        self.reference = None
        self.customerLabel = None
        self.terminal = None
        self.purpose = None
        self.dataRequest = None

class Consumer:
    def __init__(self):
        self.bankBin = None
        self.bankNumber = None

class Merchant:
    def __init__(self):
        self.id = None
        self.name = None

QRProvider = {
    'VIETQR': 'VIETQR',
    'VNPAY': 'VNPAY'
}

QRProviderGUID = {
    'VNPAY': 'A000000775',
    'VIETQR': 'A000000727'
}

FieldID = {
    'VERSION': '00',
    'INIT_METHOD': '01',
    'VNPAYQR': '26',
    'VIETQR': '38',
    'CATEGORY': '52',
    'CURRENCY': '53',
    'AMOUNT': '54',
    'TIP_AND_FEE_TYPE': '55',
    'TIP_AND_FEE_AMOUNT': '56',
    'TIP_AND_FEE_PERCENT': '57',
    'NATION': '58',
    'MERCHANT_NAME': '59',
    'CITY': '60',
    'ZIP_CODE': '61',
    'ADDITIONAL_DATA': '62',
    'CRC': '63'
}

ProviderFieldID = {
    'GUID': '00',
    'DATA': '01',
    'SERVICE': '02'
}

VietQRService = {
    'BY_ACCOUNT_NUMBER': 'QRIBFTTA',
    'BY_CARD_NUMBER': 'QRIBFTTC'
}

VietQRConsumerFieldID = {
    'BANK_BIN': '00',
    'BANK_NUMBER': '01'
}

AdditionalDataID = {
    'BILL_NUMBER': '01',
    'MOBILE_NUMBER': '02',
    'STORE_LABEL': '03',
    'LOYALTY_NUMBER': '04',
    'REFERENCE_LABEL': '05',
    'CUSTOMER_LABEL': '06',
    'TERMINAL_LABEL': '07',
    'PURPOSE_OF_TRANSACTION': '08',
    'ADDITIONAL_CONSUMER_DATA_REQUEST': '09'
}


