from django.core.management.base import BaseCommand

class DocStringCommand(BaseCommand):
    def __init__(self):
        self.help = self.__doc__
        super().__init__()
