# 📸 Instagram Fotoğraf Düzenleyici

Instagram'a yüklenecek fotoğrafları otomatik olarak 4:5 oranına dönüştüren modern masaüstü uygulaması.

## ✨ Özellikler

- 🎯 **Otomatik 4:5 Oran Dönüştürme**: Instagram'ın portrait formatına uygun
- 🖼️ **Çoklu Format Desteği**: JPEG ve PNG çıktı seçenekleri
- 📦 **Toplu İşlem**: Birden fazla fotoğrafı aynı anda işleyebilme
- 🎨 **Modern UI**: Kullanıcı dostu ve güzel arayüz
- 💻 **Masaüstü Uygulaması**: Web tarayıcısı gerektirmez
- 📊 **Progress Bar**: İşlem ilerlemesi takibi
- 🎪 **Beyaz Padding**: Orijinal fotoğraf kesilmez, yanları beyaz alanla doldurulur

## 🚀 Kurulum

### Gereksinimler
- Python 3.7+
- Pip paket yöneticisi

### Bağımlılıklar
```bash
pip install flask pillow eel werkzeug
```

## 💻 Kullanım

### Web Uygulaması Olarak
```bash
python app.py
```
Tarayıcınızda `http://localhost:5000` adresine gidin.

### Masaüstü Uygulaması Olarak
```bash
python desktop_app.py
```
Otomatik olarak masaüstü penceresi açılacak.

## 📱 Özellikler Detayı

### Tek Fotoğraf İşleme
- Bir fotoğraf seçin
- JPEG veya PNG formatını seçin
- "Dönüştür ve İndir" butonuna tıklayın

### Toplu Fotoğraf İşleme
- Birden fazla fotoğraf seçin (Ctrl + tıklama)
- Format seçin
- ZIP dosyası olarak toplu indirin

## 🏗️ Proje Yapısı

```
instagram-fotograf-duzenleyici/
├── app.py                 # Flask web uygulaması
├── desktop_app.py        # Eel masaüstü uygulaması
├── web/
│   └── index.html        # Frontend arayüzü
├── dist/
│   └── InstagramHazirlayici.exe  # Derlenmiş EXE
└── README.md
```

## 🎯 Nasıl Çalışır?

1. **Oran Hesaplama**: Orijinal fotoğrafın en-boy oranını kontrol eder
2. **Padding Ekleme**: 4:5 oranına ulaşmak için gerekli beyaz alanları ekler
3. **Format Dönüştürme**: Seçilen formatta (JPEG/PNG) kayıt eder
4. **Otomatik İndirme**: İşlenmiş dosyayı kullanıcıya sunar

## 🛠️ Teknik Detaylar

- **Backend**: Python Flask / Eel
- **Frontend**: HTML5, CSS3, JavaScript
- **Görüntü İşleme**: PIL (Pillow)
- **UI Framework**: Modern CSS Grid/Flexbox
- **İkonlar**: Font Awesome 6

## 📦 EXE Olarak Derleme

### Web Uygulaması için:
```bash
pyinstaller --onefile --name=InstagramHazirlayici app.py
```

### Masaüstü Uygulaması için:
```bash
pyinstaller --onefile --windowed --add-data "web;web" desktop_app.py
```

## 🎨 Ekran Görüntüleri

- Modern gradient arka plan
- Instagram renk teması
- Drag & drop dosya yükleme
- Progress bar ile işlem takibi
- Responsive tasarım

## 📝 Lisans

Bu proje MIT lisansı altında yayınlanmıştır.

## 👨‍💻 Geliştirici

**iglthedev** - Instagram Fotoğraf Düzenleyici

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📞 İletişim

- GitHub: [@iglthedev](https://github.com/iglthedev)
- Proje Link: [https://github.com/iglthedev/instagram-fotograf-duzenleyici](https://github.com/iglthedev/instagram-fotograf-duzenleyici)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 