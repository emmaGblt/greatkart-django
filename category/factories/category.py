import factory
from category.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "Jeans"
    slug = factory.LazyAttribute(lambda c: c.name.lower())
    description = factory.Faker("text")
    image = factory.Faker("file_path", category="image")
