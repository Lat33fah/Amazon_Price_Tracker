import requests
from bs4 import BeautifulSoup
import smtplib
import os

amazon_url = 'https://www.amazon.com/s?k=television&crid=2Y6ER58YGYVPM&sprefix=television%2Caps%2C325&ref=nb_sb_noss_2'
header = {
    "Accept-Language": "en-GB,en;q=0.9,ar-AE;q=0.8,ar;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 "
                  "Safari/537.36 "
}
my_email = os.environ['my_email']
password = os.environ['password']

response = requests.get(url=amazon_url, headers=header)
soup = BeautifulSoup(response.text, 'lxml')
price = soup.find(name='span', class_="a-offscreen").text
text = soup.find(name='span', class_="a-size-medium a-color-base a-text-normal").text
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

target_price = 20.00
if price_as_float < target_price:
    with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as connection:
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=os.environ['to_address'],
                            msg=f"Subject:Amazon Price Alert\n\n{text} is now ${price_as_float}.\nBuy now:{amazon_url}")
