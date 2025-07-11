# 📄 README - API Inteligente de Análise de Currículos

## Visão Geral

Essa API foi criada para ajudar profissionais, que precisam lidar diariamente com dezenas de currículos em PDF ou imagens escaneadas.

A solução permite:

* Receber múltiplos arquivos PDF ou imagem (JPG/PNG);
* Extrair e resumir conteúdo dos currículos via OCR;
* Responder a perguntas como: *"Qual desses currículos se encaixa melhor para uma vaga de Desenvolvedor Python com experiência em Django?"*;
* Registrar logs detalhados em MongoDB para auditoria.

## 🛠 Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI**
* **Pytesseract (OCR)**
* **PyMuPDF (leitura de PDF)**
* **SentenceTransformers (LLM embeddings)**
* **MongoDB (logs)**
* **Docker**

## 📦 Instalação

### Requisitos

* Docker + Docker Compose

### Executar localmente

```bash
docker-compose up --build
```

Acesse: [http://localhost:8000/docs](http://localhost:8000/docs) para interagir com a API via Swagger.

---

### Executar Testes

Para garantir que tudo está funcionando corretamente, você pode executar os testes automatizados com `pytest`.

### Rodando os testes localmente

No terminal, na raiz do projeto, execute:

```bash
pytest 

```
## 🚀 Como Funciona

### Endpoint Principal: `/`

#### Requisição

* `POST /`
* FormData:

  * `files`: Lista de arquivos (PDF/JPG/PNG)
  * `query` *(opcional)*: pergunta para a LLM
  * `request_id`: UUID da requisição
  * `user_id`: ID do solicitante

#### Comportamento

* Se **`query` estiver preenchido**:

  * A API retorna os currículos mais relevantes para a pergunta feita, junto com justificativas.
* Se **`query` estiver vazio**:

  * A API retorna um resumo textual de cada currículo processado.

#### Resposta (exemplo com query):

```json
{
  "request_id": "96c7a5b1-5e0a-4f4f-8e2f-3e5346fa3de6",
  "user_id": "fabio-techmatch",
  "query": "Quem é mais adequado para vaga de engenheiro de software com foco em Python e AWS?",
  "result": {
    "message": "Análise finalizada. Aqui está a classificação dos candidatos com base na pergunta enviada.",
    "ranked_resumes": [
      {
        "filename": "joao_silva.pdf",
        "similarity": 0.88,
        "justification": "Experiência com Python, AWS e DevOps. Combina fortemente com os requisitos."
      },
      {
        "filename": "maria_oliveira.png",
        "similarity": 0.71,
        "justification": "Boa experiência em backend com Python, mas pouca menção a cloud computing."
      }
    ]
  }
}
```

#### Resposta (exemplo sem query):

```json
{
  "request_id": "9a10bdf4-03d3-4a33-a24b-7bd8b7986ee7",
  "user_id": "fabio-techmatch",
  "query": null,
  "result": {
    "message": "Resumo dos currículos gerado com sucesso.",
    "all_resumes": [
      {
        "filename": "ana_martins.jpg",
        "text": "Ana Martins - Desenvolvedora Backend com 5 anos de experiência em Java e Python..."
      },
      {
        "filename": "lucas_lima.pdf",
        "text": "Lucas Lima - Recém-formado em Engenharia de Software pela UFRN..."
      }
    ]
  }
}
```

---

## 🧾 Log de Auditoria

Todos os acessos são registrados automaticamente em MongoDB com os seguintes dados:

* `request_id`
* `user_id`
* `query`
* `result` (resumido)
* `timestamp`
* `status` (success ou error)

---

## ✅ Boas Práticas Adotadas

* Async/Await com `asyncio.create_task` para salvar logs sem bloquear a API.
* Swagger com exemplos reais e textos amigáveis para facilitar o uso por pessoas não-técnicas.
* Sem armazenamento de arquivos para reduzir custos e riscos de privacidade.

---

## 🤝 Contribuições

PRs são bem-vindos! Foco atual: adicionar suporte a modelos locais de LLM, sumarização por partes (chunking) e painel web.

---

## 📬 Contato

Para dúvidas ou suporte:

* Email: [heitor.santosprog@gmail.com](heitor.coelhoDF@outlook.com)
* GitHub: [github.com/heitor-coelho](https://github.com/seu-repo)
