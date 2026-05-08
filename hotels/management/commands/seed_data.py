from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hotels.models import City, Hotel, Room
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Seed the database with sample Ethiopian hotel data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Cities
        cities_data = [
            ('Addis Ababa', 'The capital and largest city of Ethiopia'),
            ('Bahir Dar', 'A city on the southern shore of Lake Tana'),
            ('Gondar', 'Historic city known for its medieval castles'),
            ('Hawassa', 'Capital of the Sidama Region, on Lake Hawassa'),
            ('Dire Dawa', 'Second largest city in Ethiopia'),
            ('Mekelle', 'Capital of the Tigray Region'),
        ]
        cities = {}
        for name, desc in cities_data:
            city, _ = City.objects.get_or_create(name=name, defaults={'description': desc})
            cities[name] = city
        self.stdout.write(f'  [OK] {len(cities)} cities created')

        # Admin user
        admin, created = User.objects.get_or_create(username='admin', defaults={
            'email': 'admin@ethiostay.et', 'first_name': 'Admin', 'last_name': 'EthioStay',
            'is_staff': True, 'is_superuser': True
        })
        if created:
            admin.set_password('admin123')
            admin.save()
            UserProfile.objects.get_or_create(user=admin, defaults={'role': 'admin', 'phone': '+251 11 000 0001'})

        # Owner user
        owner, created = User.objects.get_or_create(username='owner1', defaults={
            'email': 'owner@ethiostay.et', 'first_name': 'Abebe', 'last_name': 'Girma'
        })
        if created:
            owner.set_password('owner123')
            owner.save()
            UserProfile.objects.get_or_create(user=owner, defaults={'role': 'hotel_owner', 'phone': '+251 91 234 5678'})

        # Customer user
        customer, created = User.objects.get_or_create(username='customer1', defaults={
            'email': 'customer@example.com', 'first_name': 'Tigist', 'last_name': 'Bekele'
        })
        if created:
            customer.set_password('customer123')
            customer.save()
            UserProfile.objects.get_or_create(user=customer, defaults={'role': 'customer', 'phone': '+251 91 987 6543'})

        self.stdout.write('  [OK] 3 users created')

        # Hotels
        hotels_data = [
            {
                'name': 'Sheraton Addis',
                'city': 'Addis Ababa',
                'address': 'Taitu Street, Addis Ababa',
                'description': 'The Sheraton Addis is a luxurious 5-star hotel in the heart of Addis Ababa. Featuring world-class amenities, stunning gardens, multiple restaurants, and a rooftop pool with panoramic city views.',
                'star_rating': 5, 'price_per_night': 4500,
                'amenities': 'WiFi, Pool, Gym, Spa, Restaurant, Bar, Room Service, Parking, Airport Shuttle',
                'phone': '+251 11 517 1717', 'email': 'info@sheraton-addis.com',
            },
            {
                'name': 'Radisson Blu Addis Ababa',
                'city': 'Addis Ababa',
                'address': 'Bole Road, Addis Ababa',
                'description': 'Modern luxury hotel near Bole International Airport. Offers contemporary rooms, outdoor pool, fitness center, and multiple dining options with stunning city views.',
                'star_rating': 5, 'price_per_night': 4200,
                'amenities': 'WiFi, Pool, Gym, Restaurant, Bar, Business Center, Parking, Spa',
                'phone': '+251 11 515 1515', 'email': 'info@radissonblu-addis.com',
            },
            {
                'name': 'Kuriftu Resort Bahir Dar',
                'city': 'Bahir Dar',
                'address': 'Lake Tana Shore, Bahir Dar',
                'description': 'A beautiful lakeside resort on the shores of Lake Tana, source of the Blue Nile. Enjoy stunning lake views, traditional architecture, boat trips to ancient island monasteries.',
                'star_rating': 4, 'price_per_night': 2800,
                'amenities': 'WiFi, Pool, Lake View, Restaurant, Bar, Boat Tours, Spa, Garden',
                'phone': '+251 58 220 3030', 'email': 'info@kuriftu-bahirdar.com',
            },
            {
                'name': 'Goha Hotel Gondar',
                'city': 'Gondar',
                'address': 'Hillside, Gondar',
                'description': 'Perched on a hill overlooking the historic Royal Enclosure. Goha Hotel offers breathtaking views of Gondar medieval castles and combines traditional Ethiopian style with modern comfort.',
                'star_rating': 4, 'price_per_night': 2200,
                'amenities': 'WiFi, Pool, Restaurant, Bar, Castle View, Garden, Parking',
                'phone': '+251 58 111 2222', 'email': 'info@gohahotel.com',
            },
            {
                'name': 'Haile Resort Hawassa',
                'city': 'Hawassa',
                'address': 'Lake Hawassa Road, Hawassa',
                'description': 'A premier resort on the shores of beautiful Lake Hawassa. Features spacious rooms, lush gardens, lake views, water sports, and a world-class spa.',
                'star_rating': 5, 'price_per_night': 3500,
                'amenities': 'WiFi, Pool, Spa, Lake View, Water Sports, Restaurant, Bar, Gym, Parking',
                'phone': '+251 46 212 3456', 'email': 'info@haileresort.com',
            },
            {
                'name': 'Rift Valley Hotel Hawassa',
                'city': 'Hawassa',
                'address': 'Hawassa Promenade, Hawassa',
                'description': 'Comfortable hotel with stunning Rift Valley lake views. Ideal for travelers exploring southern Ethiopia. Features cozy rooms, lakeside restaurant serving fresh tilapia.',
                'star_rating': 3, 'price_per_night': 1500,
                'amenities': 'WiFi, Restaurant, Lake View, Garden, Parking',
                'phone': '+251 46 215 6789', 'email': 'info@riftvalleyhotel.com',
            },
            {
                'name': 'Dire Dawa Business Hotel',
                'city': 'Dire Dawa',
                'address': 'Kezira District, Dire Dawa',
                'description': 'Modern business hotel in the heart of Dire Dawa. Perfect for business travelers with conference facilities, reliable WiFi, and easy access to the railway station.',
                'star_rating': 3, 'price_per_night': 1800,
                'amenities': 'WiFi, Restaurant, Conference Room, Parking, Airport Shuttle',
                'phone': '+251 25 111 3333', 'email': 'info@ddhotel.com',
            },
            {
                'name': 'Axum Hotel Mekelle',
                'city': 'Mekelle',
                'address': 'Central Mekelle, Tigray',
                'description': 'A welcoming hotel in the heart of Mekelle, gateway to the ancient ruins of Aksum and Lalibela. Features comfortable rooms with Tigrayan decor and a rooftop restaurant.',
                'star_rating': 3, 'price_per_night': 1600,
                'amenities': 'WiFi, Restaurant, Rooftop Terrace, Tour Desk, Parking',
                'phone': '+251 34 412 1111', 'email': 'info@axumhotel.com',
            },
        ]

        room_templates = [
            ('single', '101', 1),
            ('single', '102', 1),
            ('double', '201', 2),
            ('double', '202', 2),
            ('twin', '203', 2),
            ('suite', '301', 4),
            ('deluxe', '401', 3),
            ('family', '501', 5),
        ]
        multipliers = {'single': 0.6, 'double': 1.0, 'twin': 1.0, 'suite': 2.5, 'deluxe': 1.8, 'family': 2.0}

        for h in hotels_data:
            hotel, created = Hotel.objects.get_or_create(
                name=h['name'],
                defaults={
                    'city': cities[h['city']], 'address': h['address'],
                    'description': h['description'], 'star_rating': h['star_rating'],
                    'price_per_night': h['price_per_night'], 'amenities': h['amenities'],
                    'phone': h['phone'], 'email': h['email'],
                    'owner': owner, 'is_active': True,
                }
            )
            if created:
                for rtype, rnum, cap in room_templates:
                    Room.objects.get_or_create(
                        hotel=hotel, room_number=rnum,
                        defaults={
                            'room_type': rtype,
                            'price_per_night': round(h['price_per_night'] * multipliers[rtype], -2),
                            'capacity': cap,
                            'description': f'Comfortable {rtype} room with modern amenities.',
                            'is_available': True,
                        }
                    )

        self.stdout.write(f'  [OK] {len(hotels_data)} hotels with rooms created')
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('Login credentials:')
        self.stdout.write('  Admin:    username=admin      password=admin123')
        self.stdout.write('  Owner:    username=owner1     password=owner123')
        self.stdout.write('  Customer: username=customer1  password=customer123')
