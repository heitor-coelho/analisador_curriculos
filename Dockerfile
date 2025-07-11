FROM python:3.12-slim


# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.7.1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Cria diretório da aplicação
WORKDIR /app

# Copia arquivos do projeto
COPY pyproject.toml poetry.lock* /app/

# Instala dependências via Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copia o restante do código
COPY . /app/

# Expõe porta da API
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
