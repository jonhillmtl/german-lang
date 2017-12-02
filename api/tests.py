from django.test import TestCase
from .models import GrammarQueryModel, GrammarQueryStub, Noun, Answer
from django.contrib.auth.models import User

class RarelyDoneTestCase(TestCase):
    user = None

    def setUp(self):
        for i in range(0, 5):
            Noun().save()
        self.user = User.objects.create()

    def test_set_up(self):
        assert Noun.objects.count() == 5

    def test(self):
        for i in range(1, 6):
            for j in range(0, i):
                Answer(
                    user=self.user,
                    noun=Noun.objects.get(pk=i)
                ).save()

        grammar_query_stub = GrammarQueryStub(
            user=self.user
        )

        print(Noun.rarely_done(grammar_query_stub).values('id'))
        assert [n.id for n in Noun.rarely_done(grammar_query_stub)] == [1, 2, 3, 4, 5]

        for i in range(0, 10):
            Answer(
                user=self.user,
                noun=Noun.objects.get(pk=1)
            ).save()
        assert [n.id for n in Noun.rarely_done(grammar_query_stub)] == [2, 3, 4, 5, 1]
            
