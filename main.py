import os
from base64 import b64encode
import telebot
import pymysql.cursors
import time
import random
import string
# Connect to the database
connection = pymysql.connect(host='localhost',
user='risaro',
password='Korvo228',
db='vmail',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)
bot = telebot.TeleBot('TOKEN')
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'WRITE COUNT EMAIL TO CREATE )')
@bot.message_handler(content_types=["text"])
def handle_text(message):
    count = message.text
    os.path.isfile("email.txt")
    email_file = open("email.txt", "w")
    email_file.close()
    i = int(message.text)
    while i != 0:
      login = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(6))
      password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(8))
      ps = password
      p = str(password).strip()
      from hashlib import sha512
      salt = os.urandom(8)
      pw = sha512(p.encode('utf-8'))
      pw.update(salt)
      password = '{SSHA512}' + b64encode(pw.hexdigest().encode('utf_16_le') + salt).decode('utf-8')
      try:
        with connection.cursor() as cursor:
          sql = "INSERT INTO mailbox (username, password, name, storagebasedirectory,storagenode, maildir, quota, domain, active, passwordlastchange, created) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, '1', NOW(), NOW());"
          cursor.execute(sql, (
          str(login) + '@mail.aurakingdom.ru', str(password), 'Letin Kilk', 'Maildir', '/var/vmail', 'vmail', '1024',
          'mail.aurakingdom.ru/' + login[0] + '/' + login[1] + '/' + login[2] + '/' + login))
          connection.commit()
        with connection.cursor() as cursor:
          # Create a new record
          sql = "SET @@global.sql_mode= '';"
          cursor.execute(sql)
          connection.commit()
        with connection.cursor() as cursor:
          # Create a new record
          sql = "INSERT INTO forwardings (address, forwarding, domain, dest_domain, is_forwarding) VALUES (%s, %s,%s, %s, 1);"
          cursor.execute(sql, (str(login) + '@mail.aurakingdom.ru', str(login) + '@mail.aurakingdom.ru',
                               'mail.aurakingdom.ru/' + login[0] + '/' + login[1] + '/' + login[2] + '/' + login,
                               'mail.aurakingdom.ru/' + login[0] + '/' + login[1] + '/' + login[2] + '/' + login))
          connection.commit()
      finally:
        i = i - 1
        time.sleep(2)
        file = open('email.txt', 'a')
        file.write(login + "@mail.aurakingdom.ru:"+ps+"|")
        print('write in file' + str(login) + '@mail.aurakingdom.ru:' + str(ps))
        file.close()
    bot.send_message(message.chat.id, 'Закночил работу , созданно более '+count+' почт')
    with open('email.txt', 'rb') as f1:
      bot.send_document(message.chat.id, f1)
bot.polling(none_stop=True, interval=0)



