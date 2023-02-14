FROM python:3.10

WORKDIR /app

COPY ./extractor ./
COPY ./windowmaker ./
COPY run.sh ./

RUN cd /app/extractor \
    && python -m venv extractor_venv \
    && source extractor_venv/bin/activate \
    && pip install -r requirements.txt \
    && deactivate \
    && cd /app/windowmaker \
    && python -m venv windowmaker_venv \
    && source windowmaker_venv/bin/activate \
    && pip install -r requirements.txt \
    && deactivate

CMD run.sh