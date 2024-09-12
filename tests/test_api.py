import pytest
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APIClient

from api_v1.models import HandBook, HandBookElement, VersionHandBook


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def handbook():
    return HandBook.objects.create(
        uniq_code='42',
        title='Тестовый справочник',
        description='Описание тестового справочника',
    )


@pytest.fixture
def version_handbook(handbook):
    return VersionHandBook.objects.create(
        handbook=handbook, version='1.0', version_start_date=now()
    )


@pytest.fixture
def handbook_element(version_handbook):
    return HandBookElement.objects.create(
        version_hand_book=version_handbook,
        uniq_code='1',
        value='Тестовое значение',
    )


@pytest.mark.django_db
def test_get_all_handbooks(api_client, handbook):
    url = reverse('all_handbooks')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['refbooks']) > 0


@pytest.mark.django_db
def test_check_element_exists(
    api_client, handbook, version_handbook, handbook_element
):
    url = reverse('check_element', kwargs={'id': handbook.id})
    response = api_client.get(
        url,
        {
            'code': '1',
            'value': 'Тестовое значение',
            'version': version_handbook.version,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] is True


@pytest.mark.django_db
def test_check_element_not_found(api_client, handbook):
    url = reverse('check_element', kwargs={'id': handbook.id})
    response = api_client.get(url, {'code': '1', 'value': 'Неверное значение'})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_filter_handbooks_by_date(api_client, handbook, version_handbook):
    url = reverse('all_handbooks')
    response = api_client.get(url, {'date': '2000-01-01'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['refbooks'] == []
