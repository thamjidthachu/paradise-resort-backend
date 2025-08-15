from django.urls import path
from .views import ServiceListView, ServiceDetailView, ServiceCommentsView, CommentReplyView

app_name = 'service'
urlpatterns = [
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<slug:slug>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/<int:service_id>/comments/', ServiceCommentsView.as_view(), name='service-comments'),
    path('comments/<int:comment_id>/reply/', CommentReplyView.as_view(), name='comment-reply'),
]
