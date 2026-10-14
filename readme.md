# 🛍️ Vision Detect & Customer Intent Analytics API

> **E-commerce uchun AI vizual qidiruv (Visual Search) va xaridor talablarini tahlil qilish mikroxizmati (Customer Intent & Demand Analytics)**

Ushbu mikroxizmat istalgan mavjud e-commerce internet-do'koniga (WordPress, OpenCart, Laravel, Next.js, HTML/PHP) **sun'iy intellekt asosidagi rasm orqali qidiruv** va **marketing talablarini tahlil qilish** imkoniyatini taqdim etadi.

Mijoz qidiruv paneliga rasm yuklaganda, **Google Gemini Multimodal AI** modelimiz soniyalar ichida uning rangi, turkumi, kiyim yoki buyum xususiyatlarini aniqlaydi va do'kon bazasidan eng mos tovarlarni chiqaradi. Shu bilan birga, xaridorning barcha xatti-harakatlari (ko'rdi, savatga qo'shdi, tashlab ketdi, sotib oldi) yig'ilib, do'kon egasi uchun **aniq marketing grafiklari** va **qondirilmagan talab hisoboti** shakllantiriladi.

---

## 📸 Loyiha Ko'rinishi va Skrinshotlar

### 1. E-Commerce Do'kon Sahifasi (`LUXEVISION AI Store`)
Do'kon katalogi 15 ta namunaviy mahsulot (poyabzal, kiyim, aksessuar, elektronika) bilan boyitilgan. Qidiruv panelida matn kiritish joyining yonida maxsus **`[ 📷 Rasm orqali ]`** kamera tugmasi joylashtirilgan.

![1. E-Commerce Do'kon Sahifasi](image/1_ecommerce_store.png)

---

### 2. Marketing Analitikasi & Asosiy KPI Ko'rsatkichlari
Do'kon boshqaruvchisi va marketologlar uchun 4 ta asosiy KPI kartochkasi:
* **🔍 Jami AI Qidiruvlar:** Mijozlar rasm orqali qidirgan jami so'rovlar soni.
* **🛒 Savatga Qo'shilganlar:** Rasm orqali topilib, savatga solingan tovarlar.
* **💸 Yo'qotilgan Daromad (Savatda):** Savatga qo'shilib, sotib olinmay qolgan tovarlar bo'yicha yo'qotilgan summa ($).
* **📈 Konversiya Foizi (%):** Rasm yuklashdan to xaridgacha bo'lgan muvaffaqiyat darajasi.

![2. Marketing Analitikasi KPI](image/2_marketing_analytics_kpi.png)

---

### 3. Chuqur Marketing Diagrammalari va Dinamika
* **🔻 Konversiya Voronkasi (Funnel):** *Qidirdi ➔ Ko'rdi ➔ Savatga soldi ➔ Xarid qildi*.
* **📂 Qidirilgan Kategoriyalar:** Kiyim, Poyabzal, Aksessuar va Elektronika ulushi (Doughnut).
* **⏰ Qidiruvlar Vaqti Dinamikasi:** Soatlar bo'yicha mijozlarning faollik dinamikasi (Qachon qidirildi?).
* **🎨 Eng Ommabop Ranglar:** AI aniqlagan eng ko'p talab qilinayotgan ranglar palitrasi.
* **⚠️ Do'konda Bor vs Yo'q:** Topilgan mahsulotlar va qondirilmagan talab nisbati (Pie chart).

![3. Analitika Grafiklari](image/3_analytics_charts.png)

---

### 4. Qondirilmagan Talab va Tashlab Ketilgan Savatlar Jadvallari
* **📦 Qondirilmagan Talab (Unmet Demand):** Xaridorlar rasm orqali izlagan, biroq do'konda **mavjud bo'lmagan** tovarlar ro'yxati va do'konga qaysi mahsulotlarni olib kelish bo'yicha AI tavsiyalari (masalan: *sariq xudi*, *yashil sport kepka*, *iPhone 15 g'ilofi*, *oq charm kurtka*).
* **🛒 Savatda Qolgan Mahsulotlar:** Qaysi tovarlar savatda qolib ketgani va yo'qotilgan summa ($) hisoboti (Chegirma yoki promo-kod taklif qilish uchun).
* **⚡ Real-time Qidiruvlar Jurnali:** Jonli ravishda qaysi soatda qanday tovar qidirilgani va qaysi Gemini modeli ishlatilgani jurnali.

