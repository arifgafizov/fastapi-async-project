FROM python:3.10.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG GID=1000
ARG UID=1000
ARG USER=ubuntu

RUN apt-get update && \
    apt-get install gettext -y && \
    groupadd -g $GID $USER && \
    useradd  -u $UID -g $GID $USER

WORKDIR /app

COPY src/requirements /app/requirements

RUN pip install -r requirements/local.txt --no-cache-dir

COPY ./src /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0" , "--reload" , "--port", "8000"]
