from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerRegisterForm(UserCreationForm):
    # เปลี่ยนช่อง username เดิมของ Django ให้แสดงผลเป็นเบอร์โทรศัพท์
    username = forms.CharField(label='เบอร์โทรศัพท์ (ใช้เข้าสู่ระบบ)', max_length=10, required=True)
    first_name = forms.CharField(label='ชื่อจริง', max_length=50, required=True)
    last_name = forms.CharField(label='นามสกุล', max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')