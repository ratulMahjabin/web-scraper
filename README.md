# web-scraper
WebINT technology that can scrape data from Facebook

There are two methods of scraping data from facebook.

(i) selenium (ii) Graph API

I chose selenium because of the functionality limitations of Graph API although facebook made it very difficult to scrape using other methods. In any case code gets broke then please look into the `xpath`s.

Steps:

0. Install the necessary libraries using `pip install -r requirements.txt`
1. Modify username and password in config file
2. execute any of the commands
    
    Command: 
    
    `py .\WebINT.py 2 <user-name>`
    
    `py .\WebINT.py 3 <user-name>`
    
    2 == Search for users by username and export all profile URLs to a CSV or Excel file.
    
    3 == Collect all of a user's public posts and save them to a file.
    
    note: use py3 if multiple python2 and python3 is install in the system
