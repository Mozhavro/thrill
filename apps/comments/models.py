from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from mptt.models import MPTTModel, TreeForeignKey

# from apps.users.models import User
from apps.base.models import Timestamps
from apps.likes.models import Like


class Comment(MPTTModel, Timestamps):
    author = models.ForeignKey('users.User')
    content = models.TextField(max_length=240)
    likes_count = models.PositiveIntegerField(default=0)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    likes = GenericRelation(Like)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    
    def model_label(self):
        return "{app_label}.{class_name}".format(
            app_label=self._meta.app_label,
            class_name=self.__class__.__name__
        )