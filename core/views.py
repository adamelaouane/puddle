from django.shortcuts import render,redirect
from .forms import SignupForm
from item.models import Category , Item
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

def index(request):
    Items=Item.objects.filter(is_sold=False)[0:6]
    Categories= Category.objects.all()

    return render(request,"core/index.html",{
         "categories":Categories,
         "items": Items
    })

def contact(request):
     return render(request,"core/contact.html")

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/login/')

    else:
        form =SignupForm()

    return render(request, "core/signup.html", {"form": form})
def about(request):
    return render(request,"core/about.html")
def privacy(request):
    return render(request,"core/privacy.html")
def terms(request):
    return render(request, 'core/terms.html')
@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    products = Item.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    total_products = products.count()
    sold_products = products.filter(is_sold=True).count()
    available_products = products.filter(is_sold=False).count()
    return render(request, 'core/profile.html', {
        'profile_user': request.user,
        'user_profile': user_profile,
        'products': products,
        'total_products': total_products,
        'sold_products': sold_products,
        'available_products': available_products,
    })


@login_required
def edit_profile(request):
    user_profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=user_profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('core:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    return render(request, 'core/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })