from django.forms import ModelForm

from store.models import ProductReview


class ProductReviewForm(ModelForm):
    class Meta:
        model = ProductReview
        fields = ["title", "content", "rating"]
