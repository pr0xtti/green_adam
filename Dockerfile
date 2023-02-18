FROM python:3.10

WORKDIR /app

COPY ./collective/requirements.txt ./ext-requirements.txt

RUN pwd && ls -lah \
    #&& echo "Creating venv ..." \
    #&& python -m venv ext-venv \
    #&& echo "Activating venv ..." \
    #&& . ext-venv/bin/activate \
    && echo "pip install -r ..." \
    && pip install --no-cache-dir --upgrade -r ./ext-requirements.txt \
    #&& echo "Deactivating ..." \
    #&& deactivate \
    && echo "Some tools ..." \
    && apt update && apt install -y iputils-ping \
    && ls -lah

COPY ./collective /app/collective
COPY ./run.sh /app/

CMD ["/bin/bash", "/app/run.sh"]
