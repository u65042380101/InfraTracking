from django.db import models

class BranchInfo(models.Model):
    id = models.AutoField(primary_key=True)
    branch_code = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=255)
    tel_6_digits = models.CharField(max_length=255)

    def __str__(self):
        return self.branch_name

class InternetLink(models.Model):
    id = models.AutoField(primary_key=True)
    branch_id = models.IntegerField()
    branch_name = models.CharField(max_length=255)
    proivider = models.CharField(max_length=255)
    fttx = models.CharField(max_length=255)
    speed = models.CharField(max_length=255)
    start_date = models.DateField()
    last_service = models.DateField()
    service_center = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.branch_name} - {self.proivider}"

class HelpdeskRecord(models.Model):
    id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=255)
    device = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    problem = models.CharField(max_length=255)
    solution = models.CharField(max_length=255)
    date = models.DateField()
    by = models.CharField(max_length=255)
    status = models.IntegerField()

    def __str__(self):
        return f"{self.branch_name} - {self.device} - {self.problem}"