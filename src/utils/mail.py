from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List




conf = ConnectionConfig(
    MAIL_USERNAME = "your-email@gmail.com",
    MAIL_PASSWORD = "you-email app password",
    MAIL_FROM = "teschsimplus@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="TechSimplus Learnings",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)



async def send_email(email:List[str]):
    html = """<p>Hi, Thanks for Registration.Our team will contact you soon.</p> """

    message = MessageSchema(
        subject="Registration confirmation",
        recipients=email,  
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    print({"message": "email has been sent:"})
