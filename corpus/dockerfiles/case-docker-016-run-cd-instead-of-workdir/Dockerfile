FROM alpine:3.20.3

WORKDIR /app

RUN cd /tmp \
    && echo "benchmark" > marker.txt

USER 10001

HEALTHCHECK CMD ["sh", "-c", "exit 0"]

CMD ["sh"]
