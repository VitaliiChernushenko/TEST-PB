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

# Пример использования
hostname1 = get_container_hostname("oracle-db1")
hostname2 = get_container_hostname("oracle-db2")

print(f"Hostname контейнера oracle-db1: {hostname1}")
print(f"Hostname контейнера oracle-db2: {hostname2}")