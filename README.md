# 🗂️ filemaster-py

Professional fayl boshqaruv tizimi Python uchun.

## ✨ Imkoniyatlar

- 📝 CRUD operatsiyalar (yaratish, o'qish, yangilash, o'chirish)
- 📋 JSON, CSV, TXT formatlar
- 🔍 Qidiruv va filtrlash
- 🗜️ ZIP arxiv yaratish/ochish
- 🔒 Avtomatik backup
- 📊 Statistika va logging

## 🚀 Ishlatish

```python
from file_manager import FileManager

fm = FileManager()

# Fayl yaratish
fm.create_file("hello.txt", "Salom!", "docs")

# JSON saqlash
data = {"name": "Ali", "age": 25}
fm.save_json("user.json", data)

# CSV saqlash
fm.save_csv("users.csv", [["Ali", "25"]], ["Ism", "Yosh"])

# Fayllar ro'yxati
files = fm.list_files("docs")

# Fayl ma'lumoti
info = fm.get_file_info("hello.txt", "docs")

# Qidirish
results = fm.search_files("hello")

# ZIP yaratish
fm.create_zip("archive.zip", ["file1.txt", "file2.txt"])

# Statistika
stats = fm.get_storage_stats()
```

## 📋 Metodlar

| Metod | Tavsif |
|-------|--------|
| `create_file()` | Fayl yaratish |
| `read_file()` | Faylni o'qish |
| `update_file()` | Yangilash (backup bilan) |
| `delete_file()` | O'chirish |
| `copy_file()` | Nusxalash |
| `move_file()` | Ko'chirish |
| `save_json()` | JSON saqlash |
| `load_json()` | JSON yuklash |
| `save_csv()` | CSV saqlash |
| `load_csv()` | CSV yuklash |
| `list_files()` | Fayllar ro'yxati |
| `search_files()` | Qidirish |
| `get_file_info()` | Ma'lumot olish |
| `get_file_hash()` | MD5 hash |
| `create_zip()` | ZIP yaratish |
| `extract_zip()` | ZIP ochish |
| `get_storage_stats()` | Statistika |

## 🎯 Demo

```bash
python main.py
```
