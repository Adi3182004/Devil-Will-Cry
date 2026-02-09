from emergency.email_alert import EmailAlert

email = EmailAlert()
email.send(
    subject="TEST ALERT – Devil Will Cry",
    message="This is a test emergency email from Devil Will Cry system."
)
