from flask import Flask, request, render_template_string, send_file
from PIL import Image, ImageOps
import os
import io
import zipfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Fotoğraf Hazırlayıcı</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
            padding: 40px 30px;
            text-align: center;
            color: white;
            position: relative;
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.1);
        }

        .header h1 {
            position: relative;
            font-size: 2.5rem;
            font-weight: 300;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .header p {
            position: relative;
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 300;
        }

        .content {
            padding: 40px 30px;
        }

        .upload-section {
            margin-bottom: 40px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
            overflow: hidden;
            transition: transform 0.3s ease;
        }

        .upload-section:hover {
            transform: translateY(-5px);
        }

        .section-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px 30px;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .section-header i {
            font-size: 1.5rem;
        }

        .section-header h3 {
            font-size: 1.3rem;
            font-weight: 500;
        }

        .section-body {
            padding: 30px;
        }

        .file-input-container {
            position: relative;
            margin-bottom: 25px;
        }

        .file-input {
            display: none;
        }

        .file-input-label {
            display: block;
            padding: 20px;
            border: 3px dashed #667eea;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: linear-gradient(135deg, #f5f7ff, #e8f0ff);
        }

        .file-input-label:hover {
            border-color: #5a67d5;
            background: linear-gradient(135deg, #e8f0ff, #d4e6ff);
            transform: scale(1.02);
        }

        .file-input-label i {
            font-size: 3rem;
            color: #667eea;
            margin-bottom: 15px;
            display: block;
        }

        .file-input-label .text {
            font-size: 1.1rem;
            color: #667eea;
            font-weight: 500;
        }

        .file-input-label .subtext {
            font-size: 0.9rem;
            color: #8a92b2;
            margin-top: 5px;
        }

        .format-options {
            margin: 25px 0;
            display: flex;
            gap: 20px;
            justify-content: center;
        }

        .format-option {
            position: relative;
        }

        .format-option input[type="radio"] {
            display: none;
        }

        .format-option label {
            display: block;
            padding: 12px 25px;
            background: #f8f9ff;
            border: 2px solid #e0e6ff;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            color: #667eea;
        }

        .format-option input[type="radio"]:checked + label {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-color: #667eea;
            transform: scale(1.05);
        }

        .submit-btn {
            width: 100%;
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }

        .submit-btn:active {
            transform: translateY(0);
        }

        .info-card {
            background: linear-gradient(135deg, #e3f2fd, #f1f8e9);
            border-radius: 12px;
            padding: 20px;
            margin: 25px 0;
            border-left: 5px solid #4caf50;
        }

        .info-card i {
            color: #4caf50;
            margin-right: 10px;
        }

        .info-card strong {
            color: #2e7d32;
        }

        .download-section {
            background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            margin-top: 30px;
            border: 2px solid #4caf50;
        }

        .download-link {
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(135deg, #4caf50, #45a049);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        }

        .download-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.6);
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: #8a92b2;
            font-size: 0.9rem;
        }

        /* Animasyonlar */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .upload-section {
            animation: fadeInUp 0.6s ease forwards;
        }

        .upload-section:nth-child(2) {
            animation-delay: 0.2s;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 16px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .content {
                padding: 20px;
            }
            
            .format-options {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fab fa-instagram"></i> Instagram Fotoğraf Hazırlayıcı</h1>
            <p>Fotoğraflarınızı Instagram'a uygun hale getirin</p>
        </div>

        <div class="content">
            <!-- Tek Fotoğraf İşleme -->
            <div class="upload-section">
                <div class="section-header">
                    <i class="fas fa-image"></i>
                    <h3>Tek Fotoğraf İşleme</h3>
                </div>
                <div class="section-body">
                    <form method="post" enctype="multipart/form-data" action="/single">
                        <div class="file-input-container">
                            <input type="file" name="photo" accept="image/*" required class="file-input" id="single-file">
                            <label for="single-file" class="file-input-label">
                                <i class="fas fa-cloud-upload-alt"></i>
                                <div class="text">Fotoğraf Seçin</div>
                                <div class="subtext">JPG, PNG, WEBP desteklenir</div>
                            </label>
                        </div>
                        
                        <div class="format-options">
                            <div class="format-option">
                                <input type="radio" name="format" value="jpeg" checked id="single-jpeg">
                                <label for="single-jpeg"><i class="fas fa-file-image"></i> JPEG</label>
                            </div>
                            <div class="format-option">
                                <input type="radio" name="format" value="png" id="single-png">
                                <label for="single-png"><i class="fas fa-file-image"></i> PNG</label>
                            </div>
                        </div>
                        
                        <button type="submit" class="submit-btn">
                            <i class="fas fa-magic"></i> Dönüştür ve İndir
                        </button>
                    </form>
                </div>
            </div>

            <!-- Toplu Fotoğraf İşleme -->
            <div class="upload-section">
                <div class="section-header">
                    <i class="fas fa-images"></i>
                    <h3>Toplu Fotoğraf İşleme</h3>
                </div>
                <div class="section-body">
                    <div class="info-card">
                        <i class="fas fa-lightbulb"></i>
                        <strong>İpucu:</strong> Birden fazla fotoğraf seçerek hepsini aynı anda işleyebilirsiniz. ZIP dosyası olarak indirilecek.
                    </div>
                    
                    <form method="post" enctype="multipart/form-data" action="/batch">
                        <div class="file-input-container">
                            <input type="file" name="photos" accept="image/*" multiple required class="file-input" id="batch-files">
                            <label for="batch-files" class="file-input-label">
                                <i class="fas fa-folder-open"></i>
                                <div class="text">Birden Fazla Fotoğraf Seçin</div>
                                <div class="subtext">Ctrl tuşuna basılı tutarak çoklu seçim yapabilirsiniz</div>
                            </label>
                        </div>
                        
                        <div class="format-options">
                            <div class="format-option">
                                <input type="radio" name="format" value="jpeg" checked id="batch-jpeg">
                                <label for="batch-jpeg"><i class="fas fa-file-archive"></i> JPEG</label>
                            </div>
                            <div class="format-option">
                                <input type="radio" name="format" value="png" id="batch-png">
                                <label for="batch-png"><i class="fas fa-file-archive"></i> PNG</label>
                            </div>
                        </div>
                        
                        <button type="submit" class="submit-btn">
                            <i class="fas fa-download"></i> Toplu Dönüştür ve ZIP İndir
                        </button>
                    </form>
                </div>
            </div>

            {% if download_link %}
            <div class="download-section">
                <h3><i class="fas fa-check-circle" style="color: #4caf50;"></i> İşlem Tamamlandı!</h3>
                <p style="margin: 15px 0;">Dönüştürülmüş dosyanız hazır.</p>
                <a href="{{ download_link }}" class="download-link">
                    <i class="fas fa-download"></i> Dosyayı İndir
                </a>
            </div>
            {% endif %}
            
            <div class="info-card">
                <i class="fas fa-info-circle"></i>
                <strong>Bilgi:</strong> Bu uygulama fotoğraflarınızı Instagram'ın 4:5 oranına uygun hale getirir ve beyaz arka plan ekler.
            </div>
        </div>

        <div class="footer">
            <p><i class="fas fa-heart" style="color: #ff6b6b;"></i> Instagram Fotoğraf Hazırlayıcı - iglthedev</p>
        </div>
    </div>

    <script>
        // Dosya seçim feedback'i
        document.getElementById('single-file').addEventListener('change', function(e) {
            const label = this.nextElementSibling;
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                label.querySelector('.text').textContent = fileName;
                label.querySelector('.subtext').textContent = 'Dosya seçildi ✓';
                label.style.borderColor = '#4caf50';
                label.style.background = 'linear-gradient(135deg, #e8f5e8, #f0f8f0)';
            }
        });

        document.getElementById('batch-files').addEventListener('change', function(e) {
            const label = this.nextElementSibling;
            const fileCount = e.target.files.length;
            if (fileCount > 0) {
                label.querySelector('.text').textContent = `${fileCount} dosya seçildi`;
                label.querySelector('.subtext').textContent = 'Dosyalar hazır ✓';
                label.style.borderColor = '#4caf50';
                label.style.background = 'linear-gradient(135deg, #e8f5e8, #f0f8f0)';
            }
        });
    </script>
</body>
</html>
'''

def convert_to_instagram_format(image, output_format='JPEG'):
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
    return 'png' if format_type.lower() == 'png' else 'jpg'

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/single', methods=['POST'])
def single_upload():
    file = request.files.get('photo')
    output_format = request.form.get('format', 'jpeg').upper()
    
    if not file:
        return render_template_string(HTML_TEMPLATE)
    
    try:
        image = Image.open(file.stream)
        result = convert_to_instagram_format(image, output_format)

        # Görseli bellekte tut
        img_io = io.BytesIO()
        save_format = 'PNG' if output_format == 'PNG' else 'JPEG'
        
        if save_format == 'PNG':
            result.save(img_io, 'PNG', optimize=True)
        else:
            result.save(img_io, 'JPEG', quality=95, optimize=True)
        
        img_io.seek(0)
        
        extension = get_file_extension(output_format)
        filename = f'hazir_instagram.{extension}'
        mimetype = 'image/png' if output_format == 'PNG' else 'image/jpeg'

        return send_file(img_io, mimetype=mimetype, as_attachment=True, download_name=filename)
    
    except Exception as e:
        return f"Hata oluştu: {str(e)}", 400

@app.route('/batch', methods=['POST'])
def batch_upload():
    files = request.files.getlist('photos')
    output_format = request.form.get('format', 'jpeg').upper()
    
    if not files or len(files) == 0:
        return render_template_string(HTML_TEMPLATE)
    
    try:
        # ZIP dosyası oluştur
        zip_io = io.BytesIO()
        
        with zipfile.ZipFile(zip_io, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, file in enumerate(files, 1):
                if file and file.filename:
                    try:
                        image = Image.open(file.stream)
                        result = convert_to_instagram_format(image, output_format)
                        
                        # Her görsel için ayrı buffer
                        img_buffer = io.BytesIO()
                        save_format = 'PNG' if output_format == 'PNG' else 'JPEG'
                        
                        if save_format == 'PNG':
                            result.save(img_buffer, 'PNG', optimize=True)
                        else:
                            result.save(img_buffer, 'JPEG', quality=95, optimize=True)
                        
                        img_buffer.seek(0)
                        
                        # Dosya adını güvenli hale getir
                        original_name = secure_filename(file.filename)
                        name_without_ext = os.path.splitext(original_name)[0]
                        extension = get_file_extension(output_format)
                        new_filename = f"hazir_{i:03d}_{name_without_ext}.{extension}"
                        
                        zip_file.writestr(new_filename, img_buffer.getvalue())
                        
                    except Exception as e:
                        # Hatalı dosyaları atla
                        continue
        
        zip_io.seek(0)
        
        return send_file(
            zip_io, 
            mimetype='application/zip', 
            as_attachment=True, 
            download_name='instagram_hazir_fotograflar.zip'
        )
    
    except Exception as e:
        return f"Toplu işlem hatası: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)
