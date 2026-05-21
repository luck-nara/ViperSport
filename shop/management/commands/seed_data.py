from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from shop.models import (
    Category,
    Favorite,
    MemberProfile,
    Order,
    OrderItem,
    PhonePointLog,
    Product,
)

DEMO_PASSWORD = 'Member2025!'

MEMBERS = [
    ('somchai', 'somchai@vipersport.demo', 'สมชาย', 'ใจดี', '0812345001', True),
    ('malinee', 'malinee@vipersport.demo', 'มาลี', 'รักกีฬา', '0812345002', True),
    ('watana', 'watana@vipersport.demo', 'วาทนา', 'วิ่งไว', '0812345003', True),
    ('piraya', 'piraya@vipersport.demo', 'พิรญา', 'แบดมินตัน', '0812345004', True),
    ('anan', 'anan@vipersport.demo', 'อานันท์', 'ฟิตเนส', '0812345005', True),
    ('naree', 'naree@vipersport.demo', 'นารี', 'ว่ายน้ำ', '0812345006', True),
    ('kittisak', 'kittisak@vipersport.demo', 'กิตติศักดิ์', 'บาสเกต', '0812345007', True),
    ('siriporn', 'siriporn@vipersport.demo', 'ศิริพร', 'จักรยาน', '0812345008', True),
    ('prasert', 'prasert@vipersport.demo', 'ประเสริฐ', 'ฟุตบอล', '0812345009', True),
    ('duangjai', 'duangjai@vipersport.demo', 'ดวงใจ', 'สมาชิกใหม่', '0812345010', False),
]

# (username, [(product_name, qty), ...], status, note)
DEMO_ORDERS = [
    ('somchai', [('ลูกฟุตบอลมาตรฐาน FIFA', 2), ('ถุงเท้าฟุตบอล 3 คู่', 1)], 'paid', 'รับที่หน้าร้านแล้ว'),
    ('malinee', [('รองเท้าวิ่ง Adidas Ultraboost', 1)], 'paid', ''),
    ('watana', [('ชุดวิ่งระบายอากาศ Dri-FIT', 1), ('กระเป๋าใส่น้ำวิ่ง 500ml', 1)], 'pending', 'รอชำระเงินสด'),
    ('piraya', [('ไม้แบดมินตัน Yonex Arcsaber', 1), ('ลูกขนไก่ 12 ลูก', 2)], 'paid', ''),
    ('anan', [('ดัมเบล 5 กก. (คู่)', 1), ('ยางยืดออกกำลังกาย Set 3 ระดับ', 1)], 'paid', ''),
    ('naree', [('ชุดว่ายน้ำกีฬา Speedo', 1), ('แว่นตาว่ายน้ำ Anti-Fog', 1)], 'paid', ''),
    ('kittisak', [('ลูกบาสเกตบอล Spalding TF', 1)], 'pending', ''),
    ('siriporn', [('หมวกกันน็อคจักรยาน Aero', 1)], 'paid', ''),
    ('prasert', [('รองเท้าฟุตบอล Nike Phantom', 1), ('ชุดฟุตบอลทีมชาติไทย', 1)], 'paid', ''),
]

# (username, [product names for favorites])
DEMO_FAVORITES = [
    ('somchai', ['ลูกฟุตบอลมาตรฐาน FIFA', 'รองเท้าฟุตบอล Nike Phantom', 'ชุดฟุตบอลทีมชาติไทย']),
    ('malinee', ['รองเท้าวิ่ง Adidas Ultraboost', 'นาฬิกาวิ่ง GPS Garmin']),
    ('watana', ['ชุดวิ่งระบายอากาศ Dri-FIT', 'กระเป๋าใส่น้ำวิ่ง 500ml']),
    ('piraya', ['ไม้แบดมินตัน Yonex Arcsaber', 'กระเป๋าใส่ไม้แบด 6 ช่อง']),
    ('anan', ['ดัมเบล 5 กก. (คู่)', 'เสื่อโยเกะหนา 6mm', 'เข็มขัดยกน้ำหนัก Leather']),
    ('naree', ['ชุดว่ายน้ำกีฬา Speedo', 'แว่นตาว่ายน้ำ Anti-Fog']),
    ('kittisak', ['ลูกบาสเกตบอล Spalding TF', 'รองเท้าบาส Nike Air Jordan']),
    ('siriporn', ['หมวกกันน็อคจักรยาน Aero']),
    ('prasert', ['ลูกฟุตบอลมาตรฐาน FIFA', 'ถุงเท้าฟุตบอล 3 คู่']),
    ('duangjai', ['ยางยืดออกกำลังกาย Set 3 ระดับ', 'เสื่อโยเกะหนา 6mm']),
]


