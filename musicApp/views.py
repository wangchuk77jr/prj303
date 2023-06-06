from django.shortcuts import render
from .models import Feedback
from artistApp.models import Music
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from deepface import DeepFace
from django.db.models import Q
# pacakages for model
import cv2
import numpy as np
from django.http import HttpResponseServerError
from tensorflow.keras.models import load_model
import base64
import json

# Create your views here.


@csrf_exempt # This decorator allows the view to accept POST requests without CSRF tokens
def Home(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        # check if the user has already submitted the form
        if email not in request.session:
            feedback = Feedback(email=email, message=message)
            feedback.save()

            # set the session key to mark the submission
            request.session[email] = True

            # return a success response
            response_data = {'status': 'success', 'message': 'Thank you for your feedback!'}
            return JsonResponse(response_data)
        else:
            # if the user has already submitted the form, show an error message
            response_data = {'status': 'error', 'message': 'You have already submitted the feedback.'}
            return JsonResponse(response_data, status=400)

    return render(request, 'Home.html')

def my_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        request.session['name'] = name
    else:
        name = request.session.get('name', 'default_name')
    return render(request, 'Home.html', {'name': name})

def MusicPlay(request):
    context = request.session.get('expression_data')
    category = context['category']
    music_list = Music.objects.filter(category=category)
    image_data = context['image_data']
    context = {'music_list': music_list,'category':category,'image_data':image_data}
    return render(request,'Musicplay.html',context)

def music_search(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    if category:
        results = Music.objects.filter(
            Q(songTitle__icontains=query) &
            Q(category=category)
        )
    else:
        results = Music.objects.filter(
            songTitle__icontains=query
        )

    return render(request, 'music_search.html', {'results': results})

# def FaceDetection(request):
#     # Load the trained model
#     # model = load_model("FER_Model/best_model (2).h5")

#     # Get the uploaded image from the request
#     # Get the uploaded image from the request
#     if request.method == 'POST':
#         if request.FILES.get('image'):
#             image_file = request.FILES['image'].read()
            
#         elif request.POST.get('image-data'):
#             image_data = request.POST['image-data']
#             header, encoded = image_data.split(",", 1)
#             image_file = base64.b64decode(encoded)
#         else:
#             return HttpResponseServerError('Error in image uploading')
        
#         img = cv2.imdecode(np.fromstring(image_file, np.uint8), cv2.IMREAD_UNCHANGED)

#         # Check if the image size is within a certain range
#         if img.shape[0] < 40 or img.shape[1] < 40:
#             error_message = 'Image too small to detect your face. Please upload a bigger image between 40x40px to 2000x2000px.'
#             return render(request,'Expression-Detection.html',{'error_message':error_message})
            
#         if img.shape[0] > 2000 or img.shape[1] > 2000:
#             error_message = 'Image is too big. Resize between 40 40px to 2000 2000px.Use this link to reduce the image size (https://www.reduceimages.com/)'
#             return render(request,'Expression-Detection.html',{'error_message':error_message})   

#         # Load the face cascade classifier
#         face_cascade_path = "FER_Model/haarcascade_frontalface_default.xml"
#         face_cascade = cv2.CascadeClassifier(face_cascade_path)
#         if face_cascade.empty():
#             return HttpResponseServerError("Failed to load face cascade classifier")

#         # Detect faces in the image
#         faces = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=4)

#         # If no faces are detected, return an error message
#         if len(faces) == 0:
#             error_message = "No human face detected. Please upload an image with your face."
#             return render(request,'Expression-Detection.html',{'error_message':error_message})
#         # If multiple faces are detected, return an error message
#         elif len(faces) > 1:
#             error_message = "Multiple faces detected. Please upload an image with only one face."
#             return render(request,'Expression-Detection.html',{'error_message':error_message})

#         # Choose the largest face as the region of interest (ROI)
#         # Set a threshold for minimum required size of detected face region
#         min_face_size = 50

#         #Get the first face detected and its size
#         x, y, w, h = faces[0]
#         face_size = max(w, h)

#         # If the face size is smaller than the threshold, consider it unimportant for expression detection
#         if face_size < min_face_size:
#             error_message = "Face detected is too small to reliably detect expression. Please upload an image with a larger face."
#             return render(request,'Expression-Detection.html',{'error_message':error_message})

#         # Otherwise, crop the detected face region
#         face_img = img[y:y+h, x:x+w]

#         # Preprocess the face image
#         face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
#         face_img = cv2.resize(face_img, (48, 48))
#         face_img = np.reshape(face_img, (1, 48, 48, 1))

#         # Predict the expression
#         # predictions = model.predict(face_img)
#         predictions = DeepFace.analyze(face_img, actions=['emotion'])

#         # Get the predicted label
#         label = np.argmax(predictions)

#         # Convert the label to the corresponding emotion
#         emotions = {
#             0: "angry",
#             1: "disgust",
#             2: "fear",
#             3: "happy",
#             4: "neutral",
#             5: "sad",
#             6: "surprise"
#         }
#         expression = emotions[label]
#         # Draw a rectangle around the detected face and label it with the predicted expression
#         img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
#         img = cv2.putText(img, expression.capitalize(), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3, cv2.LINE_AA)

#         # Convert the image to base64 for display in HTML
#         _, buffer = cv2.imencode('.png', img)
#         image_data = base64.b64encode(buffer).decode()

#         # Render the Musicplay.html template with the detected expression as a parameter
#         context = {
#         'category': expression,
#         'image_data': image_data
#     }
#         request.session['expression_data'] = context
#         return render(request, 'Expression-Detection.html', context)

#     return render(request, "Expression-Detection.html")

def FaceDetection(request):
    # Load the face cascade classifier
    face_cascade_path = "FER_Model/haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    if face_cascade.empty():
        return HttpResponseServerError("Failed to load face cascade classifier")

    # Get the uploaded image from the request
    if request.method == 'POST':
        if request.FILES.get('image'):
            image_file = request.FILES['image'].read()
        elif request.POST.get('image-data'):
            image_data = request.POST['image-data']
            header, encoded = image_data.split(",", 1)
            image_file = base64.b64decode(encoded)
        else:
            return HttpResponseServerError('Error in image uploading')

        img = cv2.imdecode(np.frombuffer(image_file, np.uint8), cv2.IMREAD_UNCHANGED)

        # Check if the image size is within a certain range
        if img.shape[0] < 48 or img.shape[1] < 48:
            error_message = 'Image too small to detect your face. Please upload a bigger image between 48x48px to 8000x8000px.'
            return render(request, 'Expression-Detection.html', {'error_message': error_message})

        if img.shape[0] > 2000 or img.shape[1] > 2000:
            error_message = 'Image is too big. Resize between 48x48px to 2000x2000px. Use this link to reduce the image size (https://www.reduceimages.com/)'
            return render(request, 'Expression-Detection.html', {'error_message': error_message})

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=4)

        # If no faces are detected, return an error message
        if len(faces) == 0:
            error_message = "No human face was detected. Please upload an image that clearly shows a human face."
            return render(request, 'Expression-Detection.html', {'error_message': error_message})
        # If multiple faces are detected, return an error message
        elif len(faces) > 1:
            error_message = "Multiple faces were detected. Please upload an image containing only one clearly visible face."
            return render(request, 'Expression-Detection.html', {'error_message': error_message})

        # Choose the largest face as the region of interest (ROI)
        # Set a threshold for the minimum required size of the detected face region
        min_face_size = 50

        # Get the first face detected and its size
        x, y, w, h = faces[0]
        face_size = max(w, h)

        # If the face size is smaller than the threshold, consider it unimportant for expression detection
        if face_size < min_face_size:
            error_message = "The detected face is too small to ensure reliable expression detection. Please upload an image with a larger, more prominent face."
            return render(request, 'Expression-Detection.html', {'error_message': error_message})

        # Predict the expression
        predictions = DeepFace.analyze(img, actions=['emotion'],enforce_detection=False)
        emotions = predictions[0]['emotion']
        expression = max(emotions, key=lambda x: emotions[x])
        dominant_emotion = predictions[0]['dominant_emotion']
        print('Dominant Emotion:', dominant_emotion)
        # Draw a rectangle around the detected face and label it with the predicted expression
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        img = cv2.putText(img, expression.capitalize(), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

        # Convert the image to base64 for display in HTML
        _, buffer = cv2.imencode('.png', img)
        image_data = base64.b64encode(buffer).decode()

        # Render the Musicplay.html template with the detected expression as a parameter
        context = {
            'category': expression,
            'image_data': image_data
        }
        request.session['expression_data'] = context
        return render(request, 'Expression-Detection.html', context)

    return render(request, "Expression-Detection.html")

def My_Music(request):
    return render(request,'my_music.html')

def Upload_Music(request):
    return render(request,'upload_music.html')


