import os
import json
import shutil
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import zipfile
import csv


class FileManager:
    """Professional fayl boshqaruv klassi"""
    
    def __init__(self, base_dir: str = "file_storage"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self._setup_logging()
        
    def _setup_logging(self):
        """Logging tizimini sozlash"""
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / f"file_manager_{datetime.now().strftime('%Y%m%d')}.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_file(self, filename: str, content: str, subdir: str = "") -> bool:
        """Yangi fayl yaratish"""
        try:
            file_path = self.base_dir / subdir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Fayl yaratildi: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Fayl yaratishda xatolik: {e}")
            return False
    
    def read_file(self, filename: str, subdir: str = "") -> Optional[str]:
        """Faylni o'qish"""
        try:
            file_path = self.base_dir / subdir / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.logger.info(f"Fayl o'qildi: {file_path}")
            return content
        except Exception as e:
            self.logger.error(f"Faylni o'qishda xatolik: {e}")
            return None
    
    def update_file(self, filename: str, content: str, subdir: str = "") -> bool:
        """Faylni yangilash"""
        try:
            file_path = self.base_dir / subdir / filename
            if not file_path.exists():
                self.logger.warning(f"Fayl topilmadi: {file_path}")
                return False
            
            # Backup yaratish
            self._create_backup(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Fayl yangilandi: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Faylni yangilashda xatolik: {e}")
            return False
    
    def delete_file(self, filename: str, subdir: str = "") -> bool:
        """Faylni o'chirish"""
        try:
            file_path = self.base_dir / subdir / filename
            if file_path.exists():
                file_path.unlink()
                self.logger.info(f"Fayl o'chirildi: {file_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Faylni o'chirishda xatolik: {e}")
            return False
    
    def copy_file(self, source: str, destination: str, subdir: str = "") -> bool:
        """Faylni nusxalash"""
        try:
            src_path = self.base_dir / subdir / source
            dst_path = self.base_dir / subdir / destination
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(src_path, dst_path)
            self.logger.info(f"Fayl nusxalandi: {src_path} -> {dst_path}")
            return True
        except Exception as e:
            self.logger.error(f"Faylni nusxalashda xatolik: {e}")
            return False
    
    def move_file(self, source: str, destination: str, subdir: str = "") -> bool:
        """Faylni ko'chirish"""
        try:
            src_path = self.base_dir / subdir / source
            dst_path = self.base_dir / subdir / destination
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(src_path), str(dst_path))
            self.logger.info(f"Fayl ko'chirildi: {src_path} -> {dst_path}")
            return True
        except Exception as e:
            self.logger.error(f"Faylni ko'chirishda xatolik: {e}")
            return False
    
    def get_file_info(self, filename: str, subdir: str = "") -> Optional[Dict]:
        """Fayl haqida ma'lumot olish"""
        try:
            file_path = self.base_dir / subdir / filename
            if not file_path.exists():
                return None
            
            stats = file_path.stat()
            return {
                'name': filename,
                'size': stats.st_size,
                'size_mb': round(stats.st_size / (1024 * 1024), 2),
                'created': datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'extension': file_path.suffix,
                'is_file': file_path.is_file(),
                'path': str(file_path)
            }
        except Exception as e:
            self.logger.error(f"Fayl ma'lumotini olishda xatolik: {e}")
            return None
    
    def list_files(self, subdir: str = "", pattern: str = "*") -> List[str]:
        """Papkadagi fayllar ro'yxati"""
        try:
            dir_path = self.base_dir / subdir
            if not dir_path.exists():
                return []
            
            files = [f.name for f in dir_path.glob(pattern) if f.is_file()]
            return sorted(files)
        except Exception as e:
            self.logger.error(f"Fayllar ro'yxatini olishda xatolik: {e}")
            return []
    
    def search_files(self, keyword: str, subdir: str = "") -> List[str]:
        """Fayllarni qidirish"""
        try:
            dir_path = self.base_dir / subdir
            results = []
            
            for file_path in dir_path.rglob("*"):
                if file_path.is_file() and keyword.lower() in file_path.name.lower():
                    results.append(str(file_path.relative_to(self.base_dir)))
            
            return results
        except Exception as e:
            self.logger.error(f"Qidirishda xatolik: {e}")
            return []
    
    def get_file_hash(self, filename: str, subdir: str = "") -> Optional[str]:
        """Fayl hash kodini olish (MD5)"""
        try:
            file_path = self.base_dir / subdir / filename
            hash_md5 = hashlib.md5()
            
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Hash olishda xatolik: {e}")
            return None
    
    def _create_backup(self, file_path: Path):
        """Fayl backupini yaratish"""
        backup_dir = self.base_dir / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = backup_dir / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.logger.info(f"Backup yaratildi: {backup_path}")
    
    def create_zip(self, zip_name: str, files: List[str], subdir: str = "") -> bool:
        """Fayllarni zip arxivga joylash"""
        try:
            zip_path = self.base_dir / subdir / zip_name
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    file_path = self.base_dir / subdir / file
                    if file_path.exists():
                        zipf.write(file_path, file)
            
            self.logger.info(f"ZIP arxiv yaratildi: {zip_path}")
            return True
        except Exception as e:
            self.logger.error(f"ZIP yaratishda xatolik: {e}")
            return False
    
    def extract_zip(self, zip_name: str, extract_dir: str = "", subdir: str = "") -> bool:
        """ZIP arxivni ochish"""
        try:
            zip_path = self.base_dir / subdir / zip_name
            extract_path = self.base_dir / subdir / extract_dir
            extract_path.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(extract_path)
            
            self.logger.info(f"ZIP arxiv ochildi: {zip_path}")
            return True
        except Exception as e:
            self.logger.error(f"ZIP ochishda xatolik: {e}")
            return False
    
    def save_json(self, filename: str, data: dict, subdir: str = "") -> bool:
        """JSON formatda saqlash"""
        try:
            file_path = self.base_dir / subdir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"JSON saqlandi: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"JSON saqlashda xatolik: {e}")
            return False
    
    def load_json(self, filename: str, subdir: str = "") -> Optional[dict]:
        """JSON faylni yuklash"""
        try:
            file_path = self.base_dir / subdir / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            self.logger.error(f"JSON yuklashda xatolik: {e}")
            return None
    
    def save_csv(self, filename: str, data: List[List], headers: List[str] = None, subdir: str = "") -> bool:
        """CSV formatda saqlash"""
        try:
            file_path = self.base_dir / subdir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if headers:
                    writer.writerow(headers)
                writer.writerows(data)
            
            self.logger.info(f"CSV saqlandi: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"CSV saqlashda xatolik: {e}")
            return False
    
    def load_csv(self, filename: str, subdir: str = "") -> Optional[List[List[str]]]:
        """CSV faylni yuklash"""
        try:
            file_path = self.base_dir / subdir / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                data = list(reader)
            return data
        except Exception as e:
            self.logger.error(f"CSV yuklashda xatolik: {e}")
            return None
    
    def get_storage_stats(self) -> Dict:
        """Xotira statistikasi"""
        try:
            total_size = 0
            file_count = 0
            
            for file_path in self.base_dir.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_count += 1
            
            return {
                'total_files': file_count,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'total_size_gb': round(total_size / (1024 * 1024 * 1024), 2),
                'base_directory': str(self.base_dir)
            }
        except Exception as e:
            self.logger.error(f"Statistika olishda xatolik: {e}")
            return {}


def demo():
    """Tizimni sinab ko'rish"""
    fm = FileManager()
    
    print("=== Professional Fayl Boshqaruv Tizimi ===\n")
    
    # 1. Oddiy matn fayl yaratish
    fm.create_file("test.txt", "Bu test fayli", "documents")
    print("✓ Test fayl yaratildi")
    
    # 2. JSON ma'lumot saqlash
    data = {
        "ism": "Ali",
        "yosh": 25,
        "shahar": "Toshkent",
        "kasb": "Dasturchi"
    }
    fm.save_json("user_data.json", data, "data")
    print("✓ JSON ma'lumot saqlandi")
    
    # 3. CSV ma'lumot saqlash
    csv_data = [
        ["Ali", "25", "Toshkent"],
        ["Vali", "30", "Samarqand"],
        ["Sardor", "28", "Buxoro"]
    ]
    fm.save_csv("users.csv", csv_data, ["Ism", "Yosh", "Shahar"], "data")
    print("✓ CSV ma'lumot saqlandi")
    
    # 4. Fayllar ro'yxati
    files = fm.list_files("data")
    print(f"\n📁 Data papkasidagi fayllar: {files}")
    
    # 5. Fayl ma'lumoti
    info = fm.get_file_info("user_data.json", "data")
    if info:
        print(f"\n📄 Fayl ma'lumoti:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    # 6. Xotira statistikasi
    stats = fm.get_storage_stats()
    print(f"\n💾 Xotira statistikasi:")
    print(f"  Jami fayllar: {stats.get('total_files', 0)}")
    print(f"  Jami hajm: {stats.get('total_size_mb', 0)} MB")
    
    print("\n✅ Demo yakunlandi!")


if __name__ == "__main__":
    demo()
