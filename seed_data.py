"""
Do'konga 15 ta yangi sifatli mahsulotlarni kiritish skripti.
"""
from app.db.session import SessionLocal, init_db
from app.models.entities import Product

SAMPLE_PRODUCTS = [
    {
        "name": "Nike Air Zoom Pegasus Ko'k Krossovka",
        "category": "poyabzal",
        "color": "ko'k",
        "price": 120.0,
        "description": "Erkaklar va ayollar uchun qulay sport yugurish krossovkasi. Moviy va ko'k rang uyg'unligi.",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600",
        "tags": "poyabzal, krossovka, ko'k, sport, nike, yugurish"
    },
    {
        "name": "Adidas Ultraboost Qora Krossovka",
        "category": "poyabzal",
        "color": "qora",
        "price": 150.0,
        "description": "Kundalik kiyish uchun qora sport krossovkasi, amortizatsiyali qulay taglik bilan.",
        "image_url": "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?w=600",
        "tags": "poyabzal, krossovka, qora, sport, adidas, yengil"
    },
    {
        "name": "Klassik Qora Charm Tufli",
        "category": "poyabzal",
        "color": "qora",
        "price": 85.0,
        "description": "Erkaklar uchun rasmiy klassik qora tabiiy charm tufli, kostyumlar uchun ideal.",
        "image_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=600",
        "tags": "poyabzal, tufli, qora, charm, klassik, erkaklar, rasmiy"
    },
    {
        "name": "Puma White Star Oq Krossovka",
        "category": "poyabzal",
        "color": "oq",
        "price": 95.0,
        "description": "Zamonaviy shahar uslubidagi oq krossovka, har qanday kiyimga mos keladi.",
        "image_url": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=600",
        "tags": "poyabzal, krossovka, oq, puma, kundalik, sport"
    },
    {
        "name": "Oq Paxtali Erkaklar Futbolkasi",
        "category": "kiyim",
        "color": "oq",
        "price": 25.0,
        "description": "100% paxtadan tayyorlangan yozgi nafas oluvchi qulay oq futbolka.",
        "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600",
        "tags": "kiyim, futbolka, oq, paxta, yozgi, asosiy"
    },
    {
        "name": "Ko'k Jinsi Kurtka (Denim)",
        "category": "kiyim",
        "color": "ko'k",
        "price": 65.0,
        "description": "Klassik ko'k rangli jinsi kurtka, qalin sifatli paxta denim matosi.",
        "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=600",
        "tags": "kiyim, kurtka, jinsi, ko'k, denim, bahorgi"
    },
    {
        "name": "Qizil Yozgi Ayollar Ko'ylagi",
        "category": "kiyim",
        "color": "qizil",
        "price": 55.0,
        "description": "Yengil va nafis qizil ipak ko'ylak, tantanalar va yozgi sayrlar uchun.",
        "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600",
        "tags": "kiyim, koylak, ayollar, qizil, yozgi, nafis"
    },
    {
        "name": "Sariq Qishki Issiq Kurtka (Puffer)",
        "category": "kiyim",
        "color": "sariq",
        "price": 110.0,
        "description": "Yorqin sariq rangli, sovuq va shamoldan himoyalovchi zamonaviy qishki kurtka.",
        "image_url": "https://images.unsplash.com/photo-1544923246-77307dd654cb?w=600",
        "tags": "kiyim, kurtka, sariq, qishki, issiq, puffer"
    },
    {
        "name": "Klassik Bej Rangli Kuzgi Trench Palto",
        "category": "kiyim",
        "color": "bej",
        "price": 135.0,
        "description": "Ayollar uchun bej rangli uzun suv o'tkazmaydigan klassik kuzgi palto.",
        "image_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600",
        "tags": "kiyim, palto, trench, bej, kuzgi, klassik"
    },
    {
        "name": "Charm Ayollar Qo'l Sumkasi Jigarrang",
        "category": "aksessuar",
        "color": "jigarrang",
        "price": 90.0,
        "description": "Ayollar uchun tabiiy charm qo'l sumkasi, qulay cho'ntaklar va tasmali.",
        "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600",
        "tags": "aksessuar, sumka, qo'l sumkasi, ayollar, charm, jigarrang"
    },
    {
        "name": "Ray-Ban Qora Quyosh Ko'zoynagi",
        "category": "aksessuar",
        "color": "qora",
        "price": 75.0,
        "description": "UV400 ultrabinafsha nurlaridan himoyalovchi zamonaviy qora quyosh ko'zoynagi.",
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600",
        "tags": "aksessuar, kozoynak, qora, quyosh, yozgi, uslub"
    },
    {
        "name": "Tabiiy Charm Erkaklar Kamari",
        "category": "aksessuar",
        "color": "qora",
        "price": 30.0,
        "description": "Mustahkam metall to'qali, 100% tabiiy charmdan qora erkaklar kamari.",
        "image_url": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=600",
        "tags": "aksessuar, kamar, qora, charm, erkaklar, klassik"
    },
    {
        "name": "Yashil Suv O'tkazmas Sayohat Ryukzaki",
        "category": "aksessuar",
        "color": "yashil",
        "price": 45.0,
        "description": "Sayohat va noutbuk ko'tarib yurish uchun qulay yashil sport ryukzaki.",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600",
        "tags": "aksessuar, ryukzak, yashil, sayohat, sport, sumka"
    },
    {
        "name": "Apple AirPods Max Kumushrang Quloqchin",
        "category": "elektronika",
        "color": "kumushrang",
        "price": 320.0,
        "description": "Faol shovqinni bekor qiluvchi simsiz premium quloqchin, tiniq ovoz.",
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600",
        "tags": "elektronika, quloqchin, kumushrang, apple, bluetooth, musiqa"
    },
    {
        "name": "Sport Smart Soat Qora (Waterproof)",
        "category": "elektronika",
        "color": "qora",
        "price": 80.0,
        "description": "Yurak urishi, qadamlar va uyqu sifatini o'lchovchi suv o'tkazmaydigan smart soat.",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600",
        "tags": "elektronika, soat, smart soat, qora, sport, fitnes"
    }
]

def seed():
    init_db()
    db = SessionLocal()
    try:
        # Avvalgi eski tovarlarni tozalab, 15 ta to'liq sifatli tovar kiritamiz
        db.query(Product).delete()
        db.commit()

        for p in SAMPLE_PRODUCTS:
            prod = Product(**p)
            db.add(prod)
        db.commit()
        print(f"[OK] {len(SAMPLE_PRODUCTS)} ta yangi mahsulot PostgreSQL bazasiga muvaffaqiyatli kiritildi!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
