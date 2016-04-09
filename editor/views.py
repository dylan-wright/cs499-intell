'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

    editor/views.py
        Django class based views
            CharacterCreate
            CharacterUpdate
            CharacterDelete
            CharacterList
            LocationCreate
            LocationUpdate
            LocationDelete
            LocationList
            DescriptionCreate
            DescriptionUpdate
            DescriptionDelete
            DescriptionList
            EventCreate
            EventUpdate
            EventDelete
            EventList
            DescribedByCreate
            DescribedByUpdate
            DescribedByDelete
            DescribedByList
            HappenedAtCreate
            HappenedAtUpdate
            HappenedAtDelete
            HappenedAtList
            InvolvedCreate
            InvolvedUpdate
            InvolvedDelete
            InvolvedList
        Django func based views
            index
            edit
            accept_ajax_scenario
            login
            logout_view
            register
            dump_session
            dump_request

    TODO:   clean this up
'''

#TODO: remove this
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.db import connection
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .forms import *
from django.template import RequestContext
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.files import File
from django.conf import settings
from django.core.files.base import ContentFile

# Create your views here.
'''
generic Create/Update/Delete/List pages
    CreateView -> templates/editor/edit/create_form.html
    UpdateView -> templates/editor/edit/update_form.html
    DeleteView -> templates/editor/edit/delete_form.html
    ListView   -> templates/editor/edit/list_view.html
'''
class CharacterCreate(CreateView):
    template_name = "editor/edit/create_form.html"
    model = Character
    fields = ["name", "key", "notes"]
class CharacterUpdate(UpdateView):
    template_name = "editor/edit/update_form.html"
    model = Character
    fields = ["name", "key", "notes"]
class CharacterDelete(DeleteView):
    template_name = "editor/edit/delete_form.html"
    model = Character
    success_url = "../../"
class CharacterList(ListView):
    template_name = "editor/edit/list_view.html"
    model = Character
    def get_context_data(self, **kwargs):
        context = super(CharacterList, self).get_context_data(**kwargs)
        context["tablename"]="character"
        return context

class LocationCreate(CreateView):
    template_name = "editor/edit/create_form.html"
    model = Location
    fields = ["name", "x", "y"]
class LocationUpdate(UpdateView):
    template_name = "editor/edit/update_form.html"
    model = Location
    fields = ["name", "x", "y"]
class LocationDelete(DeleteView):
    template_name = "editor/edit/delete_form.html"
    model = Location
    success_url = "../../"
class LocationList(ListView):
    template_name = "editor/edit/list_view.html"
    model = Location
    def get_context_data(self, **kwargs):
        context = super(LocationList, self).get_context_data(**kwargs)
        context["tablename"]="location"
        return context

class DescriptionCreate(CreateView):
    template_name = "editor/edit/create_form.html"
    model = Description
    fields = ["text", "key", "hidden"]
class DescriptionUpdate(UpdateView):
    template_name = "editor/edit/update_form.html"
    model = Description
    fields = ["text", "key", "hidden"]
class DescriptionDelete(DeleteView):
    template_name = "editor/edit/delete_form.html"
    model = Description
    success_url = "../../"
class DescriptionList(ListView):
    template_name = "editor/edit/list_view.html"
    model = Description
    def get_context_data(self, **kwargs):
        context = super(DescriptionList, self).get_context_data(**kwargs)
        context["tablename"]="description"
        return context

class EventCreate(CreateView):
    template_name = "editor/edit/create_form.html"
    model = Event
    fields = ["turn"]
class EventUpdate(UpdateView):
    template_name = "editor/edit/update_form.html"
    model = Event
    fields = ["turn"]
class EventDelete(DeleteView):
    template_name = "editor/edit/delete_form.html"
    model = Event
    success_url = "../../"
class EventList(ListView):
    template_name = "editor/edit/list_view.html"
    model = Event
    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context["tablename"]="event"
        return context


class DescribedByCreate(CreateView):
    template_name = "editor/edit/create_form.html"
    model = DescribedBy
    fields = ["event", "description"]
class DescribedByUpdate(UpdateView):
    template_name = "editor/edit/update_form.html"
    model = DescribedBy
    fields = ["event", "description"]
class DescribedByDelete(DeleteView):
    template_name = "editor/edit/delete_form.html"
    model = DescribedBy
    success_url = "../../"
class DescribedByList(ListView):
    template_name = "editor/edit/list_view.html"
    model = DescribedBy
    def get_context_data(self, **kwargs):
        context = super(DescribedByList, self).get_context_data(**kwargs)
        context["tablename"]="describedby"
        return context

class HappenedAtCreate(CreateView):
    template_name = "editor/edit/create_form.html"
    model = HappenedAt
    fields = ["event", "location"]
class HappenedAtUpdate(UpdateView):
    template_name = "editor/edit/update_form.html"
    model = HappenedAt
    fields = ["event", "location"]
class HappenedAtDelete(DeleteView):
    template_name = "editor/edit/delete_form.html"
    model = HappenedAt
    success_url = "../../"
class HappenedAtList(ListView):
    template_name = "editor/edit/list_view.html"
    model = HappenedAt
    def get_context_data(self, **kwargs):
        context = super(HappenedAtList, self).get_context_data(**kwargs)
        context["tablename"]="happenedat"
        return context

class InvolvedCreate(CreateView):
    template_name = "editor/edit/create_form.html"
    model = Involved
    fields = ["event", "character"]
class InvolvedUpdate(UpdateView):
    template_name = "editor/edit/update_form.html"
    model = Involved
    fields = ["event", "character"]
class InvolvedDelete(DeleteView):
    template_name = "editor/edit/delete_form.html"
    model = Involved
    success_url = "../../"
class InvolvedList(ListView):
    template_name = "editor/edit/list_view.html"
    model = Involved
    def get_context_data(self, **kwargs):
        context = super(InvolvedList, self).get_context_data(**kwargs)
        context["tablename"]="involved"
        return context

'''
index for editor
    index -> templates/editor/index.html
