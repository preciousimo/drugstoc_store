from django.shortcuts import render, redirect

def landing_page(request):
    return render(request, 'index.html')

def redirect_to_landing(request):
    return redirect('/')