from django.shortcuts import render
from api.models import GrammarQueryModel

def noun_gender(request):
    return render(request, 'apps/noun_gender.html')
    
def noun_translation_multi(request):
    return render(request, 'apps/noun_translation_multi.html')

def noun_pluralization(request):
    return render(request, 'apps/noun_pluralization.html')

def noun_translation(request):
    return render(request, 'apps/noun_translation.html')
    
def verb_translation_multi(request):
    return render(request, 'apps/verb_translation_multi.html')
    
def verb_pp_multi(request):
    return render(request, 'apps/verb_pp_multi.html')

def stats(request):
    levels = GrammarQueryModel.levels()
    tags = GrammarQueryModel.all_tags()
    
    return render(request, 'apps/misc/stats.html', dict(levels=levels, tags=tags))