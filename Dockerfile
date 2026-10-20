FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       git \
       curl \
       ca-certificates \
       libssl-dev \
       zlib1g-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ساخت باینری واقعی MTProxy
RUN git clone --depth 1 \
    https://github.com/TelegramMessenger/MTProxy.git /tmp/MTProxy \
    && make -C /tmp/MTProxy \
    && install -m 0755 \
       /tmp/MTProxy/objs/bin/mtproto-proxy \
       /usr/local/bin/mtproto-proxy \
    && rm -rf /tmp/MTProxy

# دریافت و آماده‌سازی هسته واقعی پنل
RUN git clone --depth 1 \
    https://github.com/amirh00sain/spiderpanel.git /tmp/panel-source \
    && cp -a /tmp/panel-source/. /app/ \
    && rm -rf /tmp/panel-source

# اعمال برندینگ بدون بازنویسی منطق اصلی
COPY pompnet_brand.py /tmp/pompnet_brand.py

RUN test -f /app/main.py \
    && test -f /app/requirements.txt \
    && pip install -r /app/requirements.txt \
    && python /tmp/pompnet_brand.py /app \
    && python -m py_compile /app/main.py

EXPOSE 8080
EXPOSE 443

CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
