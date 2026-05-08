import os
import django
import urllib.request
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_project.settings')
django.setup()

from hotels.models import Hotel, HotelImage
from django.core.files.base import ContentFile

# A pool of guaranteed working Unsplash hotel images
working_urls = [
    'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1522798514-97ceb8c4f1c8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1549294413-26f195200c16?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
    'https://images.unsplash.com/photo-1560067174-c5a3a8f37060?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
    'https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
]

def download_image(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        return ContentFile(response.read())
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

print("Checking for missing images on all hotels...")
all_hotels = Hotel.objects.all()
for hotel in all_hotels:
    # Check Thumbnail
    if not hotel.thumbnail:
        print(f"Downloading missing thumbnail for {hotel.name}...")
        url = random.choice(working_urls)
        img_content = download_image(url)
        if img_content:
            hotel.thumbnail.save(f"hotel_{hotel.id}_thumb.jpg", img_content, save=True)
            print(f"-> Saved thumbnail for {hotel.name}")

    # Check Gallery
    current_images = hotel.images.count()
    if current_images < 3:
        print(f"Adding {3 - current_images} missing gallery images for {hotel.name}...")
        for i in range(current_images, 3):
            url = random.choice(working_urls)
            content = download_image(url)
            if content:
                img = HotelImage(hotel=hotel, caption=f"Interior View {i+1}")
                img.image.save(f"gallery_{hotel.id}_{i}.jpg", content, save=True)
                print(f"-> Saved gallery image {i+1} for {hotel.name}")

print("Successfully fixed all missing images!")
