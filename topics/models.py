from djongo import models
import uuid

# Create your models here.
class Option(models.Model):
    _id = models.CharField(max_length=36, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=255)
    bias = models.PositiveIntegerField()
    pulls = models.PositiveIntegerField()
    reward = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Topic(models.Model):
    _id = models.CharField(max_length=36, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=255)
    policy = models.PositiveIntegerField()
    t = models.IntegerField()
    options = models.ArrayField(model_container=Option, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AppUser(models.Model):
    _id = models.CharField(
        max_length=36, default=uuid.uuid4, unique=True, editable=False
    )
    username = models.CharField(max_length=255, unique=True)
    language = models.CharField(max_length=2, default="en")
    selectedTopicId = models.CharField(max_length=255, null=True)
    topics = models.ArrayField(model_container=Topic, blank=True)

    def __str__(self):
        return self.username
