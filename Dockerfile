# Используем официальный Python-образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Открываем порт Flask
EXPOSE 5000

# Запускаем Flask
CMD ["flask", "run"]