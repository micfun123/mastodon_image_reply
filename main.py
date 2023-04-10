from mastodon import Mastodon
import time
from dotenv import load_dotenv
import os
import random

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
                if random.randint(1, 15) == 5:
                    file = random.choice(os.listdir("pics"))
                    print(file)
                    #reply to the post
                    print(str(follower))
                    follower_link = mastodon.account(follower).acct
                    mastodon.status_post(f"@{follower_link} Here is a picture of a cat", media_ids=mastodon.media_post("pics/" + file), in_reply_to_id=post.id)
                    
    time.sleep(250)
    os.system("git pull")
