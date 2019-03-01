# Basic example server analytics

Used:
 - Tornado http server
 - Apache Kafka is stream-processing software platform
 - Clickhouse is an open source column-oriented database


### Build services analytics
```bash
sudo docker-compose -f docker-compose.yml build
```

### Up services analytics
```bash
sudo docker-compose -f docker-compose.yml up
```

### Remove services analytics
```bash
sudo docker-compose -f docker-compose.yml rm -f
```

### View basic dashboard
[http://localhost:8090/analytics/dashboard/](http://localhost:8090/analytics/dashboard/)