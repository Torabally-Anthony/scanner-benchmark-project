FROM alpine:3.20.3

WORKDIR /app

COPY app.conf settings.conf /app/config

USER 10001

HEALTHCHECK CMD ["sh", "-c", "exit 0"]

CMD ["sh"]
