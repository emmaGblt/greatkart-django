import factory
from factory.fuzzy import FuzzyChoice
from category.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = FuzzyChoice(choices=["Jeans", "Shoes", "Shirts", "T-Shirts", "Jackets"])
    slug = factory.LazyAttribute(lambda c: c.name.lower())
    description = factory.Faker("text")
    image = factory.Faker("file_path", category="image")
