from mastodon import Mastodon
import asyncio
import time
from dotenv import load_dotenv
import os
import requests
import random

imglist = "https://raw.githubusercontent.com/micfun123/mastodon_image_reply/main/pics/imagenames.txt"

load_dotenv()

mastodon = Mastodon(
    client_id=os.getenv("Client_key"),
    client_secret=os.getenv("Client_secret"),
    access_token=os.getenv("access_token"),
    api_base_url="https://mastodon.social"
)

#get account id
followers = []
posts = []
for follower in mastodon.account_followers(110090602223960345):
    followers.append(follower.id)

print(followers)
for follower in followers:
    #get posts from the user
    for post in mastodon.account_statuses(follower):
        posts.append(post.id)



r = requests.get(imglist)
list = r.text 
list = list.splitlines()

while True:
    #get all new posts from the people that follow me
    for follower in followers:
        for post in mastodon.account_statuses(follower):
            if post.id not in posts:
                posts.append(post.id)
                print("New post from: " + str(follower))
                print(post.id)
                print(post.content)
                print("")
                if random.randint(1, 15) == 1:
                    #get list of files from github
                    #pick random file from list
                    name = random.choice(list)
                    file = requests.get(f"https://raw.githubusercontent.com/micfun123/mastodon_image_reply/main/pics/{name}")
                    mastodon.status_post(f"{name}", in_reply_to_id=post.id, media_ids=[file.json()["id"]])

                    
                    
    time.sleep(250)
