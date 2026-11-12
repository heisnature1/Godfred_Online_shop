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
    {"name": "Nike Air Max Sneakers", "category": "Footwear",
     "price": 350.00, "sale_price": 290.00, "stock": 25, "featured": True,
     "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&h=600&fit=crop&auto=format",
     "description": "Premium Nike Air Max sneakers with visible air cushioning. Iconic style for everyday wear."},
    {"name": "Adidas Ultraboost Sneakers", "category": "Footwear",
     "price": 420.00, "sale_price": 360.00, "stock": 20, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&h=600&fit=crop&auto=format",
     "description": "Adidas Ultraboost running shoes with responsive Boost midsole and Primeknit upper."},
    {"name": "Puma Suede Classic", "category": "Footwear",
     "price": 180.00, "sale_price": 145.00, "stock": 35, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1608235582875-48456174507e?w=600&h=600&fit=crop&auto=format",
     "description": "Timeless Puma Suede Classic sneakers with soft suede upper and gum rubber sole."},
    {"name": "New Balance Fresh Foam", "category": "Footwear",
     "price": 280.00, "sale_price": 230.00, "stock": 28, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1552346355-74f4948573c4?w=600&h=600&fit=crop&auto=format",
     "description": "New Balance Fresh Foam sneakers with plush cushioning for all-day comfort."},
    {"name": "Converse Chuck Taylor", "category": "Footwear",
     "price": 150.00, "sale_price": None, "stock": 45, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1560769061-2543b4652ef3?w=600&h=600&fit=crop&auto=format",
     "description": "Classic Converse Chuck Taylor All Star high-top sneakers. Canvas upper with rubber toe cap."},
    {"name": "Vans Old Skool", "category": "Footwear",
     "price": 160.00, "sale_price": 125.00, "stock": 40, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1537944121711-206e1a299bde?w=600&h=600&fit=crop&auto=format",
     "description": "Vans Old Skool skate sneakers with suede and canvas upper, signature side stripe."},
    {"name": "Air Jordan 1 High", "category": "Footwear",
     "price": 550.00, "sale_price": None, "stock": 15, "featured": True,
     "image_url": "https://images.unsplash.com/photo-1557152897-d24c395e590d?w=600&h=600&fit=crop&auto=format",
     "description": "Iconic Air Jordan 1 high-top sneakers with premium leather upper and Nike Air cushioning."},
    {"name": "Reebok Classic Leather", "category": "Footwear",
     "price": 170.00, "sale_price": 135.00, "stock": 30, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1606107650775-2238d744bb37?w=600&h=600&fit=crop&auto=format",
     "description": "Reebok Classic Leather sneakers with retro running style and comfortable EVA midsole."},
    {"name": "Fila Disruptor II", "category": "Footwear",
     "price": 140.00, "sale_price": 110.00, "stock": 35, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1592634274748-9085d6addc75?w=600&h=600&fit=crop&auto=format",
     "description": "Fila Disruptor II chunky sneakers with bold retro 90s design and thick platform sole."},
    {"name": "Asics Gel-Kayano", "category": "Footwear",
     "price": 320.00, "sale_price": 260.00, "stock": 22, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1543163522-672e10be3054?w=600&h=600&fit=crop&auto=format",
     "description": "Asics Gel-Kayano running shoes with GEL technology cushioning for superior comfort."},
    {"name": "Timberland 6-Inch Boots", "category": "Footwear",
     "price": 450.00, "sale_price": None, "stock": 18, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1605813943832-15b9ba69392a?w=600&h=600&fit=crop&auto=format",
     "description": "Timberland 6-Inch premium waterproof boots with rugged construction for outdoor wear."},
    {"name": "Dr. Martens 1460", "category": "Footwear",
     "price": 380.00, "sale_price": None, "stock": 20, "featured": False,
     "image_url": "https://images.unsplash.com/photo-1594753732849-62c6b87490b2?w=600&h=600&fit=crop&auto=format",
     "description": "Dr. Martens 1460 classic 8-eye boots with air-cushioned sole and durable leather upper."},
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
