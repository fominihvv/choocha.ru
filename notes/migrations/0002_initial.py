# Generated by Django 5.1 on 2024-12-19 11:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='note',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='notes.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='notes', to='notes.tagpost', verbose_name='Тэги'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['title', '-time_create'], name='notes_note_title_4445b1_idx'),
        ),
    ]