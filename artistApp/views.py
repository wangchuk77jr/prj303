from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import re
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
from .models import Music
from random import shuffle
#graph library
import matplotlib.pyplot as plt
import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# Create your views here.
def Signup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        # confirmpassword=request.POST.get('confirmPassword')
        try:
            if User.objects.filter(username=username).exists():
                messages.success(request, ' Opps!! username is already taken. Try with another username')
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.success(request, 'Email address is already registered. Please try with different one.')
                return redirect('signup')

            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()

            auth_token = str(uuid.uuid4())
            expiration_time = timezone.now() + datetime.timedelta(hours=12)

            profile_obj = Profile.objects.create(user = new_user, auth_token = auth_token,  token_expiration_time=expiration_time)
            profile_obj.save()
            
            send_mail_for_verification(email, auth_token, expiration_time)

            return render(request, 'token_send.html',{'email':email})

        except Exception as e:
            print(e)

    return render(request,'Signup.html')

def Login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()

        if user_obj is None:
            messages.success(request, "User not found, plaese try with valid username !!!")
            return redirect('login')
        
        profile_obj = Profile.objects.filter(user=user_obj).first()
        if profile_obj is not None:
            if not profile_obj.is_verified:
                messages.success(request, "Your account is not verified. Please check your email to verify your account.")
                return redirect('login')
        else:
            messages.success(request, "User name not found.")
            return redirect('login')

        user=authenticate(request, username=username, password=password)
        if user is None:
             messages.success(request, "You have entered wrong password !!!")
             return redirect('login')

        login(request, user)
        return redirect('userdashboard')

    return render(request,'Login.html')

def Token_send(request):
    return render(request, 'token_send.html')

def Success(request):
    return render(request, 'success.html')

def Verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, "Your account is already verified.")
                return redirect('login')

            if profile_obj.token_expiration_time and profile_obj.token_expiration_time < timezone.now():
                messages.error(request, "The verification link has expired.")
                return redirect('error')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('success')
        else:
            messages.error(request, 'Invalid verification link.')
            return redirect('error')
    except Exception as e:
        print(e)

    return HttpResponse('Error verifying account.')

def Error(request):
    return render(request, 'Error.html') 

def send_mail_for_verification(email, auth_token, expiration_time):
    subject = 'Emovibe Music | Verification Link'
    message = f'Hi, please click the link below to verify your account. This link will expire on {expiration_time.strftime("%Y/%m/%d %I:%M %p")}: http://127.0.0.1:8000/artist/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    
@login_required(login_url='userdashboard')
def UserDashboard(request):
    # total number of each music
    profile = Profile.objects.get(user=request.user)
    user = request.user
    happy_count = int(user.music_set.filter(category='happy').count())
    sad_count = int(user.music_set.filter(category='sad').count())
    fear_count = int(user.music_set.filter(category='fear').count())
    neutral_count = int(user.music_set.filter(category='neutral').count())
    disgust_count = int(user.music_set.filter(category='disgust').count())
    surprise_count = int(user.music_set.filter(category='surprise').count())
    angry_count = int(user.music_set.filter(category='angry').count())

    total_music = int(user.music_set.count())

    # Set up the chart
    emotions = ['Happy', 'Sad', 'Disgust', 'Fear', 'Neutral','Surprise','Angry']
    counts = [happy_count, sad_count, disgust_count, fear_count, neutral_count, surprise_count,angry_count]
    colors = ['yellowgreen', 'lightcoral', 'gold', 'lightskyblue', 'plum','orange','red']

    fig, ax = plt.subplots()
    ax.bar(emotions, counts, color=colors)

    # Set the chart title and axis labels
    ax.set_title('Music Overview Charts')
    ax.set_xlabel('Music Catagory')
    ax.set_ylabel('Total Number Of Music')

    # Save the chart as an image
    chart_name = 'emotions_chart.png'
    chart_path = os.path.join(settings.MEDIA_ROOT, chart_name)
    plt.savefig(chart_path)
    # user profile change from default
    if request.method == 'POST':
        profile_picture = request.FILES['profile_picture']
        request.user.profile.profile_picture = profile_picture
        request.user.profile.save()
        return redirect('userdashboard')
    
    context = {
        'total_music':total_music,
        'happy_count':happy_count,
        'sad_count':sad_count,
        'fear_count':fear_count,
        'neutral_count':neutral_count,
        'disgust_count':disgust_count,
        'surprise_count':surprise_count,
        'angry_count':angry_count,
        'username': user.username,
        'chart_path':chart_path,
        'profile': profile,
    }
    return render(request,'ArtistDashboard.html',context)

