from django.shortcuts import render
from django.views.generic import TemplateView


class DashBoardView(TemplateView):
    template_name = 'base_layouts/index.html'


class Random(TemplateView):
    template_name = 'base_layouts/index.html'