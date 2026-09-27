FROM rockylinux:9.3

RUN yum install -y curl

WORKDIR /app

USER 10001

HEALTHCHECK CMD ["sh", "-c", "exit 0"]

CMD ["sh"]
