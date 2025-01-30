# Menggunakan image Python 3.10
FROM python:3.10-slim

# Menetapkan working directory
WORKDIR /app

# Menyalin requirements.txt ke dalam container
COPY requirements.txt /app/

# Instal dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh aplikasi ke dalam container
COPY . /app/

# Menjalankan aplikasi dengan gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
