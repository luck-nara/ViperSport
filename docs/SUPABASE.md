# เชื่อมต่อ Supabase (PostgreSQL)

## ขั้นตอน

### 1. สร้างโปรเจกต Supabase

1. เข้า [https://supabase.com](https://supabase.com) → **New Project**
2. ตั้งชื่อโปรเจกต → รอสร้างเสร็จ

### 2. คัดลอก Connection String

1. หน้าโปรเจกต → ปุ่ม **Connect** → แท็บ **Database**  
   หรือ **Project Settings** (เฟือง) → **Database**
2. คัดลอก **URI** แบบ Direct (พอร์ต 5432) เช่น:

```
postgresql://postgres:[YOUR-PASSWORD]@db.evxpuovoplfhcjkdcnag.supabase.co:5432/postgres
```

3. แทน `[YOUR-PASSWORD]` ด้วยรหัสจาก **Database → Settings → Reset database password**

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
| `could not translate host name` / Name or service not known | ใช้ **Session pooler** แทน Direct (ดูด้านล่าง) — host `db.xxx.supabase.co` บางโปรเจกตมีแค่ IPv6 |
| SSL error | ตั้ง `DB_SSLMODE=require` |
| password authentication failed | รีเซ็ตรหัส DB ใน Supabase แล้วอัปเดต `.env` |
| connection timeout | ตรวจอินเทอร์เน็ต / โปรเจกต Supabase ไม่ถูก Pause |

### แก้ DNS / IPv6 (แนะนำถ้า `check_db` ล้มเหลว)

1. หน้าโปรเจกต Supabase → ปุ่ม **Connect** → **Database**
2. เลือก **Session pooler** (พอร์ต **5432**) — ไม่ใช่ Direct
3. คัดลอก URI แบบนี้ (ตัวอย่าง):

```env
DATABASE_URL=postgresql://postgres.evxpuovoplfhcjkdcnag:รหัสผ่าน@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres
```

> User เป็น `postgres.รหัสโปรเจกต` ไม่ใช่แค่ `postgres` — ต้องตรงกับที่ Supabase แสดง

4. รันใหม่: `python manage.py check_db`
