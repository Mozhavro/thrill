from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse_lazy

from apps.base.views import PostCreateView, PostEditView, CommunityAdminRequiredMixin
from apps.users.models import User
from .models import Community, CommunityPost


class CommunityDetail(DetailView):
    model = Community

    def get_object(self):
        try:
            key = int(self.kwargs['key'])
            return Community.objects.get(pk=key)
        except ValueError:
            return Community.objects.get(short_link=self.kwargs['key'])


class CommunityList(ListView):
    model = Community
    context_object_name = 'communities'


class CommunityCreateView(LoginRequiredMixin, CreateView):
    model = Community
    fields = [
        'title',
        'short_link',
        'description',
        'avatar_pic',
    ]

    def form_valid(self, form):
        community = form.save(commit=False)
        community.admin = self.request.user # community here
        community.save()
        return redirect('community_detail', community.pk)


class CommunityEditView(CommunityAdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Community
    fields = [
        'title',
        'short_link',
        'description',
        'avatar_pic',
    ]

    def get_object(self):
        try:
            key = int(self.kwargs['key'])
            return Community.objects.get(pk=key)
        except ValueError:
            return Community.objects.get(short_link=self.kwargs['key'])

    def form_valid(self, form):
        community = form.save(commit=True)
        return redirect('community_detail', community.pk)


class CommunityDeleteView(CommunityAdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Community

    def get_object(self):
        try:
            key = int(self.kwargs['key'])
            return Community.objects.get(pk=key)
        except ValueError:
            return Community.objects.get(short_link=self.kwargs['key'])


class SubscribeToCommunity(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        community_to_subscribe = Community.objects.get(id=self.kwargs['community_id'])
        request.user.subscribe(community_to_subscribe)
        request.user.save()
        # TODO Json response
        return redirect(request.META.get('HTTP_REFERER', '/'))


class UnsubscribeFromCommunity(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        community_to_unsubscribe = Community.objects.get(id=self.kwargs['community_id'])
        request.user.unsubscribe(community_to_unsubscribe)
        request.user.save()
        # TODO Json response
        return redirect(request.META.get('HTTP_REFERER', '/'))


class CommunityPostCreateView(CommunityAdminRequiredMixin, PostCreateView):
    # TODO refactoring for:
    # 1. getting community object by url param in more generic way

    model = CommunityPost

    def get_community_object(self):
        try:
            key = int(self.kwargs['key'])
            community = Community.objects.get(pk=key)
        except ValueError:
            community = Community.objects.get(short_link=self.kwargs['key'])

        return community

    def form_valid(self, form):
        post = form.save(commit=False)

        community = self.get_community_object()

        post.community = community
        post.save()

        community_key = community.short_link or community.pk
  
        return redirect('community_post_detail', community_key, post.pk)
    

class CommunityPostEditView(CommunityAdminRequiredMixin, PostEditView):
    model = CommunityPost
    template_name = 'posts/post_form.html'

    def get_community_object(self):
        try:
            key = int(self.kwargs['key'])
            community = Community.objects.get(pk=key)
        except ValueError:
            community = Community.objects.get(short_link=self.kwargs['key'])

        return community


    def form_valid(self, form):
        post = form.save(commit=True)

        community = self.get_community_object()
        community_key = community.short_link or community.pk
  
        return redirect('community_post_detail', community_key, post.pk)


class CommunityPostDeleteView(CommunityAdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = CommunityPost
    template_name = "posts/post_confirm_delete.html"

    def get_community_object(self):
        try:
            key = int(self.kwargs['key'])
            community = Community.objects.get(pk=key)
        except ValueError:
            community = Community.objects.get(short_link=self.kwargs['key'])

        return community

    def get_success_url(self):
        community = self.get_community_object()
        key = community.short_link or community.pk
        return reverse_lazy( 'community_detail', kwargs={'key': key})


class CommunityPostDetail(DetailView):
    model = CommunityPost
    template_name = 'posts/post_detail.html'
