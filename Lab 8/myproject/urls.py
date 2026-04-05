from django.contrib import admin
from django.urls import path
from myapp import views # ดึง views จาก myapp มาใช้

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),          # หน้าแรก
    path('about/', views.about, name='about'),    # หน้าเกี่ยวกับเรา
    path('form/', views.form, name='form'),       # หน้าแบบฟอร์ม
]