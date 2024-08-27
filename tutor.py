from dotenv import dotenv_values
from flask import Flask, render_template, request
from flask_mail import Mail, Message

import verify_recaptcha

config = dotenv_values(".env")
app = Flask(__name__)

app.config["MAIL_SERVER"] = config["MAIL_SERVER"]
app.config["MAIL_PORT"] = int(config["MAIL_PORT"])
app.config["MAIL_USERNAME"] = config["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = config["MAIL_PASSWORD"]
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)

@app.route('/')
def index():
    sitekey = config['RECAPTCHA_SITE_KEY']
    return render_template('index.html', sitekey=sitekey)

@app.route("/submit", methods=["POST"])
def submit():
    # get token from recaptcha
    recaptcha_token = request.form["g-recaptcha-response"]
    recaptcha_score = verify_recaptcha.get_assessment_score(recaptcha_token, "SUBMIT")
    if recaptcha_score < 0.5:
        return "Recaptcha failed. If you're not a bot, try again."
    # get data from form
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]
    # send email
    msg = Message(
        subject='Tutor Request', 
        sender=config['MAIL_USERNAME'],
        recipients=[config['MAIL_USERNAME']]
    )
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    mail.send(msg)
    return "Message sent!"


@app.route("/sendemail")
def send_email():
    msg = Message(
        subject='Hello from the other side!', 
        sender=config['MAIL_USERNAME'],
        recipients=[config['MAIL_USERNAME']]
    )
    msg.body = "Hey, sending you this email from my Flask app, let me know if it works."
    mail.send(msg)
    return "Message sent!"

if __name__ == '__main__':
    app.run(debug=True)
