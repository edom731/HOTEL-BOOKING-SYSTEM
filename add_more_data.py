import os, django, urllib.request
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_project.settings')
django.setup()

from hotels.models import City, Hotel, Room, HotelImage
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

try:
    owner = User.objects.get(username='owner1')
except Exception as e:
    print("Error fetching owner1. Make sure to run python manage.py createsuperuser with username 'owner1' first.")
    exit(1)

# Ensure cities exist
cities_data = ['Addis Ababa', 'Hawassa', 'Bahir Dar', 'Gondar', 'Lalibela', 'Dire Dawa']
city_objs = {}
for c_name in cities_data:
    city_objs[c_name], _ = City.objects.get_or_create(name=c_name, defaults={'description': f'Beautiful city of {c_name}'})

new_hotels_data = [
    {
        'name': 'Skylight Hotel',
        'city': city_objs['Addis Ababa'],
        'address': 'Bole International Airport, Addis Ababa',
        'description': 'Ethiopian Skylight Hotel offers unparalleled luxury right next to the airport. It features massive swimming pools, numerous restaurants offering global cuisines, and state-of-the-art facilities.',
        'star_rating': 5, 'price_per_night': 5000,
        'amenities': 'WiFi, Large Pool, Gym, Multiple Restaurants, Bar, Airport Shuttle, Spa',
        'phone': '+251 11 681 8181', 'email': 'info@skylighthotel.com',
        'thumbnail_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    },
    {
        'name': 'Golden Tulip Addis Ababa',
        'city': city_objs['Addis Ababa'],
        'address': 'Cameroon Street, Bole, Addis Ababa',
        'description': 'An upscale international hotel offering modern comfort, excellent dining options, and a vibrant atmosphere in the popular Bole district.',
        'star_rating': 4, 'price_per_night': 3500,
        'amenities': 'WiFi, Gym, Restaurant, Bar, Room Service, Parking',
        'phone': '+251 11 617 0740', 'email': 'info@goldentulipaddis.com',
        'thumbnail_url': 'https://images.unsplash.com/photo-1522798514-97ceb8c4f1c8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    },
    {
        'name': 'South Star International Hotel',
        'city': city_objs['Hawassa'],
        'address': 'Main Road, Hawassa',
        'description': 'One of the best hotels in Hawassa, offering excellent service, modern rooms, and a large swimming pool. A perfect getaway spot.',
        'star_rating': 4, 'price_per_night': 2500,
        'amenities': 'WiFi, Pool, Restaurant, Bar, Conference Center, Garden',
        'phone': '+251 46 220 7777', 'email': 'info@southstarhotel.com',
        'thumbnail_url': 'https://images.unsplash.com/photo-1549294413-26f195200c16?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    },
    {
        'name': 'Jacaranda Hotel',
        'city': city_objs['Bahir Dar'],
        'address': 'City Center, Bahir Dar',
        'description': 'A beautiful modern hotel in Bahir Dar featuring a rooftop restaurant with panoramic views of Lake Tana and the city.',
        'star_rating': 4, 'price_per_night': 2000,
        'amenities': 'WiFi, Rooftop Restaurant, Bar, Tour Desk, Parking',
        'phone': '+251 58 226 5555', 'email': 'info@jacarandahotel.com',
        'thumbnail_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    },
    {
        'name': 'Goha Hotel',
        'city': city_objs['Gondar'],
        'address': 'Hilltop, Gondar',
        'description': 'Perched on a hill overlooking the historic castles of Gondar, Goha Hotel offers breathtaking views, traditional architecture, and a serene environment.',
        'star_rating': 3, 'price_per_night': 1800,
        'amenities': 'WiFi, Pool, Restaurant, Bar, Panoramic Views, Cultural Shows',
        'phone': '+251 58 111 0634', 'email': 'info@gohahotel.com',
        'thumbnail_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    },
    {
        'name': 'Maribela Hotel',
        'city': city_objs['Lalibela'],
        'address': 'Main Street, Lalibela',
        'description': 'Designed in the style of the famous rock-hewn churches, Maribela provides a luxurious and comfortable stay with stunning views of the Ethiopian highlands.',
        'star_rating': 4, 'price_per_night': 2200,
        'amenities': 'WiFi, Restaurant, Bar, Balcony Views, Traditional Coffee Ceremony',
        'phone': '+251 33 336 0335', 'email': 'info@hotelmaribela.com',
        'thumbnail_url': 'https://images.unsplash.com/photo-1542314831-c6a4d4598eb7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    },
    {
        'name': 'Samrat Hotel',
        'city': city_objs['Dire Dawa'],
        'address': 'Kebele 02, Dire Dawa',
        'description': 'A comfortable and modern stay in the warm city of Dire Dawa. Enjoy great local hospitality, a relaxing atmosphere, and easy access to the city center.',
        'star_rating': 3, 'price_per_night': 1500,
        'amenities': 'WiFi, Restaurant, Air Conditioning, Parking',
        'phone': '+251 25 111 2233', 'email': 'info@samrathotel.com',
        'thumbnail_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    }
]

room_templates = [
    ('single', '101', 1),
    ('double', '201', 2),
    ('suite', '301', 4),
]
multipliers = {'single': 0.6, 'double': 1.0, 'suite': 2.5}

def download_image(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        return ContentFile(response.read())
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

print("Adding new hotels and updating existing ones...")
for h in new_hotels_data:
    hotel, created = Hotel.objects.get_or_create(
        name=h['name'],
        defaults={
            'city': h['city'], 'address': h['address'],
            'description': h['description'], 'star_rating': h['star_rating'],
            'price_per_night': h['price_per_night'], 'amenities': h['amenities'],
            'phone': h['phone'], 'email': h['email'],
            'owner': owner, 'is_active': True,
        }
    )
    if created:
        print(f"Created {hotel.name}, setting up rooms...")
        for rtype, rnum, cap in room_templates:
            Room.objects.get_or_create(
                hotel=hotel, room_number=rnum,
                defaults={
                    'room_type': rtype,
                    'price_per_night': round(h['price_per_night'] * multipliers[rtype], -2),
                    'capacity': cap,
                    'description': f'Comfortable {rtype} room.',
                    'is_available': True,
                }
            )

gallery_urls = [
    'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
    'https://images.unsplash.com/photo-1560067174-c5a3a8f37060?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
    'https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
]

default_thumbnail = 'https://images.unsplash.com/photo-1551882547-ff40c0d5bf8f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'

print("Checking for missing images on all hotels...")
all_hotels = Hotel.objects.all()
for hotel in all_hotels:
    # Ensure thumbnail exists
    if not hotel.thumbnail:
        print(f"Downloading missing thumbnail for {hotel.name}...")
        # Try to find a specific thumbnail from our data
        thumb_url = default_thumbnail
        for hd in new_hotels_data:
            if hd['name'] == hotel.name:
                thumb_url = hd['thumbnail_url']
                break
        
        img_content = download_image(thumb_url)
        if img_content:
            hotel.thumbnail.save(f"hotel_{hotel.id}_thumb.jpg", img_content, save=True)

    # Ensure gallery images exist
    if hotel.images.count() < 3:
        print(f"Adding gallery images for {hotel.name}...")
        for i, url in enumerate(gallery_urls):
            if hotel.images.count() >= 3:
                break
            content = download_image(url)
            if content:
                img = HotelImage(hotel=hotel, caption=f"Interior View {i+1}")
                img.image.save(f"gallery_{hotel.id}_{i}.jpg", content, save=True)

print("Done adding hotels and images!")
