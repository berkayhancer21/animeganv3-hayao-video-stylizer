# 1_video_karelere_ayirma.py

import cv2 as cv
import os             # Dosya ve klasör işlemleri için os modülünü içe aktarır

# İşlenecek video dosyasının yolu
video_path = 'input/outside_video.mp4'

# Karelerin kaydedileceği çıktı klasörü
output_folder = 'output/frames_1/'

# Eğer çıktı klasörü yoksa oluştur (exist_ok=True: zaten varsa hata fırlatma)
os.makedirs(output_folder, exist_ok=True)

# Video dosyasını okumak için VideoCapture nesnesi oluştur
cap = cv.VideoCapture(video_path)

# Videonun kare/saniye değerini (FPS) al
frame_rate = cap.get(cv.CAP_PROP_FPS)

# Kaydedilen kare sayısını takip etmek için sayaç
frame_count = 0

# Döngü: Videodaki tüm kareleri okur ve kaydeder
while True:
    # Bir sonraki kareyi oku
    ret, frame = cap.read()
    # Okuma başarısızsa (video sonu), döngüyü sonlandır
    if not ret:
        break

    # Kaydedilecek kare dosya yolunu oluştur
    # Örneğin: output/frames_1/frame_0000.png, frame_0001.png, ...
    frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.png')

    # Kareyi diske PNG formatında yaz
    cv.imwrite(frame_filename, frame)

    # Kare sayacını bir artır
    frame_count += 1

# İşlem bitince VideoCapture nesnesini kapat ve kaynakları serbest bırak
cap.release()
