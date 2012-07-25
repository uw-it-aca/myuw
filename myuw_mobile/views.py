from django.shortcuts import render_to_response
from models import Term  

def index(request):
    return render_to_response('index.html')


