from django.core.management.base import BaseCommand
from category.factories import CategoryFactory


class Command(BaseCommand):
    help = "Initialize test categories"

    def handle(self, *args, **options):
        NAMES = ["Jeans", "Shirts", "T-Shirts", "Shoes", "Jackets"]
        for name in NAMES:
            CategoryFactory(name=name)
