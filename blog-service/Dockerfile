FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY manage.py .
COPY app /app/app
ENV PYTHONPATH=/app/app
CMD ["gunicorn", "blog_service.wsgi:application", "--bind", "0.0.0.0:8001", "--timeout", "120", "--chdir", "app"]