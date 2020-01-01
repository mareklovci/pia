from app.models import InvoiceType, Payment


def type_converter(arg):
    identifier = [item.value for item in InvoiceType if item.value[0] == arg][0]
    return InvoiceType(identifier).value[1]


def payment_converter(arg):
    identifier = [item.value for item in Payment if item.value[0] == arg][0]
    return Payment(identifier).value[1]
