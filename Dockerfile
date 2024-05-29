# Use a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /servidor

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências listadas em requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da aplicação para o diretório de trabalho
COPY . .

COPY .env .

# Expose a porta que a aplicação vai rodar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "servidor.py"]
