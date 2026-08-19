# Используем официальный легковесный образ Python
FROM python:3.11-slim

# Установка системных зависимостей (если понадобятся дополнительные пакеты)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копирование файлов приложения и зависимостей внутрь образа
COPY requirements.txt .
COPY agent_sim_ref.py .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Команда, которая выполнится при старте контейнера
CMD ["python", "./agent_sim_ref.py"]
