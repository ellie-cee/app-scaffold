from datetime import timedelta
from django.utils import timezone
from django_q.tasks import async_task, schedule
from django_q.models import Schedule
import logging
from home.lmno import sendEmail

logger = logging.Logger(__name__)

def test():
    sendEmail(
        recipient="cassafyeleanor@gmail.com",
        subject="test scheduler",
    )