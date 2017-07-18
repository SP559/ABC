import os
import time
import sys
import json
import re
import random
import requests
from flask import Flask, request
from flask import Flask, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

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
                            "make me laugh": send_gif,
                            "sumit": send_call,
                            "shaique": send_call,
                            "aman": send_call,
                            "youtube": send_button,
                            "enjoy": send_generic,
                            "amit": send_call,
                            "quick reply": send_quick_reply,
                            "amrendra": send_call,
                            "hi": send_bd,
                            "hello": send_bd,
                            "hey": send_bd
                        }

                        if message_text in special_keywords:
                            special_keywords[message_text](sender_id) # activate the function
                            send_message(sender_id, "Ok!")
                            return "ok", 200
                        
                        elif ((time.strftime("%d/%m/%Y"))==message_text):
                             send_photo(sender_id)
                             return "0k", 200
                        else:
                            send_message(sender_id, str(english_bot.get_response(message_text)))
                            
                            
                               
                            
                            #page.send(recipient_id, message_text, callback=send_text_callback, notification_type=NotificationType.REGULAR)
                   
                    if messaging_event["message"].get("attachments"):
                       sender_id = messaging_event["sender"]["id"] 
                       attachment_link = messaging_event["message"]["attachments"][0]["payload"]["url"]
                       send_message(sender_id, "Attachment recieved, Ok!")
                       send_photo(sender_id)
                     
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

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
            "url": "https://media.glassdoor.com/sqll/518746/axa-business-services-squarelogo-1424923973982.png"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_gif(recipient_id):
    log("sending gif to {recipient}".format(recipient=recipient_id))

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
            "url": "http://wanna-joke.com/wp-content/uploads/2016/09/gif-3d-cool.gif"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_call(recipient_id):
    log("sending gif to {recipient}".format(recipient=recipient_id))

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
    "attachment":{
      "type":"template",
         "payload":{
            "template_type":"button",
            "text":"You like him? Talk to him",
            "buttons":[
               {
                  "type":"phone_number",
                  "title":"Call him",
                  "payload":"+917872684490"
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

def send_button(recipient_id):
    log("sending buttons to {recipient}".format(recipient=recipient_id))

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
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"What do you want to do next?",
                    "buttons":[
                    {
                    "type":"web_url",
                    "url":"https://www.youtube.com",
                    "title":"Visit Youtube"
                    },
                    {
                    "type":"postback",
                    "payload":"https://www.rainymood.com",
                    "title":"peace"
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

def send_generic(recipient_id):
    log("sending generic template to {recipient}".format(recipient=recipient_id))

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
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "elements":[
                      {
                        "title":"AXA",
                        "item_url":"http://www.axa-bs.com",
                        "image_url":"https://media.glassdoor.com/sqll/518746/axa-business-services-squarelogo-1424923973982.png",
                        "subtitle":"Company you want to work with!",
                        "buttons":[
                          {
                            "type":"web_url",
                            "url":"http://www.youtube.com",
                            "title":"Enjoy"
                          },
                          {
                            "type":"postback",
                            "payload":"https://www.rainymood.com",
                            "title":"peace"
                          }              
                        ]
                      },
                      {
                        "title":"AXA",
                        "item_url":"https://www.axa-bs.com",
                        "image_url":"https://media.glassdoor.com/sqll/518746/axa-business-services-squarelogo-1424923973982.png",
                        "subtitle":"Company you want to work with!",
                        "buttons":[
                          {
                            "type":"web_url",
                            "url":"https://www.youtube.com",
                            "title":"Enjoy"
                          },
                          {
                            "type":"postback",
                            "payload":"https://www.rainymood.com",
                            "title":"peace"
                          }              
                        ]
                      },
                      {
                        "title":"AXA",
                        "item_url":"https://www.axa-bs.com",
                        "image_url":"https://media.glassdoor.com/sqll/518746/axa-business-services-squarelogo-1424923973982.png",
                        "subtitle":"Company you want to work with!",
                        "buttons":[
                          {
                            "type":"web_url",
                            "url":"https://www.youtube.com",
                            "title":"Enjoy"
                          },
                          {
                            "type":"postback",
                            "payload":"https://www.rainymood.com",
                            "title":"peace"
                          }              
                        ]
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
            "text":"Who is the Coolest guy in the team? or type axa, make me laugh, youtube, enjoy",
            "quick_replies":[
              {
                "content_type":"text",
                "title":"sumit",
                "payload":"make me laugh"
              },
              {
                "content_type":"text",
                "title":"shaique",
                "payload":"make me laugh"
              },
              {
                "content_type":"text",
                "title":"aman",
                "payload":"make me laugh"
              },
              {
                "content_type":"text",
                "title":"amit",
                "payload":"make me laugh"
              },
              {
                "content_type":"text",
                "title":"amrendra",
                "payload":"make me laugh"
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
