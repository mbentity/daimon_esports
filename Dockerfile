FROM python:3.12.3-alpine

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

RUN python manage.py collectstatic --noinput && python manage.py migrate --noinput

EXPOSE 8000

# waitress
CMD ["waitress-serve", "--port=8000", "daimon_esports.wsgi:application"]