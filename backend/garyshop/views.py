from django.shortcuts import render

# Create your views here.
def index(request):
    # get the request in
    # do some logic with models in database
    # return a webpage to the user
    dic = {'name':'Gareth', 'Title':'Mstr.'}
    names = ['Tinky Winky', 'Dipsy', 'Laa-Laa', 'Po']
    return render(request, 'index.html', {'names':names })
