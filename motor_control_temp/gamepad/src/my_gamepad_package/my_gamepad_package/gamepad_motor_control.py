import evdev
from evdev import InputDevice, categorize, ecodes
import serial
import time
# Gamepad ve Arduino'ya bağlı motorlar
gamepad = InputDevice('/dev/input/event0')
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)

# Başlangıç hız ve yön değerleri
motor1_speed = 127
motor1_speed1=127
motor1_direction = "stop"
motor2_speed = 127
motor2_speed1=127
motor2_direction = "stop"

# Motor hızlarını ve yönlerini kontrol eden işlev
def control_motors(motor1_speed, motor1_direction, motor2_speed, motor2_direction):
    # Arduino'ya gönderilen komutun doğru formatta olup olmadığını kontrol edelim
    command = f'{motor1_speed1},{motor1_speed},{motor1_direction},{motor2_speed1},{motor2_speed},{motor2_direction}\n'
    print(f'Gönderilen komut: {command}')  # Debugging için komutu yazdır
    arduino.write(command.encode())
    time.sleep(0.05)
# Gamepad'den gelen verileri sürekli oku ve motor kontrolünü sağla
for event in gamepad.read_loop():
    if event.type == ecodes.EV_ABS:
        # Motor 1 kontrolü (Sol Joystick)
        if event.code == ecodes.ABS_X:  # Sol joystick yatay ekseni
            motor1_direction = "left" if event.value < 0 else "right" if event.value > 0 else "stop"
            motor1_speed1 = int((event.value + 32768) * 255 / 65535)  # 0-255 arasında hız
        elif event.code == ecodes.ABS_Y:  # Sol joystick dikey ekseni
            motor1_speed = int((event.value + 32768) / 256)  # 0-255 aralığında hız

        # Motor 2 kontrolü (Sağ Joystick)
        if event.code == ecodes.ABS_RX:  # Sağ joystick yatay ekseni
            motor2_direction = "left" if event.value < 0 else "right" if event.value > 0 else "stop"
            motor2_speed1 = int((event.value + 32768) * 255 / 65535)  # 0-255 arasında hız
        elif event.code == ecodes.ABS_RY:  # Sağ joystick dikey ekseni
            motor2_speed = int((event.value + 32768) / 256)  # 0-255 aralığında hız

        # Motor kontrol fonksiyonunu çağırın
        control_motors(motor1_speed, motor1_direction, motor2_speed, motor2_direction)

    # Düğmelere basıldığında tepki ver
    if event.type == ecodes.EV_KEY:
        if event.code == ecodes.BTN_SOUTH and event.value == 1:  # A butonuna basıldığında
            print("A butonuna basıldı!")
            control_motors(0, "stop", 0, "stop")  # Her iki motoru durdur
