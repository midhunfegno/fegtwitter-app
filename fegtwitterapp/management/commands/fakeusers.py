import requests
from django.core.management import BaseCommand

from fegtwitterapp.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # sample = {
        #     {"results": [{
        #         "name": {"title": "Mr", "first": "Coşkun", "last": "Sinanoğlu"},
        #         "email": "coskun.sinanoglu@example.com",
        #         "login": {"uuid": "3be5412e-1dcf-4394-858b-a3aa97a5e0ce", "username": "orangepeacock706",
        #                   "password": "forest", "salt": "g1X8nJrr", "md5": "f5c9c4dd97c17aeb6d7529cfc3770663",
        #                   "sha1": "51e0ddb44fe77f9e34f4a140de0d5fa8d98ac381",
        #                   "sha256": "4e0f8773470823a2617ff7695828386735e31e2fe8c0a647939cac2b7089a649"}}],
        #     "info": {"seed": "bcd2c1bd25f5796c", "results": 20, "page": 1, "version": "1.3"}}

        a = requests.get('https://randomuser.me/api/?inc=name,email,login&results=10')
        result = a.json()
        user_list = []
        for i in result.get('results'):
            flname = i['name']['first']+' '+i['name']['last']
            user_list.append(User(fullname=flname, email=i['email'],
                                 username=i['login']['username'],
                                 password=i['login']['password']))
        User.objects.bulk_create(user_list)
