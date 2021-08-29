from django.contrib import admin
from Main.models import *
import Main.models

# Register your models here.

for model in dir(Main.models):
    try:
        admin.site.register(eval("Main.models." + model))
    except:
        continue
