from django.test import TestCase

from .models import Link, domain, base_url


class TestLinkImport(TestCase):
    def test_simple_from_json(self):
        json = {
            'url': 'https://abc.efg.com/asdf/asdf.html?abc=123#234',
            'title': 'Test abc article 123!',
            'timestamp': '15444234325',
            'tags': 'abc,def,feg',
        }
        self.link = Link.from_json(json)

        assert self.link.url == json['url']
        assert self.link.title == json['title']
        assert self.link.timestamp == json['timestamp']
        assert {tag.name for tag in self.link.tags.all()} == {name for name in json['tags'].split(',')}

    def tearDown(self):
        self.link.tags.all().delete()
        self.link.delete()


class TestLinkAttrs(TestCase):
    def setUp(self):
        self.link = Link.from_json({
            'url': 'https://abc.efg.com/asdf/asdf.html?abc=123#234',
            'title': 'Test abc article 123!',
            'timestamp': '15444234325',
            'tags': 'abc,def,feg',
        })

    def test_domain_attrs(self):
        assert self.link.domain == 'abc.efg.com'
        assert self.link.base_url == 'abc.efg.com/asdf/asdf.html'

        assert domain(self.link.url) == self.link.domain
        assert base_url(self.link.url) == self.link.base_url

    def tearDown(self):
        self.link.tags.all().delete()
        self.link.delete()
