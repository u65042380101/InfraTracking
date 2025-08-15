## วิธีเริ่มต้นใช้งานโปรเจค

1. **สร้าง Virtual Environment**
   ```bash
   python -m venv venv
   ```

2. **เข้าใช้งาน Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

3. **(ถ้ามี Docker) เริ่มต้นบริการด้วย Docker Compose**
   ```bash
   docker compose up
   ```

4. **ติดตั้ง dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **สร้างไฟล์ migration**
   ```bash
   python manage.py makemigrations
   ```

6. **รัน migration**
   ```bash
   python manage.py migrate
   ```

7. **เริ่มต้นเซิร์ฟเวอร์**
   ```bash
   python manage.py runserver
   ```

---

> แก้ไขค่าต่าง ๆ ใน `.env` หรือ `settings.py` ตามความเหมาะสมก่อนเริ่มใช้งาน
