import factory
from store.models import Product
from category.factories import CategoryFactory
import re


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("catch_phrase")
    slug = factory.LazyAttribute(lambda p: re.sub(r"[\W_]+", "-", p.name.lower()))
    description = factory.Faker("text")
    price = factory.Faker(
        "pyfloat", right_digits=2, positive=True, min_value=10.0, max_value=2000.0
    )
    image = factory.Faker("file_path", category="image")
    stock = factory.Faker("pyint", min_value=1)
    is_available = True
    category = factory.SubFactory(CategoryFactory)