@login_required
def My_Music(request):
    if request.method == 'POST':
        sort_option = request.POST.get('sort_option')
        if sort_option == 'category':
            music_list = Music.objects.filter(user=request.user).order_by('category', 'songTitle')
            music_list = sorted(music_list, key=lambda x: x.category)

        elif sort_option == 'alphabetical':
            music_list = Music.objects.filter(user=request.user).order_by('songTitle')
        elif sort_option == 'random':
            music_list = list(Music.objects.filter(user=request.user))
            shuffle(music_list)
        else:
            music_list = Music.objects.filter(user=request.user).order_by('-id')
        if 'search_button' in request.POST:
            search_query = request.POST.get('search_query')
            music_list = Music.objects.filter(user=request.user, songTitle__icontains=search_query)
            context = {'music_list': music_list}
            return render(request,'my_music.html', context)

        if 'delete_button' in request.POST:
            # Retrieve the music item to be deleted
            music_id = request.POST.get('music_id')
            music = get_object_or_404(Music, id=music_id, user=request.user)

            # Delete the music item
            music.delete()

            # Add success message
            messages.success(request, f"'{music.songTitle}' has been successfully deleted")
            return redirect('myMusic')

        elif 'edit_button' in request.POST:
            # Retrieve the music item to be edited
            music_id = request.POST.get('music_id')
            music = get_object_or_404(Music, id=music_id, user=request.user)

            # Retrieve the updated data from the form
            updated_title = request.POST.get('updated_title')
            updated_singer = request.POST.get('updated_singer')
            updated_category = request.POST.get('updated_category')
            updated_img = request.FILES.get('updated_img')
            updated_audio = request.FILES.get('updated_audio')

            # Update the music item with the new data
            music.songTitle = updated_title
            music.singer = updated_singer
            music.category = updated_category

            # Check if the image file is provided and update it
            if updated_img:
                music.img = updated_img

            # Check if the audio file is provided and update it
            if updated_audio:
                music.audio_file = updated_audio

            # Save the changes to the database
            music.save()

            # Add success message
            messages.success(request, f"'{music.songTitle}' has been successfully updated")
            return redirect('myMusic')

    else:
        # Retrieve all music objects from the database
        music_list = Music.objects.filter(user=request.user).order_by('-id')

    context = {'music_list': music_list}
    return render(request, 'my_music.html', context)

@login_required
def Upload_Music(request):
    if request.method == 'POST':
        user = request.user
        song_title = request.POST.get('songTitle')
        singer = request.POST.get('singer')
        img = request.FILES.get('img')
        audio_file = request.FILES.get('audio_file')
        category = request.POST.get('category')
    
        if song_title and singer and img and audio_file and category:
            music = Music(songTitle=song_title, singer=singer, img=img, audio_file=audio_file, category=category,user=user)
            music.save()
            messages.success(request, 'Music uploaded successfully.')
            return redirect('myMusic')
        else:
            messages.error(request, 'Error uploading music. Please check the form is filled correctly or not!')
            return redirect('uploadMusic')
    return render(request, 'upload_music.html')

@login_required
def SettingProfile(request):
    user = request.user
    if request.method == 'POST':
        if 'update_user' in request.POST:
            # Update username
            new_username = request.POST.get('new_username')
            if new_username:
                # Check if the new username already exists
                if User.objects.filter(username=new_username).exists():
                    user__name__exist = 'Username already exists. Please choose a different username.'
                    return render(request, 'SettingPage.html', {'user_error':user__name__exist})
                else:
                    user.username = new_username
                    user.save()
                    messages.success(request, f'Username has been successfully updated to {user.username}!')
                    return redirect('userdashboard')

        if 'update_password' in request.POST:
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if old_password and new_password1 and new_password2:
                password_change_form = PasswordChangeForm(user, request.POST)
                if password_change_form.is_valid():
                    # Password validation rules
                    if new_password1 != new_password2:
                        messages.error(request, 'New password and confirmed password do not match.')
                        return redirect('profile_setting')
                    if len(new_password1) < 8:
                        messages.error(request, 'Password should be at least 8 characters long.')
                        return redirect('profile_setting')
                    if not re.search(r'[A-Z]', new_password1):
                        messages.error(request, 'Password should contain at least one uppercase letter.')
                        return redirect('profile_setting')
                    if not re.search(r'[a-z]', new_password1):
                        messages.error(request, 'Password should contain at least one lowercase letter.')
                        return redirect('profile_setting')
                    if not re.search(r'\d', new_password1):
                        messages.error(request, 'Password should contain at least one digit.')
                        return redirect('profile_setting')
                    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password1):
                        messages.error(request, 'Password should contain at least one special character.')
                        return redirect('profile_setting')

                    # Change password
                    user = password_change_form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Password has been successfully changed!')
                    return redirect('userdashboard')
                else:
                    # Check if old password didn't match
                    if 'old_password' in password_change_form.errors:
                        messages.error(request, 'Old password is incorrect.')
                        return redirect('profile_setting')
                    # Check if new password and confirmed password didn't match
                    elif 'new_password2' in password_change_form.errors:
                        messages.error(request, 'New password and confirmed password do not match.')
                        return redirect('profile_setting')
                    else:
                        messages.error(request, 'Please correct the error(s) below.')
                    return redirect('profile_setting')
            else:
                messages.error(request, 'Please fill in all the password fields.')
                return redirect('profile_setting')

    context = {'user': user}
    return render(request, 'SettingPage.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')