import csv
import random
import smtplib, ssl
from email.message import EmailMessage

## CREATING MATCHING TABLE

with open('list.csv', 'r') as f:
  reader = csv.reader(f) ## CSV must be : first line names, second line emails
  raw = list(reader)

#print(raw[1]) ## csv converted to python list

L = [] ## shape of the list will be [[name1,email1],[name2,email2],...]

for i in range(0,len(raw[0])):
    L.append([raw[0][i],raw[1][i]])


random_indexes = [] ## List will be [[index_1,index_x],[index_2,index_y],...] with index_1 matching with index_x
available = [i for i in range(0,len(L))] ## available indexes

## construction de tirage_indices
for i in range(0,len(L)):
    if len(available) == 1: ## last email case
        assert(i != available[0]) ## if they're identical
        random_indexes.append([i,available[0]]) ## if they're not identical, it's ok
    else: ## as long as there is at least 2 elements
        a = random.choice(available) ## choosing a random index
        while a == i: ## repeating the choice if matching with itself
            a = random.choice(available)
        random_indexes.append([i,a])
        available.remove(a) ## a isn't available anymore

random_names = [] ## same as random_indexes but [email, name]

for l in random_indexes:
    random_names.append([L[l[0]][1],L[l[1]][0]])

## ENVOI DES MAILS

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = ## your mail here, must be gmail account
password = ## your password here

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, password)

    for i in range(0,len(random_names)):
        receiver_email = random_names[i][0]
        message = EmailMessage()
        message.set_content("""Hey, you got """+random_names[i][1]+""" !""") ## this is the message
        message['Subject'] = "Secret Santa"
        message['From'] = sender_email
        message['To'] = random_names[i][0]
        server.send_message(message) ## sends the email
        print(random_names[i][0], ", email sent.")


except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()
