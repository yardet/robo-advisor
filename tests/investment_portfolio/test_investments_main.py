from typing import Callable

import pytest
from django.urls import reverse

from accounts.models import CustomUser

# Global constant variables
DASHBOARD: str = "'s Investments Page"
ATTRIBUTES: list[str] = ['Investments History', 'Discover Stocks', 'Top Stocks']


@pytest.mark.django_db
class TestInvestmentsMain:
    def test_get_request_as_logged_user(self, client, user_factory: Callable):
        user: CustomUser = user_factory()
        client.force_login(user)
        response = client.get(reverse('investments_main'))
        assert response.status_code == 200
        assert 'investment_portfolio/investments_main.html' in response.templates[0].name
        generic_assertions(response, user, '')

    def test_get_request_as_guest(self, client):
        response = client.get(reverse('investments_main'))
        assert response.status_code == 302

def generic_assertions(response, user: CustomUser, webpage_title: str):
    # Title
    assert webpage_title in response.content.decode()
    # Sidebar
    assert f"{user.first_name}{DASHBOARD}" in response.content.decode()
    for attribute in ATTRIBUTES:
        assert attribute in response.content.decode()
