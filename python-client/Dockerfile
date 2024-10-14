# Используем базовый образ с Python
FROM python:3.11.5

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    libaio1 wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Скачиваем Oracle Instant Client
#RUN unzip instantclient-basiclite-linux.x64-12.2.0.1.0.zip -d /opt/oracle
#unzip instantclient-basiclite-linux.x64-12.2.0.1.0.zip && \
#    mv instantclient_* /opt/oracle && \
#    rm instantclient-basiclite-linux.x64-12.2.0.1.0.zip

# Копируем архив Oracle Instant Client в контейнер
#COPY instantclient-basiclite-linux.x64-12.2.0.1.0.zip /tmp/

# Распаковываем архив в /opt/oracle и удаляем его после распаковки
#RUN unzip /tmp/instantclient-basiclite-linux.x64-12.2.0.1.0.zip -d /opt/oracle && \
#    rm /tmp/instantclient-basiclite-linux.x64-12.2.0.1.0.zip

# Установите зависимости
# RUN apt-get update && \
#     apt-get install -y wget unzip && \
#     wget https://download.oracle.com/otn_software/linux/instantclient/21.9/instantclient-basic-linux.x64.zip && \
#     unzip instantclient-basic-linux.x64.zip -d /opt/ && \
#     rm instantclient-basic-linux.x64.zip && \
#     ln -s /opt/instantclient_21_9/libclntsh.so.21.1 /usr/lib/libclntsh.so
# Устанавливаем переменную окружения для Oracle Instant Client
ENV LD_LIBRARY_PATH=/opt/oracle

# Установка необходимых системных библиотек
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    libssl-dev \
    libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Установка pandas через pip
RUN pip install --no-cache-dir pandas
# Установка библиотеки oracledb
RUN pip install oracledb
RUN pip install --upgrade docker
# Устанавливаем необходимые зависимости
RUN pip install boto3


# Копируем файлы в контейнер
WORKDIR /app
# Копирование файлов приложения в контейнер
COPY . /app
#COPY . /requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска по умолчанию
#CMD ["python", "/app/report-pandas.py"]

