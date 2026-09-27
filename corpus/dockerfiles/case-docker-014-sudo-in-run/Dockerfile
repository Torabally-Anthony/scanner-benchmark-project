FROM alpine:3.20.3

RUN apk add --no-cache sudo \
    && sudo true

WORKDIR /app

USER 10001

HEALTHCHECK CMD ["sh", "-c", "exit 0"]

CMD ["sh"]
