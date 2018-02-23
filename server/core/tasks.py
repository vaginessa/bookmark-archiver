import dramatiq

from django.contrib.contenttypes.models import ContentType

from .models import Link

@dramatiq.actor
def run_extractor(link_id, method):
    link = Link.objects.get(id=link_id)
    
    ResultModel = ContentType.objects.get(app_label=method, model="Result").model_class()

    ResultModel.from_link(link)
