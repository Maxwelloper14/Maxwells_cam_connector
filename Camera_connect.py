import cv2
import requests
import socket
import threading

# Функция для поиска IP-камер в сети
def scan_ip_cameras(network):
    cameras = []
    for i in range(1, 255):
        ip = f"{network}.{i}"
        try:
            # Проверяем доступность порта RTSP
            socket.create_connection((ip, 554), timeout=1)
            cameras.append(ip)
        except (socket.timeout, ConnectionRefusedError):
            continue
    return cameras

# Функция для подключения и отображения видео с камеры
def display_camera_feed(ip):
    rtsp_url = f"rtsp://{ip}/stream"  # Проверьте правильный путь к потоку
    cap = cv2.VideoCapture(rtsp_url)

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Не удалось получить изображение с {ip}")
            break

        cv2.imshow(f"Камера: {ip}", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Основной код
if __name__ == "__main__":
    network_prefix = "192.168.1"  # Замените на ваш сетевой префикс
    cameras = scan_ip_cameras(network_prefix)

    if cameras:
        print("Найденные камеры:")
        # Создание и запуск потоков для каждой камеры
        threads = []
        for camera in cameras:
            print(camera)
            thread = threading.Thread(target=display_camera_feed, args=(camera,))
            thread.start()
            threads.append(thread)

        # Дождаться завершения всех потоков
        for thread in threads:
            thread.join()
    else:
        print("Камеры не найдены.")