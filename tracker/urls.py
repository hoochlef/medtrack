from django.urls import path
from . import views

app_name = "tracker"
urlpatterns = [
    path("", views.medication_lookup, name="medication_lookup"),
    path('test-fda/', views.test_openfda, name='test_fda'),
]