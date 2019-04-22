#!/usr/bin/python

import praw
import time
import config
import char_gen


# logs in the bot
def login():
    print("Logging in...")
    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         password=config.password,
                         user_agent="RPG bot",
                         username=config.username)

    return reddit


# searches for comments containing keyword and replies with a generated
# character
def find_comments(reddit):
    keyword = "!rpgme"
    print("Searching comments...")

    for comment in reddit.subreddit(config.reddit_sub).stream.comments():
        if keyword in comment.body:
            if not comment.saved:
                char_dict = char_gen.main(comment.author.name)
                reply_text = char_gen.print_char(char_dict)
                comment.reply(reply_text).disable_inbox_replies()
                comment.save()
                print("Replied to comment...")


def main():
    reddit = login()
    find_comments(reddit)


while True:
    try:
        print("Starting up...")
        main()
    except Exception as err:
        print("Error")

    time.sleep(60 * 5)
