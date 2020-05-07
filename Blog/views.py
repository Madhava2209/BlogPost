from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import *
# Create your views here.
def signup(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        email=request.POST["email"]
        user=User.objects.create_user(username=username,password=password,email=email)
        login(request,user)

        #subject = "Welcome to BlogPost!!!"
        #message = f"Hi {user.username}, use this application for reading and posting the blogs."
        #email_from = settings.EMAIL_HOST_USER
        #recipient_list = [user.email,]
        #send_mail(subject,message,email_from,recipient_list)
        
        return redirect("/home/")
    return render(request,"signup.html")


def signin(request):
    context = {}
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(username=username,password=password)
        if user :
            login(request,user)
            return redirect("/home/")
        else:
            context['error']="Provide valid credentials!!"
            return render(request,'login.html',context)
    return render(request,"login.html",context)

def signout(request):
    logout(request)
    return redirect("/login/")

def home(request):
    all_posts = BlogPost.objects.all()
    return render(request,"home.html",{"all":all_posts})

def post_page(request,post_id):
    post = BlogPost.objects.get(pk=post_id)
    comment=Comment.objects.filter(blog=post)
    return render(request,"post_page.html",{"post":post,"comment":comment})


def create_post(request):
    if request.method=="POST":
        title=request.POST["title"]
        content=request.POST["content"]
        author=request.POST["author"]
        
        new_post=BlogPost.objects.create(title=title,content=content,author=author,cover=request.FILES["cover"])
        return redirect("/home/")
    return render(request,"create.html")

def delete(request,post_id):
    post=BlogPost.objects.get(pk=post_id)
    post.delete()
    return redirect("/home/")

def edit_post(request,post_id):
    post=BlogPost.objects.get(pk=post_id)

    if request.method=="POST":
        title=request.POST["title"]
        content=request.POST["content"]
        timestamp=request.POST["timestamp"]
        author=request.POST["author"]
        
        post.title=title
        post.content=content
        post.timestamp=timestamp
        post.author=author
        post.cover=request.POST["cover"]
        post.save()
        return redirect(f"/post/{post.id}/")

    return render(request,"edit_post.html",{"post":post})

def comment(request,post_id):
    user=request.user
    context={}
    blog_instance=BlogPost.objects.get(pk=post_id)
    comment=Comment.objects.filter(blog=blog_instance)
    if request.method=="POST":
        if user.is_authenticated:
            comment=request.POST["comment"]
            reader=request.user
            blog=blog_instance
            comment_instance=Comment.objects.create(
                comment=comment,
                reader=reader,
                blog=blog,
                )
            return redirect(f"/post/{blog.id}/")
        else:
            context["error"]="Please login!!!"
            return render(request,"login.html",context)
    return render(request,"post_page.html",{"blog":blog_instance,"comment":comment})


def like(request,post_id):
    blog=BlogPost.objects.get(pk=post_id)
    like=Like.objects.filter(reader=request.user,blog=blog)
    if like :
        return redirect(f"/post/{post_id}/")
    blog.likes +=1
    blog.save()
    like=Like.objects.create(reader=request.user,blog=blog)
    return redirect(f"/post/{blog.id}/")


def delete(request,post_id):
    post=BlogPost.objects.get(pk=post_id)
    post.delete()
    return redirect("/home/")