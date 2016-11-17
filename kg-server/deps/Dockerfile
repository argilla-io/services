FROM python:3.6


RUN apt-get update && apt-get install -y gfortran \
  && apt-get install -y libopenblas-dev \
  && apt-get install -y liblapack-dev \
  && apt-get install -y redis-server \
  && service redis-server stop

# install scikit-kge from github
RUN pip3 install requests --upgrade \
  && pip3 install setuptools \
  && pip3 install nose \
  && pip3 install scipy \
  && pip3 install sklearn


EXPOSE 8888 8000