'''
def index(request):
    return render(request, "editor/index.html")

'''
navigation page for page based (protoeditor)
    edit -> templates/editor/edit/index.html
'''
def edit(request):
    return render(request, "editor/edit/edit.html")

'''
    accept_ajax_scenario
        recv ajax from editor FE
        sanitize JSON contents
        validate contents
        generate file name and save
        store file name in db

    ref:
        djangoproject serializer/deserializer
        https://docs.djangoproject.com/en/dev/topics/serialization/

    current use:
        Dump deserialized objects from JSON file. currently using 
        /editor/static/editor/fixture.json for testing
'''
@csrf_exempt
def accept_ajax_scenario(request):
    # recv assumed
    # sanitize
    # validate
    # generate file name
    # save json
    # add file name to db
    if request.method == 'POST':
        data = []

        #fileUpload = request.FILES['fileUpload']
        body = request.body
        for obj in serializers.deserialize("json", body):
            if isinstance(obj.object, Scenario):
                scenario = obj.object
            else:
                obj.save()
            data.append(obj)
        context = {"data":data}

        if (scenario != None):
            scenario.author=""
            scenario.save()
            scenario.file_name.save(str(scenario.id), ContentFile(body))
            scenario.save()
        #scenario.save()
        #file_name = str(scenario.id)
        #scenario.file_name.save(file_name, fileUpload)
        #scenario.save()
    else:
        context = {"data":request}
    return render(request, "editor/accept_ajax_scenario.html", context)

#TODO: move registrations things out of editor
'''
    login
        read post username/password
        authenticate
'''
'''
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect("/account/loggedin")
    else:
        return HttpResponseRedirect("/account/invalid")
'''

'''
    logout
        logout user
'''
'''
def logout_view(request):
    logout(request)
    HttpResponseRedirect("/account/loggedout")
'''
'''
    register

    http://www.djangobook.com/en/2.0/chapter14.html
'''
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/editor/dump_session/")
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, "registration/register.html", context)

def dump_session(request):
    context = {"session": request.session.items}
    return render(request, "editor/dump_session.html", context)

@csrf_exempt
def dump_request(request):
    if request.method == "GET":
        context = {"request": request.GET, "meta": request.META}
    elif request.method == "POST":
        context = {"request": request.POST, 
                   "files": request.body,
                   "meta": request.META}
    return render(request, "editor/dump_request.html", context)
