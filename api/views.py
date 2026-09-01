from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Renders api/templates/home.html
def about(request):
    return render(request, 'about.html')
