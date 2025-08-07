import random

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User

from apartment.EmailBackEnd import EmailBackEnd
import os
import cv2
import numpy as np
import uuid
import sys
import zipfile
import company.settings
from datetime import datetime
from zipfile import ZipFile

from django.contrib import admin
from django.contrib.auth.backends import ModelBackend
from django.core.files.base import ContentFile
from company.settings import BASE_DIR

detector = cv2.CascadeClassifier(os.path.join(BASE_DIR, 'organisation/haarcascade_frontalface_default.xml'))
recognizer = cv2.face.LBPHFaceRecognizer_create()

from PIL import Image
recognizer = cv2.face.LBPHFaceRecognizer_create()

from .models import *
from .forms import AlbumForm, EditApartmentForm

# Create your views here.

def gallery(request):
    list = Album.objects.filter(is_visible=True).order_by('region')
    paginator = Paginator(list, 10)

    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        albums = paginator.page(
            paginator.num_pages)  # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, 'home_template/home.html', {'albums': list})


class AlbumDetail(DetailView):
     model = Album

     def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = AlbumImage.objects.filter(album=self.object.id)
        return context


def handler404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)


def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method == "POST":
        if User.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            user = User.objects.get(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                custom = CustomUser.objects.get(user=user)
                user_type = custom.user_type
                # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
                if user_type == '1':
                    return redirect('admin_home')

                elif user_type == '2':
                    # return HttpResponse("Staff Login")
                    return redirect('staff_home')

                elif user_type == '3':
                    # return HttpResponse("Student Login")
                    return redirect('student_home')
                elif user_type == '4':
                    return redirect('user_home')
                elif user_type == '5':
                    return redirect("/")
                else:
                    messages.error(request, "Invalid Login!")
                    return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('login')


def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: " + request.user.email + " User Type: " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return redirect('login')


def cart_item_counter(request):
    user = Random_users.objects.get(id=request.user.id)
    qs = Order.objects.filter(user=user, ordered=False)
    orders = qs.items.count()

    context = {
        "user": user,
        "orders": orders,
    }
    return render(request, 'home_template/base_template.html', context)


class FaceRecognition:

    def camera(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)  # set Width
        cap.set(4, 480)  # set Height

        while True:
            ret, img = cap.read()
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(
                gray,

                scaleFactor=1.2,
                minNeighbors=5,

                minSize=(20, 20)
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]

            cv2.imshow('video', img)

            k = cv2.waitKey(30) & 0xff
            if k == 27:  # press 'ESC' to quit
                break

        cap.release()
        cv2.destroyAllWindows()

    def faceDetect(self, Entry1, ):
        face_id = Entry1
        cascadePath = BASE_DIR + '\\organisation\\haarcascade_frontalface_default.xml'
        faceCascade = cv2.CascadeClassifier(cascadePath)
        # face_name = Entry2
        # try:
        #     conn.execute('''insert into facedata values ( ?, ?)''', (face_id, face_name))
        #     conn.commit()
        # except sqlite3.IntegrityError:
        #     print("\n ERROR! This id alreeady exists in database!")
        #     print("\n Try agian with new id\n")
        #     exit()

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)  # set Width
        cap.set(4, 480)  # set Height

        count = 0

        while (True):

            ret, img = cap.read()
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,

                scaleFactor=1.2,
                minNeighbors=5,

                minSize=(20, 20)
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]
            count += 1

            cv2.imshow('video', img)
            cv2.imwrite(BASE_DIR + '\\organisation\\dataset\\User.' + str(face_id) + '.' + str(count) + ".jpg", gray)

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 60:  # Take 30 face sample and stop video
                break

        cap.release()
        cv2.destroyAllWindows()

    def trainFace(self):
        # Path for face image database
        path = BASE_DIR + '\\organisation\\dataset'

        # function to get the images and label data
        def getImagesAndLabels(path):

            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []

            for imagePath in imagePaths:

                pilimg = Image.open(imagePath).convert('L')  # convert it to grayscale
                img_numpy = np.array(pilimg, 'uint8')
                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_numpy)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(id)

            return faceSamples, ids

        print("\n Training faces. It will take a few seconds. Wait ...")
        faces, ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.save(BASE_DIR + '\\organisation\\trainer\\trainer.yml')  # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))


def addFace(request):
    recognizer.read(BASE_DIR + '\\organisation\\trainer\\trainer.yml')
    cascadePath = BASE_DIR + '\\organisation\\haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX
    face_id = 0
    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'Abbas', 'Mwatum', 'Mama', 'Z', 'W']

    confidence = 0

    # Retriving names from database
    # data = conn.execute('''select * from facedata''')
    # for x in data:
    #     names.append(x[1])

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:

        ret, img = cam.read()
        img = cv2.flip(img, 1)  # Flip vertically

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            face_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            # Check if confidence is less then 100 ==> "0" is perfect match
            if (confidence < 15):
                face_id = names[face_id]
                confidence = "  {0}%".format(round(100 - confidence))
                cv2.putText(img, str(face_id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                return redirect('faceAdd')
            else:
                face_id = "Unknown"
                confidence = "  {0}%".format(round(100 - confidence))
                cv2.putText(img, str(face_id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                return redirect('/')

        cv2.imshow('Detect Face', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
        if confidence > 50:
            break

    print("\n Exiting Program")
    cam.release()
    cv2.destroyAllWindows()


def faceAdd(face_id):
    facerecognition = FaceRecognition()
    face_id = random.randrange(15)
    facerecognition.faceDetect(face_id)
    facerecognition.trainFace()
    return redirect('login')

