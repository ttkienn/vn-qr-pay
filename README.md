# Vietnam QRPay Python

<img src="https://raw.githubusercontent.com/monodyle/vnqrpay/main/.github/vietqr.png" height="25" /> <img src="https://raw.githubusercontent.com/monodyle/vnqrpay/main/.github/vnpay.png" height="19" />

The library helps you to encode QR code of VietQR/VNPay. Converted to python from the original typescript repository [xuannghia/vietnam-qr-pay]

[xuannghia/vietnam-qr-pay]: https://github.com/xuannghia/vietnam-qr-pay/

## Features

### Build QRCode

#### Static VietQR

```python

from constants.variables import BanksObject
from main import QRPay

qrPay = QRPay.initQR(
    {
        "bankBin": BanksObject["mbbank"]["bin"],
        "bankNumber": "011998199999"
    },
    "VietQR",
)

content = qrPay.build()
print(content)
# 00020101021138560010A0000007270126000697042201120119981999990208QRIBFTTA53037045802VN630401C5
```

#### Dynamic VietQR

```python
from constants.variables import BanksObject
from main import QRPay

qrPay = QRPay.initQR(
    {
        "bankBin": BanksObject["mbbank"]["bin"],
        "bankNumber": "011998199999",  # Số tài khoản
        "amount": "10000",  # Số tiền
        "description": "DE TU ANH THIEU TRUNG KIEN GUI TIEN BAO KE",  # Nội dung chuyển tiền
    },
    "VietQR",
)

content = qrPay.build()
print(content)
# 00020101021138560010A0000007270126000697042201120119981999990208QRIBFTTA53037045405100005802VN62460842DE TU ANH THIEU TRUNG KIEN GUI TIEN BAO KE63043641

```

#### VNPay

```python
from main import QRPay

qrPay = QRPay.initQR(
    {
        "merchantId": '0123456789',
        "merchantName": 'COMPANY',
        "store": 'YOUR COMPANY',
        "terminal": 'YC01',
    },
    "VNPAY",
)

content = qrPay.build()
print(content)
```
