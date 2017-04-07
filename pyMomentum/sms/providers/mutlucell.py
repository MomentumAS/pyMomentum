# -*- Encoding:utf-8 -*-

import requests

from pyMomentum.sms.providers.providers import SMSProvider, SMSProviderNotConfiguredException, SMSProviderAPIException, \
    SMSProviderValueException


# **********************************************************************************************************
# Author: Emir Tagmat <emir@tagmat.net> / Momentum Teknoloji A.S. <info@mtas.com.tr>
# **********************************************************************************************************
# SMS Api Library for MutluCell API
# You should provide your username, api key as password and your header
# **********************************************************************************************************
# Example usage:
# sms = sms.SMS(sms.SanalSantralSMSProvider(username="test", password="test", smsHeader="test"))
# smsHeader is optional, if not provided first available header will be selected
# sms.getBalance() -> gets current balance of prepaid account
# sms.getProviderName() -> gets provider name
# sms.sendSMS(number,text) -> to send an sms
# **********************************************************************************************************

class MutluCellSMSProvider(SMSProvider):
    providerName = "Mutlucell SMS API"

    # username and password must be set at runtime
    config = {'username': "", 'password': "", 'smsHeader': ""}

    # Sanal Santral constants
    api_url = "https://smsgw.mutlucell.com/smsgw-ws"

    def __init__(self, username="", password="", smsHeader=""):
        self.config["username"] = username
        self.config["password"] = password
        self.config["smsHeader"] = smsHeader

    def setUsername(self, username):
        self.config["username"] = username

    def setPassword(self, password):
        self.config["password"] = password

    def setSmsHeader(self, smsHeader):
        self.config["smsHeader"] = smsHeader

    def checkConfig(self):
        if self.config['username'] is None or self.config['username'] == "":
            raise SMSProviderNotConfiguredException("Please provide username")
        if self.config['password'] is None or self.config['username'] == "":
            raise SMSProviderNotConfiguredException("Please provide password")

    def getBalance(self):
        self.checkConfig()
        api_credit_url = self.api_url + "/gtcrdtex"

        request_text = '<?xml version="1.0" encoding="UTF-8"?><smskredi ka="' + self.config['username'] + '" pwd="' + \
                       self.config['password'] + '" />'

        resulttext = requests.post(api_credit_url, request_text).text

        response_text = ""

        if resulttext.__contains__("$"):
            response_text = resulttext[1:]
            response_code = "00"
        else:
            response_code = resulttext
            response_text = resulttext

        if response_code == "00":
            retval = response_text
        elif response_code == "20":
            raise SMSProviderAPIException(u"Post edilen xml eksik veya hatalı")
        elif response_code == "23":
            raise SMSProviderAPIException(u"Kullanıcı adı ya da parolanız hatalı")
        else:
            raise SMSProviderAPIException("Error is not documented, failed to receive success message from server")

        return int(float(retval))

    def getStatus(self, message_id=0):
        self.checkConfig()
        status_results = {
            '0': "GÖNDERİLMEDİ",
            '1': "İŞLENİYOR",
            '2': "GÖNDERİLDİ",
            '3': "BAŞARILI",
            '4': "BEKLEMEDE",
            '5': "ZAMANAŞIMI",
            '6': "BAŞARISIZ",
            '7': "REDDEDİLDİ",
            '11': "BİLİNMİYOR",
            '12': "HAT YOK",
            '13': "HATALI",
            '15': "KULLANILMAYAN NUMARA",
            '16': "SMS ALMAYA KAPALI",
            '17': "MESAJ HAFIZASI DOLU",
            '18': "ROAMING",
            '19': "TELESERVİS KAPALI",
            '20': "TAŞINACAK NUMARA"
        }
        if message_id == 0:
            raise SMSProviderValueException("Please provide valid SMS id ", message_id)
        api_dlr_url = self.api_url + "/gtblkrprtex"

        request_text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                       "<smsrapor ka=\"{0}\" pwd=\"{1}\" id=\"{2}\" />".format(self.config['username'],
                                                                               self.config['password'],
                                                                               message_id.__str__())

        resulttext = requests.post(api_dlr_url, request_text).text

        response = []
        responsecode = -1
        if resulttext.__contains__("\n"):
            results = resulttext.split("\n")
            for result in results:
                if result.__contains__(" "):
                    res_number, res_status = result.split(" ")
                    response.append(
                        {'number': res_number, 'status': res_status, 'status_detail': status_results[res_status.__str__()]}
                    )

        else:
            if resulttext == "20":
                raise SMSProviderAPIException("Post edilen xml eksik veya hatalı.")
            elif resulttext == "23":
                raise SMSProviderAPIException("Kullanıcı adı ya da parolanız hatalı.")
            elif resulttext == "30":
                raise SMSProviderAPIException("Hesap Aktivasyonu sağlanmamış")
            else:
                raise SMSProviderAPIException("Unknown error, failed to receive data from server")

        return {'results': response}

    def sendSMS(self, smsNumber=0, smsText="", smsHeader=""):
        self.checkConfig()
        # todo: smsHeader max 11 chars
        if smsHeader == "":
            smsHeader = self.config["smsHeader"]
        # todo: smsNumber can be 10,11 or 12 digits
        if smsNumber == 0:
            raise SMSProviderValueException("smsNumber is not valid: ", smsNumber)
        if smsText.__len__() == 0:
            raise SMSProviderValueException("smsText is not valid: ", smsNumber)

        # todo: validity is now a constant should be parameter
        api_sendsms_url = self.api_url + "/sndblkex"
        # todo: multiple numbers

        api_xml_text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                       "<smspack ka=\"{0}\" pwd=\"{1}\" org=\"{2}\" >" \
                       "<mesaj>" \
                       "<metin><![CDATA[{4}]]></metin>" \
                       "<nums>{3}</nums>" \
                       "</mesaj>" \
                       "</smspack>".format(self.config["username"],
                                           self.config["password"],
                                           smsHeader,
                                           smsNumber,
                                           smsText)

        resulttext = requests.post(api_sendsms_url, api_xml_text).text

        print(resulttext)
        response_text = ""

        if resulttext.__contains__("$"):
            response_text, spent_credit = resulttext[1:].split("#")
            response_code = "00"
        else:
            response_code = resulttext
            response_text = resulttext

        if response_code == "00":
            retval = {"message_id": int(response_text), "spent_credit": int(float(spent_credit))}
        elif response_code == "20":
            raise SMSProviderAPIException("Post edilen xml eksik veya hatalı.")
        elif response_code == "21":
            raise SMSProviderAPIException("Kullanılan originatöre sahip değilsiniz")
        elif response_code == "22":
            raise SMSProviderAPIException("Kontörünüz yetersiz")
        elif response_code == "23":
            raise SMSProviderAPIException("Kullanıcı adı ya da parolanız hatalı.")
        elif response_code == "24":
            raise SMSProviderAPIException("Şu anda size ait başka bir işlem aktif.")
        elif response_code == "25":
            raise SMSProviderAPIException("SMSC Stopped (Bu hatayı alırsanız, işlemi 1-2 dk sonra tekrar deneyin)")
        elif response_code == "30":
            raise SMSProviderAPIException("Hesap Aktivasyonu sağlanmamış")

        else:
            raise SMSProviderAPIException("Unknown error, failed to receive data from server")

        return retval
