# Generated by Django 3.2.11 on 2022-02-21 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210930_0141'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='main.project')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='main.project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='child_projects',
            field=models.ManyToManyField(blank=True, related_name='parent_projects', through='main.ProjectRelation', to='main.Project'),
        ),
        migrations.AddConstraint(
            model_name='projectrelation',
            constraint=models.UniqueConstraint(fields=('parent', 'child'), name='uq_project_parent_child'),
        ),
    ]