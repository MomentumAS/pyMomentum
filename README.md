![Momentum Teknoloji AS](https://mtas.com.tr/wp-content/uploads/2016/03/logoMTAS.png "Momentum AS Logo")

# pyMomentum
This repository contains python libraries developed and used by Momentum AS. You can find detailed information below. Please feel free to contribute or ask. More libraries and documentation will be here soon.

---

## Available Libraries
- **sms** is a library for sending text messages using provider API's.
  - **Providers** currently available are:
    - Sanal Santral SMS API V1.0.0
    - MutluCell SMS API

---

## Installation

To install latest stable version of our library, simply run:

    pip install pyMomentum


If you installed before, to update simply run:

    pip install pyMomentum --upgrade

To install library from GitHub master branch:

    pip install git+https://github.com/MomentumAS/pyMomentum.git

To update from GitHub master branch:

    pip install git+https://github.com/MomentumAS/pyMomentum.git --upgrade



---
## Details about Libraries
---
### sms

You should create a provider with its parameters and then you can simply use **sms.SMS()**

If you are located in Turkey and sending advertorial texts to end users, you should provide a opt-out option. Please learn your local regulations about sending short messages.

Available providers in the library are **Sanal Santral** and **MutluCell** at the moment. Here is an example usage:
```python
from pyMomentum.sms import sms
from pyMomentum.sms.providers.sanalsantral import SanalSantralSMSProvider

# create a provider object, username is your username and password is API key. smsHeader should be one of your registered headers (alphanumerical from information of SMS)
provider = SanalSantralSMSProvider(username="test", password="test", smsHeader="test")
# create an sms object with the provider above
mysms = sms.SMS(provider)
# send an sms
sms_id = mysms.send(smsNumber="123456789", smsText="Message Text")

#>>> sms_id
#{'message_id': 77300600}

# sms_id is numerical value that you can track your send report
# you can store this id in a database so you can reach send report later

mysms.status(message_id=sms_id['message_id'])

# this will return a list like:
# {'result_detail': 'Pending', 'results': [{'status_detail': 'Send report operation started', 'status': '25', 'number': '90500000000'}], 'result_code': '5'}
# you should expect a pending status a bit later
# {'results': [{'status_detail': 'Send report operation started', 'number': '90500000000', 'status': '25'}], 'result_detail': 'Pending', 'result_code': '5'}
# and you should expect success message as soon as your message received
# {'result_code': '9', 'results': [{'status_detail': 'Send report operation completed', 'status': '23', 'number': '90500000000'}], 'result_detail': 'Success'}
```
---

MIT License

Copyright (c) 2017 Momentum Teknoloji Anonim Sirketi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
