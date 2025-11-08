<div align="center">

# 🛒 Agro Web — Django Store & Product Showcase

A modern, responsive Django-based e-commerce website for showcasing agricultural products.  
Includes product browsing, search, wishlist, cart system, and a clean user experience.

[![Django](https://img.shields.io/badge/Framework-Django-0C4B33?logo=django&style=for-the-badge)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205-563d7c?logo=bootstrap&style=for-the-badge)](https://getbootstrap.com/)
[![PythonAnywhere](https://img.shields.io/badge/Hosting-PythonAnywhere-blue?logo=python&style=for-the-badge)](https://www.pythonanywhere.com/)
[![GitHub](https://img.shields.io/badge/Repo-GitHub-black?logo=github&style=for-the-badge)](https://github.com/byte-journey/agro_web)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 🚀 Overview

**Agro Web** is a lightweight Django application designed for business owners who want a simple, clean online store.  
The project supports product listings, categories, search, user authentication, wishlist, cart and checkout — all wrapped in a fast Bootstrap UI.

---

## ✨ Features

✅ Beautiful homepage with product cards  
✅ Category-based product filtering  
✅ Search with live suggestions (AJAX)  
✅ Wishlist (localStorage)  
✅ Cart + Checkout functionality  (Will be added in the future)  
✅ User login & signup  (Will be added in the future)  
✅ SEO-friendly clean URLs  
✅ Mobile-friendly responsive design  

---

## 🧰 Technologies Used

| Area | Tools |
|------|------|
| Backend | Django 5, Django REST Framework (optional) |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Database | SQLite (dev) / MySQL (PythonAnywhere) |
| Deployment | PythonAnywhere |
| Assets | Static & media file handling via Django |

---

## 📁 Project Structure

agro_web/  
│  
├── config/ # Django project settings  
├── store/ # Main app: models, views, urls  
├── templates/ # HTML templates  
│ ├── store/  
│ ├── partials/  
│ ├── base.html  
│ └── navbar.html  
├── static/ # CSS + images for frontend  
├── media/ # Uploaded images (not in repo)  
├── staticFiles/ # collectstatic output (ignored)  
├── manage.py  
└── requirements.txt  

---

## ⚙️ Local Development Setup

1️⃣ **Clone the repository**
```bash
git clone https://github.com/byte-journey/agro_web.git
cd agro_web
python -m venv ~/agro_env
source ~/agro_env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

```

---


## 👨‍💻 Author

**Gideon Gakpetor**  
🔗 [GitHub:] https://github.com/byte-journey

Passionate about Django, full-stack web development, and clean UI design.


