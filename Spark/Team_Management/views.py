from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def get_user_details(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_details = {
            'username': user.username,
            'email': user.email,
            # Add more user details as needed
        }
        return JsonResponse(user_details)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
def is_superuser(user):
    return user.is_superuser

def forbidden_response():
    return HttpResponseForbidden('You are not authorized to access this page.')

# Create your views here.
@user_passes_test(is_superuser, login_url=forbidden_response)
def view_all(request):
    ''' Vew for displaying all team members '''
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'Team_Management/index.html', context=context)

def sign_in(request):
    ''' view for authentication form '''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/MyTeam/viewall')  # Replace 'home' with the name of your home page URL
        else:
            error_message = 'Invalid username or password'
            return render(request, 'Team_Management/Sign.html', {'error_message': error_message})
    else:
        return render(request, 'Team_Management/Sign.html')

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('/MyTeam/Viewall')

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/MyTeam/viewall')  # Replace 'user_list' with the URL name of your user list view
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'Team_Management/create_user.html', context)

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize specific labels
        self.fields['username'].label = 'Custom Username Label'
        self.fields['password1'].label = 'Custom Password Label'
        self.fields['password2'].label = 'Custom Confirm Password Label'