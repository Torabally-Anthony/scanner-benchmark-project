FROM alpine:3.20.3 AS builder

RUN echo "first stage" > /tmp/output.txt

FROM alpine:3.20.3 AS builder

WORKDIR /app

COPY --from=0 /tmp/output.txt /app/output.txt

USER 10001

HEALTHCHECK CMD ["sh", "-c", "exit 0"]

CMD ["sh"]