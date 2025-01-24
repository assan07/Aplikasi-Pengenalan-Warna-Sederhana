import cv2
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import csv
import os


#hzn_lly
# Fungsi untuk menyimpan data ke file CSV
def save_to_csv(data, filename='dataset_warna.csv'):
    file_exists = os.path.isfile(filename)  # Periksa apakah file sudah ada
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Tambahkan header jika file belum ada
            writer.writerow(['Hue', 'Saturation', 'Value', 'Color'])
        writer.writerow(data)

# Cek apakah file CSV ada, jika tidak buat DataFrame kosong
if os.path.exists('dataset_warna.csv'):
    data = pd.read_csv('dataset_warna.csv', header=None, names=['Hue', 'Saturation', 'Value', 'Color'])
    print(f"Dataset terbaca dengan {len(data)} baris.")
else:
    print("File CSV tidak ditemukan.")
    data = pd.DataFrame(columns=['Hue', 'Saturation', 'Value', 'Color'])

# Menampilkan beberapa baris pertama untuk memverifikasi data
print("Beberapa data awal:")
print(data.head())  # Menampilkan 5 baris pertama


# Inisialisasi model k-NN dan variabel pelatihan
knn = None
X_train, X_test, y_train, y_test = None, None, None, None
accuracy = None  # Menyimpan akurasi untuk ditampilkan

#hzn_lly

# Inisialisasi kamera
cam = cv2.VideoCapture(0)  # Coba ganti dengan 1 atau 2 jika kamera default tidak bekerja
if not cam.isOpened():
    print("Kamera tidak dapat dibuka. Pastikan kamera terhubung dan tidak digunakan oleh aplikasi lain.")
    exit()  # Keluar jika kamera gagal dibuka
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Mapping warna untuk teks
color_map = {
    "PUTIH": (255, 255, 255),  # White
    "HITAM": (0, 0, 0),        # Black
    "ABU-ABU": (169, 169, 169),  # Gray
    "MERAH": (0, 0, 255),      # Red
    "ORANGE": (0, 165, 255),   # Orange
    "KUNING": (0, 255, 255),   # Yellow
    "HIJAU": (0, 255, 0),      # Green
    "BIRU": (255, 0, 0),       # Blue
    "UNGU": (255, 0, 255),     # Purple
    "PINK": (255, 192, 203)    # Pink
}

# Jika dataset sudah cukup (misalnya 10 data), latih model k-NN
if len(data) > 6 and knn is None:
    print("Melatih model...")

    # Membaca data dari file CSV
    data = pd.read_csv('dataset_warna.csv', header=None, names=['Hue', 'Saturation', 'Value', 'Color'])
    X = data[['Hue', 'Saturation', 'Value']]
    y = data['Color']

    # Membagi data untuk pelatihan dan pengujian
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Membuat dan melatih model k-NN
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)

    # Evaluasi model
    accuracy = knn.score(X_test, y_test)
    print(f'Akurasi Model: {accuracy * 100:.2f}%')  # Menampilkan akurasi model
else:
    print("Data tidak cukup untuk melatih model.")   

while True:
    ret, frame = cam.read()
    if not ret:
        print("Gagal membaca frame.")
        break

    print("Frame dibaca.")  # Menambahkan log untuk memastikan frame terbaca dengan benar

    # Menghilangkan efek mirror
    frame = cv2.flip(frame, 1)

    # Konversi ke HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    # Ambil pixel di tengah-tengah gambar
    cx, cy = width // 2, height // 2
    pixel_center = hsv_frame[cy, cx]
    
    # Ambil nilai HSV
    hue = int(pixel_center[0])
    saturation = int(pixel_center[1])
    value = int(pixel_center[2])
    print(f"Hue: {hue}, Saturation: {saturation}, Value: {value}")

    # Prediksi warna menggunakan model k-NN jika sudah dilatih
    #hzn_lly
    if hue == 0 or saturation == 0:
        predicted_color = "PUTIH"
    elif value < 50:
        predicted_color = "HITAM"
    elif saturation < 50:
        predicted_color = "ABU-ABU"
    elif hue < 5:  # 0 < Merah < 5
        predicted_color = "MERAH"
    elif hue < 20:  # 5 < Orange < 20
        predicted_color = "ORANGE"
    elif hue < 30:  # 20 < Kuning < 30
        predicted_color = "KUNING"
    elif hue < 70:  # 30 < Hijau < 70
        predicted_color = "HIJAU"
    elif hue < 125:  # 70 < Biru < 125
        predicted_color = "BIRU"
    elif hue < 145:  # 125 < Ungu < 145
        predicted_color = "UNGU"
    elif hue < 170:  # 145 < Pink < 170
        predicted_color = "PINK"
    else:
        predicted_color = "MERAH"
    
    # Menyimpan data (HSV + label warna) ke dalam CSV
    data = [hue, saturation, value, predicted_color]
    save_to_csv(data)

    # Mendapatkan warna BGR sesuai dengan prediksi warna
    text_color = color_map.get(predicted_color, (255, 255, 255))  # Default ke putih jika warna tidak ditemukan

    # Tampilkan label warna dengan warna yang sesuai
    cv2.putText(frame, predicted_color, (cx - 100, cy - 150), 0, 1.5, text_color, 8)
    cv2.circle(frame, (cx, cy), 5, text_color, -1)

    # Tampilkan akurasi jika model sudah dilatih
    if accuracy is not None:
        accuracy_text = f"Akurasi: {accuracy * 100:.2f}%"
        print(f"Akurasi Model: {accuracy * 100:.2f}%")  # Tampilkan juga di terminal
        cv2.putText(frame, accuracy_text, (width - 400, height - 50), 0, 1, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "Data tidak cukup untuk melatih model..", (width - 500, height - 30), 0, 1, (0, 0, 255), 2)

    # Tampilkan frame
    cv2.imshow("Pengenalan Warna (Machine Learning)", frame)

           
    # Tekan 'q' untuk keluar dari aplikasi
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Tutup kamera dan jendela
cam.release()
cv2.destroyAllWindows()
