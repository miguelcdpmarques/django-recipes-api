from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsAPITests(TestCase):
    """Test the publicly available Tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='admin@admin.com',
            password='admin',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_tags_limited_to_user(self):
        """Test retrieving tags only from authenticated user"""
        new_user = get_user_model().objects.create_user(
            email='random@admin.com',
            password='random',
            name='random'
        )
        Tag.objects.create(user=new_user, name='Random Tag')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Fruity'}
        res = self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(user=self.user, name=payload['name']).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED) 
        self.assertTrue(exists)
    
    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) 
