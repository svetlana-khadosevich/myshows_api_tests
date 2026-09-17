#Базовый образ — легковесный Python 3.11
FROM python:3.11-slim

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка /app как рабочей директории для команд Dockerfile
WORKDIR /app

# Копируем только requirements
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда по умолчанию при запуске контейнера
CMD ["pytest", "-v"]
