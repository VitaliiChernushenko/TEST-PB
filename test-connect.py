import oracledb
import docker

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
def main():
    # Попробуйте сначала использовать IP-адрес
    hostname = "oracle-db1"  # или используйте имя контейнера 'oracle-db1'
    port = "1521"
    service_name = "xepdb1"

    print(f"Подключение к {hostname}:{port}/{service_name}")
    hostname1 = get_container_hostname("oracle-db1")
    # Инициализация клиента Oracle
    oracledb.init_oracle_client(lib_dir=None)

    # Создание DSN
    dsn = oracledb.makedsn('172.18.0.2', port, service_name=service_name)

    try:
        # Подключение к базе данных
        conn = oracledb.connect(user='vitalii', password='vitalii', dsn=dsn)
        print("Подключение успешно!")
    except oracledb.DatabaseError as e:
        error, = e.args
        print("Ошибка подключения:", error.message)

if __name__ == "__main__":
    main()
