from djongo import models
import uuid
from datetime import datetime, timedelta

# Create your models here.
class ResetPasswordToken(models.Model):
    userId = models.IntegerField(unique=True, editable=False)
    uuidToken = models.CharField(
        max_length=36, default=str(uuid.uuid4()), unique=True, editable=False
    )
    expDate = models.DateTimeField(
        default=datetime.now() + timedelta(hours=12), editable=False
    )

    def __str__(self):
        return self.uuidToken
