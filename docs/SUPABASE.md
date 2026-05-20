# เชื่อมต่อ Supabase (PostgreSQL)

## ขั้นตอน

### 1. สร้างโปรเจกต Supabase

1. เข้า [https://supabase.com](https://supabase.com) → **New Project**
2. ตั้งชื่อโปรเจกต → รอสร้างเสร็จ

### 2. คัดลอก Connection String

1. **Project Settings** (ไอคอนเฟือง) → **Database**
2. เลือก **Connection string** → แท็บ **URI**
3. เลือกโหมด **Session** หรือ **Direct**
4. คัดลอก URI แบบนี้:

```
postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
```

### 3. สร้างไฟล์ `.env`

```bash
copy .env.example .env
```

เปิด `.env` แล้วใส่:

```env
DATABASE_URL=postgresql://postgres.xxxxx:รหัสผ่าน@db.xxxxx.supabase.co:5432/postgres
DB_SSLMODE=require
SECRET_KEY=สุ่มคีย์ยาวๆ
DEBUG=True
```

> แทนที่ `[YOUR-PASSWORD]` ด้วยรหัส Database จาก Supabase (หน้า Settings → Database → Database password)

### 4. ทดสอบและ migrate

```bash
python manage.py check_db
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

ถ้า `check_db` แสดง **Database connection OK** แสดงเชื่อม Supabase สำเร็จ

## ทางเลือก: ตั้งค่าแยกตัวแปร

แทน `DATABASE_URL` ใช้ได้:

```env
DB_HOST=db.xxxxxxxxxxxx.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=รหัสผ่าน
DB_PORT=5432
DB_SSLMODE=require
```

## แก้ปัญหา

| อาการ | วิธีแก้ |
|--------|--------|
| SSL error | ตั้ง `DB_SSLMODE=require` |
| password authentication failed | รีเซ็ตรหัส DB ใน Supabase แล้วอัปเดต `.env` |
| connection timeout | ลองใช้ **Direct connection** แทน pooler ใน URI |
