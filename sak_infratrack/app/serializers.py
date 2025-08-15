from rest_framework import serializers
from .models import BranchInfo, InternetLink, HelpdeskRecord

class BranchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchInfo
        fields = '__all__'

class InternetLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternetLink
        fields = '__all__'

class HelpdeskRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpdeskRecord
        fields = '__all__'