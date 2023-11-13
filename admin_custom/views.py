from django.shortcuts import render, redirect

from Post.models import Post
from accounts.models import UserAccount
from testimonials.models import Testimonial


def admin_panel(request):
    if UserAccount.is_superuser:
        return render(request, 'admin/admin_panel.html')
    else:
        return redirect('home')


def admin_user(request):
    if request.method == 'POST':
        if 'select_delete' in request.POST:
            user_ids_to_delete = request.POST.getlist('delete_user')
            UserAccount.objects.filter(id__in=user_ids_to_delete).delete()

            return redirect('admin_panel_users')  # Refreshes the page

    users = UserAccount.objects.all()  # Displays all users

    return render(request, 'admin/admin_user.html', {'users': users})


def admin_post(request):
    posts = Post.objects.all()  # Displays all posts

    return render(request, 'admin/admin_post.html', {'posts': posts})


def admin_testimonial(request):
    testimonials = Testimonial.objects.all()  # Displays all testimonials

    return render(request, 'admin/admin_testimonials.html', {'testimonials': testimonials})