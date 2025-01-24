import cv2

# Inisialisasi kamera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    # Baca frame dari kamera
    ret, frame = cam.read()
    if not ret:
        print("Gagal membaca frame dari kamera.")
        break

    # Menghilangkan efek mirror
    frame = cv2.flip(frame, 1)  # 1 = Flip horizontal

    # Konversi ke HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    # Posisi pusat frame
    cx = int(width / 2)
    cy = int(height / 2)

    # Mengambil nilai dari pixel warna di pusat
    pixel_center = hsv_frame[cy, cx]
    hue = pixel_center[0]
    saturation = pixel_center[1]
    value = pixel_center[2]

    # Identifikasi warna berdasarkan nilai HSV
    color = "Tak Terdeteksi"
    if hue == 0 or saturation == 0:
        color = "PUTIH"
    elif value < 50:
        color = "HITAM"
    elif saturation < 50:
        color = "ABU-ABU"
    elif hue < 5:  # 0 < Merah < 5
        color = "MERAH"
    elif hue < 20:  # 5 < Orange < 20
        color = "ORANGE"
    elif hue < 30:  # 20 < Kuning < 30
        color = "KUNING"
    elif hue < 70:  # 30 < Hijau < 70
        color = "HIJAU"
    elif hue < 125:  # 70 < Biru < 125
        color = "BIRU"
    elif hue < 145:  # 125 < Ungu < 145
        color = "UNGU"
    elif hue < 170:  # 145 < Pink < 170
        color = "PINK"
    else:
        color = "MERAH"

    # Tampilkan warna di layar
    pixel_center_bgr = frame[cy, cx]
    b = int(pixel_center_bgr[0])
    g = int(pixel_center_bgr[1])
    r = int(pixel_center_bgr[2])

    cv2.putText(frame, color, (cx - 100, cy - 150), 0, 1.5, (b, g, r), 8)
    cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)

    # Tampilkan hasil frame
    cv2.imshow("Program Pengenalan Warna", frame)

    # Keluar dari program jika tombol ESC ditekan
    key = cv2.waitKey(1)
    if key == 27:
        break

# Tutup kamera dan jendela
cam.release()
cv2.destroyAllWindows()
