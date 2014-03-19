from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from areyouin.models import Event, Participating
from areyouin.forms import UserForm, EventForm

# Create your views here.

def index(request):
    all_events_list = Event.objects.all().order_by('-created_at')
    if not request.user.is_authenticated():
        context = {'all_events_list': all_events_list}
    else: 
        unconfirmed_events_list = Event.objects.filter(participating__participant=request.user, participating__date_accepted__isnull=True)
        confirmed_events_list = Event.objects.filter(participating__participant=request.user, participating__date_accepted__isnull=False)
        context = {'all_events_list': all_events_list, 'unconfirmed_events_list': unconfirmed_events_list, 'confirmed_events_list': confirmed_events_list}
    return render(request, 'areyouin/index.html', context)


    
def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants = Participating.objects.filter(event=event)
    context = {'event': event, 'participants': participants}
    return render(request, 'areyouin/detail.html', context)
    
@login_required
def add_to_event(request, event_id, participant_id):
    event = Event.objects.get(pk=event_id)
    participant = User.objects.get(pk=participant_id)
    participant_event = participant.participating_set.get(event=event)
    participant_event.date_accepted = timezone.now()
    participant_event.save()
    
    return HttpResponseRedirect(reverse('areyouin:detail', args=(event.id,)))
    
def create_event(request):
    context = RequestContext(request)
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = Event.objects.create(
                event_name=event_form.cleaned_data['event_name'],
                event_description=event_form.cleaned_data['event_description'],
                event_datetime=event_form.cleaned_data['event_datetime']
            )
            for participant_id in request.POST.getlist('participants'):
                p1 = Participating(participant_id=participant_id, event=event)
                p1.save()
            return HttpResponseRedirect(reverse('areyouin:index'))
        else:
            print event_form.is_valid()
            print event_form.errors
    event_form = EventForm()
    return render_to_response(
        'areyouin/create_event.html',
        {'event_form': event_form},
        context)
    
def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('areyouin:index'))
            return HttpResponseRedirect(reverse('areyouin:login'))
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    return render_to_response(
        'areyouin/register.html',
        {'user_form': user_form, 'registered': registered},
        context)
        
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('areyouin:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: %s, %s." % (username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('areyouin/login.html', {}, context)
        
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('areyouin:index'))
        
    