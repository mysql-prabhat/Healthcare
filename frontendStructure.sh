cd D:/GenAI/Healthcare/frontend

#npm create vite@latest . -- --template react
#npm install
#npm install axios react-router-dom

mkdir -p src/components
mkdir -p src/pages
mkdir -p src/services

mkdir -p  src && touch src/components/UploadDocument.jsx
mkdir -p  src && touch src/components/ReviewQueue.jsx
mkdir -p  src && touch src/components/AuditTrail.jsx

mkdir -p  src && touch src/services/api.js