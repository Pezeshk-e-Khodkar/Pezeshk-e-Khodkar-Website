from django.shortcuts import render
from django.views import View


class HomeView(View):
    """Home Page
    """
    def get(self, request):
        return render(request, 'index.html')


class HelpPage(View):
    """Help Page
    """
    def get(self, request):
        return render(request, 'help_page.html')
