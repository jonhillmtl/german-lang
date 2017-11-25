from django.shortcuts import render

def noun_gender(request):
    return render(request, 'apps/noun_gender.html')