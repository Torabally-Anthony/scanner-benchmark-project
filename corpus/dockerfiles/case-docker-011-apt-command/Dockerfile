FROM ubuntu:24.04

RUN apt install -y curl

WORKDIR /app

USER 10001

HEALTHCHECK CMD ["sh", "-c", "exit 0"]

CMD ["sh"]
