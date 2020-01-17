from django.test import TestCase, Client
from django.urls import reverse
from unittest import mock
import requests
import httpretty
import json
import pytest
from django.apps import apps
from django.core.cache import cache

Link = apps.get_model(app_label='analyzer', model_name='Link')
Analysis = apps.get_model(app_label='analyzer', model_name='Analysis')

pytestmark = pytest.mark.django_db


class TestPageAnalyzer:
    client = Client()
    api_url = "/api/v1/analyze-url/"
    test_url = 'https://testpage.com/test/'
    test_title = 'Web page title'
    CODE_500 = '500'
    CODE_200 = '200'

    @httpretty.activate
    def test_page_analyzer(self):
        login_input_name = 'login'
        login_input_type = 'text'
        inaccessible_internal_link = 'https://testpage.com/test/bad-link/'
        accessible_internal_link = 'https://testpage.com/test/good-link/'
        inaccessible_external_link = 'https://externalpage/test/bad-link/'
        accessible_external_link = 'https://externalpage.com/test/good-link/'
        external_links = 2
        internal_links = 2
        bad_external_links = 1
        bad_internal_links = 1

        httpretty.register_uri(httpretty.GET, inaccessible_internal_link, status=500)
        httpretty.register_uri(httpretty.GET, accessible_internal_link, status=200)
        httpretty.register_uri(httpretty.GET, inaccessible_external_link, status=500)
        httpretty.register_uri(httpretty.GET, accessible_external_link, status=200)

        httpretty.register_uri(httpretty.GET, self.test_url,
                               body="""<title>{}</title>
                                      <input name="{}" type="{}"></input>
                                      <a href="{}">link</a>
                                      <a href="{}">link</a>
                                      <a href="{}">link</a>
                                      <a href="{}">link</a>
                                    """.format(self.test_title,
                                               login_input_name,
                                               login_input_type,
                                               inaccessible_external_link,
                                               accessible_external_link,
                                               inaccessible_internal_link,
                                               accessible_internal_link),
                               status=200)

        response = self.client.post(self.api_url, {'url': self.test_url})
        json_response = json.loads(response.content)

        assert json_response['page_title'] == self.test_title
        assert json_response['response_code'] == self.CODE_200
        assert json_response['is_login'] is True

        for link in json_response['links']:
            if link['link_type'] == Link.EXTERNAL:
                assert link['count'] == external_links
                assert link['inaccessible_count'] == bad_external_links
            if link['link_type'] == Link.INTERNAL:
                assert link['count'] == internal_links
                assert link['inaccessible_count'] == bad_internal_links

    @httpretty.activate
    def test_analyzer_bad_response(self):
        httpretty.register_uri(httpretty.GET, self.test_url,
                               body="""
                                        <title>{}</title>
                                    """.format(self.test_title), status=500)
        response = self.client.post(self.api_url, {'url': self.test_url})
        json_response = json.loads(response.content)
        assert json_response['response_code'] == self.CODE_500

    @httpretty.activate
    def test_analyzer_cache(self):
        httpretty.register_uri(httpretty.GET, self.test_url,
                               body="""
                                       <title>{}</title>
                                    """.format(self.test_title), status=200)
        response = self.client.post(self.api_url, {'url': self.test_url})
        json_response = json.loads(response.content)
        cached_id = json_response['id']

        cached_response = self.client.post(self.api_url, {'url': self.test_url})
        json_cached_response = json.loads(response.content)

        assert cached_id == json_cached_response['id']
