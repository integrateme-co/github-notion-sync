import pytest
from model_bakery import baker
from django.urls import reverse
from django.test import RequestFactory, TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User, AnonymousUser
from api_data.views import save_apis
from api_data.models import apiStoreModel
from .conftest import *
from mixer.backend.django import mixer

@pytest.fixture
def api_client():
    return APIClient

@pytest.mark.django_db
class TestSaveAPIView(TestCase):
    """Testing api_data Views"""
    url = reverse('save_apis')

    @classmethod
    def set_up_class(cls):
        """Setting Up The Class"""
        super(TestSaveAPIView, cls).set_up_class()
        mixer.blend('api_data.apiStoreModel')

    def test_save_api_authenticated(self):
        """Testing Authenticated User in save_api"""
        path = reverse('save_apis')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = save_apis(request)
        assert response.status_code == 200

    def test_save_api_unauthenticated(self):
        """Testing Un-Authenticated User in save_api"""
        path = reverse('save_apis')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = save_apis(request)
        assert 'accounts/login' in response.url

    def test_saving_api(self, api_client):
        """Testing Saving API"""
        api_data = baker.make(apiStoreModel)
        url = reverse('save_apis')
        print(url)
        expected_data = {
            'dev_api':api_data.dev_api,
            'medium_api': api_data.medium_api,
            'hashnode_api': api_data.hashnode_api
        }
        response = api_client.post(
            url,
            data=expected_data,
            format='json'
        )
        assert response.status_code == 201




@pytest.mark.django_db
class TestSaveIntegrationView(TestCase):
    """Testing api_data Views"""

    @classmethod
    def set_up_class(cls):
        """Setting Up The Class"""
        super(TestSaveAPIView, cls).set_up_class()
        mixer.blend('api_data.integrationModel')

    def test_save_integration_authenticated(self):
        """Testing Authenticated User in save_api"""
        path = reverse('save_integration')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = save_apis(request)
        assert response.status_code == 200

    def test_save_integration_unauthenticated(self):
        """Testing Un-Authenticated User in save_api"""
        path = reverse('save_integration')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = save_apis(request)
        assert 'accounts/login' in response.url
