from django.db import models
from django.conf import settings
from accounts.models import UserAccount
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Testimonial(models.Model):
    user_from = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='testimonials_given')
    user_to = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='testimonials_received')
    content = models.TextField()
    createdAt = models.DateTimeField(default=timezone.now)
    # rating = models.PositiveIntegerField(
    #     default=0,
    #     validators=[
    #         MinValueValidator(1, "Rating must be at least 1"),
    #         MaxValueValidator(5, "Rating cannot be more than 5")
    #     ]
    # )

    def __str__(self):
        return f"Testimonial from {self.user_from.username} to {self.user_to.username}"

    def __repr__(self):
        return f"Testimonial('{self.content}', '{self.createdAt}')"



