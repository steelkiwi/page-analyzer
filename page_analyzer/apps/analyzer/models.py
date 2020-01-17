from urllib.request import urlparse, urljoin
from django.db import models
from bs4 import BeautifulSoup
import requests
from model_utils import Choices


class Analysis(models.Model):
    #  Waiting timeout for server response in seconds
    REQUEST_TIMEOUT = 5

    HANDLED_HEADINGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
    # Form detecting constants
    INPUT_TYPES = ["password", "text", "email", "submit", "tel", "hidden"]
    INPUT_NAMES = ["login", "user", "username", "passwd", "pass", "password", "tel", "email", "uid"]

    created = models.DateTimeField(auto_now_add=True)
    url = models.URLField()

    response_code = models.CharField(max_length=5, blank=True, default='')
    error_description = models.CharField(max_length=300, blank=True, default='')

    http_version = models.CharField(max_length=5, blank=True, default='')
    page_title = models.CharField(max_length=300, blank=True, default='')
    is_login = models.BooleanField(default=False)

    def perform_analysis(self):
        try:
            response = requests.get(self.url, timeout=self.REQUEST_TIMEOUT)
            self.response_code = response.status_code
            self.error_description = response.reason
            self.http_version = str(response.raw.version)[:1] + '.' + str(response.raw.version)[1:]
            if response.status_code == requests.codes.ok:  # pylint: disable=no-member
                soup = BeautifulSoup(response.text, 'html.parser')

                self.page_title = soup.title.string
                self.collect_headings(soup)
                self.detect_login(soup)

                links_dict = self.get_links(soup)
                self.collect_links(links=links_dict[Link.EXTERNAL], link_type=Link.EXTERNAL)
                self.collect_links(links=links_dict[Link.INTERNAL], link_type=Link.INTERNAL)

        except requests.Timeout:
            self.response_code = '000'
            self.error_description = 'No response due to timeout.'

        self.save()

    def collect_links(self, links, link_type):
        link = Link(analysis=self, link_type=link_type, count=len(links),
                    inaccessible_count=self.links_count_inaccessible(links))
        link.save()

    def collect_headings(self, soup):
        for tag in self.HANDLED_HEADINGS:
            heading_count = len(soup.find_all(tag))
            heading = Tag(tag=tag, count=heading_count, analysis=self, tag_type=Tag.HEADINGS)
            heading.save()

    def detect_login(self, soup):
        login_related_inputs = soup.findAll('input', {'type': self.INPUT_TYPES, 'name': self.INPUT_NAMES})
        self.is_login = bool(login_related_inputs)

    def is_valid_url(self, url):  # pylint: disable=no-self-use
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_links(self, soup):
        links = set()
        internal_links = set()
        external_links = set()
        domain_name = urlparse(self.url).netloc
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href != "" or href is not None:
                # join the URL if it's relative (not absolute link)
                href = urljoin(self.url, href)
                parsed_href = urlparse(href)
                # remove URL GET parameters, URL fragments, etc.
                href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                if self.is_valid_url(href):
                    links.add(href)
                    if domain_name not in href:
                        external_links.add(href)
                    else:
                        internal_links.add(href)

        return {'links': links, Link.INTERNAL: internal_links, Link.EXTERNAL: external_links}

    def link_is_accessible(self, link):
        try:
            response = requests.get(link, timeout=self.REQUEST_TIMEOUT)
            return response.status_code == requests.codes.ok  # pylint: disable=no-member
        except (requests.Timeout, requests.TooManyRedirects, requests.RequestException):
            return False

    def links_count_inaccessible(self, links):
        inaccessible_count = 0
        for link in links:
            if not self.link_is_accessible(link):
                inaccessible_count += 1
        return inaccessible_count


class Tag(models.Model):
    TAG_TYPE = Choices(('UNSET', 'Tag type not set.'), ('HEADINGS', 'Headings'))
    HEADINGS = TAG_TYPE.HEADINGS

    tag_type = models.CharField(max_length=30, choices=TAG_TYPE, default=TAG_TYPE.UNSET)
    analysis = models.ForeignKey(Analysis, related_name='tags', on_delete=models.CASCADE)
    tag = models.CharField(max_length=15, blank=True, default='')
    count = models.PositiveSmallIntegerField(null=True)


class Link(models.Model):
    LINK_TYPE = Choices(('UNSET', 'Links type not set.'), ('INTERNAL', 'Internal links'),
                        ('EXTERNAL', 'External links'))
    INTERNAL = LINK_TYPE.INTERNAL
    EXTERNAL = LINK_TYPE.EXTERNAL

    analysis = models.ForeignKey(Analysis, related_name='links', on_delete=models.CASCADE)
    link_type = models.CharField(max_length=30, choices=LINK_TYPE, default=LINK_TYPE.UNSET)
    count = models.PositiveSmallIntegerField(null=True)
    inaccessible_count = models.PositiveSmallIntegerField(null=True)
