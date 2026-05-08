import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from shop.models import Category, Product

User = get_user_model()

CATEGORY_NAMES = [
    "Elektronika",
    "Məişət texnikası",
    "Geyim",
    "Ayaqqabı",
    "Kitab",
    "İdman",
    "Oyuncaqlar",
    "Mebel",
    "Bağ və təsərrüfat",
    "Avtomobil aksesuarları",
    "Kosmetika",
    "Ofis ləvazimatı",
    "Musiqi alətləri",
    "Telefon aksesuarları",
    "Ev tekstili",
    "Mətbəx ləvazimatı",
    "İçkilər və qida",
    "Hədiyyə",
    "Təhlükəsizlik",
    "Tikinti materialları",
]

PRODUCT_PREFIXES = [
    "Premium",
    "Klassik",
    "Smart",
    "Eco",
    "Pro",
    "Mini",
    "Ultra",
    "Comfort",
    "Deluxe",
    "Start",
]


class Command(BaseCommand):
    help = "Admin superuser, nümunə istifadəçilər, kateqoriyalar və məhsullar yaradır."

    def handle(self, *args, **options):
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "first_name": "Super",
                "last_name": "Admin",
                "phone_number": "+994501112233",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin_user.set_password("123123")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS("Superuser OK: admin / 123123"))

        for i in range(1, 31):
            u, _ = User.objects.get_or_create(
                username=f"user{i}",
                defaults={
                    "email": f"user{i}@example.com",
                    "first_name": f"Ad{i}",
                    "last_name": f"Soyad{i}",
                    "phone_number": f"+99450{100000 + i}",
                },
            )
            if not u.has_usable_password():
                u.set_password("demo12345")
                u.save()

        categories = []
        for name in CATEGORY_NAMES:
            slug = slugify(name)[:220]
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": f"{name} kateqoriyası üzrə məhsullar.",
                },
            )
            categories.append(cat)

        if not categories:
            self.stdout.write(self.style.WARNING("Kateqoriya yoxdur."))
            return

        target_count = 180
        existing = Product.objects.count()
        to_create = max(0, target_count - existing)
        users = list(User.objects.filter(is_superuser=False))

        for n in range(to_create):
            cat = random.choice(categories)
            prefix = random.choice(PRODUCT_PREFIXES)
            base_name = f"{prefix} {cat.name} məhsulu {existing + n + 1}"
            sku = f"SKU-{existing + n + 1:05d}"
            if Product.objects.filter(sku=sku).exists():
                continue
            slug_base = slugify(base_name)[:250] or f"mehsul-{n}"
            slug = slug_base
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{slug_base}-{counter}"
                counter += 1

            author = random.choice(users) if users else admin_user
            Product.objects.create(
                name=base_name[:255],
                slug=slug[:280],
                description=f"Təsvir: {base_name}. Keyfiyyətli məhsul.",
                price=Decimal(random.randint(5, 2500)) + Decimal(random.randint(0, 99)) / 100,
                stock=random.randint(0, 500),
                sku=sku,
                is_active=True,
                category=cat,
                created_by=author,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Categories: %s, products: %s, users: %s"
                % (
                    Category.objects.count(),
                    Product.objects.count(),
                    User.objects.count(),
                )
            )
        )
