import urllib.request

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from shop.models import Product

# รูปกีฬาเฉพาะทางจาก Pexels / Unsplash (ใช้ในโปรเจกตเรียน)
PRODUCT_IMAGE_URLS = {
    'ลูกฟุตบอลมาตรฐาน FIFA': [
        'https://images.pexels.com/photos/1618269/pexels-photo-1618269.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'รองเท้าฟุตบอล Nike Phantom': [
        'https://images.pexels.com/photos/1904838/pexels-photo-1904838.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.pexels.com/photos/2526878/pexels-photo-2526878.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'ชุดฟุตบอลทีมชาติไทย': [
        'https://images.pexels.com/photos/3621104/pexels-photo-3621104.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=600&q=80',
    ],
    'ถุงเท้าฟุตบอล 3 คู่': [
        'https://images.pexels.com/photos/4348078/pexels-photo-4348078.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'รองเท้าวิ่ง Adidas Ultraboost': [
        'https://images.pexels.com/photos/190330/pexels-photo-190330.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80',
    ],
    'ชุดวิ่งระบายอากาศ Dri-FIT': [
        'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&q=80',
        'https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'นาฬิกาวิ่ง GPS Garmin': [
        'https://images.pexels.com/photos/4377792/pexels-photo-4377792.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80',
    ],
    'กระเป๋าใส่น้ำวิ่ง 500ml': [
        'https://images.pexels.com/photos/416528/pexels-photo-416528.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&q=80',
    ],
    'ดัมเบล 5 กก. (คู่)': [
        'https://images.pexels.com/photos/703012/pexels-photo-703012.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.pexels.com/photos/416778/pexels-photo-416778.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'ยางยืดออกกำลังกาย Set 3 ระดับ': [
        'https://images.pexels.com/photos/416476/pexels-photo-416476.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'เสื่อโยเกะหนา 6mm': [
        'https://images.pexels.com/photos/317155/pexels-photo-317155.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'เข็มขัดยกน้ำหนัก Leather': [
        'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80',
        'https://images.pexels.com/photos/416476/pexels-photo-416476.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'ไม้แบดมินตัน Yonex Arcsaber': [
        'https://images.pexels.com/photos/6552194/pexels-photo-6552194.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.pexels.com/photos/3601094/pexels-photo-3601094.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'ลูกขนไก่ 12 ลูก': [
        'https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?w=600&q=80',
    ],
    'กระเป๋าใส่ไม้แบด 6 ช่อง': [
        'https://images.pexels.com/photos/2906755/pexels-photo-2906755.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&q=80',
    ],
    'ลูกบาสเกตบอล Spalding TF': [
        'https://images.pexels.com/photos/1752757/pexels-photo-1752757.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=600&q=80',
    ],
    'รองเท้าบาส Nike Air Jordan': [
        'https://images.pexels.com/photos/17817175/pexels-photo-17817175.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'ชุดว่ายน้ำกีฬา Speedo': [
        'https://images.pexels.com/photos/261375/pexels-photo-261375.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.unsplash.com/photo-1530549387789-4c1017266635?w=600&q=80',
    ],
    'แว่นตาว่ายน้ำ Anti-Fog': [
        'https://images.unsplash.com/photo-1519315901367-f34ff9154487?w=600&q=80',
        'https://images.pexels.com/photos/1263349/pexels-photo-1263349.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
    'หมวกกันน็อคจักรยาน Aero': [
        'https://images.pexels.com/photos/11498209/pexels-photo-11498209.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.pexels.com/photos/100582/pexels-photo-100582.jpeg?auto=compress&cs=tinysrgb&w=600',
    ],
}


def download_image(urls: list[str]) -> bytes:
    last_error = None
    for url in urls:
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'ViperSport-Seed/1.0'},
            )
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.read()
        except Exception as exc:
            last_error = exc
    raise last_error or RuntimeError('No URLs provided')


class Command(BaseCommand):
    help = 'Download sport-specific product images (Pexels/Unsplash)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Re-download even if image exists',
        )

    def handle(self, *args, **options):
        force = options['force']
        updated = 0
        skipped = 0
        failed = 0

        for product in Product.objects.all():
            if product.image and not force:
                skipped += 1
                continue

            urls = PRODUCT_IMAGE_URLS.get(product.name)
            if not urls:
                self.stdout.write(self.style.WARNING(f'No mapping for id={product.pk}'))
                failed += 1
                continue

            try:
                data = download_image(urls)
                filename = f'product-{product.pk}.jpg'
                if product.image:
                    product.image.delete(save=False)
                product.image.save(filename, ContentFile(data), save=True)
                updated += 1
            except Exception as exc:
                failed += 1
                self.stdout.write(self.style.ERROR(f'FAIL id={product.pk}: {exc}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'Done: {updated} sport images, {skipped} skipped, {failed} failed.'
            )
        )
