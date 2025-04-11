import socket
from clickhouse_driver import Client

def check_ports():
    hosts = ['clickhouse01', 'clickhouse02', 'clickhouse03', 'clickhouse04']
    for host in hosts:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, 9000))
            print(f"✅ {host}:9000 - доступен")
        except Exception as e:
            print(f"❌ {host}:9000 - ошибка: {str(e)}")
        finally:
            s.close()

def try_clickhouse_connection():
    try:
        client = Client(
            host='clickhouse01',
            port=9000,
            user='admin',
            password='password123',
            connect_timeout=5
        )
        print("Подключение успешно:", client.execute("SELECT 1"))
    except Exception as e:
        print("Ошибка подключения:", str(e))

if __name__ == "__main__":
    print("Проверка портов:")
    check_ports()
    print("\nПопытка подключения к ClickHouse:")
    try_clickhouse_connection()