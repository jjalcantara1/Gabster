from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Redirect to a success page.
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'customization/customization.html', {'form': form})
