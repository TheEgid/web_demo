from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import time
import random


def generate_unical_hash(_lon=3):
    def has_letters(_):
        return any(symbol.isalpha() for symbol in _)
    offset = random.randint(100, 400)
    while has_letters('{0:010x}'.format(int(time.time() * offset))[:_lon]):
        return '{0:010x}'.format(int(time.time() * offset))[:_lon]
    else:
        return generate_unical_hash()


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    objects = QuestionManager()

    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes_user')
    slug = models.SlugField(unique=True, max_length=50)

    def save(self, *args, **kwargs):
        strtime = "".join(str(time.time()).split("."))[6:]
        hash = generate_unical_hash()
        self.slug = slugify(strtime + hash)
        super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(null=True, blank=False, auto_now_add=True)
    question = models.ForeignKey(Question, related_name='answer_set', default=1, blank=False, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

