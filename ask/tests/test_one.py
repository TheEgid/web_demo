import unittest
import time
from django.test import Client
from django.contrib.auth.models import User
from django.db.models import Max
from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields import CharField, TextField, IntegerField, \
    DateField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils import timezone

from qa.models import QuestionManager
from qa.models import Answer
from qa.models import Question


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        self.assertTrue(1==1)



class TestModels(unittest.TestCase):
    def test_import(self):
        import qa.models


class TestUser(unittest.TestCase):
    def test_user(self):
        try:
            user, _ = User.objects.get_or_create(
                username='x',
                defaults={'password':'y', 'last_login': timezone.now()})
        except:
            assert False, "Failed to create user model, check db connection"

class TestQuestion(unittest.TestCase):
    def test_question(self):

        try:
            title = Question._meta.get_field('title')
        except FieldDoesNotExist:
            assert False, "title field does not exist in Question model"
        assert isinstance(title, CharField), "title field is not CharField"
        try:
            text = Question._meta.get_field('text')
        except FieldDoesNotExist:
            assert False, "text field does not exist in Question model"
        assert isinstance(text, TextField), "text field is not TextField"
        try:
            added_at = Question._meta.get_field('added_at')
        except FieldDoesNotExist:
            assert False, "added_at field does not exist in Question model"
        assert isinstance(text, DateField) or isinstance(added_at, DateField), \
            "added_at field is not DateTimeField"
        try:
            rating = Question._meta.get_field('rating')
        except FieldDoesNotExist:
            assert False, "rating field does not exist in Question model"
        assert isinstance(rating, IntegerField), "text field is not IntegerField"
        try:
            author = Question._meta.get_field('author')
        except FieldDoesNotExist:
            assert False, "author field does not exist in Question model"
        assert isinstance(author, ForeignKey), "author field is not ForeignKey"
        if hasattr(author, 'related'):
            assert author.related.parent_model == User, \
                "author field does not refer User model"
        elif hasattr(author, 'rel'):
            assert author.rel.to == User, "author field does not refer User model"
        try:
            likes = Question._meta.get_field('likes')
        except FieldDoesNotExist:
            assert False, "likes field does not exist in Question model"
        assert isinstance(likes, ManyToManyField), \
            "likes field is not ManyToManyField"
        if hasattr(likes, 'related'):
            assert likes.related.parent_model == User, \
                "likes field does not refer User model"
        elif hasattr(likes, 'rel'):
            assert likes.rel.to == User, "likes field does not refer User model"
        user, _ = User.objects.get_or_create(
            username='x',
            defaults={'password':'y', 'last_login': timezone.now()})
        try:
            question = Question(title='qwe', text='qwe', author=user)
            question.save()
        except:
            assert False, "Failed to create question model, check db connection"


class TestQuestionManager(unittest.TestCase):
    def test_question_manager(self):
        mgr = Question.objects
        assert isinstance(mgr, QuestionManager), "Question.objects is not an QuestionManager"
        assert hasattr(mgr, 'new'), "QuestionManager has no 'new' queryset method"
        assert hasattr(mgr, 'popular'), "QuestionManager has no 'popular' queryset method"


class TestAnswer(unittest.TestCase):
    def test_answer(self):
        try:
            text = Answer._meta.get_field('text')
        except FieldDoesNotExist:
            assert False, "text field does not exist in Answer model"
        assert isinstance(text, TextField), "text field is not TextField"
        try:
            question = Answer._meta.get_field('question')
        except FieldDoesNotExist:
            assert False, "question field does not exist in Answer model"
        assert isinstance(question, ForeignKey), "question field is not ForeignKey"
        if hasattr(question, 'related'):
            assert question.related.parent_model == Question, "question field does not refer Question model"
        elif hasattr(question, 'rel'):
            assert question.rel.to == Question, "question field does not refer Question model"
        try:
            added_at = Answer._meta.get_field('added_at')
        except FieldDoesNotExist:
            assert False, "added_at field does not exist in Answer model"
        assert isinstance(text, DateField) or isinstance(added_at, DateField), "added_at field is not DateTimeField"
        try:
            author = Answer._meta.get_field('author')
        except FieldDoesNotExist:
            assert False, "author field does not exist in Answer model"
        assert isinstance(author, ForeignKey), "author field is not ForeignKey"
        if hasattr(author, 'related'):
            assert author.related.parent_model == User, "author field does not refer User model"
        elif hasattr(author, 'rel'):
            assert author.rel.to == User, "author field does not refer User model"
        user, _ = User.objects.get_or_create(
            username='x',
            defaults={'password':'y', 'last_login': timezone.now()})
        question = Question.objects.create(title='qwe', text='qwe', author=user)
        try:
            answer = Answer(text='qwe', question=question, author=user)
            question.save()
        except:
            assert False, "Failed to create answer model, check db connection"

class TestInitData(unittest.TestCase):
    def test_import(self):
        res = Question.objects.all().aggregate(Max('rating'))
        max_rating = res['rating__max'] or 0
        user, _ = User.objects.get_or_create(
            username='x',
            defaults={'password':'y', 'last_login': timezone.now()})
        for i in range(30):
            question = Question.objects.create(
                title='question ' + str(i),
                text='text ' + str(i),
                author=user,
                rating=max_rating+i
            )
        time.sleep(2)
        question = Question.objects.create(title='question last', text='text', author=user)
        question, _ = Question.objects.get_or_create(pk=3141592, title='question about pi', text='what is the last digit?', author=user)
        question.answer_set.all().delete()
        for i in range(5):
            answer = Answer.objects.create(text='answer ' + str(i), question=question, author=user)
