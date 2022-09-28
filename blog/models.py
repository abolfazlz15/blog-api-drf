import os
import uuid

from accounts.models import User
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext as _


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join('article/post', filename)


class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(blank=True, null=True, upload_to=get_file_path, verbose_name=_('Image'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article', verbose_name=_('Author'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='articles', verbose_name=_('Category'))
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True, related_name='articles', verbose_name=_('Tag'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     self.slug = slugify(self.title)
    #     super(Article, self).save()

    def __str__(self):
        return f'{self.title} - {self.text[:20]}'

    def showImage(self):
        # show image in admin panel
        if self.image:
            return format_html(f'<img src="{self.image.url}" alt="" width="50px" height="50px">')
        else:
            return format_html('no image')
    showImage.short_description = 'image'

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes', verbose_name=_('Article'))
    user = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='like', verbose_name=_('User'))

    def __str__(self):
        return f'{self.article} - {self.user}'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Article'))
    user = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment', verbose_name=_('User'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies',
                               verbose_name=_('Subset'))
    text = models.TextField(verbose_name=_('Text'))
    status = models.BooleanField(default=True, verbose_name=_('Status'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return f'{self.article} - {self.user}|{self.text[:20]}'
