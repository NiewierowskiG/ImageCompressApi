import datetime
from .models import TemporaryUrl


def delete_expired_temporary_urls():
    expired_urls = TemporaryUrl.objects.filter(expires__lte=datetime.datetime.now())
    expired_urls.delete()
    