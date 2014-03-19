from django.contrib import admin

from areyouin.models import Event, Participating

# Register your models here.

class ParticipatingInline(admin.TabularInline):
    model = Event.participants.through
    extra = 1
    
class ParticipatingAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event', 'date_accepted')
    
    
    
# class ParticipantAdmin(admin.ModelAdmin):
    # list_display = ('name', 'email', 'event_count')
    
    # def event_count(self, Participant):
        # return Participant.participating_set.count()
    
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'participant_count')
    inlines = [ParticipatingInline]
    
    
    
    def participant_count(self, Event):
        return Event.participants.all().count()
    participant_count.short_description = 'Number Invited'
    
   
    


admin.site.register(Event, EventAdmin)
# admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Participating, ParticipatingAdmin)

