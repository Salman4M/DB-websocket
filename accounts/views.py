from django.shortcuts import render,redirect,HttpResponse,get_object_or_404

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from accounts.models import Profile
from accounts.forms import UpdateProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
def account_create_view(request):
    form = UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST,request.FILES or None)

        if form.is_valid():
            form.save()

            return redirect('accounts:login')


    return render(request,'account/create.html',{'form':form})


def login_view(request):
    username=request.POST.get('username')
    password=request.POST.get('password')

    user=authenticate(username=username,password=password)
    if user:
        login(request,user)
        return redirect('accounts:profile')

    return render(request,'account/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_view(request):
    profile=get_object_or_404(Profile,user=request.user)
    return render(request,'account/profile.html',{'profile':profile})


@login_required
def profile_update_view(request):
    profile=get_object_or_404(Profile,user=request.user)
    form=UpdateProfileForm(instance=profile)
    if request.method=='POST':
        form=UpdateProfileForm(request.POST,request.FILES or None,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    
    if request.path==reverse('accounts:profile_onboarding'):
        onboarding=True
    else:
        onboarding=False

    return render(request,'account/profile_update.html',{'form':form,'onboarding':onboarding})

@login_required
def home_view(request):
    return render(request,'account/home.html',{"user":request.user})
