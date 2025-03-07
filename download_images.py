import os
import urllib.request
import ssl

# Create the images directory if it doesn't exist
os.makedirs('app/static/images', exist_ok=True)

# Disable SSL certificate verification (not recommended for production)
ssl._create_default_https_context = ssl._create_unverified_context

# List of image files we need with their URLs
image_files = [
    # Men's products
    ('men_tshirt.jpg', 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=600&auto=format&fit=crop'),
    ('men_jeans.jpg', 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=600&auto=format&fit=crop'),
    ('men_shirt.jpg', 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&auto=format&fit=crop'),
    ('men_blazer.jpg', 'https://images.unsplash.com/photo-1593032465175-481ac7f401a0?w=600&auto=format&fit=crop'),
    
    # Women's products
    ('women_dress.jpg', 'https://images.unsplash.com/photo-1612336307429-8a898d10e223?w=600&auto=format&fit=crop'),
    ('women_jeans.jpg', 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600&auto=format&fit=crop'),
    ('women_blouse.jpg', 'https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=600&auto=format&fit=crop'),
    ('women_cardigan.jpg', 'https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=600&auto=format&fit=crop'),
    
    # Kids' products
    ('kids_tshirt.jpg', 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=600&auto=format&fit=crop'),
    ('kids_jeans.jpg', 'https://images.unsplash.com/photo-1519278409-1f56fdda7fe5?w=600&auto=format&fit=crop'),
    ('kids_dress.jpg', 'https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=600&auto=format&fit=crop'),
    ('kids_hoodie.jpg', 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=600&auto=format&fit=crop'),
    
    # Other images
    ('hero-bg.jpg', 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=1200&auto=format&fit=crop'),
    ('about-banner.jpg', 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=1200&auto=format&fit=crop')
]

# Download images
for image_file, url in image_files:
    try:
        print(f"Downloading {image_file}...")
        urllib.request.urlretrieve(url, f"app/static/images/{image_file}")
        print(f"Successfully downloaded {image_file}")
    except Exception as e:
        print(f"Error downloading {image_file}: {e}")

print("Image download process completed!") 