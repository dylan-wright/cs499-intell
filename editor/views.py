from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.db import connection
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .forms import *
from django.template import RequestContext


# Create your views here.
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

def index(request):
    return render(request, "editor/index.html")

def edit(request):
    tableselect = ["character", "location", "description", "event",
                   "describedby", "happenedat", "involved"]
    context = {"tableselect": tableselect}
    return render(request, "editor/edit/index.html", context)

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
        dump request data to template
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
        context = {"data":request.body}
    else:
        context = {"data":request}
    return render(request, "editor/accept_ajax_scenario.html", context)
