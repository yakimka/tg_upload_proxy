### Builder ###
FROM python:3.8 as builder

WORKDIR /usr/src/app
COPY . .
RUN pip install wheel && pip wheel -r requirements.txt --wheel-dir=./wheels
RUN pip wheel --wheel-dir=./wheels .

### Image ###
FROM python:3.8-slim

ENV PATH /home/tg_upload_proxy/.local/bin:$PATH

COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-index --find-links=/wheels /wheels/*.whl  && rm -rf /wheels

COPY entrypoint.sh /usr/local/bin/

RUN groupadd -r tg_upload_proxy && useradd -r -g tg_upload_proxy tg_upload_proxy -m --uid 1000
WORKDIR /home/tg_upload_proxy
USER tg_upload_proxy

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
