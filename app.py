#Libraries Needed
import random
from flask import Flask, request
from pymessenger.bot import Bot
import os

#Basic blocks needed
ACCESS_TOKEN = 'EAAC4MK9k4bMBAFupDg7BvcC83P59mwL6VNpoXEPzQCJFCRc3lGexgvyLZBu4lJDnuhX6KcutQsNToXFik3gn6lI5hEYKapr7UOueZBccstXGt4hMZA1tZCEPPPoXd1MoEgbMTSLwtPanrJz9eIewVoMP5RjqkXY7Tug4w0j0IAZDZD'
VERIFY_TOKEN = '1133557799'

bot = Bot (ACCESS_TOKEN)

app = Flask(__name__)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    print('Receiving Message')
    if request.method == 'GET':
        print('Method : GET')
    	# Before allowing people to message your bot, Facebook has implemented a verify token
    	# that confirms all requests that your bot receives came from Facebook.
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        print('Method : Post')
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run()
