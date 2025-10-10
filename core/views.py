from django.shortcuts import render
from django.http import HttpResponseForbidden
# from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required 
# Create your views here.

@login_required
def profile_show(request):
    template_name = "core/profile/show.html"
    return render(request, template_name)

@login_required
def profile_edit(request):
    template_name = "core/profile/edit.html"
    return render(request, template_name)
