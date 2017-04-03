import requests

from pyMomentum.sms.providers.providers import SMSProvider, SMSProviderNotConfiguredException, SMSProviderAPIException, \
    SMSProviderValueException


# **********************************************************************************************************
# Author: Emir Tagmat <emir@tagmat.net> / Momentum Teknoloji A.S. <info@mtas.com.tr>
# **********************************************************************************************************
# SMS Api Library for Sanal Santral v 1.0.0
# You should provide your username, api key as password and your header
# **********************************************************************************************************
# Example usage:
# sms = sms.SMS(sms.SanalSantralSMSProvider(username="test", password="test", smsHeader="test"))
# sms.getBalance() -> gets current balance of prepaid account
# sms.getProviderName() -> gets provider name
# sms.sendSMS(number,text) -> to send an sms
# **********************************************************************************************************

class SanalSantralSMSProvider(SMSProvider):
    providerName = "Sanal Santral SMS API V1.0.0"

    # username and password must be set at runtime
    config = {'username': "", 'password': "", 'smsHeader': ""}

    # Sanal Santral constants
    api_url = "http://sms.sanalsantral.com.tr:8080/api"

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
        if self.config['smsHeader'] is None or self.config['smsHeader'] == "":
            raise SMSProviderNotConfiguredException("Please provide header")

    def getBalance(self):
        self.checkConfig()
        api_credit_url = self.api_url + "/credit/v1?username=" + \
                         self.config['username'] + "&password=" + \
                         self.config['password']
        resulttext = requests.get(api_credit_url).text

        response_text = ""
        if resulttext.__contains__(" "):
            response_code, response_text = resulttext.split(" ")
        else:
            response_code = resulttext

        if response_code == "00":
            retval = response_text
        elif response_code == "95":
            raise SMSProviderAPIException("Use get method")
        elif response_code == "93":
            raise SMSProviderAPIException("Missing get params")
        elif response_code == "87":
            raise SMSProviderAPIException("Wrong username or password")
        else:
            raise SMSProviderAPIException("Error is not documented, failed to receive success message from server")

        return int(retval)

    def getStatus(self, message_id=0):
        self.checkConfig()
        status_results = {
            '0': "Waiting",
            '5': "Pending",
            '6': "Failed",
            '9': "Success",
            '25': "Send report operation started",
            '23': "Send report operation completed",
            '27': "Unexpected server error while sending message",
            '29': "Message is waiting to send"
        }
        if message_id == 0:
            raise SMSProviderValueException("Please provide valid SMS id ", message_id)
        api_dlr_url = self.api_url + "/dlr/v1?" \
                                     "username=" + self.config['username'] \
                      + "&password=" + self.config['password'] \
                      + "&id=" + message_id.__str__()
        resulttext = requests.get(api_dlr_url).text

        response = []
        responsecode = -1
        if resulttext.__contains__(" "):
            results = resulttext.split(" ")
            for result in results:
                if result.__contains__("|"):
                    res_status, res_number = result.split("|")
                    response.append(
                        {'number': res_number, 'status': res_status, 'status_detail': status_results[res_status]}
                    )
                else:
                    responsecode = result
        else:
            if resulttext == "95":
                raise SMSProviderAPIException("Use get method")
            elif resulttext == "93":
                raise SMSProviderAPIException("Missing get params")
            elif resulttext == "87":
                raise SMSProviderAPIException("Wrong username or password")
            elif resulttext == "79":
                raise SMSProviderAPIException("Message id not found")
            elif resulttext == "29":
                # information level error
                responsecode = resulttext
            elif resulttext == "27":
                # information level error
                responsecode = resulttext
            elif resulttext == "25":
                raise SMSProviderAPIException("DLR_OPERATION_STARTED: Started updating message status")
            elif resulttext == "23":
                raise SMSProviderAPIException("DLR_OPERATION_COMPLETED: Updating message status is completed")
            else:
                raise SMSProviderAPIException("Error is not documented, failed to receive success message from server")

        return {'results': response, 'result_code': responsecode, 'result_detail': status_results[responsecode]}

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
        api_sendsms_url = self.api_url + "/smspost/v1"
        # todo: multiple numbers
        api_xml_text = "<sms>" \
                       "<username>{0}</username>" \
                       "<password>{1}</password>" \
                       "<header>{2}</header>" \
                       "<validity>{3}</validity>" \
                       "<message>" \
                       "<gsm><no>{4}</no></gsm>" \
                       "<msg><![CDATA[{5}]]></msg></message>" \
                       "</sms>".format(self.config["username"],
                                       self.config["password"],
                                       smsHeader,
                                       2880,
                                       smsNumber,
                                       smsText)

        resulttext = requests.post(api_sendsms_url, api_xml_text).text

        response_text = ""
        if resulttext.__contains__(" "):
            response_code, response_text = resulttext.split(" ")
        else:
            response_code = resulttext

        if response_code == "00":
            retval = {"message_id": int(response_text)}
        elif response_code == "97":
            raise SMSProviderAPIException("Use post method")
        elif response_code == "91":
            raise SMSProviderAPIException("Missing post data")
        elif response_code == "89":
            raise SMSProviderAPIException("Wrong xml format", api_xml_text)
        elif response_code == "87":
            raise SMSProviderAPIException("Wrong username or password")
        elif response_code == "85":
            raise SMSProviderAPIException("Wrong sms header")
        elif response_code == "83":
            raise SMSProviderAPIException("Empty sms")
        elif response_code == "81":
            raise SMSProviderAPIException("Not enough credits")
        else:
            raise SMSProviderAPIException("Unknown error, failed to receive data from server")

        return retval
