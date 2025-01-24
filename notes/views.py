from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView

from .forms import AddPostForm
from .models import Note, TagPost, Category
from .utils import DataMixin


from django.conf import settings
from django.core.mail import send_mail

class NoteHome(DataMixin, ListView):
    template_name = 'notes/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self) -> QuerySet:
        return Note.published.all().select_related('cat')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Главная страница', cat_selected=0)


class ShowPost(DataMixin, DetailView):
    # model = Notes #Не использовать этот способ, если определен get_queryset
    template_name = 'notes/show_post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_queryset(self) -> QuerySet:
        return Note.published.all()

    def get_object(self, queryset: QuerySet = None) -> QuerySet:
        return get_object_or_404(queryset or self.get_queryset(), slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)


class NotesCategory(DataMixin, ListView):
    template_name = 'notes/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self) -> QuerySet:
        return Note.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return self.get_mixin_context(context, cat_selected=category.pk, title='Категория: ' + category.name)


class NotesTags(DataMixin, ListView):
    template_name = 'notes/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self) -> QuerySet:
        return Note.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)


class AddPost(PermissionRequiredMixin, DataMixin, CreateView):
    template_name = 'notes/add_post.html'
    form_class = AddPostForm
    success_url = reverse_lazy('home')  # Если не указывать, то идёт редирект на саму статью используя get_absolute_url
    login_url = reverse_lazy('home')
    permission_required = ('notes.add_note',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title_page='Добавление статьи')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class DeletePost(PermissionRequiredMixin, DataMixin, DeleteView):
    model = Note
    template_name = 'notes/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    permission_required = ('notes.delete_note',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title_page='Удаление статьи')


class UpdatePost(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Note
    fields = ['title', 'content_short', 'content_full', 'image', 'is_published', 'cat', 'tags']
    template_name = 'notes/add_post.html'
    success_url = reverse_lazy('home')  # Если не указывать, то идёт редирект на саму статью используя get_absolute_url
    login_url = reverse_lazy('home')
    permission_required = ('notes.change_note',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title_page='Редактирование статьи')


class AboutView(DataMixin, TemplateView):
    template_name = 'notes/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title_page='О сайте')


class ContactView(DataMixin, TemplateView):
    template_name = "notes/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title_page='Обратная связь')
