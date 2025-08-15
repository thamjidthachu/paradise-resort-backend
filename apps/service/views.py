# Create your views here.
import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions

from resortproject import settings
from .forms import CommentsForm
from .models import Service, Comment
from .serializers import ServicesSerializer, CommentsSerializer


class EndlessScroll(ListView):
    model = Service
    template_name = 'services/endless_service.html'
    context_object_name = 'resort_services'
    paginate_by = 5
    ordering = ['-create_time']


class PageList(ListView):
    template_name = 'services/service_list.html'
    context_object_name = 'resort_services'
    paginate_by = 5

    def get_queryset(self):
        return Service.objects.order_by('-create_time')

    def listing(request):
        name = Service.objects.all()
        paginator = Paginator(name, 5)  # Show 5 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'list.html', {'page_obj': page_obj})


# Service_Individual
class Details(FormMixin, DetailView):
    template_name = 'services/service.html'
    form_class = CommentsForm
    model = Service
    context_object_name = 'service_data'

    def get_queryset(self):
        return Service.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Details, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('service:datas', kwargs={'slug': self.kwargs['slug']})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        myform = form.save(commit=False)
        myform.post = self.get_object()
        myform.author = get_object_or_404(User, user_id=self.request.user.id)
        myform.content_type = ContentType.objects.get(app_label='Services', model='services')
        myform.content_object = get_object_or_404(Services, pk=self.object.id)
        myform.save()
        return super(Details, self).form_valid(form)

    def form_invalid(self, form):
        return super(Details, self).form_invalid(form)


def replyPost(request):
    content_obj = ContentType.objects.get(app_label='Services', model='comments')
    obj_id = request.POST['reply_id']
    reply = request.POST['reply']
    auth = get_object_or_404(User, user_id=request.POST['authuser'])
    commenter = get_object_or_404(Comment, id=request.POST['reply_id'])
    users = get_object_or_404(User, id=commenter.author.id)
    check = get_object_or_404(User, id=users.user_id)
    email = check.email
    timestamp = datetime.datetime.now(tz=timezone.utc)
    newreply, created = Comment.objects.get_or_create(
        content_type=content_obj,
        object_id=obj_id,
        message=reply,
        author=auth,
        comment_time=timestamp
    )

    test = get_object_or_404(Service, id=request.POST['service'])
    slugify = test.slug
    subject = 'Resort Business'
    message = f'Hi {users}, {auth} replied on your Comment "{commenter}" as "{reply}"'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]

    if not created:
        newreply.save()
    send_mail(subject, message, email_from, recipient_list)
    return redirect(reverse('service:datas', args=[slugify]))


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.order_by('-create_time')
    serializer_class = ServicesSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Add pagination if needed


class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


class ServiceCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        service_id = self.kwargs['service_id']
        return Comment.objects.filter(content_type=ContentType.objects.get_for_model(Services), object_id=service_id)

    def perform_create(self, serializer):
        service = get_object_or_404(Service, pk=self.kwargs['service_id'])
        author = get_object_or_404(User, user_id=self.request.user.id)
        serializer.save(
            content_object=service,
            author=author,
            content_type=ContentType.objects.get_for_model(Service),
            object_id=service.id
        )


class CommentReplyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id, format=None):
        parent_comment = get_object_or_404(Comment, id=comment_id)
        service = parent_comment.content_object
        reply_text = request.data.get('reply')
        if not reply_text:
            return Response({'detail': 'Reply text required.'}, status=status.HTTP_400_BAD_REQUEST)
        author = get_object_or_404(User, user_id=request.user.id)
        timestamp = timezone.now()
        reply = Comment.objects.create(
            content_type=ContentType.objects.get_for_model(Comment),
            object_id=parent_comment.id,
            message=reply_text,
            author=author,
            comment_time=timestamp
        )
        # Email notification
        users = parent_comment.author
        user_obj = get_object_or_404(User, id=users.id)
        email = user_obj.user.email
        subject = 'Resort Business'
        message = f'Hi {users}, {author} replied on your Comment "{parent_comment}" as "{reply_text}"'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        return Response({'detail': 'Reply posted.'}, status=status.HTTP_201_CREATED)