class Command(BaseCommand):
    help = 'Seed demo data: categories, products, 10 members, orders, favorites, points'

    def handle(self, *args, **options):
        points_per_phone = getattr(settings, 'POINTS_PER_PHONE', 50)
        stats = {
            'products_new': 0,
            'members_new': 0,
            'favorites_new': 0,
            'orders_new': 0,
            'phone_logs_new': 0,
        }

        stats['products_new'] = self._seed_products()
        member_map, stats['members_new'] = self._seed_members(points_per_phone)
        stats['phone_logs_new'] = self._seed_phone_logs(member_map, points_per_phone)
        stats['favorites_new'] = self._seed_favorites(member_map)
        stats['orders_new'] = self._seed_orders(member_map)

        self.stdout.write(self.style.SUCCESS('=== Seed complete ==='))
        self.stdout.write(f"Products: {Product.objects.count()} (+{stats['products_new']} new)")
        self.stdout.write(f"Members: {MemberProfile.objects.count()} (+{stats['members_new']} new)")
        self.stdout.write(f"Favorites: {Favorite.objects.count()} (+{stats['favorites_new']} new)")
        self.stdout.write(f"Orders: {Order.objects.count()} (+{stats['orders_new']} new)")
        self.stdout.write(f"Phone logs: {PhonePointLog.objects.count()} (+{stats['phone_logs_new']} new)")
        self.stdout.write(self.style.WARNING(f'Demo password for all members: {DEMO_PASSWORD}'))

    def _seed_products(self):
        categories = [
            ('ฟุตบอล', 'football', 'ลูกบอล รองเท้า ชุดกีฬา'),
            ('วิ่ง', 'running', 'รองเท้าวิ่ง ชุดวิ่ง อุปกรณ์วิ่ง'),
            ('ฟิตเนส', 'fitness', 'ดัมเบล ยางยืด อุปกรณ์ยกน้ำหนัก'),
            ('แบดมินตัน', 'badminton', 'ไม้แบด ลูกขนไก่'),
            ('บาสเกตบอล', 'basketball', 'ลูกบาส รองเท้าบาส'),
            ('ว่ายน้ำ', 'swimming', 'ชุดว่ายน้ำ แว่นตา'),
            ('จักรยาน', 'cycling', 'หมวกกันน็อค อุปกรณ์จักรยาน'),
        ]
        for name, slug, desc in categories:
            Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})

        samples = [
            ('football', 'ลูกฟุตบอลมาตรฐาน FIFA', 'ลูกฟุตบอลคุณภาพสูง เหมาะสนามหญ้าและสนามเทียม', 890, 25),
            ('football', 'รองเท้าฟุตบอล Nike Phantom', 'รองเท้าสนามหญ้าเทียม น้ำหนักเบา ยึดเกาะดี', 2490, 15),
            ('football', 'ชุดฟุตบอลทีมชาติไทย', 'เสื้อ+กางเกง ผ้าระบายอากาศ ใส่สบาย', 590, 30),
            ('football', 'ถุงเท้าฟุตบอล 3 คู่', 'ถุงเท้ากันลื่น ซับเหงื่อ สำหรับฝึกซ้อม', 199, 50),
            ('running', 'รองเท้าวิ่ง Adidas Ultraboost', 'รองเท้าวิ่งซัพพอร์ต กันกระแทก ใส่ยาว', 3200, 12),
            ('running', 'ชุดวิ่งระบายอากาศ Dri-FIT', 'เสื้อกล้าม+กางเกงขาสั้น ผ้าเย็น', 650, 28),
            ('running', 'นาฬิกาวิ่ง GPS Garmin', 'วัดระยะ จังหวะหัวใจ กันน้ำ', 4590, 8),
            ('running', 'กระเป๋าใส่น้ำวิ่ง 500ml', 'กระเป๋าคาดเอว เบา ไม่กระเด้ง', 450, 35),
            ('fitness', 'ดัมเบล 5 กก. (คู่)', 'ดัมเบลเคลือบ จับถนัดมือ เหมาะเริ่มต้น', 450, 40),
            ('fitness', 'ยางยืดออกกำลังกาย Set 3 ระดับ', 'ยางลาเท็กซ์ 3 ความต้าน พกพาสะดวก', 299, 45),
            ('fitness', 'เสื่อโยเกะหนา 6mm', 'กันลื่น รองรับข้อต่อ มีสายรัด', 890, 22),
            ('fitness', 'เข็มขัดยกน้ำหนัก Leather', 'รองรับหลัง ปรับขนาดได้ มาตรฐานยก', 1200, 18),
            ('badminton', 'ไม้แบดมินตัน Yonex Arcsaber', 'ไม้คาร์บอน น้ำหนักเบา ส่งลูกแรง', 1890, 14),
            ('badminton', 'ลูกขนไก่ 12 ลูก', 'ลูกขนไก่มาตรฐานแข่งขัน ทนทาน', 350, 60),
            ('badminton', 'กระเป๋าใส่ไม้แบด 6 ช่อง', 'ใส่ไม้ 2 ด้าม ลูกขนไก่ รองเท้า', 750, 20),
            ('basketball', 'ลูกบาสเกตบอล Spalding TF', 'ลูกบาสมาตรฐาน indoor/outdoor', 1290, 16),
            ('basketball', 'รองเท้าบาส Nike Air Jordan', 'รองรับข้อเท้า กระโดดสูง ยึดเกาะดี', 2790, 10),
            ('swimming', 'ชุดว่ายน้ำกีฬา Speedo', 'ลดแรงต้านน้ำ แห้งเร็ว', 890, 24),
            ('swimming', 'แว่นตาว่ายน้ำ Anti-Fog', 'กันไอฝ้า ปรับสายได้', 350, 40),
            ('cycling', 'หมวกกันน็อคจักรยาน Aero', 'เบา ระบายอากาศ มาตรฐาน CE', 1150, 15),
        ]

        created = 0
        for slug, name, desc, price, stock in samples:
            cat = Category.objects.get(slug=slug)
            _, was_created = Product.objects.get_or_create(
                name=name,
                category=cat,
                defaults={
                    'description': desc,
                    'price': Decimal(str(price)),
                    'stock': stock,
                    'is_active': True,
                },
            )
            if was_created:
                created += 1
        return created

    def _seed_members(self, points_per_phone):
        member_map = {}
        created = 0
        for username, email, first, last, phone, verified in MEMBERS:
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first,
                    'last_name': last,
                },
            )
            if user_created:
                user.set_password(DEMO_PASSWORD)
                user.save()
                created += 1
            elif not user.has_usable_password():
                user.set_password(DEMO_PASSWORD)
                user.save()

            profile, _ = MemberProfile.objects.get_or_create(user=user)
            profile.phone = phone
            profile.phone_verified = verified
            profile.points = points_per_phone if verified else 0
            profile.save()
            member_map[username] = profile
        return member_map, created

    def _seed_phone_logs(self, member_map, points_per_phone):
        created = 0
        for username, _, _, _, phone, verified in MEMBERS:
            if not verified:
                continue
            profile = member_map[username]
            _, was_created = PhonePointLog.objects.get_or_create(
                phone=phone,
                defaults={
                    'member': profile,
                    'points_awarded': points_per_phone,
                },
            )
            if was_created:
                created += 1
        return created

    def _seed_favorites(self, member_map):
        created = 0
        for username, product_names in DEMO_FAVORITES:
            profile = member_map.get(username)
            if not profile:
                continue
            for pname in product_names:
                product = Product.objects.filter(name=pname).first()
                if not product:
                    continue
                _, was_created = Favorite.objects.get_or_create(
                    member=profile,
                    product=product,
                )
                if was_created:
                    created += 1
        return created

    def _seed_orders(self, member_map):
        created = 0
        for username, lines, status, note in DEMO_ORDERS:
            profile = member_map.get(username)
            if not profile:
                continue
            marker = f'[demo:{username}]'
            if Order.objects.filter(member=profile, note__startswith=marker).exists():
                continue

            order_total = Decimal('0')
            line_data = []
            for pname, qty in lines:
                product = Product.objects.filter(name=pname).first()
                if not product:
                    continue
                subtotal = product.price * qty
                order_total += subtotal
                line_data.append((product, qty))

            if not line_data:
                continue

            order_note = f'{marker} {note}'.strip() if note else marker
            order = Order.objects.create(
                member=profile,
                total=order_total,
                status=status,
                payment_method='cash',
                note=order_note,
            )
            for product, qty in line_data:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    unit_price=product.price,
                )
            created += 1
        return created
