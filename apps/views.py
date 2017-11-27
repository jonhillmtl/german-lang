from django.shortcuts import render

def noun_gender(request):
    return render(request, 'apps/noun_gender.html')
    
def noun_translation_multi(request):
    return render(request, 'apps/noun_translation_multi.html')

def noun_pluralization(request):
    return render(request, 'apps/noun_pluralization.html')