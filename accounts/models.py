from django.db.models.fields import CharField, IntegerField
from djongo import models
import uuid
from datetime import datetime, timedelta

# Create your models here.
class ResetPasswordToken(models.Model):
    userId = models.IntegerField()
    uuidToken = models.CharField(max_length=36, default=uuid.uuid4(), unique=True, primary_key=True)
    expDate = models.DateTimeField(default=datetime.now()+timedelta(hours=12))