# Basic example server analytics

Used:
 - Tornado http server
 - Apache Kafka is stream-processing software platform
 - Clickhouse is an open source column-oriented database


## Init python environment 
### *nix
```bash
mkdir venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r ./app/requirements.txt
```

### Windows
```bash
mkdir venv
python -m venv venv
.\venv\Scripts\activate
pip3 install -r requirements.txt
```


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