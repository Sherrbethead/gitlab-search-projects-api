from django.contrib import admin
from .models import SearchData

# Admin panel for handling SearchData model
# The only way to delete all the data simultaneously
admin.site.register(SearchData)
