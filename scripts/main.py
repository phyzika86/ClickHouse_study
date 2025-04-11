"""
Модуль основных функций для подключения к ClickHouse, создания таблиц и наполнении их данными
"""
import time
from clickhouse_driver import Client

def connect_clickhouse(max_retries=5, retry_delay=3):
    for i in range(max_retries):
        try:
            client = Client(
                host='clickhouse',
                port=9000,  # Явно указываем порт
                user='admin',
                password='password123',
                connect_timeout=10,  # Таймаут подключения
                settings={'max_execution_time': 3600}  # Увеличиваем таймаут выполнения
            )
            # Проверяем подключение
            client.execute('SELECT 1')
            return client
        except Exception as e:
            print(f"Попытка {i + 1}/{max_retries}: Ошибка подключения - {str(e)}")
            if i < max_retries - 1:
                time.sleep(retry_delay)
    raise ConnectionError("Не удалось подключиться к ClickHouse")


def connect_cluster_clickhouse(max_retries=5, retry_delay=3):
    # Список нод для подключения (в правильном формате)
    hosts = [
        ('clickhouse01', 9000),
        ('clickhouse02', 9000),
        ('clickhouse03', 9000),
        ('clickhouse04', 9000)
    ]

    for i in range(max_retries):
        for host, port in hosts:
            try:
                client = Client(
                    host=host,
                    port=port,
                    user='admin',
                    password='password123',
                    connect_timeout=10,
                    settings={
                        'connect_timeout': 10,
                        'send_receive_timeout': 30,
                        'distributed_connections_pool_size': 4
                    }
                )
                # Проверка подключения
                client.execute('SELECT 1')
                print(f"Успешное подключение к {host}:{port}")
                return client
            except Exception as e:
                print(f"Попытка {i + 1}/{max_retries}: Ошибка подключения к {host}:{port} - {str(e)}")
                if i < max_retries - 1:
                    time.sleep(retry_delay)

    raise ConnectionError(f"Не удалось подключиться ни к одной ноде после {max_retries} попыток")


def load_data(client, query):
    print("Начало загрузки данных...")
    start_time = time.time()

    try:
        progress = client.execute_with_progress(query)

        for num_rows, total_rows in progress:
            elapsed = time.time() - start_time
            rows_per_sec = num_rows / elapsed if elapsed > 0 else 0
            print(f"\rПрогресс: {num_rows}/{total_rows} строк | "
                  f"{num_rows / 1000:.1f}k | "
                  f"Скорость: {rows_per_sec / 1000:.1f}k строк/сек", end="", flush=True)

        print(f"\nЗагрузка завершена за {time.time() - start_time:.2f} секунд")
        return True

    except Exception as e:
        print(f"\nОшибка при загрузке: {e}")
        return False


def create_table(client, ddl):
    try:
        client.execute(ddl)
        print(f"Таблица {ddl} успешно создана или уже существует")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")
        raise


def create_cluster_tables(client, local_ddl, distributed_ddl):
    try:
        print("Создание локальной таблицы...")
        client.execute(local_ddl)
        print("Создание распределенной таблицы...")
        client.execute(distributed_ddl)
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")
        raise
