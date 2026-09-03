FROM alpine:3.20.3

WORKDIR /app

ADD app.conf /app/app.conf

USER 10001

HEALTHCHECK CMD ["sh", "-c", "exit 0"]

CMD ["sh"]