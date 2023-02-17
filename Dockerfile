FROM python:3.10

WORKDIR /app

COPY ./extractor/requirements.txt ./ext-requirements.txt

RUN pwd && ls -lah \
    #&& echo "Creating venv ..." \
    #&& python -m venv ext-venv \
    #&& echo "Activating venv ..." \
    #&& . ext-venv/bin/activate \
    && echo "pip install -r ..." \
    && pip install --no-cache-dir --upgrade -r ./ext-requirements.txt \
    #&& echo "Deactivating ..." \
    #&& deactivate \
    && ls -lah

COPY ./extractor /app/extractor
COPY ./run.sh /app/

CMD ["/bin/bash", "/app/run.sh"]
