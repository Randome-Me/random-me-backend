from djongo import models

# Create your models here.  
class Option(models.Model):
    name = models.CharField(max_length=255)
    bias = models.PositiveIntegerField()
    pulls = models.PositiveIntegerField()
    reward = models.PositiveIntegerField()
    
    class Meta:
        abstract = True
    
class Topic(models.Model):
    name = models.CharField(max_length=255)
    policy = models.CharField(max_length=255)
    t = models.IntegerField()
    option = models.ArrayField(
        model_container=Option,
        blank=True
    )
    
    class Meta:
        abstract = True
    
class AppUser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    selectedTopicId = models.CharField(max_length=255)
    topic = models.ArrayField(
        model_container=Topic,
        blank=True
    )