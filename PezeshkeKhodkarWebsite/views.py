from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.views import View
from django.conf import settings


# View for robot.txt
class RobotTxtView(View):
    lines = [
        "User-Agent: *",
        "Disallow: /media/",
        "Sitemap: https://pezeshkekhodkar.ir/sitemap.xml",
    ]

    def get(self, request):
        return HttpResponse("\n".join(self.lines), content_type="text/plain")


class SitMapView(View):
    sitemap = open(settings.BASE_DIR/"sitemap.xml", "r").read()
    def get(self, request):
        return HttpResponse(self.sitemap, content_type="text/plain")
