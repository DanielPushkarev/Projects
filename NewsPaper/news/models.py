from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Post(models.Model):
    positions = [
        ('Novost', 'Новость'),
        ('Article', 'Статья')
    ]
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    field_choice = models.CharField(max_length=20, choices=positions, default='Article')
    autodata = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    ranking = models.SmallIntegerField(default=0)

    def like(self):
        self.ranking += 1
        self.save()

    def dislike(self):
        self.ranking -= 1
        self.save()

    def preview(self):
        return self.text[0:128] + '...'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_1 = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    ranking = models.SmallIntegerField(default=0)

    def like(self):
        self.ranking += 1
        self.save()

    def dislike(self):
        self.ranking -= 1
        self.save()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ranking_user = models.IntegerField(default=0)

    def update_rating(self):
        rating_of_posts = Post.objects.filter(author=self).aggregate(Sum('_ranking'))['_ranking__sum'] * 3
        rating_of_comments = Comment.objects.filter(user=self.user).aggregate(Sum('_ranking'))['_ranking__sum']
        rating_of_comments_by_others = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('_ranking'))['_ranking__sum']

        self.ranking_user = rating_of_posts + rating_of_comments + rating_of_comments_by_others
        self.save()

class Category(models.Model):
    catg = models.CharField(max_length=100, unique=True)

class PostCategory(models.Model):
    post_with = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_with = models.ForeignKey(Category, on_delete=models.CASCADE)


