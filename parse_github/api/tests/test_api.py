import json
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import GitItem, GitUser
from django.urls import reverse
from api.serializers import GitItemSerialize
from rest_framework.test import force_authenticate
from rest_framework_api_key.models import APIKey

class GitApiTestCase(APITestCase):
    def setUp(self):
        self.owner = GitUser.objects.create(owner_name='collective', owner_link='https://github.com/collective')
        GitItem.objects.create(link_rep='https://github.com/collective/plonetheme.tokyo',
                               link_site=None, name_rep='plonetheme.tokyo', about='A Theme for Plone',
                               stars=6, watching=12,
                               forks=6, commit_count=32, commit_author='collective',
                               commit_name='edit Readme', commit_datetime='2022-02-03T13:00:29Z',
                               release_count='0', release_datetime=None, owner=self.owner)
        self.name_key, self.token = APIKey.objects.create_key(name="my-remote-service")


    def test_get_all(self):
        url = reverse('gitgetall-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.token}')
        response = self.client.get(url)
        item = GitItem.objects.all()
        serializer_data = GitItemSerialize(item, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['name_rep'], 'plonetheme.tokyo')

    def test_get_individual_stat(self):
        url = reverse('gitindividualstats', kwargs={'pk': self.owner.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.token}')
        response = self.client.get(url)
        data = {
            "Репозиторий с максимальным количеством коммитов": {
                "name_rep": "plonetheme.tokyo",
                "commit_count": 32
            },
            "Среднее количество звезд в репозиториях": {
                "stars__avg": 6.0
            }
        }
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data, response.data)

    def test_create(self):
        self.assertEqual(1, GitItem.objects.all().count())
        url = reverse('gitcreate-list')
        data = {
            "link_rep": "https://github.com/MariyaSha/BinarytoDecimal",
            "name_rep": "BinarytoDecimal",
            "about": "Binary to Decimal Converter Mobile App With KivyMD",
            "link_site": "None",
            "stars": 24,
            "watching": 4,
            "forks": 20,
            "commit_count": 10,
            "commit_author": str(self.owner.owner_name),
            "commit_name": "update readme",
            "commit_datetime": "2021-08-05T14:06:00Z",
            "release_count": "0",
            "release_version": None,
            "release_datetime": None,
            "owner": self.owner.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.token}')
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, GitItem.objects.all().count())
        self.assertEqual(GitItem.objects.last().owner, self.owner)
