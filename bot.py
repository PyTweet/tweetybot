import os
import logging
import pytweet
from flask import Flask

client=pytweet.Client(
    os.environ["bearer_token"], 
    consumer_key=os.environ["api_key"], 
    consumer_secret=os.environ["api_key_secret"], 
    access_token=os.environ["access_token"],
    access_token_secret=os.environ["access_token_secret"]
)


logger = logging.getLogger('pytweet')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='pytweet.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[%(levelname)s] %(asctime)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client.webapp = Flask(__name__)


@client.event
def on_direct_message(message):
    if message.application_info:
        return

    text = message.text
    author = message.author
    if text == "!help":
        quick_reply = pytweet.QuickReply(

        ).add_option(
            label="!help",
            description="📖 Command for displaying the help menu <this message>.",
            metadata="help-command"
        ).add_option(
            label="!hello",
            description="👋 Command for greeting me.",
            metadata="hello-command"
        ).add_option(
            label="!info",
            description="ℹ️ Command for displaying your profile user info.",
            metadata="info-command"
        ).add_option(
            label="!echo [Word]",
            description="ℹ️ Command for sending.",
            metadata="echo-command"
        )
        author.send("Help Menu\n[] --> Required Arguments, must specified!\n() --> Optional Arguments, you can specified or not\n\nHello there! Welcome to my HelpCommand, to invoke a command please reply to the quick reply i sent to you or you can use !<command_name>.\n\n!help --> Display the help menu.\n!hello --> Greet me\n!echo [word] --> Send a message that you specified.", quick_reply=quick_reply)
        
    elif text == "!hello":
        author.send(f"Hello {author.username}!")

    elif "!echo" in text:
        arg = text.split(" ", 1)
        if not len(arg) > 1:
            return author.send("Wrong command invocation! example: !echo hello\n!echo hey\n!echo my name is tweety")
        author.send(arg[1])

    elif "!info" in text:
        info_text = f"{author.username} • {author.id}\n{author.description}\n\n🔗 {author.profile_url} • 🧭 {author.location}"
        cta = pytweet.CTA(

        ).add_button(
            label=f"Followers • {author.follower_count}",
            url="https://twitter.com/TheGenocides/following"
        ).add_button(
            label=f"Following • {author.following_count}",
            url="https://twitter.com/TheGenocides/following"
        ).add_button(
            label=f"Tweets • {author.tweet_count}",
            url="https://twitter.com/"
        )
        author.send(info_text, cta=cta)

    else:
        author.send("Wrong command! use !help to get the full documented commands") if text.startswith("!") else ...



client.listen(client.webapp, os.environ["webhook_url"], "Development", host="0.0.0.0", port=8080)