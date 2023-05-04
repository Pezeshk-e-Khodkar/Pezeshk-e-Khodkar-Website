from django.shortcuts import render
from django.views import View


class HomeView(View):
    """Home Page of API
    """
    def get(self, request):
        return render(request, 'index.html')


class HelpPage(View):
    def get(self, request):
        return render(request, 'help_page.html')
