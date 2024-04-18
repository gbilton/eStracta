FROM python:3.11

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app /app/app

ENV TZ=America/Sao_Paulo

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["flask", "--app", "app.main", "run", "--host=0.0.0.0"]

