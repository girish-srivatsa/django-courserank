from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from .models import Course, Reviews
from .forms import CourseReviewForm

def LikeView(request, pk):
    course = get_object_or_404(Course, pk = pk)
    liked = False
    if course.course_dislikes.filter(pk = request.user.pk).exists():
        course.course_dislikes.remove(request.user)
        course.course_likes.add(request.user)
    elif course.course_likes.filter(pk = request.user.pk).exists():
        course.course_likes.remove(request.user)
        liked = False
    else:
        course.course_likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("courses_detail", args = (pk, )))

def DisLikeView(request, pk):
    course = get_object_or_404(Course, pk = pk)
    disliked = False
    if course.course_likes.filter(pk = request.user.pk).exists():
        course.course_likes.remove(request.user)
        course.course_dislikes.add(request.user)
    elif course.course_dislikes.filter(pk = request.user.pk).exists():
        course.course_dislikes.remove(request.user)
        disliked = False
    else:
        course.course_dislikes.add(request.user)
        disliked = True
    return HttpResponseRedirect(reverse("courses_detail", args = (pk, )))

def reviewlikeview(request, pk):
    review = get_object_or_404(Reviews, pk = pk)
    rliked = False
    if review.review_dislikes.filter(pk = request.user.pk).exists():
        review.review_dislikes.remove(request.user)
        review.review_likes.add(request.user)
    elif review.review_likes.filter(pk = request.user.pk).exists():
        review.review_likes.remove(request.user)
        rliked = False
    else:
        review.review_likes.add(request.user)
        rliked = True
    review.save()
    return HttpResponseRedirect(reverse("courses_detail", args = (review.course.pk, )))

def reviewdislikeview(request, pk):
    review = get_object_or_404(Reviews, pk = pk)
    rdisliked = False
    if review.review_likes.filter(pk = request.user.pk).exists():
        review.review_likes.remove(request.user)
        review.review_dislikes.add(request.user)
    elif review.review_dislikes.filter(pk = request.user.pk).exists():
        review.review_dislikes.remove(request.user)
        rdisliked = False
    else:
        review.review_dislikes.add(request.user)
        rdisliked = True
    review.save()
    return HttpResponseRedirect(reverse("courses_detail", args = (review.course.pk, )))


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "courses/home.html"
    context_object_name = "courses"
    ordering = ['-rating']


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailView, self).get_context_data()
        stuff = get_object_or_404(Course, pk = self.kwargs.get('pk'))

        liked = False
        if stuff.course_likes.filter(pk = self.request.user.pk).exists():
            liked = True
        disliked = False
        if stuff.course_dislikes.filter(pk = self.request.user.pk).exists():
            disliked = True

        context["total_likes"] = stuff.course_likes.count()
        context["total_dislikes"] = stuff.course_dislikes.count()
        context["liked"] = liked
        context["disliked"] = disliked
        context["form"]=CourseReviewForm()
        reviews=Reviews.objects.filter(course=stuff).order_by("-course_rating")
        context["reviews"] = reviews
        context["courses"] = Course.objects.all().order_by("-rating")
        context["rating_count"] = range(stuff.rating)
        context["non_rating_count"] = range(5 - stuff.rating)
        return context

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course

    fields = ['course_code', 'course_name', 'course_instructor', 'rating', 'details']

    def test_func(self):
        if self.request.user.is_superuser:
            self.fields = ['course_code', 'course_name', 'course_instructor', 'rating', 'details']
        return True



class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    template_name = "courses/course_update.html"

    fields = []

    def test_func(self):
        if self.request.user.is_superuser:
            self.fields = ['course_code', 'course_name', 'course_instructor', 'rating', 'details']
        return True


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    success_url = "/"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class Form(FormView):
    form_class = CourseReviewForm

    def post(self, request, *args, **kwargs):
        review = self.request.POST['Review']
        rating = self.request.POST['Rating']
        sender = request.user
        course = get_object_or_404(Course,pk=self.kwargs.get('pk'))
        if Reviews.objects.filter(course=course, course_rater=sender).count() == 0:
            Reviews.objects.create(course=course,course_rater=sender,course_rating=rating,course_review=review)
            review_count = int(Reviews.objects.filter(course = course).count())
            course.rating = (int(course.rating) * int(review_count) + int(rating)) / (int(review_count) + 1)
            course.save()
        return HttpResponseRedirect(reverse('courses_detail',kwargs={'pk':self.kwargs.get('pk')}))
