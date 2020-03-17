import requests
from bs4 import BeautifulSoup
import smtplib
import time

def check_price():
    URL = 'https://finance.yahoo.com/quote/%5EGSPC/' # tracking real time data from Yahoo finance for S&P 500
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.select("div span[data-reactid*='35']")[0].text # might need to change the reactid value which can be found if you inspect the page, if you choose different index or change the whole line if you dont use Yahoo Finance
    check_price.new_value = float(price.split()[0].replace(',', '')) # converting the data from string to float

    if not hasattr(check_price,"old_value"): # initial value is 0 then store new_value to old_value 
        print("initial value 0")             # so the next time check_price function gets called,
        check_price.old_value = check_price.new_value # its gonna compare the old_value to new_value
    if abs(check_price.old_value - check_price.new_value) >= 50 : # if old_value and new_value differs by .5 then the function will send mail
        send_mail() 

    check_price.old_value = check_price.new_value
    
def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587) # using Gmail smtp and using port 587
    server.ehlo() # DO NOT REMOVE
    server.starttls() # Creating secure connection
    server.ehlo() # DO NOT REMOVE
    server.login('', '') # Insert sender login credentials 

    subject = "S&P Index Change" 
    body = "S&P 500 index just changed from " + str(check_price.old_value) + " to " + str(check_price.new_value)
    
    msg = 'Subject: {}\n\n{}'.format(subject, body)

    server.sendmail(
        '', # Insert sender email
        '', # Insert receiver email 
        msg
    )

    print ("Email was sent succesfully")
    server.quit()

check_price()
while (True): # runs infinitely and pauses every 3600 seconds which is 1 hour, when it runs, 
     check_price() # its gonna check the price and determine whether it should send an email or not
     time.sleep(1800)
     
      