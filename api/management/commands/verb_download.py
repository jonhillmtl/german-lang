from django.core.management.base import BaseCommand, CommandError
from api.models import Noun, Translation
import requests
import os
from lxml import html

class Command(BaseCommand):
    help = 'Populates the nouns'

    def handle(self, *args, **options):
        self.download("")
        
    def download(self, verb):
        filename = "./data/conjugations/{}.html".format(verb)

        if os.path.exists(filename) is False:
            print("downloading")
            url = "https://www.duden.de/rechtschreibung/{}"
            url = url.format(verb)
            r = requests.get(url)

            with open(filename, "w+") as f:
                f.write(r.text)
        else:
            print("file already downloaded")

        with open(filename, "r") as f:
            content = f.read()

            tree = html.fromstring(content)
            
            section = tree.xpath("//section[@id='block-duden-tiles-6']")
            part_1 = div = section[0][4][0][0][0][1].text.strip()
            part_2 = div = section[0][4][0][0][1][1].text.strip()
            
            print(part_1, part_2)
            
            # conj = section[0][0]
            # print(conj[0])
