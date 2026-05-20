from decimal import Decimal

from django.core.management.base import BaseCommand

from shop.models import Category, Product


class Command(BaseCommand):
    help = 'เพิ่มข้อมูลตัวอย่างสินค้าและหมวดหมู่'

    def handle(self, *args, **options):
        categories = [
            ('ฟุตบอล', 'football', 'ลูกบอล รองเท้า ชุดกีฬา'),
            ('วิ่ง', 'running', 'รองเท้าวิ่ง ชุดวิ่ง'),
            ('ฟิตเนส', 'fitness', 'ดัมเบล ยางยืด'),
            ('แบดมินตัน', 'badminton', 'ไม้แบด ลูกขนไก่'),
        ]
        for name, slug, desc in categories:
            Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})

        samples = [
            ('football', 'ลูกฟุตบอลมาตรฐาน FIFA', 'ลูกฟุตบอลคุณภาพสูง เหมาะสนามหญ้า', 890),
            ('football', 'รองเท้าฟุตบอล Nike', 'รองเท้าสนามหญ้าเทียม น้ำหนักเบา', 2490),
            ('running', 'รองเท้าวิ่ง Adidas', 'รองเท้าวิ่งซัพพอร์ต กันกระแทก', 3200),
            ('running', 'ชุดวิ่งระบายอากาศ', 'เสื้อกล้าม+กางเกง ผ้า Dri-FIT', 650),
            ('fitness', 'ดัมเบล 5 กก. (คู่)', 'ดัมเบลเคลือบ จับถนัดมือ', 450),
            ('fitness', 'ยางยืดออกกำลังกาย Set', '3 ระดับความต้าน', 299),
            ('badminton', 'ไม้แบดมินตัน Yonex', 'ไม้คาร์บอน น้ำหนักเบา', 1890),
            ('badminton', 'ลูกขนไก่ 12 ลูก', 'ลูกขนไก่มาตรฐานแข่งขัน', 350),
        ]
        for slug, name, desc, price in samples:
            cat = Category.objects.get(slug=slug)
            Product.objects.get_or_create(
                name=name,
                category=cat,
                defaults={
                    'description': desc,
                    'price': Decimal(str(price)),
                    'stock': 20,
                    'is_active': True,
                },
            )

        self.stdout.write(self.style.SUCCESS('Seed data completed.'))
