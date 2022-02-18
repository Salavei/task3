from django.db import models


class GitUser(models.Model):
    owner_name = models.TextField(null=True)
    owner_link = models.URLField(null=True)

    def __str__(self):
        return self.owner_name

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class GitItem(models.Model):
    link_rep = models.URLField(null=True)
    name_rep = models.TextField(null=True)
    about = models.TextField(null=True)
    link_site = models.TextField(null=True)
    stars = models.IntegerField(null=True)
    watching = models.IntegerField(null=True)
    forks = models.IntegerField(null=True)
    commit_count = models.IntegerField(null=True)
    commit_author = models.TextField(null=True)
    commit_name = models.TextField(null=True)
    commit_datetime = models.TextField(null=True)
    release_count = models.TextField(null=True)
    release_version = models.TextField(null=True)
    release_datetime = models.TextField(null=True)
    owner = models.ForeignKey(GitUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Репозиторий {self.name_rep} владелец {self.owner.owner_name}'

    class Meta:
        verbose_name = 'Репозиторий'
        verbose_name_plural = 'Репозитории'
