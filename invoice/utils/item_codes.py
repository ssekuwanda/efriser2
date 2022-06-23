import enum


class Currencies(enum.Enum):
    GBP= 103
    EURO = 104
    USD = 102
    UGX = 101

class PaymentMode(enum.Enum):
    Credit = 101
    Cash = 102
    Cheque = 103
    Demand_draft = 104
    Mobile_money = 105
    Visa = 106
    EFT = 107
    POS = 108
    RTGS = 109
    Swift_transfer = 110

# class BuyerTyper(enum.Enum):

class InvoiceIndustry(enum.Enum):
    general_industry = 101
    export = 102
    imports = 103

class InvoiceType(enum.Enum):
    invoice = 1
    receipt = 2
    debit = 4

class BuyerType(enum.Enum):
    B2B = 0
    B2C = 1
    Foreigner = 2

class InvoiceKind(enum.Enum):
    invoice = 1
    receipt = 2

    @classmethod
    def choices(cls):
        return [(i.name, i.value) for i in cls]

print(InvoiceKind.choices())

U