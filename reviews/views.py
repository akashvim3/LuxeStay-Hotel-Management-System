from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review

def review_list(request):
    reviews = Review.objects.filter(is_approved=True).select_related('user', 'room')
    review_type = request.GET.get('type')
    if review_type:
        reviews = reviews.filter(review_type=review_type)
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

@login_required
def add_review(request):
    if request.method == 'POST':
        review = Review(
            user=request.user,
            review_type=request.POST.get('review_type', 'general'),
            rating=int(request.POST.get('rating', 5)),
            title=request.POST.get('title', ''),
            content=request.POST.get('content', ''),
        )
        room_id = request.POST.get('room')
        if room_id:
            review.room_id = room_id
        review.save()
        messages.success(request, 'Thank you for your review!')
        return redirect('review_list')
    return render(request, 'reviews/add_review.html')
