from django import forms
from .models import HelpdeskRecord
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class HelpdeskRecordForm(forms.ModelForm):
    class Meta:
        model = HelpdeskRecord
        fields = '__all__'
        widgets = {
            'branch_code': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 px-3 py-2'
            }),
            'branch_name': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border-gray-200 bg-gray-100 shadow-sm px-3 py-2',
                'readonly': 'true'
            }),
            'device': forms.Select(attrs={
                'class': 'w-full rounded-xl border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 px-3 py-2'
            }),
            'provider': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border-gray-200 bg-gray-100 shadow-sm px-3 py-2',
                'readonly': 'true'
            }),
            'problem': forms.Textarea(attrs={
                'class': 'w-full rounded-xl border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 px-3 py-2',
                'rows': 3
            }),
            'solution': forms.Textarea(attrs={
                'class': 'w-full rounded-xl border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 px-3 py-2',
                'rows': 3
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full rounded-xl border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 px-3 py-2',
                'type': 'date'
            }),
            'by': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 px-3 py-2'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full rounded-xl border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 px-3 py-2'
            }),
        }


class SimpleRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="อีเมล", required=True)
    password = forms.CharField(label="รหัสผ่าน", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ["username", "email", "password"]:
            self.fields[name].widget.attrs.update({
                "class": "form-control",
                "placeholder": self.fields[name].label
            })
        self.fields["username"].widget.attrs["autofocus"] = True
        self.fields["email"].widget.attrs["type"] = "email"

    def clean_username(self):
        u = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=u).exists():
            raise forms.ValidationError("ชื่อนี้ถูกใช้แล้ว")
        return u

    def clean_email(self):
        e = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=e).exists():
            raise forms.ValidationError("อีเมลนี้ถูกใช้แล้ว")
        return e

    def clean_password(self):
        p = self.cleaned_data["password"]
        validate_password(p)
        return p

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user