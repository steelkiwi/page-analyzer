from django.urls import path, include
from .views import AnalysisTriggerView,AnalysisDetailView

urlpatterns = [
    path("", AnalysisTriggerView.as_view(), name='analysis-trigger'),
    path('analysis/<int:pk>/', AnalysisDetailView.as_view(), name='analysis-detail')
]
