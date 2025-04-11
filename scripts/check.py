import socket

def check_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            result = s.connect_ex((host, port))
            if result == 0:
                print(f"Порт {port} на {host} доступен")
            else:
                print(f"Порт {port} на {host} недоступен. Код ошибки: {result}")
    except Exception as e:
        print(f"Ошибка при проверке порта: {e}")

check_port("clickhouse01", 9000)
check_port("clickhouse01", 8123)