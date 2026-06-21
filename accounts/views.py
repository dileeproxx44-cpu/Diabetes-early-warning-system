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

    error = None

    if request.method == 'POST':

        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')

        # CHECK DUPLICATE USERNAME
        if User.objects.filter(username=username).exists():

            return render(
                request,
                'register.html',
                {
                    'error': '⚠ Username already exists'
                }
            )

        # CHECK DUPLICATE EMAIL
        if User.objects.filter(email=email).exists():

            return render(
                request,
                'register.html',
                {
                    'error': '⚠ Email already registered'
                }
            )

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # AUTO LOGIN
        login(request, user)

        return redirect('home')

    return render(
        request,
        'register.html',
        {
            'error': error
        }
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

            return redirect('home')

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