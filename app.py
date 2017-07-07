import os
import sys
import json
import re
import random
import requests
from flask import Flask, request

app = Flask(__name__)


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

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    responses = (
    ("hello",                ("Hi!", "Hello!", "Greetings!", "Howdy!")),
    ("hi",                   ("Hi!", "Hello!", "Greetings!", "Howdy!")),
    ("how are you",          ("I'm fine, thank you.",)),
    ("i need (.*)",          ("Why do you need {}?", "Would it really help you to get {}?", "Are you sure you need {}?")),
    ("why don't you (.*)",   ("Do you really think I don't {}?", "Perhaps eventually I will {}.", "Do you really want me to {}?")),
    ("why can't I (.*)",     ("Do you think you should be able to {}?", "If you could {}, what would you do?", "I don't know -- why can't you {}?", "Have you really tried?")),
    ("i can't (.*)",         ("How do you know you can't {}?", "Perhaps you could {}if you tried.", "What would it take for you to {}?")),
    ("i am (.*)",            ("Did you come to me because you are {}?", "How long have you been {}?", "How do you feel about being {}?")),
    ("are you (.*)",         ("Why does it matter whether I am {}?", "Would you prefer it if I were not {}?", "Perhaps you believe I am {}.", "I may be {}-- what do you think?")),
    ("how (.*)",             ("How do you suppose?", "Perhaps you can answer your own question.", "Why can't you answer your question?", "What is it you're really asking?")),
    ("i think (.*)",         ("Do you doubt {}?", "Do you really think so?", "But you're not sure {}?")),
    ("(.*) friend (.*)",     ("Tell me more about your friends.", "What do you value in a friend?")),
    ("yes",                  ("Okay, but can you tell me more?", "Can you actually be sure?", "You seem quite certain.")),
    ("no",                   ("Why not?", "Can you tell me why you say no?", "Are you sure?")),
    ("is it (.*)",           ("Do you think it is {}?", "Perhaps it's {}-- what do you think?", "If it were {}, what would you do?", "It could well be that {}.")),
    ("can you (.*)",         ("If I could {}, then what?", "Why do you ask if I can {}?")),
    ("can i (.*)",           ("Do you want to be able to {}?", "If you could {}, would you?")),
    ("you are (.*)",         ("Why do you think I am {}?", "Perhaps you would like me to be {}.", "Are you really talking about yourself?")),
    ("you're (.*)",          ("Why do you say I am {}?", "Why do you think I am {}?", "Are we talking about you, or me?")),
    ("i don't (.*)",         ("Why don't you {}?", "DO you want to {}?")),
    ("i feel (.*)",          ("Tell me more about these feelings.", "Do you often feel {}?", "When do you usually feel {}?", "When you feel {}, what do you do?")),
    ("i have (.*)",          ("Why do you tell me that you've {}?", "Have you really {}?", "Now that you have {}, what will you do next?")),
    ("i would (.*)",         ("Could you explain why you would {}?", "Why would you {}?", "Who else knows that you would {}?")),
    ("is there (.*)",        ("Do you think there is {}?", "Is it likely that there is {}?", "Would you like there to be {}?")),
    ("my name is (.*)",      ("Hi, {}",)),
    ("my (.*)",              ("Why do you say that your {}?", "When your {}, how do you feel?")),
    ("you (.*)",             ("We should be discussing you, not me.", "Why do you say that about me?", "Why do you care whether I {}?")),
    ("i want (.*)",          ("What would it mean to you if you got {}?", "Why do you want {}?", "What would you do if you got {}?", "If you got {}, then what you do?")),
    ("i don't know (.*)",    ("Perhaps you should learn.", "I don't know either.")),
    ("i'm (.*)",             ("Why are you {}?",)),
    ("because (.*)",         ("if {}, what else is true?", "Is that a good reason?", "Are there any other good reasons?", "Is that the only reason?", "Why do you think {}?")),
    ("i (.*)",               ("Why do you {}?",)),
    ("(.*) is (.*)",         ("Why is {} {}?",)),
    ("(.*) can't (.*)",      ("Why can't {}, {}")),
    ("why (.*)",             ("What do you think?", "Why do you think {}?", "Why don't you know the answer yourself?")),
    ("(.*) are (.*)",        ("Why are {} {}?",)),
    ("(.*)",                 ("Can you please elaborate?", "I don't fully understand.", "Let's stop talking about this.", "How are you feeling about this?")),
)

pronouns = {
    "i'm": "you're", 
    "i": "you", 
    "me": "you",
    "yours": "mine",
    "you": "I",
    "am": "are",
    "my": "your",
    "you're": "I'm",
    "was": "were"
}

    input = re.split("[\.!?]",message_text.lower().rstrip('.!?'))
    full_reply=' '
    
    for sentence in input:
        sentence=sentence.lstrip()
        for pattern in responses:
            wildcards = []
            if re.match(pattern[0], sentence):
                wildcards = filter(bool, re.split(pattern[0], sentence))
                # replace pronouns
                wildcards = [' '.join(pronouns.get(word, word) for word in wildcard.split()) for wildcard in wildcards]

                response = random.choice(pattern[1])
                response = response.format(*wildcards)
                full_reply+=response+' '
                
              
    
  
                    send_message(sender_id, "thank you! your message is '%s' and Sumit told you to visit https://axa-bs.com/" % full_reply)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


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


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
