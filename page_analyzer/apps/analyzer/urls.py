from django.urls import path
from .views import AnalysisTriggerView

urlpatterns = [
    path("analyze-url/", AnalysisTriggerView.as_view(), name='analyze-url'),

]
