from django.contrib import admin

# Register your models here.
from .models import stargate, myData, myCalc, myStatus, myTarget

admin.site.register(stargate)
admin.site.register(myData)
admin.site.register(myCalc)
admin.site.register(myStatus)
admin.site.register(myTarget)