class SMS:
    smsProvider = None;

    def __init__(self, provider):
        self.smsProvider = provider

    def getProviderName(self):
        return self.smsProvider.getProviderName()

    def getBalance(self):
        return self.smsProvider.getBalance()

    def send(self, *args, **kwargs):
        return self.smsProvider.sendSMS(*args, **kwargs)

    def status(self, *args, **kwargs):
        return self.smsProvider.getStatus(*args, **kwargs)
