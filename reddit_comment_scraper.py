###########
# Imports #
###########

# HTTP Requests
import requests
import requests.auth

# Pandas
import pandas as pd

# Python Reddit API Wrapper (PRAW)
import praw
from praw.models import MoreComments



##################################
# Settings (Credentials and URL) #
##################################

# Client ID and Secret can be obtained here (create App):
# https://www.reddit.com/prefs/apps
clientID = "INSERT CLIENT-ID"
clientSecret = "INSERT CLIENT-SECRET"

# Your Reddit Username and Password
username = "INSERT REDDIT USERNAME"
password = "INSERT REDDIT PASSWORD"

# Important rules for User-Agent!
#
# Use this template:
# <platform>:<app ID>:<version string> (by /u/<reddit username>)
#
# The User-Agent should NOT pretend to be a popular browser!
#
# Otherwise it is possible that your requests will be denied.
#
# For more information see:
# https://github.com/reddit-archive/reddit/wiki/API#rules
userAgent = "INSERT USER-AGENT"

# URL to scrape the comments from
# eg.: https://www.reddit.com/r/artificial/comments/1cwuiv5/scarlett_johansson_says_openai_ripped_off_her/
url = "INSERT REDDIT URL"



##########
# Script #
##########

# Authentication
#
# OAuth2 Tutorial for Reddit:
# https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example
client_auth = requests.auth.HTTPBasicAuth(clientID, clientSecret)
post_data = {"grant_type": "password", "username": username, "password": password}
headers = {"User-Agent": userAgent}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
response = response.json()

access_token = response['access_token']
token_type = response['token_type']

# create Reddit instance
reddit = praw.Reddit(
    client_id=clientID,
    client_secret=clientSecret,
    # If you are only scraping public comments, entering a username and password is optional.
    username=username,
    password=password,
    user_agent=userAgent,
    check_for_async=False
)

# Get comments for a single post/submission
#
# Note: Comments are NOT in order!
#
# The list() command does a breadth-first traversal,
# which means it collects all top-level comments first,
# then all second-level comments and so on...
#
# Tutorial on comment extraction:
# https://praw.readthedocs.io/en/stable/tutorials/comments.html

# Get data for a post/submission
# Note: Posts are called submissions on Reddit
submission = reddit.submission(url=url)

# Show number of comments
# This value may not match up 100% with the number of comments extracted via PRAW.
# This discrepancy is normal as that count includes deleted, removed, and spam comments.
print("Total number of comments:", submission.num_comments, "\n")

# Load all comments without a limit
# Warning: This can be a lot of API calls because each call only receives 100 comments
submission.comments.replace_more(limit=None)

comments = []

# The list() command does a breadth-first traversal
for comment in submission.comments.list():
    comments.append(comment.body)

df = pd.DataFrame(comments)

df.info()

print("\nFirst 10 rows of the DataFrame:")
print(df.head(10))
