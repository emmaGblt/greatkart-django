import factory
from carts.models import Cart, CartItem
from accounts.factories import AccountFactory
from store.factories import ProductFactory, VariationFactory


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(AccountFactory)
    session_key = factory.Faker("uuid4")


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("pyint", min_value=1)
    is_active = True

    @factory.post_generation
    def variations(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is not None:
            self.variations.add(*extracted)
        else:
            self.variations.add(VariationFactory.create(**kwargs))
