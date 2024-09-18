FROM alpine:latest

RUN apk add --no-cache sqlite

# Set working directory
WORKDIR /data

# Expose port 3306 (optional, if you want to connect remotely)
# EXPOSE 3306

CMD ["sqlite3", "/data/metrics.db"]
