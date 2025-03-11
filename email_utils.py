from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os

# Update the configuration to match FastAPI-Mail's requirements
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "shamaalam7474@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "jchi yuyg zqez fsld"),
    MAIL_FROM=os.getenv("MAIL_FROM", "shamaalam7474@gmail.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=bool(os.getenv("MAIL_STARTTLS", True)),  # Corrected field name
    MAIL_SSL_TLS=bool(os.getenv("MAIL_SSL_TLS", False)),   # Add this line
    USE_CREDENTIALS=bool(os.getenv("USE_CREDENTIALS", True)),
)

async def send_verification_email(email: str, token: str):
    verification_link = f"http://localhost:8000/users/verify-email?token={token}"
    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],
        body=f"Click the link to verify your email: {verification_link}",
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
