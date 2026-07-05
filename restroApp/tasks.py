from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_conformation(item_text, total, email, username):
    try:
        tax = total * 0.13
        total_price = tax + total

        subject = "Order Confirmed."
        
        # Render HTML template
        html_message = render_to_string('emails/order_confirmation.html', {
            'username': username,
            'item_text': item_text,
            'total': total,
            'tax': tax,
            'total_price': total_price
        })
        
        logger.info(f"HTML template rendered successfully for {email}")
        logger.info(f"HTML length: {len(html_message)}")
        
        # Plain text fallback
        plain_message = f'''Dear {username},

Your order has been confirmed. Here are your items:

{item_text}

Subtotal: Rs.{total}
Tax (13%): Rs.{tax}
Grand Total: Rs.{total_price}

Thank you for ordering with us!

Best regards,
RestroArt Team'''
        
        host_email = settings.EMAIL_HOST_USER
        
        msg = EmailMultiAlternatives(subject, plain_message, host_email, [email])
        msg.attach_alternative(html_message, "text/html")
        msg.mixed_subtype = 'related'
        msg.send()
        
        logger.info(f"Email sent successfully to {email}")
        return f"Email sent to {email}"
    except Exception as e:
        logger.error(f"Error sending email to {email}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise


@shared_task
def reservation_seat(name, date, time, guest, email):
    try:
        subject = 'Reservation Booked'
        
        # Render HTML template
        html_message = render_to_string('emails/reservation_confirmation.html', {
            'name': name,
            'date': date,
            'time': time,
            'guest': guest
        })
        
        logger.info(f"HTML template rendered successfully for {email}")
        logger.info(f"HTML length: {len(html_message)}")
        
        # Plain text fallback
        plain_message = f'''Dear {name},

We are pleased to confirm your reservation at our restaurant.
Your booking has been scheduled for {date}, at {time}, for {guest} people.

We look forward to hosting you and ensuring you have a wonderful dining experience.

Warm regards,
RestroArt Team'''
        
        host_email = settings.EMAIL_HOST_USER
        
        msg = EmailMultiAlternatives(subject, plain_message, host_email, [email])
        msg.attach_alternative(html_message, "text/html")
        msg.mixed_subtype = 'related'
        msg.send()
        
        logger.info(f"Email sent successfully to {email}")
        return f"Email sent to {email}"
    except Exception as e:
        logger.error(f"Error sending email to {email}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise
