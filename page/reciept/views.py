from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
'''
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
'''
# Create your views here.

