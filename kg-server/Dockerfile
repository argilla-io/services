FROM recog/kge-server-deps

ENV DEPS_TARGZ deps.tar.gz
ENV REPO_NAME kge-server
ENV BRANCH master

# TODO: Manage as deployed dependency
RUN wget https://github.com/vfrico/scikit-kge/tarball/v0.9#egg=scikit-kge-0.9 -O /scikit-kge.tar.gz \
  && wget  https://github.com/vfrico/${REPO_NAME}/archive/${BRANCH}.tar.gz -O /${DEPS_TARGZ} \
  && pip install /scikit-kge.tar.gz \
  && pip install /${DEPS_TARGZ}

RUN tar -zxvf /${DEPS_TARGZ} \
  && cp -R /${REPO_NAME}-${BRANCH}/rest-service /service \
  && rm -rf /${REPO_NAME}-${BRANCH} \
  && rm -rf /${DEPS_TARGZ}

WORKDIR /service

EXPOSE 8888 8000