![4. Qondirilmagan Talab va Tashlab Ketilgan Savatlar](image/4_unmet_demand_tables.png)

---

### 5. AI Rasm orqali Qidiruv Natijasi (Vidjet Oynasi)
Rasm yuklanganda **Google Gemini Flash** modeli uni soniyalarda tahlil qilib, kategoriya, rang va teglarni chiqaradi. Agar do'konda mos tovarlar bo'lsa, moslik foizi bilan chiqarib beradi va to'g'ridan-to'g'ri "Savatga" qo'shish imkonini taqdim etadi.

![5. Rasm orqali Qidiruv Natijasi](image/5_visual_search_result.png)

---

## 🌟 Asosiy Imkoniyatlar

1. **📷 AI Visual Search (Rasm orqali qidiruv):**
   * Drag & Drop, fayl tanlash yoki namunaviy rasmlarni 1-bosishda sinash.
   * SHA-256 xeshlash orqali bir xil rasmlarni keshdan bir zumda qaytarish (bepul API limitini tejaydi).
2. **🔄 Bepul Gemini Modellari Rotatori:**
   * Google AI Studio bepul kalitlari uchun aqlli model rotatori (`gemini-3.1-flash-lite`, `gemini-3.5-flash`, `gemini-3.8-flash`, `gemini-flash-latest`).
   * Birorta model band yoki limitga uchrasa, to'xtab qolmasdan darhol keyingi modelga avtomatik o'tadi.
3. **🛒 Customer Intent & Funnel Tracking:**
   * Mijozlarning `VIEW_ITEM`, `ADD_TO_CART`, `PURCHASE` xatti-harakatlarini qayd qiladi.
   * Facebook (Meta) Pixel bilan parallel ishlay oladi.
4. **📊 Marketing Intelligence Dashboard:**
   * Swagger (`/docs`) o'rniga do'kon egalari uchun ishlab chiqilgan tushunarli grafiklar (Chart.js).
   * Qondirilmagan talab (Unmet Demand) monitoringi orqali qaysi tovarlarni omborga olib kelish kerakligini ko'rsatadi.
   * Tashlab ketilgan savatlardagi yo'qotilgan summa ($) hisoboti.
5. **⚡ Interaktiv API Sinov Maydoni:**
   * Swagger `/docs` dan foydalanishga qiynalganlar uchun qulay veb interfeys.
   * Har bir API endpointni forma orqali 1-bosishda sinab ko'rish imkoniyati.
6. **🔌 1 Qatorda Ulanuvchi Vidjet (`vision-widget.js`):**
   * Istalgan mavjud veb-saytga bitta `<script>` tegi orqali ulanadi.

---

## 🛠️ Texnologiyalar Steki

