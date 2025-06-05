# AnimeGANv3 Hayao Video Stilizasyonu

Bu proje, **AnimeGANv3_Hayao_36.onnx** modelini kullanarak bir videoyu anime stiline dönüştüren üç aşamalı bir iş akışını gerçekleştirir:
1. Videoyu karelere ayırma
2. Her bir kareyi AnimeGANv3 modeli ile stillendirme
3. Stilize edilen kareleri tekrar birleştirerek anime tarzında bir video oluşturma

## 📌 İçindekiler

1. [Genel Bakış](#genel-bakış)  
2. [Özellikler](#özellikler)  
3. [Gereksinimler](#gereksinimler)  
4. [Kurulum](#kurulum)  
5. [Kullanım](#kullanım)  
   - 5.1 [1. Aşama: Video'yu Karelere Ayırma](#1-aşama-videoyu-karelere-ayırma)  
   - 5.2 [2. Aşama: Kareleri Stilize Etme](#2-aşama-kareleri-stilize-etme)  
   - 5.3 [3. Aşama: Stilize Edilen Kareleri Video'ya Dönüştürme](#3-aşama-stilize-edilen-kareleri-videoya-dönüştürme)  
6. [Proje Yapısı](#proje-yapısı)  
7. [Dosya Açıklamaları](#dosya-açıklamaları)  
8. [Gelişmiş Ayarlar](#gelişmiş-ayarlar)  

---

## 🔍 1. Genel Bakış

Bu proje, 3 dakikalık bir videoyu alıp her bir kareyi **AnimeGANv3_Hayao_36.onnx** modeli ile anime stiline dönüştürerek (stilize ederek), sonuçları tekrar birleştirip yeni bir anime tarzı video oluşturmayı amaçlar. İşlem adımları şunlardır:

1. **1. Aşama:** `_1_video_karelere_ayirma.py` script'i ile girdi videosunu tek tek karelere böler.
2. **2. Aşama:** `_2_model_ile_frame_stillendirme.py` script'i ile her bir kareyi **AnimeGANv3_Hayao_36.onnx** modeli kullanarak stilize eder.
3. **3. Aşama:** `_3_stillenmis_kareleri_birlestirerek_video_olusturma.py` script'i ile stilize edilen kareleri birleştirip yeni bir video dosyası oluşturur.

## ✨ 2. Özellikler

- **AnimeGANv3 Hayao Modeli Kullanımı:** ONNX biçimindeki `AnimeGANv3_Hayao_36.onnx` modeli ile resim stilizasyonu.
- **Otomatik İş Akışı:** Video → Kareler → Stilizasyon → Video çıktısı.
- **Kolay Uyarlanabilirlik:** Max boyut, kare uzantıları ve model yolu kolayca değiştirilebilir.
- **Hata Kontrolü:** Kare yoksa veya model yüklenemezse bilgilendirici hata mesajları.

## 🛠️ 3. Gereksinimler

- Python 3.7 veya üzeri  
- OpenCV (`opencv-python`)  
- NumPy  
- ONNX Runtime (`onnxruntime`)  
- `glob`, `os` gibi standart kütüphaneler (Python ile birlikte gelir)

### Gerekli Paketleri Yükleme

Terminal veya komut satırında projenin kök dizinindeyken:

```bash
pip install opencv-python numpy onnxruntime
```

## 🚀 4. Kurulum

1. **Projeyi Klonlayın veya İndirin**  
   ```bash
   git clone https://github.com/kullanici-adi/hayao-animegan-video-stylizer.git
   cd hayao-animegan-video-stylizer
   ```

2. **Model Dosyasını İndirin**  
   - `AnimeGANv3_Hayao_36.onnx` modelini [`models/`](models/) klasörüne yerleştirin.  
   - Dosya adı: `models/AnimeGANv3_Hayao_36.onnx`

3. **Videoyu Hazırlayın**  
   - İşlemek istediğiniz `outside_video.mp4` dosyasını `input/` klasörüne yerleştirin.  
   - Örnek: `input/outside_video.mp4`

4. **Çıkış Klasörlerini Oluşturun**  
   - Script'ler otomatik olarak ihtiyaç duyulan klasörleri oluşturacaktır (`output/frames_1`, `output/cartoonized_frames_1`, `output/cartoon_stylized_video`).

---

## 🎬 5. Kullanım

Her adımı sırasıyla çalıştırarak işlemi tamamlayabilirsiniz:

### 5.1. 1. Aşama: Video'yu Karelere Ayırma

```bash
python _1_video_karelere_ayirma.py
```
- **Açıklama:**  
  - `input/outside_video.mp4` dosyasını okur.  
  - Video karelerini `output/frames_1/` klasörüne `frame_0000.png, frame_0001.png, ...` şeklinde kaydeder.  

- **Önemli Değişkenler:**  
  - `video_path` (`input/outside_video.mp4`)  
  - `output_folder` (`output/frames_1/`)  

### 5.2. 2. Aşama: Kareleri Stilize Etme

```bash
python _2_model_ile_frame_stillendirme.py
```
- **Açıklama:**  
  - `output/frames_1/` klasöründeki `.png` kareleri sırasıyla `AnimeGANv3_Hayao_36.onnx` modeli ile stilize eder.  
  - Stilize edilen kareleri `output/cartoonized_frames_1/` klasörüne `.jpg` formatında kaydeder.  
  - Kareler, eğer boyutları `max_dimension=1024`'den büyükse yeniden boyutlandırılır ve genişlik/yükseklik 8'in katına yuvarlanır.  

- **Önemli Değişkenler:**  
  - `model_name` (`models/AnimeGANv3_Hayao_36`)  
  - `in_dir` (`output/frames_1`)  
  - `out_dir` (`output/cartoonized_frames_1`)  
  - `max_dimension` (Varsayılan: `1024`)  
  - `providers` (`['CPUExecutionProvider']`)

### 5.3. 3. Aşama: Stilize Edilen Kareleri Video'ya Dönüştürme

```bash
python _3_stillenmis_kareleri_birlestirerek_video_olusturma.py
```
- **Açıklama:**  
  - `output/cartoonized_frames_1/` klasöründeki `.jpg` kareleri alfabetik sırada okur.  
  - İlk kareden genişlik ve yükseklik değerlerini alarak `VideoWriter` nesnesi oluşturur (fps=30).  
  - Tüm kareleri `output/cartoon_stylized_video/3_dakikalik_cartoon_tarzi_video_dikey.mp4` dosyasına yazar.  

- **Önemli Değişkenler:**  
  - `input_folder` (`output/cartoonized_frames_1/`)  
  - `output_video_path` (`output/cartoon_stylized_video/3_dakikalik_cartoon_tarzi_video_dikey.mp4`)  

---

## 📁 6. Proje Yapısı

```
hayao-animegan-video-stylizer/
│
├── input/
│   └── outside_video.mp4           # İşlenecek giriş video dosyası
│
├── models/
│   └── AnimeGANv3_Hayao_36.onnx     # ONNX modeli
│
├── output/
│   ├── frames_1/                    # 1. aşamada oluşturulan ham kareler
│   │   ├── frame_0000.png
│   │   ├── frame_0001.png
│   │   └── ...
│   │
│   ├── cartoonized_frames_1/        # 2. aşamada oluşturulan stilize kareler
│   │   ├── frame_0000.jpg
│   │   ├── frame_0001.jpg
│   │   └── ...
│   │
│   └── cartoon_stylized_video/      # 3. aşamada oluşturulan anime tarzı video
│       └── 3_dakikalik_cartoon_tarzi_video_dikey.mp4
│
├── _1_video_karelere_ayirma.py      # 1. aşama: Video → Kareler
├── _2_model_ile_frame_stillendirme.py# 2. aşama: Kareleri AnimeGAN ile stilize et
├── _3_stillenmis_kareleri_birlestirerek_video_olusturma.py # 3. aşama: Kareleri → Video
├── requirements.txt                 # Gerekli Python paketleri
└── README.md                        # Bu doküman
```

---

## 📝 7. Dosya Açıklamaları

### `_1_video_karelere_ayirma.py`
- Videoyu karelere böler ve `output/frames_1/` klasörüne PNG formatında kaydeder.  
- Önemli Kütüphaneler: `cv2`, `os`.  
- Değişkenler:  
  - `video_path`: Giriş video dosyası yolu (varsayılan: `input/outside_video.mp4`)  
  - `output_folder`: Çıktı kare klasörü (varsayılan: `output/frames_1/`)  
  - Otomatik klasör oluşturma: `os.makedirs(output_folder, exist_ok=True)`

### `_2_model_ile_frame_stillendirme.py`
- ONNX Runtime ile `AnimeGANv3_Hayao_36.onnx` modelini yükler.  
- `output/frames_1/` klasöründeki kareleri okur, ön işlem (`process_image`) yapar ve model ile stilize eder.  
- Stilize edilmiş kareleri `output/cartoonized_frames_1/` klasörüne JPEG olarak kaydeder.  
- `max_dimension` ve 8'in katına yuvarlama parametreleri belleği korumak ve model uyumluluğu için kullanılır.  

### `_3_stillenmis_kareleri_birlestirerek_video_olusturma.py`
- `output/cartoonized_frames_1/` klasöründeki JPEG kareleri alfabetik sıralamayla okur.  
- İlk kare üzerinden video boyutlarını alarak `VideoWriter` oluşturur (Codec: `mp4v`, FPS: 30).  
- Tüm kareleri belirtilen `output_video_path` yoluna yazar ve işlemi tamamlar.

---

## ⚙️ 8. Gelişmiş Ayarlar

- **Video FPS Değiştirme:**  
  - `_3_stillenmis_kareleri_birlestirerek_video_olusturma.py` içindeki `fps` parametresini değiştirebilirsiniz (varsayılan: `30`).

- **Max Boyut (Hafıza Kontrolü):**  
  - `_2_model_ile_frame_stillendirme.py` içindeki `max_dimension` değerini ihtiyacınıza göre ayarlayabilirsiniz (örneğin: `512` veya `2048`).

- **Çıktı Formatı:**  
  - Kare kaydetme (`cv.imwrite`) fonksiyonuna farklı format (PNG, BMP) verme esnekliği vardır.  
  - Video kodlayıcıyı (`VideoWriter_fourcc`) istediğiniz başka bir codec ile değiştirebilirsiniz (örneğin: `'XVID'`, `'H264'`).

