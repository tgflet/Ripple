from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt, re
from .models import User, Post, Comment, Tag, Category, Message, Response, Following
# Create your views here.

def index(request):
    recent_posts=Post.objects.all().order_by('-created_at')
    context={
        "posts":recent_posts
    }
    return render(request,'app_one/index.html',context)
def register(request):
    return render(request,'app_one/register.html')
def join(request):
    errors=User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags =key)
        return redirect('/register')
    else:
        hash=bcrypt.hashpw(request.POST['pass'].encode(),bcrypt.gensalt())
        fname=f"{request.POST['fname']}"
        lname=f"{request.POST['lname']}"
        username=f"{request.POST['username']}"
        create=User.objects.create(first_name=fname,last_name=lname, username=username,email=request.POST['email'],birthday=request.POST['bday'],password=hash.decode())
        request.session['user']=create.id
        print(request.session['user'])
        messages.success(request, 'Successively Registered. Welcome!',extra_tags="welcome")
        return redirect('/splash')
def verify(request):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(request.POST['id']):
        messages.error(request, 'User could not be logged in',extra_tags="login")
        return redirect('/')
    elif len(request.POST['id'])<1:
        messages.error(request, 'User could not be logged in',extra_tags="login")
        return redirect('/')
    else:
        filtered=User.objects.filter(email=request.POST['id'])
        if filtered:
            result=User.objects.get(email=request.POST['id'])
            if bcrypt.checkpw(request.POST['pass'].encode(), result.password.encode()):
                request.session['user']=result.id
                messages.success(request, 'Successively Registered. Welcome!',extra_tags="welcome")
                return redirect('/splash')
            else:
                messages.error(request, 'User could not be logged in',extra_tags="login")
                return redirect('/')
        else:
            messages.error(request, 'User could not be logged in',extra_tags="login")
            return redirect('/')
def user(request,num):
    number=int(num)
    user_profile=User.objects.get(id=number)
    if 'user' in request.session:
        browser=User.objects.get(id=request.session['user'])
        filtered=Following.objects.filter(follower=browser)
        follow=False
        for user in filtered:
            if filtered.filter(followed_id=user_profile):
                follow=True
    else:
        follow=False
        browser=False
    user_posts=Post.objects.filter(poster=user_profile).order_by('-created_at')
    context={
        "profile": user_profile,
        "categories":Category.objects.all(),
        "posts":user_posts,
        "browser":browser,
        "follow":follow
    }
    return render(request, 'app_one/user.html',context)
def update(request,num):
    text=f"{request.POST['text']}"
    new_profile=User.objects.get(id=request.session['user'])
    new_profile.about=text
    new_profile.save()
    return redirect('/users/'+num)
def home(request):
    if "user" in request.session:
        user_profile=User.objects.get(id=request.session['user'])
        filtered=Following.objects.filter(follower=user_profile)
        posts=Post.objects.all().order_by('-created_at')
        filtering=[]

        for post in posts:
            print(post.categories.all().values('name'))
            if post.poster.id==request.session['user']:
                filtering.append(post)
            elif  filtered.filter(followed_id=post.poster.id):
                filtering.append(post)
            else:
                pass
        context={
            "profile":user_profile,
            "feed":filtering,
            "categories":Category.objects.all(),
        }
        return render(request,'app_one/splash.html',context)
    else:
        return redirect('/')
def search(request):
    if len(request.POST['query'])<1:
        if "cat" not in request.POST:
            return redirect("all/results")
        else:
            category=Category.objects.get(id=request.POST['cat'])
            cat=category.name
            return redirect(cat+"/results")
    else:
        search=f"{request.POST['query']}"
        if "cat" not in request.POST:
            return redirect("all/results/"+search)
        else:
            category=Category.objects.get(id=request.POST['cat'])
            cat=category.name
            return redirect(cat+"/results/"+search)
    
def reset(request):
    request.session.clear()
    messages.error(request, 'You have been logged out',extra_tags="out")
    return redirect('/')
def post(request,num):
    errors=Post.objects.text_validator(request.POST)
    number=int(num)
    poster=User.objects.get(id=number)
    if "cat" not in request.POST:
        errors["cat"]="Category is required"
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags =key)
        return redirect('/users/'+num)
    else:
        cat=Category.objects.get(id=request.POST['cat'])
        post=f"{request.POST['text']}"
        new_post=Post.objects.create(post=post,poster=poster)
        new_post.categories.add(cat)
        if len(request.POST['tag1'])>0:
            tag1=f"{request.POST['tag1']}"
            if Tag.objects.filter(name=tag1):
                tag_1=Tag.objects.get(name=tag1)
            else:
                tag_1=Tag.objects.create(name=tag1)
            new_post.tags.add(tag_1)
        else:
            pass
        if len(request.POST['tag2'])>0:
            tag2=f"{request.POST['tag2']}"
            if Tag.objects.filter(name=tag2):
                tag_2=Tag.objects.get(name=tag2)
            else:
                tag_2=Tag.objects.create(name=tag2)
            new_post.tags.add(tag_2)
        else:
            pass
        if len(request.POST['tag3'])>0:
            tag3=f"{request.POST['tag3']}"
            if Tag.objects.filter(name=tag3):
                tag_3=Tag.objects.get(name=tag3)
            else:
                tag_3=Tag.objects.create(name=tag3)
            new_post.tags.add(tag_3)
        else:
            pass
        return redirect('/users/'+num)
