# Imagem leve do Python
FROM python:3.12-slim

# Diretório de trabalho no container
WORKDIR /app

# Instalação das dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos (incluindo a pasta /app)
COPY . .

# Expõe a porta que o FastAPI utiliza
EXPOSE 8000

# Comando para rodar o bot
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]