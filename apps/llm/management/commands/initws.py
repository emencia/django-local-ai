from django.core.management.base import BaseCommand
from instant.models import Channel


class Command(BaseCommand):
    help = "Initialize the websockets channel for the llm app"

    def handle(self, *args, **options):
        _, created = Channel.objects.get_or_create(
            name="$llm", level=Channel.Level.Superuser
        )
        if created:
            print("Created websockets channel")
