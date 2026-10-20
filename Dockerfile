FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System dependencies required to build MTProxy
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       git \
       curl \
       ca-certificates \
       libssl-dev \
       zlib1g-dev \
       libevent-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Build the real MTProxy binary
RUN git clone --depth 1 \
    https://github.com/TelegramMessenger/MTProxy.git /tmp/MTProxy \
    && make -C /tmp/MTProxy \
    && test -f /tmp/MTProxy/objs/bin/mtproto-proxy \
    && install -m 0755 \
       /tmp/MTProxy/objs/bin/mtproto-proxy \
       /usr/local/bin/mtproto-proxy \
    && rm -rf /tmp/MTProxy

# Use the pinned SpiderPanel core
ARG SPIDERPANEL_COMMIT=e20c3849b8033c2d89f64070bebd4dca461db7e2

RUN git init /tmp/panel-source \
    && git -C /tmp/panel-source remote add origin \
       https://github.com/amirh00sain/SpiderPanel.git \
    && git -C /tmp/panel-source fetch --depth 1 origin \
       "${SPIDERPANEL_COMMIT}" \
    && git -C /tmp/panel-source checkout --detach FETCH_HEAD \
    && cp -a /tmp/panel-source/. /app/ \
    && rm -rf /tmp/panel-source

# Apply POMP NET branding
COPY pompnet_brand.py /tmp/pompnet_brand.py

# Validate files, install Python dependencies and compile checks
RUN test -f /app/main.py \
    && test -f /app/requirements.txt \
    && test -f /app/static/index.html \
    && test -f /app/static/login.html \
    && test -f /app/static/sub.html \
    && python -m pip install --upgrade pip \
    && python -m pip install -r /app/requirements.txt \
    && python -m py_compile /tmp/pompnet_brand.py \
    && python /tmp/pompnet_brand.py /app \
    && python -m py_compile /app/main.py

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
