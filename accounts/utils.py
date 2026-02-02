import random
from django.core.mail import send_mail

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_email(user, otp):
    """Send OTP to user via email"""
    subject = "Your Soko Hub Login OTP"
    message = f"Hello {user.username},\n\nYour OTP is: {otp}\nIt expires in 10 minutes."
    send_mail(subject, message, 'Soko Hub <noreply@sokohub.com>', [user.email])
