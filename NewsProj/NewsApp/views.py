from datetime import timedelta, timezone
from multiprocessing import context
from ssl import CHANNEL_BINDING_TYPES
from django.shortcuts import get_object_or_404, render,redirect
import requests
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile,SavePost
import razorpay

API_KEY = 'a292c85f3c49418396eb009380f02259'

def home(request):
    country = request.GET.get('country')
    category = request.GET.get('category')
    
    if country:
        url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
    elif category: 
        url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}'
    else: 
        url = f'https://newsapi.org/v2/top-headlines?apiKey={API_KEY}'

    response = requests.get(url)
    data = response.json()
    articles = data.get('articles',[])

    context = {'articles':articles}
    return render(request,"home.html",context)


def register_user(req):
    if req.method == "POST":
        email = req.POST['email']
        username = req.POST['username']
        first_name = req.POST['firstname']
        last_name = req.POST['lastname']
        pass1 = req.POST['pass1']
        pass2 = req.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(req, "Username is already taken. Please try another one!")
            return redirect('/register')

        if not username.isalnum():
            messages.error(req, "Username should contain letters and numbers")
            return redirect("/register")

        if pass1 != pass2:
            messages.error(req, "Passwords do not match. Please sign up again")
            return redirect("/register")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        user = authenticate(username=username, password=pass1)
        login(req, user)

        return redirect('/')
    
    return render(req, "register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect('/')
        else:
            messages.error(request, "There was an error. Try Again!!!")
            return redirect("/login")
    else:
        return render(request, "login.html")

def logout_user(req):
    logout(req)
    messages.success(req,("Logged Out Successfully"))
    return redirect("/") 

@login_required(login_url='login')
def profile(request, username):
    if request.user.is_authenticated and request.user.username == username:
        profile_object = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=profile_object)
        saved_posts = SavePost.objects.filter(author=request.user)
        context = {
            'user': profile_object,  
            'profile': profile,
            'saved_posts': saved_posts
        }
        return render(request, 'profile.html', context)
    else:
        pass



@login_required(login_url='login')
def createProfile(request):
    user = request.user
    profile_exists = Profile.objects.filter(user=user).exists()
    
    if not profile_exists:
        if request.method == 'POST':
            name = request.POST['name']
            about = request.POST['about']
            profilepic = request.FILES['profilePic']
            DOB = request.POST['DOB']
            Profile.objects.create(user=user, name=name, about=about, profilePic=profilepic, DOB=DOB)
            return redirect(reverse('profile', kwargs={'username': user.username}))  
        else:
            return render(request, 'createProfile.html')
    else:
        return redirect('profile', username=user.username)  


@login_required(login_url='login')
def editProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        name = request.POST.get('name')
        about = request.POST.get('about')
        profilePic = request.FILES.get('profilePic')
        DOB = request.POST.get('DOB')

        if name:
            profile.name = name
        if about:
            profile.about = about
        if profilePic:
            profile.profilePic = profilePic
        if DOB:
            profile.DOB = DOB

        profile.save()
        return redirect('profile', username=username)

    return render(request, 'editProfile.html', {'profile': profile})

@login_required
def makePayment(req):
    user_profile = UserProfile.objects.get(user=req.user)
    if user_profile.subscription_expiry is None or user_profile.subscription_expiry < timezone.now():
        total_price = 100  
        client = razorpay.Client(auth=("rzp_test_gN9cugzg8G8MAf", "O8AcpBUuJ3VX7sCGRKlQ0hNi"))
        data = {
            "amount": total_price * 100,  
            "currency": "INR",
            "receipt": "payment_receipt",  
        }
        payment = client.order.create(data=data)
        context = {
            'data': payment,
            'amount': payment["amount"],
        }
        user_profile.subscription_expiry = timezone.now() + timedelta(days=3)  
        user_profile.save()
        return render(req, "payment.html", context)
    else:
        return redirect('/')

@login_required
def premiumPlans(request):
    return render(request, 'premiumPlans.html')


@login_required
def savepost(request):
    if request.method == 'POST':
        title = request.POST.get('title')  
        description = request.POST.get('description')  
        new_post = SavePost.objects.create(title=title, description=description, user=request.user)
        new_post.save()
        return redirect('profile')  
    else:
        return render(request, 'savepost.html')

