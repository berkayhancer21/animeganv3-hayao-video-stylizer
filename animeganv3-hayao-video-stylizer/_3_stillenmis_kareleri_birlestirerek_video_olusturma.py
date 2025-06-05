# 3_stillenmis_kareleri_birlestirerek_video_olusturma.py

import cv2 as cv
import os

# Stilize edilmiş karelerin bulunduğu klasör yolu
input_folder = 'output/cartoonized_frames_1/'

# Oluşturulacak video dosyasının tam yolu
output_video_path = 'output/cartoon_stylized_video/3_dakikalik_cartoon_tarzi_video_dikey.mp4'

# --- Video boyutlarını belirlemek için ilk kareyi oku ---
# Klasördeki dosyalardan ilkini al (alfabetik sıraya göre)
frame_filename = os.listdir(input_folder)[0]
# Dosya yolunu birleştir
frame_path = os.path.join(input_folder, frame_filename)
# Kareyi diskten oku
frame = cv.imread(frame_path)

# Okuğun kare üzerinden yükseklik ve genişlik değerlerini al
# frame.shape bize (yükseklik, genişlik, kanal_sayısı) döner
height, width, _ = frame.shape

# --- VideoWriter (video yazıcı) oluşturma ---
# Dört karakterli codec kodunu oluştur ('mp4v' genellikle H.264 mp4 için kullanılır)
fourcc = cv.VideoWriter_fourcc(*'mp4v')
# VideoWriter nesnesini oluştur:
#   - Çıktı dosya yolu
#   - Codec
#   - FPS (Frame per second) = 30
#   - Video çerçeve boyutu = (width, height)
video_writer = cv.VideoWriter(output_video_path, fourcc, 30, (width, height))

# --- Tüm stilize edilmiş kareleri videoya ekleme ---
# input_folder içindeki dosyaları alfabetik sırada gezer
for frame_filename in sorted(os.listdir(input_folder)):
    # Yalnızca .jpg uzantılı dosyaları işle
    if frame_filename.endswith('.jpg'):
        # Her dosya için tam yol oluştur
        frame_path = os.path.join(input_folder, frame_filename)
        # Kareyi oku
        frame = cv.imread(frame_path)
        # Kareyi video akışına ekle
        video_writer.write(frame)

# --- Video dosyasını finalize et / serbest bırak ---
video_writer.release()

# İşlem tamamlandığında bilgi mesajı yazdır
print(f"Video başarıyla oluşturuldu: {output_video_path}")
