from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Post.models import Post, UserLike
from accounts.forms import (
    ProfileUpdateForm,
    ColorPreferenceForm,
    BackgroundColorPreferenceForm,
    FontColorPreferenceForm,
    # FontPreferenceForm,
    # Make sure to import all necessary forms
)
from accounts.models import UserAccount, Location
from comment.models import Comment
from testimonials.models import Testimonial


# Import your models here

@login_required
def profile_view(request, username):
    user = get_object_or_404(UserAccount, username=username)
    testimonials_received = Testimonial.objects.filter(user_to=user).order_by('-createdAt')
    posts = Post.objects.filter(user=user).order_by('-createdAt')
    color_form = ColorPreferenceForm(instance=user)
    background_color_form = BackgroundColorPreferenceForm(instance=user)
    locations = Location.objects.all()
    font_color_form = FontColorPreferenceForm(instance=user)
    # font_form = FontPreferenceForm(instance=user)  # Changed from request.user to user
    user_like = UserLike.objects.filter(voter=user, post__in=Post.objects.all())

    # Only allow users to update their own profile
    # if request.user != user:
    #     messages.error(request, "You cannot edit someone else's profile.")
    #     return redirect('search')  # Redirect to a different view such as the home page or user's own profile
    for post in posts:
        post.comment_count = Comment.objects.filter(post=post).count()
    if request.method == 'POST':
        # Assuming the submit button for the profile update has the name 'profile_update'
        if 'profile_update' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('profile_view', username=request.user.username)  # Redirect to the updated profile page
    else:
        profile_form = ProfileUpdateForm(instance=user)

    context = {
        'user': user,
        'person': request.user,
        'testimonials_received': testimonials_received,
        'post': posts,
        'user_like': user_like,
        # 'font_form': font_form,
        'user_background': user.backgroundColor,
        'bio': user.bio,
        'locations': locations,
        'color_form': color_form,
        'user_color': user.color,
        'profile_song': user.profile_song,
        'background_color_form': background_color_form,
        'fontColor': user.fontColor,
        'profile_form': profile_form,  # Add the profile form to the context
    }
    return render(request, 'profile/profile.html', context)


def search(request):
    search_performed = False  # Initialize the variable

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        users = UserAccount.objects.distinct().filter(username__icontains=search_query)
        search_performed = True  # Set to True when a search query is present
        return render(request, 'profile/search.html', {'users': users, 'search_performed': search_performed})
    else:
        users = None
        # Ensure search_performed is included in the context even when no search is performed
        return render(request, 'profile/search.html', {'users': users, 'search_performed': search_performed})