* **Backend:** Python 3.10+, [FastAPI](https://fastapi.tiangolo.com/), Uvicorn
* **Database & ORM:** [PostgreSQL](https://www.postgresql.org/), [SQLAlchemy](https://www.sqlalchemy.org/), Psycopg2-binary
* **AI & LLM:** Google Gemini Multimodal API (`google-genai` SDK)
* **Frontend:** Vanilla HTML5, CSS3 (Modern Glassmorphism & Responsive Design), JavaScript (ES6+)
* **Grafiklar:** [Chart.js](https://www.chartjs.org/)

---

## 🚀 O'rnatish va Ishga Tushirish (Qadam-baqadam)

### 1. Loyihani yuklab oling (Clone)
```bash
git clone https://github.com/sizning-akkount/vision-detect-event-handler.git
cd vision-detect-event-handler
```

### 2. Python Virtual Muhitini yarating va faollashtiring
```bash
# Windows:
python -m venv my_env
my_env\Scripts\activate

# Linux / MacOS:
python3 -m venv my_env
source my_env/bin/activate
```

### 3. Kerakli kutubxonalarni o'rnating
```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Ma'lumotlar Bazasini yarating
PostgreSQL (pgAdmin yoki psql konsoli) orqali yangi baza yarating:
```sql
CREATE DATABASE vision_detect_event_handler;
```

### 5. `.env` konfiguratsiya faylini sozlang
Loyihaning asosiy papkasidagi `.env` faylini oching va PostgreSQL parolingiz hamda Google Gemini API kalitingizni kiriting:
```ini
# PostgreSQL ulanish manzili (user:parol@host:port/baza_nomi)
DATABASE_URL=postgresql://postgres:1234@localhost:5432/vision_detect_event_handler

# Google AI Studio dan olingan Gemini API kaliti (https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=sizning_gemini_api_kalitingiz

# Bepul ishlovchi modellar ro'yxati (navbat bilan ishlaydi)
GEMINI_MODELS=gemini-3.1-flash-lite,gemini-3.5-flash,gemini-3.8-flash,gemini-flash-latest

CACHE_ENABLED=true
```

### 6. Namunaviy 15 ta tovarlarni bazaga kiritish
Baza jadvallarini avtomatik yaratish va 15 ta yuqori sifatli namunaviy tovarlarni yuklash uchun seeder skriptini ishga tushiring:
```bash
python seed_data.py
```
*Konsolda `[OK] 15 ta yangi mahsulot PostgreSQL bazasiga muvaffaqiyatli kiritildi!` xabari chiqadi.*

### 7. Serverni ishga tushiring
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

---

## 🌐 Brauzerda Ishlatish

Server ishga tushgach, brauzeringizda quyidagi manzillarni ochishingiz mumkin:

| Manzil | Tavsif |
| :--- | :--- |
| **`http://127.0.0.1:8000/store`** | 🛍️ **E-Commerce Do'kon:** Qidiruv maydoni yonida kamera tugmasi va 15 ta tovar bilan jihozlangan chiroyli vitrina. |
| **`http://127.0.0.1:8000/`** | 📊 **Marketing Dashboard:** To'liq analitika grafiklari, KPI lar, qondirilmagan talab jadvallari. |
| **`http://127.0.0.1:8000/?tab=api`** | ⚡ **API Sinov Maydoni:** Swagger o'rniga qulay interaktiv test maydoni. |
| **`http://127.0.0.1:8000/docs`** | 📖 **FastAPI Swagger:** Standart texnik API hujjatlari. |

---

## 🔌 Mavjud Do'koningizga Vidjetni Ulash (1 Qatorda)

Agar sizda alohida veb-sayt (masalan, WordPress, PHP, Laravel yoki React) bo'lsa, unga rasm orqali qidiruvni ulash uchun sahifangizning `<body>` qismiga quyidagi kodni qo'yish kifoya:

```html
<!-- Vision AI Vidjeti -->
<script src="http://127.0.0.1:8000/static/vision-widget.js" 
        data-api="http://127.0.0.1:8000" 
        data-attach-to="#cameraSearchBtn"
        data-show-floating="true"></script>
```

### Savatga qo'shish va xaridlarni kuzatish (Event Tracking):
Saytingizdagi "Savatga qo'shish" yoki "Xarid qilish" tugmasiga 1 qator JavaScript chaqiruvini qo'shasiz:
```javascript
// Savatga qo'shilganda:
window.VisionAnalytics.track('ADD_TO_CART', 7, 'Nike Air Zoom Pegasus');

// Xarid qilinganda:
window.VisionAnalytics.track('PURCHASE', 7, 'Nike Air Zoom Pegasus');
```
*Ushbu funksiya avtomatik ravishda ham bizning backendimizga, ham saytda o'rnatilgan Facebook Pixel (`fbq`) ga hodisani yuboradi.*

---

## 📡 Asosiy API Endpointlar

### 1. `POST /api/v1/visual-search`
Rasm yuklash va Gemini AI orqali bazadan mos tovarlarni topish.
* **Format:** `multipart/form-data`
* **Parametrlar:** `file` (rasm fayli), `session_id` (ixtiyoriy)
* **Javob namunasi:**
```json
{
  "status": "success",
  "search_id": "9b926a65-def9-47ed-8e42-dc4e41ae4bab",
  "ai_detected": {
    "category": "poyabzal",
    "color": "qizil",
    "search_query": "qizil sport krossovka",
    "tags": ["poyabzal", "krossovka", "qizil", "sport"]
  },
  "model_used": "gemini-3.1-flash-lite",
  "best_match_score": 0.85,
  "is_unmet_demand": false,
  "products": [...]
}
```

### 2. `POST /api/v1/track-event`
Mijozning hodisalarini (ko'rdi, savatga soldi, xarid qildi) qayd qilish.
```json
{
  "session_id": "sess_12345",
  "product_id": 7,
  "event_type": "ADD_TO_CART"
}
```

### 3. `GET /api/v1/products`
Tovarlar ro'yxatini toifa va kalit so'z bo'yicha olish.
* `/api/v1/products?category=poyabzal&q=krossovka`

### 4. `GET /api/v1/analytics/wishes`
Do'kon egasi uchun marketing analitikasi ma'lumotlari (KPI, Voronka, Qondirilmagan talab, Yo'qotilgan summa, Trendlar).

---

## 📁 Loyiha Katalogi Tuzilishi

```text
vision-detect-event-handler/
├── app/
│   ├── api/
│   │   ├── analytics.py          # Marketing analitikasi, voronka va demo data seeder
│   │   ├── events.py             # Event tracking (VIEW_ITEM, ADD_TO_CART, PURCHASE)
│   │   └── search.py             # Rasm orqali qidiruv & tovarlar ro'yxati
│   ├── core/
│   │   └── config.py             # Sozlamalar va .env o'qish
│   ├── db/
│   │   └── session.py            # PostgreSQL SQLAlchemy sessiyasi
│   ├── models/
│   │   └── entities.py           # Product, VisualSearch, UserEvent modellari
│   ├── schemas/
│   │   └── payloads.py           # Pydantic validatsiya sxemalari
│   └── services/
│       ├── gemini_rotator.py     # Gemini modellar rotatori, fallback & xeshlash
│       └── search_engine.py      # Matnli va atributli moslashtirish algoritmi
├── image/                        # README va hujjatlar uchun skrinshotlar
│   ├── 1_ecommerce_store.png
│   ├── 2_marketing_analytics_kpi.png
│   ├── 3_analytics_charts.png
│   ├── 4_unmet_demand_tables.png
│   └── 5_visual_search_result.png
├── static/
│   └── vision-widget.js          # Tashqi saytlar uchun universal embed vidjet
├── index.html                    # Asosiy Super-App: Marketing Dashboard & API Tester
├── test_external_integration.html# LUXEVISION E-Commerce vitrinasi (15 tovar & kamera)
├── main.py                       # FastAPI asosiy dastur kirish nuqtasi
├── seed_data.py                  # 15 ta tovar va jadvallarni to'ldirish skripti
├── requirements.txt              # Python kutubxonalari ro'yxati
├── .env                          # Konfiguratsiya va kalitlar
└── readme.md                     # Ushbu to'liq hujjat fayli
```

---

## 👨‍💻 Muallif va Litsenziya

* Ushbu loyiha e-commerce internet do'konlarida savdo ko'rsatkichlarini oshirish, mijozlarning vizual ehtiyojlarini qondirish va marketing intellektini shakllantirish maqsadida ishlab chiqilgan.
* Litsenziya: **MIT License**.