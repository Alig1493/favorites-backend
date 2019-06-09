import factory
from factory.fuzzy import FuzzyInteger

from backend.favorites.models import Category, Favorite
from backend.users.tests.factories import UserFactory


class CategoryFactory(factory.DjangoModelFactory):
    title = factory.Faker("word")

    class Meta:
        model = Category


class FavoriteFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    title = factory.Faker("word")
    ranking = FuzzyInteger(low=1, high=10)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Favorite
