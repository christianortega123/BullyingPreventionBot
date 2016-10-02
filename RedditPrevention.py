#__author__  'Noah Ortega'
import praw #Reddit API
import OAuth2Util #Utility to login more easily
#Logs into reddit under the current users account and requests permission from reddit to act as a bot
#oauth.ini in the same directory as this file contains all the info needed for it to login
r = praw.Reddit(user_agent = "TAMUhack")
o = OAuth2Util.OAuth2Util(r)
o.refresh(force = True)

#Message to send to flagged comments
MESSAGE = "Hello, we noticed that you recently posted a comment that contained personal information (a phone number, address, and/or email address). \n Please be mindful that when sensitive information such as this is posted on the internet, it can hurt whomever it pertains to, even if it wasn't meant to. \n \n Malicious acts of privacy exploitation occur everyday on the internet in order to cyber-bully. \n  The goal of this bot is to prevent and reduce online harassment and spread of the word of its prevalence in the world today. \n \n If you stand with us, take the pledge to stand by a bully-free internet [here](http://www.hackharassment.com/mlh/#mlh-pledge)"
#List of common domain names for emails
DOMAINS = ["aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com","google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com","live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk","email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com","lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com","safe-mail.net", "wow.com" , "ygm.com", "ymail.com", "zoho.com", "fastmail.fm","yandex.com","bellsouth.net", "charter.net", "comcast.net", "cox.net", "earthlink.net", "juno.com","btinternet.com", "virginmedia.com", "blueyonder.co.uk", "freeserve.co.uk", "live.co.uk","ntlworld.com", "o2.co.uk", "orange.net", "sky.com", "talktalk.co.uk", "tiscali.co.uk","virgin.net", "wanadoo.co.uk", "bt.com","sina.com", "qq.com", "naver.com", "hanmail.net", "daum.net", "nate.com", "yahoo.co.jp", "yahoo.co.kr", "yahoo.co.id", "yahoo.co.in", "yahoo.com.sg", "yahoo.com.ph","hotmail.fr", "live.fr", "laposte.net", "yahoo.fr", "wanadoo.fr", "orange.fr", "gmx.fr", "sfr.fr", "neuf.fr", "free.fr","gmx.de", "hotmail.de", "live.de", "online.de", "t-online.de", "web.de", "yahoo.de","mail.ru", "rambler.ru", "yandex.ru", "ya.ru", "list.ru","hotmail.be", "live.be", "skynet.be", "voo.be", "tvcablenet.be", "telenet.be","hotmail.com.ar", "live.com.ar", "yahoo.com.ar", "fibertel.com.ar", "speedy.com.ar", "arnet.com.ar","hotmail.com", "gmail.com", "yahoo.com.mx", "live.com.mx", "yahoo.com", "hotmail.es", "live.com", "hotmail.com.mx", "prodigy.net.mx", "msn.com"]
#List of strings to identify something as an address
ADDRESSES = ['AK', 'Alaska','AL', 'Alabama','AR', 'Arkansas','AS', 'American Samoa','AZ', 'Arizona','CA', 'California','CO', 'Colorado','CT', 'Connecticut','DC', 'District of Columbia','DE', 'Delaware','FL', 'Florida','GA', 'Georgia','GU', 'Guam','HI', 'Hawaii','IA', 'Iowa','ID', 'Idaho','IL', 'Illinois','IN', 'Indiana','KS', 'Kansas','KY', 'Kentucky','LA', 'Louisiana','MA', 'Massachusetts','MD', 'Maryland','ME', 'Maine','MI', 'Michigan','MN', 'Minnesota','MO', 'Missouri','MP', 'Northern Mariana Islands','MS', 'Mississippi','MT', 'Montana','NA', 'National','NC', 'North Carolina','ND', 'North Dakota','NE', 'Nebraska','NH', 'New Hampshire','NJ', 'New Jersey','NM', 'New Mexico','NV', 'Nevada','NY', 'New York','OH', 'Ohio','OK', 'Oklahoma','OR', 'Oregon','PA', 'Pennsylvania','PR', 'Puerto Rico','RI', 'Rhode Island','SC', 'South Carolina','SD', 'South Dakota','TN','Tennessee','TX', 'Texas','UT', 'Utah','VA', 'Virginia','VI', 'Virgin Islands','VT', 'Vermont','WA', 'Washington','WI', 'Wisconsin','WV', 'West Virginia','WY', 'Wyoming', 'Apartment' , 'St.' , 'Street', 'Lane', 'Ln.', 'Ct.']
subreddit = r.get_subreddit('testantibullying')#Chooses a subreddit to monitor
posts = subreddit.get_hot(limit = 50)#Collects all posts
#iterate through all posts
for post in posts:
    comments = praw.helpers.flatten_tree(post.comments)#collects all comments and iterate through them
    for comment in comments:
        flagged = False #boolean to represent if a comment has been "flagged"
        email = False #boolean to represent if the reason a comment was flagged was because an email was found in it
        phone = False #boolean to represent if the reason a comment was flagged was because a phone number was found in it
        address = False #boolean to represent if the reason a comment was flagged was because an address was found
        reasonFlagged = "" #string with the reason flagged for documentation purposes
        dashes = 0 #dashes found for detecting a phone number
        nums = 0 #number of digits found for detecting a phone number
        words = comment.body.split() #splits the string into an array
        for word in words:#iterate through that array of words
            for domain in DOMAINS:#iterate through the domain array
                if(domain in word):#if a domain is found
                    flagged = True
                    email = True
                    reasonFlagged += "Email Address"
                    break
            for index in range(0, len(word)):#iterate through all the character in the word to look for a phone number
                if(word[index] == '-'):#if the character is a dash increment
                    dashes += 1
                if(word[index].isdigit()):#if the character is a digit increment
                    nums += 1
            for address in ADDRESSES:
                if(address in word):
                    flagged = True
                    address = True
                    reasonFlagged += "Address"
        if(dashes >= 2 and nums >= 10):#if the requirements for a phone number were met
            flagged = True
            phone = True
            reasonFlagged += "Phone number"
        if(flagged):#if a comment was flagged log it into a database text file called "comment_database.txt" with the time created, comment ID, username of the harasser, reason flagged, and the comment itself
            database = open("comment_database.txt", "a")
            database.write("Time Posted: {}     CID: {}     Username: {}     Reason Flagged: {}     Comment: {} \n".format(comment.created ,comment.id, comment.author, reasonFlagged, comment.body.replace("\n", " ")))
            database.close()
            r.send_message(comment.author, 'DOX', MESSAGE)#sends a message to the harasser
        if(address and (phone or email)):#if enough information was detected to decide that the comment is worth reporting, report it
            comment.report()