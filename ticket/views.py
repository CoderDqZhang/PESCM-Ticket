from django.shortcuts import render

# Create your views here.
def page_not_found(request):
    return render(request, '../../404.html')


def page_error(request):
    return render(request, 'blog/500.html')


def permission_denied(request):
    return render(request, 'blog/403.html')
