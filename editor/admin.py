from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Character)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Description)
admin.site.register(DescribedBy)
admin.site.register(HappenedAt)
admin.site.register(Involved)
