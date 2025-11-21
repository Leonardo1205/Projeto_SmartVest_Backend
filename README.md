# SmartVest - Backend (API) 🧠

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

API RESTful e motor de Inteligência Artificial do projeto **SmartVest**. Responsável pela lógica de RAG (Retrieval-Augmented Generation), autenticação e gestão de dados.

## ⚡ Tecnologias Principais

* **Framework:** FastAPI (Python 3.12+)
* **Banco de Dados:** PostgreSQL (via Docker)
* **IA & RAG:** Google Gemini, LangChain, FAISS e SentenceTransformers.
* **Autenticação:** JWT e OAuth2 (Google).
* **Testes:** Pytest.

## 🚀 Como Rodar Localmente

### 1. Banco de Dados (Docker)

O projeto utiliza PostgreSQL em contêiner. Inicie o banco com a senha configurada:

```bash
docker run --name smartvest-db -e POSTGRES_PASSWORD=admin123 -e POSTGRES_DB=smartvest_db -p 5432:5432 -d postgres
```

### 2. Configuração do Python

Crie o ambiente virtual e instale as dependências:

```bash
python -m venv .venv
.\.venv\Scripts\Activate 
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente (.env)

Crie um arquivo .env na raiz com as configurações (exemplo):

```bash
DATABASE_URL=postgresql+psycopg://postgres:admin123@localhost:5432/smartvest_db
JWT_SECRET=seu_segredo_super_secreto
GEMINI_API_KEY=sua_chave_api_gemini
GEMINI_MODEL=gemini-2.5-flash
```

### 4. Ingestão de Dados (RAG)

Antes de iniciar, processe os arquivos Markdown para criar a base de conhecimento da IA:

```bash
python -m app.services.ingest_all --rebuild
```

### 5. Iniciar o Servidor

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 🧪 Testes Automatizados (TDD)

```bash
pytest
```

### 📚 Documentação

Documentação detalhada, RFC e guias de arquitetura estão disponíveis na Wiki: 👉 **[Link para a Wiki do Projeto](https://github.com/Leonardo1205/Projeto_Smartvest/wiki)**

