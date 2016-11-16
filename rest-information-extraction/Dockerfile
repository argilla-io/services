# FROM python:2.7-slim
FROM python:2.7

COPY  files  /run

WORKDIR /run

# TODO: Manage as deployed dependency
RUN pip install --upgrade pip \
	&& pip install git+git://github.com/recognai/textacy \
	&& pip install -r requirements.txt

RUN python -m spacy.en.download

EXPOSE 7000

CMD ["/bin/sh", "start.sh"]
