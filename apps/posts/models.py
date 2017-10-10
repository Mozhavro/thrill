from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.users.models import User
from apps.communities.models import Community
from apps.base.models import Timestamps


class Post(Timestamps):
	title = models.CharField(max_length=140)
	content = models.CharField(max_length=9999)
	excerpt = models.CharField(max_length=300, blank=True)
	thumbnail = models.ImageField(blank=True)

	class Meta:
		abstract = True


class UserPost(Post):
	user = models.ForeignKey(User)


class CommunityPost(Post):
	community = models.ForeignKey(Community)
