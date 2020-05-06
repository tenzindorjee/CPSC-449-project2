from flask import Flask
import requests
from feedgen.feed import FeedGenerator

app = Flask(__name__)

@app.route('/<string:community>/<int:amount>') #passsing in arguments refered to the requests website documentation
def ParticularRecent(amount,community):
	newRoute = 'http://127.0.0.1:5000/api/v1.0/resources/collections/recent?community=' + community + '&amount=' +str(amount) #taking user input in url and passing it into the requests feed
	
	response = requests.get(newRoute)
	jsonDict = response.json()
	
	fg = FeedGenerator() # feedgen structure for making a rss feed following guidelines on the website and github 
	fg.id('http://127.0.0.1:5100/<string:community>')
	fg.link(href='http://127.0.0.1:5100/<string:community>', rel='alternate')
	fg.title('25 recent post for particular community')
	fg.language('en')
	fg.description('printing the top 25 recent post for a particular community!')

	for post in jsonDict: # basically since the json was converted into a dictionary a loop to add entries based off the dictionary keys and info
	
		fe = fg.add_entry()
		fe.title(post['title'])
		fe.author( {'name':post['username'],'email':'john@example.de'}) #didnt have emails in the script to test so just used the random email they provided on the requests documentation examples
		fe.id(post['community'])
		
	results = fg.rss_str(pretty=True)
	return results

@app.route('/any/<int:amount>')
def any(amount):
	newRoute = 'http://127.0.0.1:5000/api/v1.0/resources/collections/any?amount='+ str(amount)
	response1 = requests.get(newRoute)
	jsonDict1 = response1.json()

	fg = FeedGenerator() # feedgen structure for making a rss feed following guidelines on the website and github 
	fg.id('http://127.0.0.1:5100/any/<int:amount>')
	fg.link(href='http://127.0.0.1:5100/any/<int:amount>', rel='alternate')
	fg.title('25 recent post for any community')
	fg.language('en')
	fg.description('printing the top 25 recent post for any community!')

	for post in jsonDict1: # basically since the json was converted into a dictionary a loop to add entries based off the dictionary keys and info
		fe = fg.add_entry()
		fe.title(post['title'])
		fe.author( {'name':post['username'],'email':'john@example.de'}) #didnt have emails in the script to test so just used the random email they provided on the requests documentation examples
		fe.id(post['community'])
	
	results = fg.rss_str(pretty=True)
	return results