def comment(request,num):
    errors=Comment.objects.text_validator(request.POST)
    post=Post.objects.get(id=request.POST['source'])
    user=User.objects.get(id=request.session['user'])
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags =key)
        return redirect('/users/'+num)
    else:
        comment=f"{request.POST['text']}"
        Comment.objects.create(comment=comment,commenters=user,source=post)
        return redirect('/users/'+num)
def follow(request,num):
    number=int(num)
    followed=User.objects.get(id=number)
    follower=User.objects.get(id=request.session['user'])
    Following.objects.create(followed=followed,follower=follower)
    return redirect('/users/'+num)

def local_post(request):
    errors=Post.objects.text_validator(request.POST)
    poster=User.objects.get(id=request.session['user'])
    if "cat" not in request.POST:
        errors["cat"]="Category is required"
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags =key)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        cat=Category.objects.get(id=request.POST['cat'])
        post=f"{request.POST['text']}"
        new_post=Post.objects.create(post=post,poster=poster)
        new_post.categories.add(cat)
        if len(request.POST['tag1'])>0:
            tag1=f"{request.POST['tag1']}"
            if Tag.objects.filter(name=tag1):
                tag_1=Tag.objects.get(name=tag1)
            else:
                tag_1=Tag.objects.create(name=tag1)
            new_post.tags.add(tag_1)
        else:
            pass
        if len(request.POST['tag2'])>0:
            tag2=f"{request.POST['tag2']}"
            if Tag.objects.filter(name=tag2):
                tag_2=Tag.objects.get(name=tag2)
            else:
                tag_2=Tag.objects.create(name=tag2)
            new_post.tags.add(tag_2)
        else:
            pass
        if len(request.POST['tag3'])>0:
            tag3=f"{request.POST['tag3']}"
            if Tag.objects.filter(name=tag3):
                tag_3=Tag.objects.get(name=tag3)
            else:
                tag_3=Tag.objects.create(name=tag3)
            new_post.tags.add(tag_3)
        else:
            pass
        return redirect(request.META.get('HTTP_REFERER'))
def local_comment(request):
    errors=Comment.objects.text_validator(request.POST)
    post=Post.objects.get(id=request.POST['source'])
    user=User.objects.get(id=request.session['user'])
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags =key)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        comment=f"{request.POST['text']}"
        Comment.objects.create(comment=comment,commenters=user,source=post)
        return redirect(request.META.get('HTTP_REFERER'))
def tag_sort(request,cat,tag):
    if 'user' in request.POST:
        user=User.objects.get(id=request.session['user'])
    else:
        user=False
    existing=False
    if Tag.objects.filter(name=tag):
        if cat == 'all':
            sort=Tag.objects.get(name=tag)
            filtered=Post.objects.filter(tags=sort).order_by('-created_at')
            existing=True
            length=len(filtered)
            context={
                "tag":sort,
                "posts":filtered,
                "user":user,
                "existing":existing,
                "categories":Category.objects.all(),
                "length":length
            }
            return render(request,'app_one/results.html',context)
        else:
            sort=Category.objects.get(name=cat)
            filtered=Post.objects.filter(categories=sort).order_by('-created_at')
            curated=Tag.objects.get(name=tag)
            existing=True
            results=[]
            print(filtered)
            for post in filtered:
                if post.tags.filter(name=tag):
                    results.append(post)
                print(post.tags.all().values('name'))
            length=len(results)
            context={
                "tag":curated,
                "posts":results,
                "user":user,
                "existing":existing,
                "categories":Category.objects.all(),
                "length":length
            }
            return render(request,'app_one/results.html',context)
    else:
        context={
            "tag":tag,
            "user":user,
            "existing":existing,
            "categories":Category.objects.all(),
        }
        return render(request,'app_one/results.html',context)
def cat_sort(request,cat):
    if 'user' in request.POST:
        user=User.objects.get(id=request.session['user'])
    else:
        user=False
    if cat == 'all':
        filtered=Post.objects.all().order_by('-created_at')
        context={
            'user':user,
            'posts':filtered
        }
        return render(request,'app_one/results.html',context)
    else:
        sort=Category.objects.get(name=cat)
        filtered=Post.objects.filter(categories=sort).order_by('-created_at')
        context={
            'user':user,
            'posts':filtered
        }
        return render(request,'app_one/results.html',context)
def destroy(request):
    if 'post' in request.POST:
        number=int(request.POST['post'])
        row_to_delete=Post.objects.get(id=number)
        row_to_delete.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    if 'comment' in request.POST:
        number=int(request.POST['comment'])
        row_to_delete=Comment.objects.get(id=number)
        row_to_delete.delete()
        return redirect(request.META.get('HTTP_REFERER'))