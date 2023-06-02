from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Post(models.Model):
    Positions = [
        ('Novost', 'Новость'),
        ('Article', 'Статья')
    ]
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    field_choice = models.CharField(max_length=20, choices=Positions, default='Article')
    autodata = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
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
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
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
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    ranking_user = models.IntegerField(default=0)

    def update_rating(self):
        Pr = Post.objects.filter(author=self).aggregate(Sum('_ranking'))['_ranking__sum'] * 3
        Co = Comment.objects.filter(User=self.User).aggregate(Sum('_ranking'))['_ranking__sum'])
        Co_under = Comment.objects.filter(Post__Author__User=self.User).aggregate(Sum('_ranking'))['_ranking__sum'])

        self.ranking_user = Pr + Co + Co_under
        self.save()

class Category(models.Model):
    catg = models.CharField(max_length=100, unique=True)

class PostCategory(models.Model):
    post_with = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_with = models.ForeignKey(Category, on_delete=models.CASCADE)


