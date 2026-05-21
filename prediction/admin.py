from django.contrib import admin

from .models import Patient
from .models import Prediction
from .models import Alert


admin.site.register(Patient)

admin.site.register(Prediction)

admin.site.register(Alert)