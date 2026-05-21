# ViperSport — ระบบขายอุปกรณ์กีฬา (Django MVT)

เว็บไซต์ร้านขายอุปกรณ์กีฬาพัฒนาด้วย **Django Framework** ตามรูปแบบ **Model–View–Template (MVT)**  
รองรับ **PostgreSQL บน Supabase** พร้อมระบบสมาชิก แต้มสะสม ตราถูกใจ ตะกร้าสินค้า และระบบแอดมินจัดการร้าน

**Repository:** https://github.com/luck-nara/ViperSport

---

## สารบัญ

1. [คุณสมบัติระบบ](#คุณสมบัติระบบ)
2. [ภาพหน้าเว็บไซต์](#ภาพหน้าเว็บไซต์)
3. [ความต้องการของระบบ](#ความต้องการของระบบ)
4. [การติดตั้ง](#การติดตั้ง)
5. [การตั้งค่า](#การตั้งค่า)
6. [การรันเว็บไซต์](#การรันเว็บไซต์)
7. [การใช้งานเว็บไซต์](#การใช้งานเว็บไซต์)
8. [บัญชีทดสอบ](#บัญชีทดสอบ)
9. [คำสั่งจัดการข้อมูล](#คำสั่งจัดการข้อมูล)
10. [โครงสร้างโปรเจกต](#โครงสร้างโปรเจกต)
11. [เทคโนโลยี](#เทคโนโลยี)

---

## คุณสมบัติระบบ

| ข้อกำหนดโครงงาน | รายละเอียด |
|----------------|------------|
| Django MVT | แอป `shop` — Models, Views, Templates |
| ฐานข้อมูล | Category, Product, MemberProfile, Favorite, Order, OrderItem, PhonePointLog |
| แสดงข้อมูลจาก DB | หน้าแรก, รายการสินค้า, โปรไฟล์, แอดมิน |
| ค้นหาหลายเงื่อนไข | คำค้นหา + หมวดหมู่ + ราคาต่ำสุด + ราคาสูงสุด |
| แก้ไข / ลบข้อมูล | แอดมิน CRUD สินค้าและหมวดหมู่ + หน้ายืนยันก่อนลบ |

**ฟีเจอร์เพิ่มเติม**

- สมาชิก: สมัคร / เข้าสู่ระบบ / โปรไฟล์
- แต้มสะสม: แจ้งเบอร์โทรรับแต้ม (ครั้งเดียวต่อเบอร์)
- ตราถูกใจ (Favorite) ที่หน้ารายละเอียดสินค้า
- ตะกร้าและสั่งซื้อ — **ชำระเงินสดเท่านั้น**
- แอดมิน hard-coded ที่ `/manage/login/` (ไม่ใช้ Django Admin ปกติ)
- รูปสินค้าจากคำสั่ง `seed_images` (Pexels/Unsplash)

---

## ภาพหน้าเว็บไซต์

### หน้าแรก

แสดงสินค้าแนะนำและลิงก์ไปยังรายการสินค้าทั้งหมด

![หน้าแรก](docs/screenshots/01-home.png)

---

### รายการสินค้าและค้นหา

ค้นหาด้วยคำค้นหา หมวดหมู่ และช่วงราคา (4 เงื่อนไข)

![รายการสินค้า](docs/screenshots/02-products.png)

---

### รายละเอียดสินค้า

ดูราคา สต็อก คำอธิบาย — สมาชิกกดตราถูกใจและใส่ตะกร้าได้

![รายละเอียดสินค้า](docs/screenshots/03-product-detail.png)

---

### สมัครสมาชิก / เข้าสู่ระบบ

![สมัครสมาชิก](docs/screenshots/04-register.png)

![เข้าสู่ระบบ](docs/screenshots/05-login.png)

---

### โปรไฟล์สมาชิก

ดูแต้มสะสม รายการตราถูกใจ และประวัติคำสั่งซื้อ

![โปรไฟล์สมาชิก](docs/screenshots/06-profile.png)

---

### ตะกร้าสินค้า

ตรวจสอบรายการก่อนสั่งซื้อ (ชำระเงินสด)

![ตะกร้า](docs/screenshots/07-cart.png)

---

### ระบบแอดมิน

เข้าจัดการสินค้า หมวดหมู่ คำสั่งซื้อ และสมาชิก

![แดชบอร์ดแอดมิน](docs/screenshots/08-admin-dashboard.png)

![ฟอร์มเพิ่มสินค้า](docs/screenshots/09-admin-product-form.png)

> ถ่าย screenshot ใหม่: รัน `python manage.py runserver` แล้วรัน `python scripts/capture_screenshots.py` (ต้องติดตั้ง `playwright` ก่อน)

---

## ความต้องการของระบบ

| รายการ | เวอร์ชัน |
|--------|----------|
| Python | 3.10 ขึ้นไป |
| pip | ล่าสุด |
| PostgreSQL | (แนะนำ) ผ่าน [Supabase](https://supabase.com) |
| เบราว์เซอร์ | Chrome, Edge, Firefox |

---

## การติดตั้ง

### 1. Clone โปรเจกต

```bash
git clone https://github.com/luck-nara/ViperSport.git
cd ViperSport
```

### 2. สร้าง Virtual Environment (แนะนำ)

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. ติดตั้งแพ็กเกจ Python

```bash
pip install -r requirements.txt
```

### 4. สร้างไฟล์การตั้งค่า

**Windows**

```powershell
copy .env.example .env
```

**macOS / Linux**

```bash
cp .env.example .env
```

จากนั้นแก้ไข `.env` ตาม [การตั้งค่า](#การตั้งค่า) ด้านล่าง

### 5. สร้างฐานข้อมูลและข้อมูลตัวอย่าง

```bash
python manage.py check_db      # ทดสอบการเชื่อมต่อ DB (ถ้าใช้ PostgreSQL)
python manage.py migrate
python manage.py seed_data       # สมาชิก สินค้า คำสั่งซื้อ ตัวอย่าง
python manage.py seed_images     # ดาวน์โหลดรูปสินค้า (ครั้งแรก)
```

### 6. รันเซิร์ฟเวอร์

```bash
python manage.py runserver
```

เปิดเบราว์เซอร์: **http://127.0.0.1:8000/**

---

## การตั้งค่า

คัดลอกจาก `.env.example` แล้วแก้ค่าตามตารางนี้

| ตัวแปร | คำอธิบาย | ค่าเริ่มต้น |
|--------|----------|-------------|
| `SECRET_KEY` | คีย์ลับ Django | ต้องเปลี่ยนใน production |
| `DEBUG` | โหมด debug | `True` (พัฒนา) |
| `ALLOWED_HOSTS` | โดเมนที่อนุญาต | `localhost,127.0.0.1` |
| `ADMIN_USERNAME` | ชื่อแอดมิน | `viperadmin` |
| `ADMIN_PASSWORD` | รหัสแอดมิน | `ViperSport2025!` |
| `POINTS_PER_PHONE` | แต้มต่อการแจ้งเบอร์ | `50` |
| `DATABASE_URL` | URI PostgreSQL (Supabase) | ว่าง = ใช้ SQLite |
| `DB_SSLMODE` | SSL สำหรับ PostgreSQL | `require` |

### ตัวอย่าง `.env` (SQLite — ทดสอบในเครื่อง)

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ADMIN_USERNAME=viperadmin
ADMIN_PASSWORD=ViperSport2025!
```

ไม่ต้องใส่ `DATABASE_URL` — ระบบใช้ไฟล์ `db.sqlite3` อัตโนมัติ

### ตัวอย่าง `.env` (Supabase PostgreSQL)

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres
DB_SSLMODE=require
```

คู่มือเชื่อม Supabase แบบละเอียด: **[docs/SUPABASE.md](docs/SUPABASE.md)**

> **หมายเหตุ Windows:** ถ้า Direct host (`db.xxx.supabase.co`) ต่อไม่ได้ ให้ใช้ **Session pooler** จาก Supabase → Connect → Database

### ทดสอบการเชื่อมต่อฐานข้อมูล

```bash
python manage.py check_db
```

---

## การรันเว็บไซต์

```bash
python manage.py runserver
```

| หน้า | URL |
|------|-----|
| หน้าแรก | http://127.0.0.1:8000/ |
| สินค้าทั้งหมด | http://127.0.0.1:8000/products/ |
| สมัครสมาชิก | http://127.0.0.1:8000/register/ |
| เข้าสู่ระบบ | http://127.0.0.1:8000/login/ |
| โปรไฟล์ | http://127.0.0.1:8000/profile/ |
| ตะกร้า | http://127.0.0.1:8000/cart/ |
| แอดมิน | http://127.0.0.1:8000/manage/login/ |

---

## การใช้งานเว็บไซต์

### ผู้เยี่ยมชม (ยังไม่ล็อกอิน)

1. เปิด **หน้าแรก** หรือ **สินค้า** เพื่อดูรายการ
2. ใช้แถบค้นหา: กรอกชื่อสินค้า เลือกหมวด กำหนดราคาต่ำสุด–สูงสุด แล้วกด **ค้นหา**
3. คลิกการ์ดสินค้าเพื่อดู **รายละเอียด**
4. กด **สมัครสมาชิก** หรือ **เข้าสู่ระบบ** เพื่อสั่งซื้อ

### สมาชิก

| ขั้นตอน | การทำ |
|---------|--------|
| สมัคร | `/register/` — กรอก username, อีเมล, รหัสผ่าน |
| แต้มสะสม | **โปรไฟล์** → แจ้งเบอร์โทร (รับแต้มครั้งเดียวต่อเบอร์) |
| ตราถูกใจ | หน้ารายละเอียดสินค้า → กด ♡ / ♥ |
| สั่งซื้อ | **ใส่ตะกร้า** → **ตะกร้า** → **สั่งซื้อ** (เงินสดเท่านั้น) |
| ดูคำสั่งซื้อ | **โปรไฟล์** → รายการคำสั่งซื้อ |

### แอดมิน

1. เข้า **http://127.0.0.1:8000/manage/login/**
2. ใช้ username/password จาก `.env` (`ADMIN_USERNAME`, `ADMIN_PASSWORD`)
3. เมนูด้านซ้าย:
   - **แดชบอร์ด** — สรุปยอด
   - **สินค้า** — เพิ่ม / แก้ไข / ลบ (มีหน้ายืนยันก่อนลบ)
   - **หมวดหมู่** — จัดการหมวด
   - **คำสั่งซื้อ** — เปลี่ยนสถานะ (pending / paid)
   - **สมาชิก** — ดูรายชื่อสมาชิก
4. กด **กลับหน้าร้าน** เพื่อดูหน้าลูกค้า

---

## บัญชีทดสอบ

หลังรัน `python manage.py seed_data`

### แอดมิน

| รายการ | ค่า |
|--------|-----|
| URL | `/manage/login/` |
| Username | `viperadmin` |
| Password | `ViperSport2025!` |

### สมาชิก (รหัสผ่านทุกคน: `Member2025!`)

| Username | ชื่อ | แต้ม |
|----------|------|------|
| somchai | สมชาย | 50 |
| malinee | มาลี | 50 |
| watana | วาทนา | 50 |
| piraya | พิรญา | 50 |
| anan | อานันท์ | 50 |
| naree | นารี | 50 |
| kittisak | กิตติศักดิ์ | 50 |
| siriporn | ศิริพร | 50 |
| prasert | ประเสริฐ | 50 |
| duangjai | ดวงใจ | 0 (ยังไม่แจ้งเบอร์) |

**ข้อมูลตัวอย่าง:** สินค้า 20 รายการ · ตราถูกใจ ~21 · คำสั่งซื้อ 9 รายการ

---

## คำสั่งจัดการข้อมูล

```bash
# ข้อมูลตัวอย่าง (สมาชิก สินค้า คำสั่งซื้อ)
python manage.py seed_data

# รูปสินค้า (ดาวน์โหลดจากอินเทอร์เน็ต)
python manage.py seed_images
python manage.py seed_images --force   # โหลดรูปใหม่ทั้งหมด

# ทดสอบ DB
python manage.py check_db

# ถ่าย screenshot สำหรับ README
pip install playwright
python -m playwright install chromium
python scripts/capture_screenshots.py
```

รูปสินค้าเก็บที่ `media/products/`

---

## โครงสร้างโปรเจกต

```
ViperSport/
├── viperproject/              # settings.py, urls หลัก
├── shop/                      # แอปหลัก (MVT)
│   ├── models.py              # Model
│   ├── views.py               # View
│   ├── forms.py               # Form
│   ├── urls.py
│   ├── context_processors.py  # เมนู active, ตะกร้า
│   └── management/commands/
│       ├── seed_data.py
│       ├── seed_images.py
│       └── check_db.py
├── templates/
│   ├── base.html
│   └── shop/                  # หน้าลูกค้า + admin
├── static/
│   ├── css/style.css
│   └── images/logo-sit.png
├── media/products/            # รูปสินค้าอัปโหลด/seed
├── docs/
│   ├── SUPABASE.md
│   └── screenshots/           # ภาพประกอบ README
├── scripts/capture_screenshots.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## การอัปโหลด GitHub

```bash
git add .
git commit -m "docs: update README with screenshots and usage guide"
git push origin main
```

> **อย่า commit ไฟล์ `.env`** — มีรหัสผ่านฐานข้อมูลและแอดมิน

---

## เทคโนโลยี

| เทคโนโลยี | การใช้งาน |
|-----------|-----------|
| Django 5.x–6.x | Framework หลัก (MVT) |
| PostgreSQL / SQLite | ฐานข้อมูล |
| Supabase | PostgreSQL บนคลาวด์ |
| Pillow | อัปโหลดรูปสินค้า |
| WhiteNoise | ไฟล์ static ใน production |
| python-dotenv | อ่านค่าจาก `.env` |
| psycopg2-binary | เชื่อม PostgreSQL |

---

## ผู้พัฒนา

โครงงาน CS — ระบบขายอุปกรณ์กีฬา **ViperSport**  
มหาวิทยาลัยศรีปทุม (SPU) — สำนักเทคโนโลยีสารสนเทศ (SIT)
