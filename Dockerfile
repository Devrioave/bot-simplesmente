# Imagem leve do Python
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código
COPY . .

# Expor porta (informativo)
EXPOSE 8000

# Start command compatível com cloud
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
