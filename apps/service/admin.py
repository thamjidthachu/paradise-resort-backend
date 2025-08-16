from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Service, File, Comment


# Register your models here.
class ImagesList(admin.ModelAdmin):
    model = File


class ImagesInline(admin.StackedInline):
    model = File
    extra = 0


class CommentsInline(GenericTabularInline):
    model = Comment
    can_delete = False
    verbose_name_plural = 'Comments'
    extra = 1

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CommentAdmin(admin.ModelAdmin):
    list_display = ('message', 'author', 'object_id', 'content_type')
    list_filter = ['content_type', 'author']


class ServiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'synopsis', 'description']})
    ]
    inlines = [ImagesInline, CommentsInline]
    list_display = ('name', 'create_time',)
    readonly_fields = ('create_time',)


admin.site.register(Service, ServiceAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(File, ImagesList)
