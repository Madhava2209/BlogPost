from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class BlogPost(models.Model):
    title= models.CharField(max_length=1000)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)
    cover=models.ImageField(upload_to="cover")
    likes=models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.cover.delete()
        super().delete(*args, **kwargs)



class Comment(models.Model):
    reader=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    blog=models.ForeignKey(BlogPost,on_delete=models.CASCADE,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now=True)
    comment=models.CharField(max_length=300)


    def __str__(self):
        return self.blog

class Like(models.Model):
    reader=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    blog=models.ForeignKey(BlogPost,on_delete=models.CASCADE,null=True,blank=True)