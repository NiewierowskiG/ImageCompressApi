from django.contrib.auth.models import User
from django_q.models import Schedule
from apii.models import Tier
from django.core.management.base import BaseCommand
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        time.sleep(5)
        if not Tier.objects.all():
            admin = User.objects.create(username="admin", is_superuser=True, is_staff=True, is_active=True)
            admin.set_password("admin123")
            admin.save()
            Schedule.objects.create(name="Delete TemporaryUrls", func="apii.tasks.delete_expired_temporary_urls",
                                schedule_type="Hourly")
            Tier.objects.create(name="Basic", can_link_200px_height=True)
            Tier.objects.create(name="Premium", can_link_200px_height=True, can_link_400px_height=True,
                            can_link_original_image=True)
            Tier.objects.create(name="Enterprise", can_link_200px_height=True, can_link_400px_height=True,
                            can_link_original_image=True, can_create_tmp_url=True)
