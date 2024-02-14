# POI uploading service

## How to install

1. create a virtual environment
```bash
python3 -m venv .venv
. .venv/bin/activate
```
2. install the requirements
```bash
pip install -r requirements.txt
```

3. Run PostgreSQL
```bash
docker compose up -d --wait
```

4. run the server
```bash
cd poi_uploader
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000/


## How to use commands
```bash
python manage.py upload_poi_from_file <file_path>
```

### TODOs:
- [ ] Complete XML file reader implementation:
  - [ ] include in the command
- [ ] Make `readlines` method safe, for cases when attributes can be lost
- [ ] Store POI in bulk
- [ ] Add tests for the command and file readers
- [ ] Add admin interface for the POI model
- [ ] Add avg rating to the POI model
- [ ] Add serializers & viewsets for the POI model API endpoints
  - [ ] Add pagination to POI model API endpoints
  - [ ] Add filters to POI model API endpoints
- [ ] Read secret key, usernames and passwords from the environment
- [ ] Pack into a docker container
