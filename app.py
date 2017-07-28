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
			    "visit website": send_website_button,
			    "visit products": send_products_button,
			    "visit policies": send_policies_button,
                            "contact us": send_contact,
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
		       send_message(sender_id, "Attachment recieved, we wiil contact you soon")
                       

                     
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                    # The payload param is a developer-defined field which is set in a postback
                    # button for Structured Messages
                    payload = event["postback"]["payload"]

                    log("received postback from {recipient} with payload {payload}".format(recipient=recipient_id, payload=payload))

   
                    # Notify sender that postback was successful
                    send_message(sender_id, "Postback called")

    return "ok", 200

def send_website_button(recipient_id):
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
            "attachment": {
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"Know about AXA",
                    "buttons":[
                    {
                        "type":"web_url",
                        "url":"https://www.axa-bs.com",
                        "title":"Google"
                    },
                    {
                        "type":"postback",
                        "title":"Call Postback",
                        "payload":"Payload for send_button_message()"
                    }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_products_button(recipient_id):
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
            "attachment": {
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"Know about Products",
                    "buttons":[
                    {
                        "type":"web_url",
                        "url":"https://www.axa-bs.com",
                        "title":"Google"
                    },
                    {
                        "type":"postback",
                        "title":"Call Postback",
                        "payload":"Payload for send_button_message()"
                    }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

	
	
def send_policies_button(recipient_id):
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
            "attachment": {
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"Know about Policies",
                    "buttons":[
                    {
                        "type":"web_url",
                        "url":"https://www.axa-bs.com",
                        "title":"Google"
                    },
                    {
                        "type":"postback",
                        "title":"Call Postback",
                        "payload":"Payload for send_button_message()"
                    }
                    ]
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
                "title":"contact us",
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

def send_contact(recipient_id, message_text="please mail us at-sumitpandey559@gmail.com or call-+917872684490"):

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
                "title":"contact us",
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
