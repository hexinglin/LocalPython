from .Read import Camera

from django.http import HttpResponse
import cv2

camera = Camera()
def get_home_pic(request):
    ret,frame = camera.read()
    image_data = cv2.imencode('.jpg', frame)[1]

    return HttpResponse(image_data.tostring(), content_type="multipart/x-mixed-replace")



