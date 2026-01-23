import factory
from accounts.models import Account


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Sequence(lambda n: "person{}@example.com".format(n))
    phone_number = factory.Faker("phone_number")

    is_admin = False
    is_active = False
    is_superuser = False

    password = factory.django.Password("mdp")
