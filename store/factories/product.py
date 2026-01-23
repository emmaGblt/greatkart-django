import factory
from store.models import Product, Variation
from category.models import Category
import re
from factory.fuzzy import FuzzyChoice


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
    category = factory.Iterator(Category.objects.all())


class VariationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Variation

    product = factory.SubFactory(ProductFactory)
    category = FuzzyChoice(
        choices=Variation.CATEGORY_CHOICES.items(), getter=lambda c: c[0]
    )
    value = factory.Faker("word")
    is_active = True
