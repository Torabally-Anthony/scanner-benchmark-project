FROM nginx:1.27.5-alpine

WORKDIR /app

EXPOSE 22

USER 10001

HEALTHCHECK CMD ["sh", "-c", "exit 0"]

CMD ["nginx", "-g", "daemon off;"]