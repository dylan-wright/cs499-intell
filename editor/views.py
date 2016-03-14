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

def index(request):
    return HttpResponse("Editor Index")

def edit(request):
    tableselect = ["character", "location", "description", "event",
                   "describedby", "happenedat", "involved"]
    context = {"tableselect": tableselect}
    return render(request, "editor/edit/index.html", context)
