from django.shortcuts import render, redirect

from django.urls import reverse

from .models import Topic, Entry

from .forms import TopicForm, EntryForm

from django.contrib.auth.decorators import login_required

from django.http import Http404
# Create your views here.

def check_topic_owner(topic, request):
    return topic.owner==request.user

def index(request):
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')
    context= {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    topic=Topic.objects.get(id=topic_id)
    if not check_topic_owner(topic, request):
        raise Http404
    entries=topic.entry_set.order_by('date_added')
    context={'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    if request.method!= 'POST':
        #Дані не відправлялись, створюється пуста форма
        form=TopicForm()
    else:
        #Обробка данних
        form=TopicForm(data=request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()

            return redirect(reverse('learning_logs:topics'))
    context={"form":form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic=Topic.objects.get(id=topic_id)
    if request.method!= 'POST':
        #Дані не відправлялись, створюється пуста форма
        form=EntryForm()
    else:
        #Обробка данних
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry_object=form.save(commit=False)
            new_entry_object.topic=topic
            if not check_topic_owner(topic, request):
                raise Http404
            new_entry_object.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    context={"form":form, 'topic': topic,}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """"""
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic

    if not check_topic_owner(topic, request):
        raise Http404

    if request.method!='POST':
        form=EntryForm(instance=entry)
    else:
        form=EntryForm(instance=entry, data=request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        

    context={
        'entry':entry,
        'topic':topic,
        'form':form,
    }
    return render(request, 'learning_logs/edit_entry.html', context)