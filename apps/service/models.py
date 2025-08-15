# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.fields import DateTimeField
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType

from apps.authentication.models import User


class Service(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True, default=name)
    synopsis = models.TextField(null=True)
    description = RichTextField(null=True)
    create_time = DateTimeField(blank=True, auto_now_add=True)
    service_comment = GenericRelation('comment')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Service, self).save(*args, **kwargs)


class File(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    images = models.FileField(upload_to="service_images", max_length=256)

    def __str__(self):
        return f'{str(self.service)} - {str(self.images)}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=256)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    comment_time = DateTimeField(auto_now_add=True, blank=True)
    comment = GenericRelation('comment')

    def __str__(self):
        return self.message
