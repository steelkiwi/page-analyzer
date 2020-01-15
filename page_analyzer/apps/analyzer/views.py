from django.shortcuts import redirect, reverse
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from .forms import AnalysisTriggerForm
from .models import Analysis


class AnalysisTriggerView(FormView):
    template_name = 'analyzer/analysis.html'
    form_class = AnalysisTriggerForm
    success_url = '/done/'

    def form_valid(self, form):
        instance = form.save()
        instance.perform_analysis()
        return redirect(reverse('analysis-detail', kwargs={'pk': instance.pk}))


class AnalysisDetailView(DetailView):
    model = Analysis
    context_object_name = 'analysis'
