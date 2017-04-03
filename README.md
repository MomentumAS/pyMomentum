![alt text](https://mtas.com.tr/wp-content/uploads/2016/03/logoMTAS.png "Momentum AS Logo")

# pyMomentum
This repository contains python libraries developed and used by Momentum AS. You can find detailed information below. Please feel free to contribute or ask. More libraries and documentation will be here soon.

---

## Available Libraries
- **sms** is a library for sending text messages using provider API's.
  - **Providers** currently available are:
    - Sanal Santral API V1.0.0

## Details about Libraries
---
### sms

You should create a provider with its parameters and then you can simply use **sms.SMS()**

If you are located in Turkey and sending advertorial texts to end users, you should provide a opt-out option. Please learn your local regulations about sending short messages.

Only provider in the library is **Sanal Santral** at the moment. Here is an example usage:
```python
# create a provider object, username is your username and password is API key. smsHeader should be one of your registered headers (alphanumerical from information of SMS)
provider = sms.SanalSantralSMSProvider(username="test", password="test", smsHeader="test")
# create an sms object with the provider above
sms = sms.SMS(provider)
# send an sms
sms_id = sms.send(smsNumber="123456789", smsText="Message Text")
# sms_id is numerical value that you can track your send report
# you can store this id in a database so you can reach send report later
sms.status(message_id=sms_id) 
# this will return a list like:
# {'result_detail': 'Pending', 'results': [{'status_detail': 'Send report operation started', 'status': '25', 'number': '90500000000'}], 'result_code': '5'}
# you should expect a pending status a bit later
# {'results': [{'status_detail': 'Send report operation started', 'number': '90500000000', 'status': '25'}], 'result_detail': 'Pending', 'result_code': '5'}
# and you should expect success message as soon as your message received
# {'result_code': '9', 'results': [{'status_detail': 'Send report operation completed', 'status': '23', 'number': '90500000000'}], 'result_detail': 'Success'}
```
---