cd backend

mkdir app
mkdir -p app/api
mkdir -p app/api/v1
mkdir -p app/core
mkdir -p app/services
mkdir -p app/tests

mkdir -p app && touch app/main.py
mkdir -p app && touch app/api/v1/documents.py
mkdir -p app && touch app/api/v1/review.py
mkdir -p app && touch app/api/v1/audit.py

mkdir -p app && touch app/core/auth.py
mkdir -p app && touch app/core/db.py
mkdir -p app && touch app/core/schemas.py
mkdir -p app && touch app/core/models.py
mkdir -p app && touch app/core/llm_adapter.py

mkdir -p app && touch app/services/fhir_ingest.py
mkdir -p app && touch app/services/ehr_connector.py

mkdir -p app && touch app/requirements.txt
mkdir -p app && touch app/Dockerfile
mkdir -p app && touch app/docker-compose.yml