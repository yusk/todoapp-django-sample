# Generated by Django 3.1.6 on 2021-09-24 03:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import main.models.base
import main.models.schedule
import main.models.user
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(default='guest user', max_length=64)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, validators=[django.core.validators.EmailValidator])),
                ('password', models.CharField(max_length=254)),
                ('icon', models.ImageField(blank=True, null=True, upload_to=main.models.user.icon_file_path)),
                ('device_uuid', models.UUIDField(default=uuid.uuid4)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            bases=(main.models.base.DeletePreviousFileMixin, models.Model),
            managers=[
                ('objects', main.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(default='')),
                ('deadline', models.DateTimeField(db_index=True, null=True)),
                ('done_at', models.DateTimeField(db_index=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='main.task')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='main.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='child_tasks',
            field=models.ManyToManyField(blank=True, related_name='parent_tasks', through='main.TaskRelation', to='main.Task'),
        ),
        migrations.AddField(
            model_name='task',
            name='projects',
            field=models.ManyToManyField(related_name='tasks', to='main.Project'),
        ),
        migrations.AddField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(related_name='tasks', to='main.Tag'),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_time', models.TimeField()),
                ('to_time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.task', validators=[main.models.schedule.validate_task])),
            ],
        ),
        migrations.AddConstraint(
            model_name='task',
            constraint=models.UniqueConstraint(fields=('user', 'no'), name='task_user_no_unique'),
        ),
    ]
