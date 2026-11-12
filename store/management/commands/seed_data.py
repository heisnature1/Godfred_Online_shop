import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from store.models import Category, Product

CATEGORIES = [
    {"name": "Footwear", "icon": "fa-shoe-prints", "description": "Slippers, crocs, sneakers, and more footwear"},
]

PRODUCTS = [
    {"name": "Men's Leather Slippers", "category": "Footwear",
     "price": 120.00, "sale_price": 85.00, "stock": 40, "featured": True,
     "image_url": "https://images.unsplash.com/photo-1608375370149-2a809752903f?w=600&h=600&fit=crop&auto=format",
     "description": "Comfortable genuine leather slippers for men. Soft indoor sole, perfect for home and casual wear."},
    {"name": "Crocs Classic Clogs", "category": "Footwear",
     "price": 95.00, "sale_price": None, "stock": 60, "featured": True,
     "image_url": "https://images.unsplash.com/photo-1613757529256-2e12b9459216?w=600&h=600&fit=crop&auto=format",
     "description": "Lightweight, water-friendly clogs with ventilation ports. Easy to clean and all-day comfortable."},
    {"name": "Air Cushion Sneakers", "category": "Footwear",
     "price": 150.00, "sale_price": 115.00, "stock": 50, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&h=600&fit=crop&auto=format",
     "description": "Trendy air-cushion sneakers with breathable mesh upper. Ideal for walking and daily comfort."},
    {"name": "Running Sneakers", "category": "Footwear",
     "price": 190.00, "sale_price": 155.00, "stock": 35, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1552346355-74f4948573c4?w=600&h=600&fit=crop&auto=format",
     "description": "Performance running sneakers with responsive foam midsole and durable rubber outsole."},
    {"name": "Leather Chelsea Boots", "category": "Footwear",
     "price": 250.00, "sale_price": None, "stock": 25, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1608375370149-2a809752903f?w=600&h=600&fit=crop&auto=format",
     "description": "Classic men's leather Chelsea boots with elastic side panels. Smart-casual and versatile."},
    {"name": "Suede Loafers", "category": "Footwear",
     "price": 180.00, "sale_price": 140.00, "stock": 30, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1604232762778-f12e99c799c4?w=600&h=600&fit=crop&auto=format",
     "description": "Soft suede loafers for men. Slip-on design with padded insole. Great for office and outings."},
    {"name": "Canvas Sneakers", "category": "Footwear",
     "price": 110.00, "sale_price": 85.00, "stock": 45, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1515967688168-f404f3911752?w=600&h=600&fit=crop&auto=format",
     "description": "Classic canvas sneakers with rubber sole. Lightweight and easy to pair with any casual outfit."},
    {"name": "Women's Flat Slippers", "category": "Footwear",
     "price": 90.00, "sale_price": 65.00, "stock": 55, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1543163625-97fbe7b44b65?w=600&h=600&fit=crop&auto=format",
     "description": "Elegant flat slippers for women with cushioned insole. Perfect for everyday comfort and style."},
    {"name": "Sports Running Shoes", "category": "Footwear",
     "price": 220.00, "sale_price": 180.00, "stock": 30, "featured": True,
     "image_url": "https://images.unsplash.com/photo-1595104327081-41853717dbdd?w=600&h=600&fit=crop&auto=format",
     "description": "Breathable sports running shoes with shock-absorbing sole. Built for training and daily runs."},
]


class Command(BaseCommand):
    help = "Seed the database with sample data for Godfred's Fashion Shop"

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-demo-user',
            action='store_true',
            help='Do not create the predictable local demo account.',
        )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Seeding database...'))

        admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        demo_password = os.environ.get('DJANGO_DEMO_PASSWORD')
        if (
            not settings.DEBUG
            and not User.objects.filter(username='super_admin').exists()
            and not admin_password
        ):
            raise CommandError(
                'Set DJANGO_SUPERUSER_PASSWORD before creating the production admin account.'
            )
        if (
            not kwargs['skip_demo_user']
            and not settings.DEBUG
            and not User.objects.filter(username='demo').exists()
            and not demo_password
        ):
            raise CommandError(
                'Set DJANGO_DEMO_PASSWORD before creating the production demo account.'
            )

        if not User.objects.filter(username='super_admin').exists():
            admin_password = admin_password or 'Aer!x1s#SuperAdm!n_2025'
            User.objects.create_superuser('super_admin', 'admin@shopnow.com', admin_password)
            self.stdout.write(self.style.SUCCESS('+ Superuser: super_admin created.'))

        if not kwargs['skip_demo_user'] and not User.objects.filter(username='demo').exists():
            demo_password = demo_password or 'ShopNow#DemoUser!2025'
            demo = User.objects.create_user(
                username='demo', email='demo@shopnow.com',
                password=demo_password, first_name='Kwame', last_name='Mensah'
            )
            demo.profile.phone = '0244123456'
            demo.profile.city = 'Accra'
            demo.profile.address = '12 Independence Ave, Accra'
            demo.profile.save()
            self.stdout.write(self.style.SUCCESS('+ Demo user: demo created.'))

        cat_map = {}
        for c in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                name=c['name'],
                defaults={'icon': c['icon'], 'description': c['description']}
            )
            cat_map[c['name']] = cat
            if created:
                self.stdout.write(f'  + Category: {cat.name}')

        for p in PRODUCTS:
            if not Product.objects.filter(name=p['name']).exists():
                Product.objects.create(
                    name=p['name'], category=cat_map[p['category']],
                    price=p['price'], sale_price=p['sale_price'],
                    stock=p['stock'], is_featured=p['featured'],
                    is_active=True, image_url=p['image_url'],
                    description=p['description'],
                )
                self.stdout.write(f'  + Product: {p["name"]}')

        self.stdout.write(self.style.SUCCESS('\nSeeded sample data successfully.'))
