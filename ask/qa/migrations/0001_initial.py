# Generated by Django 3.0.5 on 2020-04-05 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('added_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='likes_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('added_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answer_set', to='qa.Question')),
            ],
        ),
    ]
