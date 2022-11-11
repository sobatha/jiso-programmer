import pytest

class TestPostDetailView:
    @pytest.mark.django_db
    def test_get(self, client):
        post=PostFactory(
            title="記事タイトル",
            author_username="theusername",
        )

        res = client.get(f"/posts/{post.id}/")

        assert res.context_data["title"] == "ブログ記事のタイトル"
        assert res.context_data["body"] == "ブログ記事の本文"
        assert res.comtext_data["author_name"] == "theusername"

#factories.py
import factory
from .models import Organization, Post, User

class OrganizationFactotry(factory.django.DjangoModelFactory):
    name = 'beproud'

    class Meta:
        model = Organization

class UserFactory(factory.django.DjangoModelFactory):
    username = 'foobar'
    organization = factory.SubFactory(OrganizationFactotry)

    class Meta:
        model = User

class PostFactory(factory.django.DjangoModelFactory):
    title = '記事タイトル'
    body = '記事本文'
    author = factory.SubFactory(UserFactory)
    published_at = None

    class Meta:
        model = Post