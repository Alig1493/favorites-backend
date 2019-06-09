import factory
from django.contrib.auth import get_user_model
from faker import Faker


fake = Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.Faker("name")
    password = factory.PostGenerationMethodCall("set_password", "test_pass")
