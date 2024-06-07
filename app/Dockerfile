ARG BASE_IMAGE_VER=0.2.3
FROM gmms/gmms-python-builder:${BASE_IMAGE_VER} as builder
WORKDIR /tmp
COPY . .

RUN pip wheel --trusted-host pypi.dev.getmobit.ru --wheel-dir /tmp/wheels -r requirements.txt

FROM gmms/gmms-python-base:${BASE_IMAGE_VER}
ARG APP_UID=26262
ARG APP_GID=26262
ARG APP_USERNAME=customerportal
ARG APP_HOME=/home/${APP_USERNAME}/app

RUN addgroup --gid ${APP_GID} ${APP_USERNAME} && \
    adduser --uid ${APP_UID} --ingroup ${APP_USERNAME} ${APP_USERNAME} --disabled-password --gecos ''
COPY --from=builder /tmp/wheels /tmp/
RUN pip install --no-cache-dir /tmp/*.whl

WORKDIR ${APP_HOME}
COPY . .

RUN chmod +x entrypoint.sh && \
    mkdir ${APP_HOME}/staticfiles && \
    chown -R ${APP_USERNAME}:${APP_USERNAME} ${APP_HOME}

VOLUME ${APP_HOME}/staticfiles

USER ${APP_USERNAME}
ENTRYPOINT ["./entrypoint.sh"]

LABEL project="web/customer-portal"
LABEL version="1.1.1.dev1"
