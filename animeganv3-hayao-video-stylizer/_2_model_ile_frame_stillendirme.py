# 2_model_ile_frame_stillendirme.py

import onnxruntime as ort    # ONNX modellerini çalıştırmak için onnxruntime kütüphanesini içe aktarır
import cv2 as cv
import numpy as np
import os
from glob import glob        # Belirli bir desenle dosya listesini almak için glob
import time

# ——————————— Yapılandırma Kısmı ———————————
pic_form = ['.jpeg', '.jpg', '.png', '.JPEG', '.JPG', '.PNG']  # Desteklenen resim uzantıları
providers = ['CPUExecutionProvider']                           # ONNX modelini hangi sağlayıcıda çalıştıracağımız
model_name = 'models/AnimeGANv3_Hayao_36'                      # Model dosyasının yolu
in_dir = 'output/frames_1'                                     # Stilize edilecek orijinal karelerin bulunduğu klasör
out_dir = 'output/cartoonized_frames_1'                        # Stilize edilmiş karelerin kaydedileceği klasör
max_dimension = 1024  # İşlem sırasında en uzun kenarın alacağı maksimum boyut (bellek koruma amaçlı)

# Girdi ve çıktı klasörlerini oluştur (zaten varsa hata verme)
os.makedirs(in_dir, exist_ok=True)
os.makedirs(out_dir, exist_ok=True)

# ONNX modelini yükle ve oturum (session) oluştur
session = ort.InferenceSession(f'{model_name}.onnx', providers=providers)


def process_image(img, x8=True):
    """
    Ham bir BGR görüntüsünü modele uygun hale getirir:
    - Çok büyükse yeniden boyutlandırma (max_dimension ile sınırlı)
    - (isteğe bağlı) genişlik/yüksekliği 8'in katına yuvarlama
    - BGR -> RGB çevirme ve piksel değerlerine [-1, +1] ölçeği uygulama
    """
    h, w = img.shape[:2]
    # 1) Büyük resimleri küçült: bellek kullanımını azaltmak için
    if max(h, w) > max_dimension:
        scale = max_dimension / max(h, w)
        new_h, new_w = int(h * scale), int(w * scale)
        img = cv.resize(img, (new_w, new_h))
        print(f"Resized image from {w}x{h} to {new_w}x{new_h} to save memory")

    # 2) Genişlik ve yüksekliği 8'in katına yuvarla (x8=True ise)
    h, w = img.shape[:2]
    if x8:
        def to_8s(x):
            # 256'dan küçükse 256, aksi takdirde en yakın alt 8 katına yuvarla
            return 256 if x < 256 else x - x % 8

        img = cv.resize(img, (to_8s(w), to_8s(h)))

    # 3) BGR -> RGB çevir, float32’e dönüştür ve [-1, +1] aralığına ölçekle
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB).astype(np.float32) / 127.5 - 1.0
    # Model girişi olarak kullanmak için batch boyutu ekseni ekle
    return img


def load_test_data(image_path):
    """
    Bir resim dosyasını yükler, orijinal boyutlarını saklar,
    process_image ile dönüştürür ve modele girdi formatına hazırlar.
    """
    try:
        img0 = cv.imread(image_path)  # Resmi oku (BGR)
        if img0 is None:
            # Okuma başarısızsa hata fırlat
            raise Exception(f"Failed to load image: {image_path}")

        original_dimensions = img0.shape[:2]  # (yükseklik, genişlik) olarak kaydet

        # Görüntüyü ön işleme (yeniden boyutlandırma ve ölçekleme)
        img = process_image(img0)
        img = np.expand_dims(img, axis=0)    # Model için batch boyutu ekle

        return img, original_dimensions
    except Exception as e:
        print(f"Error loading image: {e}")
        raise


def convert(img, scale):
    """
    İşlenmiş görüntüyü ONNX modelinden geçirir,
    çıktı tensörünü uygun piksel aralığına dönüştürür
    ve orijinal boyutlara resize eder.
    """
    try:
        # Modelin ilk girdi tensörünün adını al
        input_name = session.get_inputs()[0].name
        # Model çalıştırma
        fake_img = session.run(None, {input_name: img})[0]

        # Çıktıyı [-1, +1] -> [0, 255] aralığına, uint8 tipine çevir
        images = (np.squeeze(fake_img) + 1.0) / 2.0 * 255
        images = np.clip(images, 0, 255).astype(np.uint8)

        # Orijinal boyutlara geri döndür (scale: (h, w) tuple)
        output_image = cv.resize(images, (scale[1], scale[0]))
        # RGB -> BGR çevir, böylece cv.imwrite doğru renkte kaydeder
        return cv.cvtColor(output_image, cv.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error converting image: {e}")
        raise


def process_directory():
    """
    Belirtilen girdi klasöründeki tüm resimleri sırayla modelden geçirir,
    çıktı klasörüne JPEG formatında kaydeder.
    """
    print(f"Processing images from {in_dir} to {out_dir}")
    # Klasördeki dosyaları al ve uzantıya göre filtrele
    in_files = sorted(glob(f'{in_dir}/*'))
    in_files = [x for x in in_files if os.path.splitext(x)[-1].lower() in pic_form]

    if not in_files:
        print(f"No images found in {in_dir}. Please add some images and try again.")
        return

    # Her bir resmi işleme döngüsü
    for i, img_path in enumerate(in_files):
        print(f"Processing {i + 1}/{len(in_files)}: {img_path}")
        start_time = time.time()

        try:
            # Çıktı dosya adını .jpg olarak oluştur
            base_name = os.path.basename(img_path).split('.')[0]
            out_name = f"{out_dir}/{base_name}.jpg"

            # Resmi yükle ve ön işle
            mat, scale = load_test_data(img_path)
            # Modelden geçir ve stilize sonucu al
            res = convert(mat, scale)
            # JPEG olarak kaydet
            cv.imwrite(out_name, res)

            elapsed = time.time() - start_time
            print(f"Saved to {out_name} (took {elapsed:.2f} seconds)")
        except Exception as e:
            print(f"Failed to process {img_path}: {e}")

    print(f"All done! Processed {len(in_files)} images.")


if __name__ == "__main__":
    # Süreci başlat
    process_directory()
    # Kullanım talimatları
    print(f"\nBu Kodu Kullanabilmek İçin:")
    print(f"1-) Videoyu Frame'lerine ayırın.")
    print(f"2-) Model ile Tüm Video Frame'lerini Stilize Edin.")
    print(f"3-) Stilize Edilmiş Frame'leri Birleştirerek Video Oluşturun.")
