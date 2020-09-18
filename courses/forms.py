from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile
from .models import Reviews
from django.core.validators import MaxValueValidator, MinValueValidator


class CourseReviewForm(forms.Form):
    Review=forms.CharField(max_length=150,required=True)
    Rating=forms.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    sender=forms.ModelChoiceField(queryset=User.objects,widget=forms.HiddenInput)

    class Meta:
        model = Reviews
        fields = ['Review','Rating']
        exclude=('sender',)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']