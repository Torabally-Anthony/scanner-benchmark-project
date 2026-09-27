FROM alpine:3.20.3

RUN apk add --no-cache curl \
    && wget -q https://example.invalid/archive.tar.gz \
    && curl -fsSLO https://example.invalid/checksum.txt

WORKDIR /app

USER 10001

HEALTHCHECK CMD ["sh", "-c", "exit 0"]

CMD ["sh"]
