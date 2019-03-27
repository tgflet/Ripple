from django.db import models
from datetime import timedelta, datetime as dt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        today=dt.now()
        min_age=timedelta(days=4748)
        if len(postData['fname'])<1:
            errors['fname']="All fields are required"
        elif len(postData['fname'])<3:
            errors['fname']="Name should be at least three characters"
        if len(postData['lname'])<1:
            errors['lname']="All fields are required"
        elif len(postData['lname'])<3:
            errors['lname']="Name should be at least three characters"
        if len(postData['username'])<1:
            errors['username']="All fields are required"
        elif len(postData['username'])<3:
            errors['username']="Name should be at least three characters"
        if len(postData['email'])<1:
            errors['email']="All fields are required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email']="Please enter a valid email"
        elif User.objects.filter(email=postData['email']):
            errors['email']="Enter a unique email"
        if len(postData['bday'])<1:
            errors['bday']="All fields are required"
        if len(postData['bday'])>1:
            a=dt.strptime(postData['bday'], "%Y-%m-%d")
            if today<a:
                errors['bday']="Enter a valid birth date"
            if today-a<min_age:
                errors['bday']="User must be at least 13 years old to register"
        if len(postData['pass'])<1:
            errors['pass']="All fields are required"
        elif len(postData['pass'])< 8:
            errors['pass']="Password should be at least eight characters"
        if postData['pass2']!=postData['pass']:
            errors['pass2']="Passwords don't match"
        
        return errors
class TextManager(models.Manager):
    def text_validator(self, postData):
        errors={}
        if len(postData['text'])<1:
            errors['text']="Please Enter Content"
        return errors


class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    birthday=models.DateField()
    about=models.TextField(default='Add Something')
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Post(models.Model):
    post=models.TextField()
    poster=models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TextManager()

class Category(models.Model):
    name=models.CharField(max_length=255)
    posts=models.ManyToManyField(Post, related_name="categories")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name=models.CharField(max_length=255)
    posts=models.ManyToManyField(Post, related_name="tags")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment=models.TextField()
    commenters=models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    source=models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TextManager()

class Message(models.Model):
    message=models.TextField()
    recipient=models.ForeignKey(User, related_name="recipient", on_delete=models.CASCADE)
    messager=models.ForeignKey(User, related_name="poster", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TextManager()

class Response(models.Model):
    response=models.TextField()
    responder=models.ForeignKey(User, related_name="responses", on_delete=models.CASCADE)
    source=models.ForeignKey(Message, related_name="response", on_delete=models.CASCADE)
    private=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TextManager()

class Following(models.Model):
    follower=models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    followed=models.ForeignKey(User, related_name="followed", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)






























































































































































































































































































































































































