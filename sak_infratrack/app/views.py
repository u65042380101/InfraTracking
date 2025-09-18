from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import BranchInfo, InternetLink, HelpdeskRecord
from .forms import HelpdeskRecordForm  # ต้องสร้างฟอร์มนี้ใน forms.py
from datetime import date
from django.utils.timezone import now

from .forms import SimpleRegistrationForm

def dashboard(request):
    branch_list = []
    for branch in BranchInfo.objects.all():
        pending = HelpdeskRecord.objects.filter(branch_code=branch.branch_code, status=2).count()
        preparing = HelpdeskRecord.objects.filter(branch_code=branch.branch_code, status=3).count()
        alert_count = pending + preparing
        branch_list.append({
            'branch_code': branch.branch_code,
            'branch_name': branch.branch_name,
            'address': branch.address,
            'district': branch.district,
            'region': branch.region,
            'province': branch.province,
            'mobile_number': branch.mobile_number,
            'tel_6_digits': branch.tel_6_digits,
            'alert_count': alert_count,
        })

    # นับรายการวันนี้ เดือนนี้ ปีนี้
    today = date.today()
    today_count = HelpdeskRecord.objects.filter(date=today).count()
    month_count = HelpdeskRecord.objects.filter(date__year=today.year, date__month=today.month).count()
    year_count = HelpdeskRecord.objects.filter(date__year=today.year).count()

    branch_list = sorted(
        branch_list,
        key=lambda b: (-1 if b['alert_count'] > 0 else 0, -b['alert_count'])
    )
    latest_records = HelpdeskRecord.objects.all().order_by('-date', '-id')[:10]  # 10 รายการล่าสุด
    return render(request, 'dashboard.html', {
        'branch_list': branch_list,
        'today_count': today_count,
        'month_count': month_count,
        'year_count': year_count,
        'latest_records': latest_records,#10 รายการล่าสุด
    })

def internet_links_api(request, branch_code):
    links = InternetLink.objects.filter(branch_id=branch_code)
    data = [
        {
            "proivider": link.proivider,
            "fttx": link.fttx,
            "speed": link.speed,
            "start_date": link.start_date,
            "last_service": link.last_service,
            "service_center": link.service_center,
        }
        for link in links
    ]
    return JsonResponse(data, safe=False)

def branch_info_api(request):
    branch_code = request.GET.get('branch_code')
    branch = BranchInfo.objects.filter(branch_code=branch_code).first()
    provider = ""
    if branch:
        # ดึง provider จาก InternetLink ที่ branch_id ตรงกับ branch_code
        link = InternetLink.objects.filter(branch_id=branch_code).first()
        if link:
            provider = link.proivider
        data = {
            'branch_name': branch.branch_name,
            'province': branch.province,
            'provider': provider,  # เพิ่ม provider ที่ดึงจาก InternetLink
        }
    else:
        data = {}
    return JsonResponse(data)

def helpdesk_record(request, branch_code):
    records_all = HelpdeskRecord.objects.filter(branch_code=branch_code)
    # 1 = แก้ไขแล้ว
    not_fixed = records_all.exclude(status=1).order_by('date')   # ยังไม่แก้ไข (เรียงเก่าสุดก่อน)
    fixed = records_all.filter(status=1).order_by('-date')       # แก้ไขแล้ว (เรียงใหม่สุดก่อน)
    records = list(not_fixed) + list(fixed)
    branch = BranchInfo.objects.filter(branch_code=branch_code).first()
    branch_name = branch.branch_name if branch else ""
    return render(request, 'helpdeskRecord.html', {
        'branch_code': branch_code,
        'branch_name': branch_name,
        'records': records,
    })

