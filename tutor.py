from dotenv import dotenv_values
from flask import Flask, render_template
from flask_mail import Mail, Message


app = Flask(__name__)

config = dotenv_values(".env")
app.config["MAIL_SERVER"] = config["MAIL_SERVER"]
app.config["MAIL_PORT"] = int(config["MAIL_PORT"])
app.config["MAIL_USERNAME"] = config["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = config["MAIL_PASSWORD"]
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/sendemail")
def index():
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
