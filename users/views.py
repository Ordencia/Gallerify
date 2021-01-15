from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
# Create your views here.

def register(request):
	if request.method == 'POST': #post request sent back to this route
		form = UserRegisterForm(request.POST) 
		if form.is_valid(): #start verifying fields entered
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to log in.')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})