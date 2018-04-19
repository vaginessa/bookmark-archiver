import uuid

from django.db import models
from django.conf import settings

# URL helpers
without_scheme = lambda url: (url.replace('http://', '', 1)
                                 .replace('https://', '', 1)
                                 .replace('ftp://', '', 1))
without_query = lambda url: url.split('?', 1)[0]
without_hash = lambda url: url.split('#', 1)[0]
without_path = lambda url: url.split('/', 1)[0]
domain = lambda url: without_hash(without_query(without_path(without_scheme(url))))
base_url = lambda url: wihout_scheme(url)  # uniq base url used to dedupe links



class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Tag: {self.name}>'


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    
    url = models.URLField(unique=True)
    title = models.CharField(max_length=256)
    timestamp = models.CharField(max_length=16, unique=True)
    
    tags = models.ManyToManyField(Tag)

    @property
    def domain(self):
        return domain(self.url)

    @property
    def base_url(self):
        return base_url(self.url)

    @classmethod
    def from_json(cls, json: dict):
        link, _ = Link.objects.get_or_create(
            url=json['url'],
            timestamp=json['timestamp'],
            defaults={'title': json['title']})

        for name in json['tags'].split(','):
            tag, _ = Tag.objects.get_or_create(name=name)
            link.tags.add(tag)

        return link

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Link: {self.base_url}>'
