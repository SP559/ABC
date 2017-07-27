import os
import time
import shutil
from os.path import join, dirname
import sys
import json
import re
import random
import requests
#import shutil
from flask import Flask, request
from flask import Flask, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import urllib2
import cookielib
import urllib
#from clarifai.rest import ClarifaiApp
#appp = ClarifaiApp(apii_key='c6b965c0cbb342f994ec963000661201')
'''
def file_get_contents(url):
    url = str(url).replace(" ", "+") # just in case, no space in url
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    try:
        page = urllib2.urlopen(req)
        return page.read()
    except urllib2.HTTPError, e:
        print e.fp.read()
    return ''
'''
app = Flask(__name__)
english_bot = ChatBot("English Bot")
english_bot.set_trainer(ChatterBotCorpusTrainer)
english_bot.train("chatterbot.corpus.english")

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200
'''
def download_web_image(url):
    request = urllib2.Request(url)
    img = urllib2.urlopen(request).read()
    with open ('test.jpg', 'w') as f: f.write(img)
'''
@app.route('/', methods=['POST'])
def webhook():

    print(request.get_json())
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]: # loop over each entry (there may be multiple entries if multiple messages sent at once)
            

            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    if messaging_event.get("message").get("text"):

                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"]["text"]  # the message's text
                        message_text = message_text.lower() # convert to lower case

                        #send_message(sender_id, "got it, thanks!")

                        # If we receive a text message, check to see if it matches any special
                        # keywords and send back the corresponding example. Otherwise, just echo
                        # the text we received.
                        special_keywords = {
                            "axa": send_image,
                            "insurance": send_button,
                            "insurance claim": send_generic,
		            "send attachment": send_attachment,
			    "visit website": send_website,
			    "visit products": send_products,
			    "visit policies": send_policies,
                            "call": send_call,
                            "hi": send_bd,
                            "hello": send_bd,
                            "hey": send_bd
                        }

                        if message_text in special_keywords:
                            special_keywords[message_text](sender_id) # activate the function
                            return "ok", 200
                        
                        elif ((time.strftime("%d/%m/%Y"))==message_text):
                             send_photo(sender_id)
			     send_message(sender_id, "What is your query about?")
			     send_quick_reply(sender_id)
			     #send_call(sender_id)
                             return "0k", 200
		        
			elif(re.match('(\d{2})[/.-](\d{2})[/.-](\d{4})$',time.strftime("%d/%m/%Y"))):
                             send_message(sender_id, "Hi, What is your query about?")
                             send_quick_reply(sender_id)
		             #send_call(sender_id)
                        else:
                            send_message(sender_id, str(english_bot.get_response(message_text)))
                            send_message(sender_id, "What is your query about?")
                            send_quick_reply(sender_id)
			    #send_call(sender_id)
                            
                            #page.send(recipient_id, message_text, callback=send_text_callback, notification_type=NotificationType.REGULAR)
                   
                    if messaging_event["message"].get("attachments"):
                       sender_id = messaging_event["sender"]["id"] 
		       
                       attachment_link = messaging_event["message"]["attachments"][0]["payload"]["url"]
		       send_message(sender_id,attachment_link)  		
		       send_message(sender_id, "Attachment recieved, we wiil contact you soon")
                       '''
		       #download(attachment_link)
                       #app = ClarifaiApp(api_key= 'c6b965c0cbb342f994ec963000661201')
                       #ab=type((app.tag_urls(['https://samples.clarifai.com/metro-north.jpg'])))
                       #abc=str((app.tag_urls(['%s'% attachment_link])))
                       #img_url = attachment_link
                       #file_name = "test.jpg"
                       #send_message(sender_id, os.getcwd())
                       #print abc
                       #print('%s' % ab)
                       #send_message(sender_id, str(response.text))
                       #send_message(sender_id, attachment_link )
		       api_key = 'acc_4c787cb712b1c8d'
                       api_secret = '30b7b6358e8443deac9dc509d0e62ac6'
		       #send_message(sender_id, file_get_contents(attachment_link))
                       
		       response = requests.get('https://github.com/sumitpandey5559/ABC/tree/master/app/download.jpg',auth=(api_key, api_secret))
                       send_message(sender_id, str(response.json()))
		      
		       etag = "test"
	               filename = str(etag)+'.jpg'#Download file and store it with new name
	               response = requests.get(attachment_link, stream=True)
	               with open(filename, 'wb') as out_file:
    			        shutil.copyfileobj(response.raw, out_file)
	               

		       with open(join(dirname(__file__), filename), 'rb') as imag:

                       send_message(sender_id, abc)
                       files = [f for f in os.listdir('.') if os.path.isfile(f)]
                       for f in files:
                           send_message(sender_id, f)
                       response1 = requests.get(attachment_link, stream=True)
                       with open('img.png', 'wb') as out_file:
                           shutil.copyfileobj(response1.raw, out_file)
                       del response1
                       #send_message(sender_id, str(response.text))
                      
                       # NOT WORKIN ---
                       #img = urllib2.urlopen(img_url)
                       #localFile = open(os.getcwd()+file_name , 'wb')
                       #localFile = open("https://github.com/sumitpandey5559/ABC/tree/master/"+file_name , 'wb')
                       #localFile.write(img.read())
                       #localFile.close()
                       '''  
                     
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def send_website(recipient_id):
    log("sending image to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"web_url",
            "payload":{
            "url": "https://axa-bs.com/"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_products(recipient_id):
    log("sending image to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"web_url",
            "payload":{
            "url": "https://us.axa.com/axa-products/"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_policies(recipient_id):
    log("sending image to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"web_url",
            "payload":{
            "url": "https://www.bharti-axalife.com/claims/faqs"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
	
	
def send_photo(recipient_id):
    log("sending image to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"image",
            "payload":{
            "url": "http://www.happybirthday.quotesms.com/images/latest-happy-birthday-images.jpg"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_bd(recipient_id, message_text="Hi! When is your birthday, enter in dd/mm/yyyy format!"):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
 
def send_attachment(recipient_id, message_text="please upload attachment"):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_image(recipient_id):
    log("sending quick reply to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text":"Choose from the options",
            "quick_replies":[
              {
                "content_type":"text",
                "title":"call",
                "payload":"axa"
              },
              {
                "content_type":"text",
                "title":"visit website",
                "payload":"insurance claim"
              },
            ]
          }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_call(recipient_id):
    log("sending image to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"phone_number",
            "payload":{
            "url": "+917872684490"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_button(recipient_id):
    log("sending quick reply to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text":"Choose from the options",
            "quick_replies":[
              {
                "content_type":"text",
                "title":"call",
                "payload":"axa"
              },
              {
                "content_type":"text",
                "title":"visit products",
                "payload":"insurance claim"
              },
            ]
          }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_generic(recipient_id):
    log("sending quick reply to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text":"Choose from the options",
            "quick_replies":[
              {
                "content_type":"text",
                "title":"send attachment",
                "payload":"axa"
              },
              {
                "content_type":"text",
                "title":"visit policies",
                "payload":"insurance claim"
              },
            ]
          }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_quick_reply(recipient_id):
    log("sending quick reply to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text":"Choose from the options",
            "quick_replies":[
              {
                "content_type":"text",
                "title":"axa",
                "payload":"axa"
              },
              {
                "content_type":"text",
                "title":"insurance",
                "payload":"insurance"
              },
              {
                "content_type":"text",
                "title":"insurance claim",
                "payload":"insurance claim"
              },
            ]
          }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
