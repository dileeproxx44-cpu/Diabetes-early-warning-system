from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout


# =====================================
# REGISTER VIEW
# =====================================

def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')

        # ==========================
        # CREATE USER
        # ==========================

        User.objects.create_user(

            username=username,

            email=email,

            password=password

        )

        return redirect('login')

    return render(

        request,

        'register.html'

    )


# =====================================
# LOGIN VIEW
# =====================================

def login_view(request):

    error = None

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        # ==========================
        # AUTHENTICATE USER
        # ==========================

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            error = "Invalid Username or Password"

    return render(

        request,

        'login.html',

        {

            'error': error

        }

    )


# =====================================
# LOGOUT VIEW
# =====================================

def logout_view(request):

    logout(request)

    return redirect('login')