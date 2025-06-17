from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from .models import StudentProfile, TutorProfile

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            if role == 'Student':
                StudentProfile.objects.create(user=user, preferred_learning_mode=form.cleaned_data['preferred_learning_mode'], education_level=form.cleaned_data['education_level'])
            elif role == 'Tutor':
                TutorProfile.objects.create(user=user, cv=request.FILES.get('cv'), resume=request.FILES.get('resume'), proof_of_identity=request.FILES.get('proof_of_identity'), personal_statement_or_teaching_philosophy=form.cleaned_data['personal_statement_or_teaching_philosophy'])
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()
    return render(request, "templates\register.html", context={"register_form":form})

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = CustomAuthenticationForm()
    return render(request, "template\login.html", context={"login_form":form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")

def home_view(request):
    # Render the new home.html template
    return render(request, "home.html")

def user_view(request):
    return render(request, "user.html")