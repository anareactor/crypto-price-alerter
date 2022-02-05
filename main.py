from bs4 import BeautifulSoup
import requests
import time
import smtplib
import ssl
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MM

def get_crypto_price(coin):
    url = "https://www.google.com/search?q="+coin+"+price"

    HTML = requests.get(url)

    soup = BeautifulSoup(HTML.text, 'html.parser')

    text = soup.find("div", attrs={'class':'BNeawe iBp4i AP7Wnd'}).text

    return text

receiver = ''#your email
sender = ''#your email
sender_password = ''#put your emails password

def send_email(sender, receiver, sender_password, text_price):
    msg = MM()
    msg['Subject'] = "New Crypto Price Alert !"
    msg['From']= sender
    msg['To']= receiver


    HTML = """
      <html>
        <body>
          <h1>New Crypto Price Alert !</h1>
          <h2>"""+text_price+"""
          </h2>
        </body>
      </html>
      """

    MTObj = MT(HTML, "html")

    msg.attach(MTObj)


    SSL_context = ssl.create_default_context()

    server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=SSL_context)

    server.login(sender, sender_password)

    server.sendmail(sender, receiver, msg.as_string())

def send_alert():
    last_price = -1

    while True:

        coin = 'bitcoin'#you can pick whatever coin you want!

        price = get_crypto_price(coin)

        if price != last_price:
            print(coin.capitalize()+' price: ', price)
            price_text = coin.capitalize()+' is '+price
            send_email(sender, receiver, sender_password, price_text)
            last_price = price
            time.sleep(3)


send_alert()