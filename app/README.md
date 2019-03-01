# App server analytics


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

## Run app
```bash
python3 ./server.py
```
###View basic dashboard
[http://localhost:8090/analytics/dashboard/](http://localhost:8090/analytics/dashboard/)
