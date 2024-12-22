from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Announcement
from .forms import AnnouncementForm

class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    context = {
        'announcements': announcements,
        'is_superuser': request.user.is_superuser
    }
    if request.user.is_superuser:
        return render(request, 'announcements/list.html', context)
    else:
        return render(request, 'announcements/subscriber_list.html', context)

class AnnouncementCreateView(SuperUserRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/create.html'
    success_url = reverse_lazy('announcement-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "L'annonce a été créée avec succès.")
        return super().form_valid(form)

class AnnouncementUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/create.html'
    success_url = reverse_lazy('announcement-list')

    def form_valid(self, form):
        messages.success(self.request, "L'annonce a été mise à jour avec succès.")
        return super().form_valid(form)

class AnnouncementDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Announcement
    success_url = reverse_lazy('announcement-list')
    template_name = 'announcements/confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(request, "L'annonce a été supprimée avec succès.")
        return super().delete(request, *args, **kwargs)

@login_required
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'announcements/detail.html', {'announcement': announcement})
