import factory
from accounts.models import Account


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda a: "{}.{}@example.com".format(a.first_name, a.last_name).lower()
    )
    phone_number = factory.Faker("phone_number")

    is_admin = False
    is_active = False
    is_superuser = False

    password = factory.django.Password("mdp")