def add_record(request):
    initial = {}
    branch_code = request.GET.get('branch_code')
    if branch_code:
        branch = BranchInfo.objects.filter(branch_code=branch_code).first()
        # ดึง provider จาก InternetLink
        link = InternetLink.objects.filter(branch_id=branch_code).first()
        provider = link.proivider if link else ""
        if branch:
            initial = {
                'branch_code': branch.branch_code,
                'branch_name': branch.branch_name,
                'provider': provider,  # เพิ่มบรรทัดนี้
                # เพิ่ม field อื่นๆ ที่ต้องการ autofill เช่น
                # 'province': branch.province,
                # 'address': branch.address,
            }
    if request.method == "POST":
        form = HelpdeskRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "บันทึกข้อมูลสำเร็จ")
            return redirect('helpdesk_record', branch_code=form.cleaned_data['branch_code'])
    else:
        form = HelpdeskRecordForm(initial=initial)
    return render(request, 'add_record.html', {'form': form})

def edit_record(request, pk):
    record = get_object_or_404(HelpdeskRecord, pk=pk)
    if request.method == "POST":
        form = HelpdeskRecordForm(request.POST, instance=record)
        if form.is_valid():
            # ป้องกันการแก้ไข branch_code และ date
            form.instance.branch_code = record.branch_code
            form.instance.date = record.date
            form.save()
            # redirect ไปหน้า helpdeskRecord ของสาขานั้น
            return redirect('helpdesk_record', branch_code=record.branch_code)
    else:
        form = HelpdeskRecordForm(instance=record)
    return render(request, 'edit_record.html', {'form': form})

def delete_record(request, pk):
    record = get_object_or_404(HelpdeskRecord, pk=pk)
    if request.method == "POST":
        record.delete()
        # กลับไปหน้ารายการหลังลบ
        return redirect('helpdesk_record', branch_code=record.branch_code)
    return render(request, 'confirm_delete.html', {'record': record})

def summary_report(request):
    # ใช้เฉพาะสำหรับส่วนรวมทั้งปี (อุปกรณ์/ผู้บันทึก) ให้คง status=1 ได้
    qs = HelpdeskRecord.objects.filter(status=1)

    # -----------------------------
    # 1) สรุปจำนวนปัญหาที่แก้ไข (ตามเดือน) — นับทั้งหมด ไม่สนใจว่าแก้ไขหรือไม่
    # -----------------------------
    all_records = HelpdeskRecord.objects.all()

    thai_months = [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    month_summary_list = []
    total_count = 0
    for m in range(1, 13):
        c = all_records.filter(date__month=m).count()
        total_count += c
        month_summary_list.append({
            "month": thai_months[m-1],
            "count": c,
        })
    month_summary_list.append({"month": "รวมทั้งหมด", "count": total_count})

    # -----------------------------
    # 2) สรุปปัญหาที่แก้ไข (รวมทั้งปี) — ตามอุปกรณ์ (แก้ไขแล้วเท่านั้น)
    # -----------------------------
    device_choices = dict(HelpdeskRecord._meta.get_field('device').choices) if HelpdeskRecord._meta.get_field('device').choices else {}
    device_summary_qs = (
        qs.values('device')
          .annotate(count=Count('id'))
          .order_by('device')
    )
    device_summary_list = [
        {"device": device_choices.get(row["device"], row["device"]), "count": row["count"]}
        for row in device_summary_qs
    ]

    # -----------------------------
    # 3) สรุปตามผู้บันทึก (รวมทั้งปี) — เฉพาะแก้ไขแล้ว
    # -----------------------------
    user_summary_qs = (
        qs.values('by')
          .annotate(count=Count('id'))
          .order_by('by')
    )
    user_summary_list = [
        {"by": row["by"], "count": row["count"]}
        for row in user_summary_qs
    ]

    today = timezone.now().date()
    return render(request, 'summary_report.html', {
        "today": today,
        "month_summary": month_summary_list,     # ✅ อัปเดตใหม่ → นับทั้งหมด
        "device_summary": device_summary_list,   # ยังนับเฉพาะแก้ไขแล้ว
        "user_summary": user_summary_list,       # ยังนับเฉพาะแก้ไขแล้ว
    })

# ✅ ฟังก์ชันสมัครสมาชิก,
def register(request):
    if request.method == "POST":
        form = SimpleRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "สมัครสมาชิกสำเร็จ! เข้าสู่ระบบได้เลย")
            return redirect("login")
    else:
        form = SimpleRegistrationForm()
    return render(request, "register.html", {"form": form})   # <<< เปลี่ยนตรงนี้