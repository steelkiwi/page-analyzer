from django.db import models
from django.utils import timezone
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
from .utils import get_links, links_count_inaccessible


class Analysis(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    cached = models.DateTimeField(null=True, blank=True)

    response_code = models.CharField(max_length=5, null=True, blank=True)
    error_description = models.CharField(max_length=300, blank=True, null=True)

    http_version = models.CharField(max_length=5, null=True, blank=True)
    page_title = models.CharField(max_length=300, null=True, blank=True)
    is_login = models.BooleanField(default=False)

    def perform_analysis(self):
        if self.cached is not None and (self.cached + timedelta(hours=24)) > timezone.now():
            return True
        else:
            try:
                self.flush_related()
                r = requests.get(self.url, timeout=5)
                self.response_code = r.status_code
                self.error_description = r.reason
                self.http_version = str(r.raw.version)[:1] + '.' + str(r.raw.version)[1:]
                if r.status_code == requests.codes.ok:
                    soup = BeautifulSoup(r.text, 'html.parser')

                    self.page_title = soup.title.string

                    for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                        heading_count = len(soup.find_all(tag))
                        heading = Heading(tag=tag, count=heading_count, analysis=self)
                        heading.save()

                    links_dict = get_links(soup=soup, url=self.url)

                    internal_links_inaccessible_count = links_count_inaccessible(links_dict['internal'])
                    internal_link = Link(analysis=self, type='INTERNAL', count=len(links_dict['internal']),
                                         inaccessible_count=internal_links_inaccessible_count)
                    internal_link.save()

                    external_links_inaccessible_count = links_count_inaccessible(links_dict['external'])
                    internal_link = Link(analysis=self, type='EXTERNAL', count=len(links_dict['external']),
                                         inaccessible_count=external_links_inaccessible_count)
                    internal_link.save()

                    input_types = ["password", "text", "email", "submit", "tel", "hidden"]
                    input_names = ["login", "user", "username", "passwd", "pass", "password", "tel", "email", "uid"]

                    login_related_inputs = soup.findAll('input', {'type': input_types, 'name': input_names})
                    if len(login_related_inputs) > 0:
                        self.is_login = True

            except requests.Timeout:
                self.response_code = '000'
                self.error_description = 'No response due to timeout.'

        self.cached = timezone.now()
        self.save()

    def flush_related(self):
        self.links.all().delete()
        self.headings.all().delete()


class Heading(models.Model):
    analysis = models.ForeignKey(Analysis, related_name='headings', on_delete=models.CASCADE)
    tag = models.CharField(max_length=15)
    count = models.IntegerField(null=True, blank=True)


LINK_TYPE_CHOICES = [
    ('UNSET', 'Links type not set.'),
    ('INTERNAL', 'Internal links'),
    ('EXTERNAL', 'External links')
]


class Link(models.Model):
    analysis = models.ForeignKey(Analysis, related_name='links', on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=LINK_TYPE_CHOICES, default=LINK_TYPE_CHOICES[0][0])
    count = models.IntegerField(null=True, blank=True)
    inaccessible_count = models.IntegerField(null=True, blank=True)
