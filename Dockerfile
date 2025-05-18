# Usa a imagem oficial do Python 3.13 (release candidate)
FROM python:3.13-rc

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY *.py .
COPY requirements.txt .

# Instala as dependências a partir do requirements.txt, se existir
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expõe a porta usada pela aplicação (por exemplo, Flask usa 5000)
EXPOSE 5000

# Comando para rodar a aplicação (ajuste conforme necessário)
CMD ["python", "main.py"]
