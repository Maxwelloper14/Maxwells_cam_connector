import socket
import cv2
import numpy as np
from colored import fore, back, style

def search_cameras():
    # Здесь вы можете добавить создание сетевого пакета для поиска видеокамер
    # Это будет в значительной степени зависеть от типа используемых вами камер
    # Для данного примера мы просто симулируем, что нашли камеру
    return [("192.168.1.10", "Camera 1"), ("192.168.1.11", "Camera 2")]

def connect_to_camera(ip):
    # Открытие видеопотока с камеры
    stream_url = f"http://{ip}/video"  # URL потока может варьироваться!
    cap = cv2.VideoCapture(stream_url)
    
    if not cap.isOpened():
        print(f"Не удается подключиться к камере по адресу {ip}")
        return False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр")
            break

        cv2.imshow(f"Камера: {ip}", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Нажмите 'q' для выхода
            break

    cap.release()
    cv2.destroyAllWindows()
    return True

def main_menu():
    print(fore.RED + "Добро пожаловать в видеонаблюдение!" + style.reset)
    print("=" * 40)
    print("1. Искать камеры")
    print("2. Выход")
    
    choice = input("Выберите пункт меню (1-2): ")
    return choice

def main():
    while True:
        choice = main_menu()
        
        if choice == '1':
            print("Поиск камер...")
            cameras = search_cameras()
            if cameras:
                print("Найдены камеры:")
                for idx, (ip, name) in enumerate(cameras):
                    print(f"{idx + 1}. {name} - {ip}")
                
                camera_choice = input("Выберите камеру для подключения (номер): ")
                try:
                    camera_index = int(camera_choice) - 1
                    if 0 <= camera_index < len(cameras):
                        connect_to_camera(cameras[camera_index][0])
                    else:
                        print("Неверный номер камеры")
                except ValueError:
                    print("Пожалуйста, введите номер корректно.")
            else:
                print("Камеры не найдены.")
        
        elif choice == '2':
            print("Выход из программы.")
            break
        
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == '__main__':
    main()