FROM python:3.10

WORKDIR /app

COPY ./collective/requirements.txt ./ext-requirements.txt

RUN pwd && ls -lah \
    && echo "pip install -r ..." \
    && pip install --no-cache-dir --upgrade -r ./ext-requirements.txt \
    && echo "Some tools ..." \
    && apt update && apt install -y iputils-ping \
    && apt install -y supervisor \
    && ls -lah

COPY ./collective /app/collective
COPY ./supervisord.conf /etc/supervisor/conf.d/greenadam.conf
COPY ./extractor.sh /app/extractor.sh
COPY ./martmaker.sh /app/martmaker.sh
#COPY ./run.sh /app/

CMD ["/usr/bin/supervisord"]
