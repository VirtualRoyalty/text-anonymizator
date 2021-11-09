FROM python:slim


WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt  /usr/src/app/requirements.txt
RUN pip install -r  /usr/src/app/requirements.txt
RUN python -m spacy download ru_core_news_sm

COPY . /usr/src/app/

# ENTRYPOINT ["flask"]

EXPOSE 5000

CMD gunicorn --worker-class gevent --workers 4 --bind 0.0.0.0:5000 wsgi:app --reload --max-requests 5000 --timeout 180 --keep-alive 5 --log-level info
