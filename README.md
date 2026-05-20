# ViperSport — ระบบขายอุปกรณ์กีฬา (Django MVT)

เว็บไซต์ร้านขายอุปกรณ์กีฬาพัฒนาด้วย **Django Framework** ตามรูปแบบ **Model–View–Template (MVT)**  
รองรับ **PostgreSQL บน Supabase** พร้อมฟีเจอร์สมาชิก แต้มสะสม ตราถูกใจ และระบบแอดมิน

---

## คุณสมบัติตามขอบเขตโครงงาน

| ข้อกำหนด | การ implement |
|----------|----------------|
| Django MVT | แอป `shop` — Models, Views, Templates |
| ฐานข้อมูล ≥ 1 ตาราง | Category, Product, MemberProfile, Favorite, Order, OrderItem, PhonePointLog |
| แสดงข้อมูลจาก DB | หน้ารายการสินค้า, หน้าแรก, โปรไฟล์ |
| ค้นหา ≥ 2 เงื่อนไข | คำค้นหา + หมวดหมู่ + ราคาต่ำสุด + ราคาสูงสุด |
| แก้ไขข้อมูล | แอดมินแก้ไขสินค้า/หมวดหมู่ |
| ลบข้อมูล + แจ้งเตือนก่อนลบ | หน้ายืนยันลบ (`product_delete_confirm`, `category_delete_confirm`) |
| จัดหน้าจอเหมาะสม | UI ธีมกีฬา (Kanit, สีเขียว-เทาเข้ม) |

### ฟีเจอร์เพิ่มเติม (คะแนนพิเศษ)

- **แอดมิน hard-coded** — เข้าสู่ระบบที่ `/manage/login/` (ไม่ใช้ Django superuser)
- **ระบบสมาชิก** — สมัคร / เข้าสู่ระบบ
- **แต้มสะสม** — แจ้งเบอร์โทรรับแต้ม (ครั้งเดียวต่อเบอร์)
- **ตราถูกใจ** — กดชอบสินค้า (Favorite)
- **ชำระเงินสดเท่านั้น** — `payment_method = cash` ตลอด
- **PostgreSQL + Supabase** — ตั้งค่าผ่าน `.env`

---

## ภาพหน้าเว็บไซต์

> หลังรันเซิร์ฟเวอร์ ให้ถ่าย screenshot แล้ววางใน `docs/screenshots/`

| หน้า | URL |
|------|-----|
| หน้าแรก | http://127.0.0.1:8000/ |
| สินค้า + ค้นหา | http://127.0.0.1:8000/products/ |
| สมัครสมาชิก | http://127.0.0.1:8000/register/ |
| โปรไฟล์ + แต้ม | http://127.0.0.1:8000/profile/ |
| แอดมิน | http://127.0.0.1:8000/manage/login/ |

```
docs/screenshots/
├── 01-home.png      ← ใส่ภาพหลังถ่าย screenshot
├── 02-products.png
├── 03-admin.png
└── 04-member.png
```

---

## ความต้องการของระบบ

- Python 3.10+
- pip
- (แนะนำ) บัญชี [Supabase](https://supabase.com) สำหรับ PostgreSQL

---

## การติดตั้ง

### 1. Clone จาก GitHub

```bash
git clone https://github.com/luck-nara/ViperSport.git
cd ViperSport
```

### 2. สร้าง virtual environment (แนะนำ)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. ติดตั้งแพ็กเกจ

```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า environment

```bash
copy .env.example .env
```

แก้ไขไฟล์ `.env` ตามโปรเจกต Supabase ของคุณ

---

## การตั้งค่า PostgreSQL (Supabase)

คู่มือละเอียด: **[docs/SUPABASE.md](docs/SUPABASE.md)**

1. สร้างโปรเจกตที่ [supabase.com](https://supabase.com)
2. **Project Settings → Database → Connection string (URI)**
3. ใส่ใน `.env`:

```env
DATABASE_URL=postgresql://postgres.[REF]:[PASSWORD]@db.[REF].supabase.co:5432/postgres
DB_SSLMODE=require
```

4. ทดสอบและ migrate:

```bash
python manage.py check_db
python manage.py migrate
python manage.py seed_data
```

> **หมายเหตุ:** ถ้าไม่ตั้ง `DATABASE_URL` / `DB_HOST` จะใช้ **SQLite** ในเครื่อง

---

## การรันเว็บไซต์

```bash
python manage.py runserver
```

เปิดเบราว์เซอร์: **http://127.0.0.1:8000/**

---

## บัญชีทดสอบ

### แอดมิน (hard-coded)

| รายการ | ค่าเริ่มต้น |
|--------|-------------|
| URL | `/manage/login/` |
| Username | `viperadmin` |
| Password | `ViperSport2025!` |

เปลี่ยนได้ใน `.env` → `ADMIN_USERNAME`, `ADMIN_PASSWORD`

### สมาชิก

สมัครใหม่ที่ `/register/` แล้ว:

1. เข้า **โปรไฟล์** → **แจ้งเบอร์โทรรับแต้ม** (ได้ 50 แต้ม)
2. กด **ตราถูกใจ** ที่หน้าสินค้า
3. ใส่ตะกร้า → **ชำระเงินสด** ที่ checkout

---

## โครงสร้างโปรเจกต

```
ViperSport/
├── viperproject/          # settings, urls หลัก
├── shop/                  # แอปหลัก (MVT)
│   ├── models.py          # Model
│   ├── views.py           # View
│   ├── forms.py
│   ├── urls.py
│   └── management/commands/seed_data.py
├── templates/             # Template
├── static/css/style.css
├── media/                 # รูปสินค้า
├── requirements.txt
├── .env.example
└── README.md
```

---

## การอัปโหลด GitHub

```bash
git add .
git commit -m "feat: ViperSport Django sports shop with member points and admin"
git remote add origin https://github.com/luck-nara/ViperSport.git
git push -u origin main
```

Repository: **https://github.com/luck-nara/ViperSport**

อย่า commit ไฟล์ `.env` (มีรหัสผ่าน DB)

---

## เทคโนโลยี

- Django 6.x
- PostgreSQL (Supabase) / SQLite (dev)
- Pillow (รูปสินค้า)
- WhiteNoise (static files)

---

## ผู้พัฒนา

โครงงาน CS — ระบบขายอุปกรณ์กีฬา **ViperSport**
