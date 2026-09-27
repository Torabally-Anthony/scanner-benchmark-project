FROM alpine:3.20.3

WORKDIR /app

ENTRYPOINT ["/bin/sh", "-c"]
ENTRYPOINT ["/bin/echo"]

USER 10001

HEALTHCHECK CMD ["sh", "-c", "exit 0"]

CMD ["benchmark"]
