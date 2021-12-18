import pytweet
import os
from flask import Flask

client=pytweet.Client(
    os.environ["bearer_token"], 
    consumer_key=os.environ["api_key"], 
    consumer_key_secret=os.environ["api_key_secret"], 
    access_token=os.environ["access_token"],
    access_token_secret=os.environ["access_token_secret"]
)

client.webapp = Flask('app')

@client.event
def on_direct_message(message):
    if message.author == client.account:
        return

    text = message.text    
    if text == "!help":
        message.author.send("Please reply to a the quick reply i sent to you! or you can use !<command_name> to invoke a command!", quick_reply=pytweet.QuickReply().add_option(
            label="!help",
            description="📖 Command for displaying the help menu <this message>.",
            metadata="help-command"
        ).add_option(
            label="!hello",
            description="👋 Command for greeting me.",
            metadata="hello-command"
        ).add_option(
            label="!info",
            description="ℹ️ Command for displaying the bot info.",
            metadata="info-command"
        ))

    elif text == "!hello":
        message.author.send(f"Hello {message.author.username}!")

    elif text == "!info":
        account = client.account
        message.author.send(f"I'm a bot made by @TheGenocides, I have a total of {account.follower_count} followers, {account.following_count} following and I posted a total of {account.tweet_count} tweets!")

client.listen(client.webapp, os.environ["webhook_url"], "Development", host='0.0.0.0', port=8080)