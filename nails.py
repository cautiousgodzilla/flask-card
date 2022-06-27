import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from workers import celery
from flask import current_app as app
from datetime import datetime


SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "email@mail.com"
SENDER_PASSWORD = "xxx"
from workers import celery
from celery.schedules import crontab

@celery.on_after_finalize.connect ##finalize
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour="*", minute='*/1', day_of_week='*'), send_email.s(to_address="email@mail.com", subject="Reminderz", message="Review Flashcards everyday for good memory"), name='mail daily')

@celery.task()
def send_email(to_address, subject, message):
	msg = MIMEMultipart()
	msg["From"] = SENDER_ADDRESS
	msg["To"] = to_address
	msg["Subject"] = subject

	msg.attach(MIMEText(message,"html"))
	print("works")
	s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
	print("still?")
	s.ehlo()
	#s.starttls()
	s.login(SENDER_ADDRESS, SENDER_PASSWORD)
	s.send_message(msg)
	s.quit()

	return True

def main():
	new_users = [
		{"name" : "Raj", "email" : "raj@mail.com"},
		{"name" : "Yasmin", "email" : "yasmin@mail.com"}
	]
	for user in new_users:
		send_email(user["email"], subject="Hello", message="Welcome")

if __name__ == "__main__":
	main()