FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential git curl ca-certificates libssl-dev zlib1g-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# دریافت MTProxy واقعی
RUN git clone --depth 1 \
    https://github.com/TelegramMessenger/MTProxy.git /tmp/MTProxy \
    && make -C /tmp/MTProxy \
    && install -m 0755 \
       /tmp/MTProxy/objs/bin/mtproto-proxy \
       /usr/local/bin/mtproto-proxy \
    && rm -rf /tmp/MTProxy

# دریافت سورس اصلی SpiderPanel
RUN git clone --depth 1 \
    https://github.com/amirh00sain/SpiderPanel.git /tmp/spiderpanel \
    && cp -a /tmp/spiderpanel/. /app/ \
    && rm -rf /tmp/spiderpanel

# اجرای تغییرات برندینگ، بدون جایگزینی منطق اصلی پنل
COPY pompnet_brand.py /tmp/pompnet_brand.py

RUN pip install -r requirements.txt \
    && python /tmp/pompnet_brand.py /app \
    && python -m py_compile main.py

EXPOSE 8080

CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
