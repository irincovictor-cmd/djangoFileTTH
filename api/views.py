from django.shortcuts import render


def home(request):
    """Home page with hero and CTA buttons."""
    return render(request, 'home.html')


def topics(request):
    """List of educational topics."""
    return render(request, 'topics.html')


def about(request):
    """About us page."""
    return render(request, 'about.html')


def contact(request):
    """
    Contact page.
    GET  → show the form
    POST → show a simple success message (no real email yet)
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        return render(request, 'contact.html', {
            'success': True,
            'name': name,
        })
    return render(request, 'contact.html')
