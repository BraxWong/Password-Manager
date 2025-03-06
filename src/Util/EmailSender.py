import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendEmail(emailAddr, emailSubject, emailBody):
    msg = MIMEMultipart()
    msg['From'] = "bwmin123@gmail.com"
    msg['To'] = emailAddr
    msg['Subject'] = emailSubject 
    
    msg.attach(MIMEText(emailBody, 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("","")
            text = msg.as_string()
            server.sendmail("",emailAddr,text)
            print("Email has been sent successfully.")
    except:
        print("Error: unable to send email")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Please provide the email address, subject, and the body")
    else:
        sendEmail(sys.argv[1],sys.argv[2],sys.argv[3])
        print(f"Email Address: {sys.argv[1]}\nEmail Subject: {sys.argv[2]}\nEmail Body: {sys.argv[3]}")
