from django.urls import path
from . import views

app_name = "tracker"
urlpatterns = [
    path("", views.index, name="index"),
    path('test-fda/', views.test_openfda, name='test_fda'),
]