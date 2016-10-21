# Reddit.com Archive Bot
# Scans new submissions for white listed domains and posts a link to an Imgur mirror of that webpage

import time
import praw
from selenium import webdriver
from imgurpython import ImgurClient

# Imgur.com API client_id and client_secret
client_id = ''
client_secret = ''

# Reddit.com username and password
reddit_id = ''
reddit_password = ''

#Domains to work on e.g. ['seattletimes.com/']
whiteList = ['imgur.com/']
#Subreddit to work in e.g. 'All' or 'SeattleWA'
community = 'All'

def main():
	r = praw.Reddit("Mirror Script 0.1, <github>")
	r.login(reddit_id, reddit_password, disable_warning=True)

	alreadyDone = []
	whiteListSize = len(whiteList)

	while True:
		submissions = r.get_subreddit(community).get_new(limit=25)
		for item in submissions:
			for x in range(0, whiteListSize):
				if whiteList[x] in item.url and item.id not in alreadyDone:
					mirrorURL = getScreenshot(item.url);
					comment(item, mirrorURL);
					alreadyDone.append(item.id);
					
		time.sleep(1800) #Recommended by Reddit.com's API guidelines

def getScreenshot(submissionlink):
	driver = webdriver.Firefox()
	driver.get(submissionlink)
	driver.save_screenshot('screenshot.png')
	driver.quit()
	
	client = ImgurClient(client_id, client_secret)
	
	upload = client.upload_from_path("./screenshot.png", anon = True)
	
	return upload['link']
	

def comment(submission, mirrorURL):
	submission.add_comment("Here is a mirror of the page in case it goes down: " + mirrorURL);
	return
   
if __name__ == '__main__':
	main()