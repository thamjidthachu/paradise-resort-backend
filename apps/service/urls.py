from django.urls import path
from .views import HomeView, ServiceListView, ServiceDetailView, ServiceReviewsView, ReviewReplyView

app_name = 'service'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('list/', ServiceListView.as_view(), name='service-list'),
    path('<slug:slug>/', ServiceDetailView.as_view(), name='service-detail'),
    path('<slug:service_slug>/reviews/', ServiceReviewsView.as_view(), name='service-reviews'),
    path('reviews/<int:comment_id>/reply/', ReviewReplyView.as_view(), name='review-reply'),
]
