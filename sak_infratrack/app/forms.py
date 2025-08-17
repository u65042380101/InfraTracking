from django import forms
from .models import HelpdeskRecord

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
