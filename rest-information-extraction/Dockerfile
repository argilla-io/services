FROM recog/rest-dependencies

COPY  app  /run

WORKDIR /run

# Clean all shit (seen in slim Dockerfile)
RUN pip install -r requirements.txt

EXPOSE 7000

CMD ["/bin/sh", "start.sh"]
