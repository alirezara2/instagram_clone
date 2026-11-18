# Instagram Clone

یک نمونه‌کار از کلون اینستاگرام با Django.

## ✨ ویژگی‌ها

- ثبت‌نام و لاگین با ایمیل
- پروفایل کاربری با عکس، بیو، تاریخ تولد و شماره تماس
- انتشار پست (عکس یا ویدیو) با کپشن
- سیستم لایک با AJAX
- سیستم کامنت
- فالوو / آنفالوو کاربران
- فید شخصی (پست‌های خودم و فالووینگ‌ها)
- صفحه اکسپلور
- جستجوی کاربران
- طراحی ریسپانسیو با Bootstrap 5

## 🛠 تکنولوژی‌ها

- Python 3.13
- Django 5.x
- Pillow
- Bootstrap 5
- SQLite (برای توسعه)

## 🚀 راه‌اندازی

```bash
# 1. کلون پروژه
git clone https://github.com/USERNAME/instagram-clone.git
cd instagram-clone

# 2. ساخت محیط مجازی
python -m venv .venv
.venv\Scripts\activate   # ویندوز
# source .venv/bin/activate   # لینوکس/مک

# 3. نصب پکیج‌ها
pip install -r requirements.txt

# 4. مایگریشن
python manage.py migrate

# 5. ساخت سوپریوزر
python manage.py createsuperuser

# 6. اجرا
python manage.py runserver

📸 تصاویر
(بعداً اسکرین‌شات اضافه کنید)

👤 نویسنده
نام شما - alirezara2

---

## 🟢 فایل ۱۳: `requirements.txt` (🆕 تولید مجدد)

در ترمینال (با محیط مجازی فعال) بزن:

```bash
pip freeze > requirements.txt