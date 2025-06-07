import eel
import base64
import io
import os
import zipfile
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename

# Eel'i başlat
eel.init('web')

def convert_to_instagram_format(image, output_format='JPEG'):
    """Fotoğrafı Instagram 4:5 formatına dönüştür"""
    target_ratio = 4 / 5
    orig_width, orig_height = image.size
    current_ratio = orig_width / orig_height

    if current_ratio > target_ratio:
        new_height = int(orig_width / target_ratio)
        padding_top = (new_height - orig_height) // 2
        padding_bottom = new_height - orig_height - padding_top
        padding = (0, padding_top, 0, padding_bottom)
    else:
        new_width = int(orig_height * target_ratio)
        padding_left = (new_width - orig_width) // 2
        padding_right = new_width - orig_width - padding_left
        padding = (padding_left, 0, padding_right, 0)

    # PNG için RGBA modunu koru, JPEG için RGB'ye çevir
    if output_format.upper() == 'PNG' and image.mode in ('RGBA', 'LA'):
        result = ImageOps.expand(image, padding, fill=(255, 255, 255, 255))
    else:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        result = ImageOps.expand(image, padding, fill="white")
    
    return result

def get_file_extension(format_type):
    """Format tipine göre dosya uzantısı döndür"""
    return 'png' if format_type.lower() == 'png' else 'jpg'

@eel.expose
def process_single_image(base64_data, filename, output_format):
    """Tek fotoğraf işleme fonksiyonu"""
    try:
        # Base64'ü decode et
        image_data = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(image_data))
        
        # Instagram formatına dönüştür
        result = convert_to_instagram_format(image, output_format.upper())
        
        # Sonucu base64'e çevir
        img_buffer = io.BytesIO()
        save_format = 'PNG' if output_format.upper() == 'PNG' else 'JPEG'
        
        if save_format == 'PNG':
            result.save(img_buffer, 'PNG', optimize=True)
        else:
            result.save(img_buffer, 'JPEG', quality=95, optimize=True)
        
        img_buffer.seek(0)
        result_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Dosya adını oluştur
        name_without_ext = os.path.splitext(filename)[0]
        extension = get_file_extension(output_format)
        new_filename = f"hazir_{name_without_ext}.{extension}"
        mimetype = 'image/png' if output_format.upper() == 'PNG' else 'image/jpeg'
        
        return {
            'success': True,
            'data': result_base64,
            'filename': new_filename,
            'mimetype': mimetype
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@eel.expose
def process_batch_images(files, output_format):
    """Toplu fotoğraf işleme fonksiyonu"""
    try:
        # ZIP buffer oluştur
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, file_data in enumerate(files, 1):
                try:
                    # Base64'ü decode et
                    image_data = base64.b64decode(file_data['data'])
                    image = Image.open(io.BytesIO(image_data))
                    
                    # Instagram formatına dönüştür
                    result = convert_to_instagram_format(image, output_format.upper())
                    
                    # Her görsel için buffer
                    img_buffer = io.BytesIO()
                    save_format = 'PNG' if output_format.upper() == 'PNG' else 'JPEG'
                    
                    if save_format == 'PNG':
                        result.save(img_buffer, 'PNG', optimize=True)
                    else:
                        result.save(img_buffer, 'JPEG', quality=95, optimize=True)
                    
                    img_buffer.seek(0)
                    
                    # Dosya adını güvenli hale getir
                    original_name = secure_filename(file_data['name'])
                    name_without_ext = os.path.splitext(original_name)[0]
                    extension = get_file_extension(output_format)
                    new_filename = f"hazir_{i:03d}_{name_without_ext}.{extension}"
                    
                    zip_file.writestr(new_filename, img_buffer.getvalue())
                    
                except Exception as e:
                    print(f"Dosya işlenirken hata: {file_data['name']} - {str(e)}")
                    continue
        
        zip_buffer.seek(0)
        result_base64 = base64.b64encode(zip_buffer.getvalue()).decode()
        
        return {
            'success': True,
            'data': result_base64,
            'filename': 'instagram_hazir_fotograflar.zip',
            'mimetype': 'application/zip'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == '__main__':
    # Masaüstü uygulamasını başlat
    print("🚀 Instagram Fotoğraf Hazırlayıcı başlatılıyor...")
    print("📱 Uygulama penceresi açılacak...")
    
    # Uygulamayı başlat - pencere boyutu ve ayarları
    eel.start('index.html', 
              size=(1000, 800),           # Pencere boyutu
              position=(100, 50),         # Başlangıç konumu
              disable_cache=True,         # Cache'i devre dışı bırak
              mode='chrome',              # Chrome modunda çalıştır
              host='localhost',           # Local host
              port=8000,                  # Port numarası
              block=True)                 # Ana thread'i blokla 