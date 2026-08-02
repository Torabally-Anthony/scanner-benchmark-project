FROM alpine:3.20

WORKDIR /app

RUN addgroup -S appgroup \
    && adduser -S appuser -G appgroup \
    && apk add --no-cache curl \
    && printf '#!/bin/sh\nwhile true; do echo "Application running"; sleep 30; done\n' \
       > /app/start.sh \
    && chmod +x /app/start.sh

EXPOSE 8080

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=5s \
    --retries=3 \
    CMD pgrep -f start.sh || exit 1

# Deliberate benchmark misconfiguration:
USER root

CMD ["/app/start.sh"]