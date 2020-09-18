from django.urls import path, include
from .views import (
    CourseListView,
    CourseDetailView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
    Form
)
from . import views

urlpatterns = [
    path('', CourseListView.as_view(), name = "courses_home"),
    path('course/<int:pk>/', CourseDetailView.as_view(), name = "courses_detail"),
    path('course/new/', CourseCreateView.as_view(), name = "courses_create"),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name = "courses_update"),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name = "courses_delete"),
    path('like/<int:pk>/', views.LikeView, name = "like_course"),
    path('dislike/<int:pk>/', views.DisLikeView, name = "dislike_course"),
    path('reviewlike/<int:pk>/', views.reviewlikeview, name = "like_review"),
    path('reviewdislike/<int:pk>/', views.reviewdislikeview, name = "dislike_review"),
    path('form/<int:pk>/',Form.as_view(),name="form")

]