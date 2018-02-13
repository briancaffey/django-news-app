from django.test import TestCase, Client
from django.urls import resolve
from posts.views import home
from django.http import HttpRequest
from django.contrib.auth.models import User
from .models import Post, LastUpdate
import datetime
from django.utils.dateformat import format
from django.utils.timezone import make_aware

from django.utils import timezone
import pytz

# Create your tests here.

def dt_now_aware():
    """Gives datetime.datetime.now() a time zone to remove naive datetime warnings"""
    d = datetime.datetime.now()
    timezone = pytz.timezone("America/Los_Angeles")
    d_aware = timezone.localize(d)
    return d_aware


class SimpleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        self.last_update = LastUpdate.objects.create(updated=dt_now_aware())
        self.last_update_unix = format(self.last_update.updated, "U")
        

        self.first_article = Post.objects.create(
            title="First Article", 
            content="First Content",
            published=True,
            user=self.user,
            timestamp=dt_now_aware()
            )

        self.second_article = Post.objects.create(
            title="Second Article", 
            content="Second Content",
            published=True,
            user=self.user,
            timestamp=dt_now_aware()
            )

    def test_create_article_not_published(self):
        post = Post.objects.create(
            title="A test post", 
            content="Test content",
            user=self.user,
            timestamp=dt_now_aware()
            )
        post.save()
        all_posts = Post.objects.all()
        published_posts = Post.objects.filter(published=True)
        self.assertEqual(len(all_posts),3)
        self.assertEqual(len(published_posts), 2)

    def test_article_order(self):
        post = Post.objects.create(
            title="A test post", 
            content="Test content",
            user=self.user,
            timestamp=dt_now_aware()
            )
        post.save()
        first_post = Post.objects.latest('updated')
        self.assertEqual(first_post.title, "A test post")
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts),3)