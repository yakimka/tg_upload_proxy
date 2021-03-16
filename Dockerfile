### Development image ###
FROM python:3.8 as development

ARG SKIP_TEST

WORKDIR /usr/src/app

RUN pip install --upgrade pip
# Copy requirements and install it for caching
COPY requirements.txt requirements.dev.txt /
# Install production requirements in prefix for use in production image
RUN pip install -r /requirements.txt --no-warn-script-location --prefix=/install && \
    # copy requirements to /usr/local and then install dev-requirements to handle conflicts
    cp -r /install/* /usr/local && \
    pip install -r /requirements.dev.txt --no-warn-script-location

COPY . .

# Install app in prefix for use in production image
RUN pip install . --no-warn-script-location --no-deps --prefix=/install

# Install app in editable mode for development
# without dependencies, because they were installed in the previous steps
RUN pip install -e '.[dev]' --no-deps

# Run tests
RUN if [ -z "$SKIP_TEST" ] ; then \
        make lint && make test ; \
    else echo "skip tests and linter" ; fi

### Production image ###
FROM python:3.8-slim as production

#ENV PATH /home/tg_upload_proxy/.local/bin:$PATH

# Copy installed packages to /usr/local
COPY --from=development /install /usr/local

RUN groupadd -r tg_upload_proxy && \
    useradd -r -g tg_upload_proxy tg_upload_proxy -m --uid 1000

COPY entrypoint.sh /usr/local/bin/

WORKDIR /home/tg_upload_proxy
USER tg_upload_proxy

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
