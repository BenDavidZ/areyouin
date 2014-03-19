from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


  

class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event_name = models.CharField(max_length=200)
    event_description = models.TextField()
    event_datetime = models.DateTimeField()
    participants = models.ManyToManyField(User, through='Participating')
    
    def participant_count(self):
        return self.participants.all().count()
        
    def participant_confirmed(self):
        return self.participating_set.filter(date_accepted__lt=timezone.now()).count()
        
    def is_participating(self, user):
        if user.participating_set.get(event=self).date_accepted is None:
            return "Not in"
        else:
            return "In"
    
    def __unicode__(self):
        return self.event_name
        
class Participating(models.Model):
    participant = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    date_accepted = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return self.event.event_name
        
        





