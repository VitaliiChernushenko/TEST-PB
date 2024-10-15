import oracledb
import pandas as pd
import csv
import boto3
import io
import docker
import time
import sys

def get_container_ip(container_name):
    client = docker.from_env()
    
    try:
        container = client.containers.get(container_name)
        
        # Получаем информацию о сетевых настройках
        networks = container.attrs['NetworkSettings']['Networks']
        for network_name, network_info in networks.items():
            ip_address = network_info['IPAddress']
            print(f"Контейнер {container_name} находится в сети '{network_name}' с IP-адресом: {ip_address}")
            return ip_address
        
    except docker.errors.NotFound:
        print(f"Контейнер {container_name} не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")


def get_container_hostname(container_name):
    # Инициализация клиента Docker
    client = docker.from_env()

    try:
        # Получение контейнера по имени
        container = client.containers.get(container_name)
        
        # Извлечение hostname из конфигурации контейнера
        hostname = container.attrs['Config']['Hostname']
        return hostname

    except docker.errors.NotFound:
        return f"Контейнер '{container_name}' не найден."
    except Exception as e:
        return f"Произошла ошибка: {e}"
    
def check_oracle_data_ready(conn, timeout=300):
    #Проверяет, загружены ли данные в таблицу VITALII.PURCHASES.
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM VITALII.PURCHASES")
                result = cursor.fetchone()
                if result and result[0] > 0:
                    print(f"Данные загружены: {result[0]} записей.")
                    return True
                else:
                    print("Данные еще не загружены. Ждем...")
        except oracledb.DatabaseError as e:
            print(f"Ошибка при проверке данных: {e}")
        time.sleep(10)  # Ждем перед повторной проверкой

    raise TimeoutError("Данные не загрузились в течение времени ожидания.")    

def main():
    # Пример использования
    #hostname1 = get_container_hostname("oracle-db1")
    #hostname2 = get_container_hostname("oracle-db2")
    hostname1 = get_container_ip("oracle-db1")
    hostname2 = get_container_ip("oracle-db2")
    usrname = 'vitalii'
    usrpswd = 'vitalii'
    dbsname = 'xepdb1'
    dbportn = 1521

    print(f"hostname1={hostname1} hostname2={hostname2}")
    # Включение режима Thin
    #oracledb.init_oracle_client(lib_dir=None)
    if oracledb.is_thin_mode:
        print("Тонкий режим активен")
    else:
        print("Толстый режим активен")
    # Подключение к первому экземпляру
    dsnPb1 = oracledb.makedsn(hostname1, dbportn, service_name=dbsname)  # Укажите хост, порт и сервис
    dsnPb2 = oracledb.makedsn(hostname2, dbportn, service_name=dbsname)  # Укажите хост, порт и сервис
    
    cnt = 3
    while cnt > 0:
        try:
            connPb1 = oracledb.connect(
                user=usrname, 
                password=usrpswd, 
                dsn=dsnPb1
            )
            print('connection Pb1 - OK')
            # Подключение ко второму экземпляру
            connPb2 = oracledb.connect(
                user=usrname, 
                password=usrpswd, 
                dsn=dsnPb2
            )
            cnt = 0
            print('connection Pb2 - OK') 
        except Exception as e:
           cnt -=1
           time.sleep(100)
           print(f"Осталось {cnt} попыток")     

    # Проверяем доступность данных
    if check_oracle_data_ready(connPb2):
        print("Продолжаем выполнение скрипта...")
        # Основная логика Python-кода
    else:
        print("Ошибка: данные не были загружены.")
        sys.exit(0)

    try:
        # Выполнение SQL-запроса 1
        cursorPb1 = connPb1.cursor()
        queryPb1 = "SELECT CL_ID, CL_FIO FROM VITALII.REFCLIENTS"
        cursorPb1.execute(queryPb1)
    

        # Выполнение SQL-запроса 2
        cursorPb2 = connPb2.cursor()
        queryPb2 = """SELECT CL_ID,
                 MAX (AMOUNT) KEEP (DENSE_RANK FIRST ORDER BY AMOUNT DESC)
                     AS MAX_AMOUNT,
                 MAX (ADATE) KEEP (DENSE_RANK FIRST ORDER BY AMOUNT DESC)
                     AS MAX_ADATE
            FROM VITALII.PURCHASES
            WHERE ADATE  > ADD_MONTHS(TRUNC(SYSDATE),-1)
            GROUP BY CL_ID"""
        cursorPb2.execute(queryPb2)

        dataPb1 = cursorPb1.fetchall()
        dataPb2 = cursorPb2.fetchall()

        # Преобразование данных в DataFrame для удобства работы
        dfPb1 = pd.DataFrame(dataPb1, columns=['id', 'fio'])
        dfPb2 = pd.DataFrame(dataPb2, columns=['id', 'amount', 'date'])

        # Выполнение JOIN по общему столбцу 'id'
        result = pd.merge(dfPb1, dfPb2, on='id')

        # Вывод результата
        # Создание CSV-файла и запись данных
        with open('report-pandas-simple.csv', mode='w', newline='', encoding='utf-8') as file:
         writer = csv.writer(file)
    
        # Запись результата в CSV файл
        result.to_csv('./report-pandas-simple.csv', index=False)
    
        # Конвертация DataFrame в CSV формат в памяти
        csv_buffer = io.StringIO()
        result.to_csv(csv_buffer, index=False)

        # Сохранение результата в S3
        bucket_name = 'reports'  # Замените на ваш имя бакета
        s3_file_name = 'report-pandas-simple.csv'  # Название файла в S3

        # Чтение файла CSV и получение Access Key и Secret Key
        with open("s3access.csv", mode='r') as file:
            reader = csv.DictReader(file)
            credentials = next(reader)  # Чтение первой строки с ключами
        # Создание клиента S3
        # Инициализация клиента S3 с помощью считанных ключей
        s3_client = boto3.client(
            's3',
            aws_access_key_id=credentials['Access key ID'],
            aws_secret_access_key=credentials['Secret access key']
        )
        # Загрузка файла в S3
        s3_client.put_object(Bucket=bucket_name, Key=s3_file_name, Body=csv_buffer.getvalue())

        print(f"Результат объединения записан в бакет S3: s3://{bucket_name}/{s3_file_name}")

    finally:
        # Закрытие подключений
        cursorPb1.close()
        connPb1.close()

        cursorPb2.close()
        connPb2.close()
        
if __name__ == "__main__":
    main()        
