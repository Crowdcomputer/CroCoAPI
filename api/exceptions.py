from rest_framework.exceptions import APIException

class NotEnoughMoney(APIException):
    status_code = 402
    default_detail = 'Not enough balance'