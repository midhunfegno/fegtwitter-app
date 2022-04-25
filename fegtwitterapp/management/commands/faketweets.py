from django.core.management import BaseCommand
from faker import Faker

from fegtwitterapp.models import User, UserTweet


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fake = Faker()
        for i in range(1, 100):
            random_user = User.objects.order_by("?").first()
            fparagraph = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
            UserTweet.objects.create(user=random_user, text=fparagraph)
