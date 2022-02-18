# Generated by Django 4.0.2 on 2022-02-17 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GitUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_name', models.TextField(null=True)),
                ('owner_link', models.URLField(null=True)),
            ],
            options={
                'verbose_name': 'Аккаунт',
                'verbose_name_plural': 'Аккаунты',
            },
        ),
        migrations.CreateModel(
            name='GitItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_rep', models.URLField(null=True)),
                ('name_rep', models.TextField(null=True)),
                ('about', models.TextField(null=True)),
                ('link_site', models.TextField(null=True)),
                ('stars', models.IntegerField(null=True)),
                ('watching', models.IntegerField(null=True)),
                ('forks', models.IntegerField(null=True)),
                ('commit_count', models.TextField(null=True)),
                ('commit_author', models.TextField(null=True)),
                ('commit_name', models.TextField(null=True)),
                ('commit_datetime', models.TextField(null=True)),
                ('release_count', models.TextField(null=True)),
                ('release_version', models.TextField(null=True)),
                ('release_datetime', models.TextField(null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gituser')),
            ],
            options={
                'verbose_name': 'Репозиторий',
                'verbose_name_plural': 'Репозитории',
            },
        ),
    ]
