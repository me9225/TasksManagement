from django.shortcuts import render
from .forms import loginForm,registerForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        print("valid:", form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)  # לא שומר עדיין
            password = form.cleaned_data.get('password')
            user.set_password(password)     # הצפנה מובנית של Django
            user.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
    else:
        form = registerForm()
    return render(request, 'register.html', {'form': form})
def login(request):
    if(request.method == 'POST'):
        form = loginForm(request.POST)
        if(form.is_valid()):
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    print("success")
                    auth_login(request, user)
                    return redirect('tasks')
            except Exception as e:
                print("error:", e)
                messages.error(request, 'Error occurred during login')
                form = loginForm()
        else:
            messages.error(request, 'שם משתמש או סיסמה שגויים')
    else:
        form = loginForm()
    return render(request, 'login.html', {'form': form})

def tasks(request):
    return render(request, 'tasks.html')

