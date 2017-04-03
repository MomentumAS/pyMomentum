class SMSProvider:
    providerName = None
    config = {}

    def getProviderName(self):  # default
        return self.providerName

    def getBalance(self):  # default
        return None

    def sendSMS(self):  # default
        return None


# define exception types
class SMSProviderNotConfiguredException(BaseException):
    pass


class SMSProviderAPIException(BaseException):
    pass


class SMSProviderValueException(BaseException):
    pass
