from django.shortcuts import render
from django.shortcuts import render_to_response
from PESCM import settings
import os

# Create your views here.
def page_not_found(request):
    return render_to_response(os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'templates/error/404.html'))


def page_error(request):
    return render_to_response(os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'templates/error/500.html'))


def permission_denied(request):
    return render_to_response(os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'templates/error/403.html'))

