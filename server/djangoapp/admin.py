from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
# Register CarMake and CarModel in the Django admin panel
admin.site.register(CarMake)
admin.site.register(CarModel)