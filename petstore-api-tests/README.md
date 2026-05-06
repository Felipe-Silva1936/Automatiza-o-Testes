# 🐾 Petstore API Test Automation

Automação de testes para a API [Swagger Petstore](https://petstore.swagger.io/v2), cobrindo os endpoints de **Pet**, **Store** e **User** com boas práticas de engenharia de software.

---

## 🧱 Arquitetura e Design Patterns

```
petstore-api-tests/
├── clients/              # Service Objects — encapsulam chamadas HTTP por domínio
│   ├── base_client.py    # BaseClient com Session, headers e métodos HTTP
│   ├── pet_client.py     # PetClient (Service Object)
│   ├── store_client.py   # StoreClient (Service Object)
│   └── user_client.py    # UserClient (Service Object)
│
├── models/               # Builder Pattern — construção fluente de payloads
│   ├── pet_model.py      # Pet + PetBuilder
│   ├── user_model.py     # User + UserBuilder
│   └── order_model.py    # Order + OrderBuilder
│
├── utils/                # Helper Objects — lógica de suporte reutilizável
│   ├── assertions.py     # ResponseAssertions — asserções centralizadas
│   └── data_generator.py # DataGenerator — dados únicos por execução
│
├── config/               # Configuração via variáveis de ambiente
│   └── settings.py
│
├── tests/                # Suítes de teste organizadas por domínio
│   ├── pet/test_pet.py
│   ├── store/test_store.py
│   └── user/test_user.py
│
├── conftest.py           # Fixtures compartilhadas (setup/teardown automático)
├── pytest.ini            # Configuração do pytest e relatórios
├── requirements.txt
└── .github/workflows/    # Pipeline CI (GitHub Actions)
    └── api-tests.yml
```

### Padrões utilizados
| Pattern | Onde | Benefício |
|---|---|---|
| **Service Object** | `clients/` | Isola chamadas HTTP; testes não conhecem URLs |
| **Builder** | `models/` | Criação fluente e legível de payloads |
| **Helper Object** | `utils/assertions.py` | Asserções reutilizáveis com mensagens claras |
| **Fixture (Pytest)** | `conftest.py` | Setup/teardown automático e isolamento de testes |

---

## ⚙️ Instalação

### Pré-requisitos
- Python 3.10+
- pip

### Instalar dependências

```bash
pip install -r requirements.txt
```

---

## ▶️ Execução dos Testes

### Todos os testes
```bash
pytest
```

### Por domínio
```bash
pytest tests/pet/       # Apenas endpoints de Pet
pytest tests/store/     # Apenas endpoints de Store
pytest tests/user/      # Apenas endpoints de User
```

### Com relatório HTML
```bash
pytest --html=reports/report.html --self-contained-html
```

### Verboso (com print de cada teste)
```bash
pytest -v
```

---

## 📊 Prints do Funcionamento

### Execução no terminal

```
========================== test session starts ===========================
platform linux -- Python 3.12.x, pytest-8.3.5
collected 38 items

tests/pet/test_pet.py::TestPetCreate::test_add_pet_returns_200 PASSED
tests/pet/test_pet.py::TestPetCreate::test_add_pet_returns_correct_name PASSED
tests/pet/test_pet.py::TestPetCreate::test_add_pet_returns_correct_status PASSED
tests/pet/test_pet.py::TestPetCreate::test_add_pet_contains_required_fields PASSED
tests/pet/test_pet.py::TestPetCreate::test_add_pet_with_all_fields PASSED
tests/pet/test_pet.py::TestPetRead::test_find_pets_by_status_returns_list[available] PASSED
tests/pet/test_pet.py::TestPetRead::test_find_pets_by_status_returns_list[pending] PASSED
tests/pet/test_pet.py::TestPetRead::test_find_pets_by_status_returns_list[sold] PASSED
tests/pet/test_pet.py::TestPetRead::test_find_pets_by_status_all_match[available] PASSED
...
tests/store/test_store.py::TestStoreInventory::test_get_inventory_returns_200 PASSED
tests/store/test_store.py::TestStoreOrderCreate::test_place_order_returns_200 PASSED
...
tests/user/test_user.py::TestUserAuth::test_login_with_valid_credentials_returns_200 PASSED
tests/user/test_user.py::TestUserAuth::test_login_response_contains_session_token PASSED
...

====================== 38 passed in 42.31s ===============================
```

### Relatório HTML gerado em `reports/report.html`

---

## 🔧 Configuração

As configurações são lidas do arquivo `.env` (ou variáveis de ambiente):

| Variável | Padrão | Descrição |
|---|---|---|
| `BASE_URL` | `https://petstore.swagger.io/v2` | URL base da API |
| `TIMEOUT` | `30` | Timeout das requisições (segundos) |

---

## 🚀 CI/CD — GitHub Actions

O pipeline `.github/workflows/api-tests.yml` executa automaticamente:

- Em todo `push` para `main` ou `develop`
- Em todo `pull_request` para `main`
- Diariamente às 06:00 UTC (detecção de regressões)
- Manualmente via `workflow_dispatch`

**Artefatos gerados:** relatório HTML e JSON ficam disponíveis por 30 dias na aba **Actions** do repositório.

---

## 🧪 Cobertura dos Endpoints

| Domínio | Endpoint | Método | Cenários |
|---|---|---|---|
| **Pet** | `/pet` | POST | Criar com campos válidos, todos os campos, status |
| **Pet** | `/pet` | PUT | Atualizar nome e status |
| **Pet** | `/pet/findByStatus` | GET | available / pending / sold |
| **Pet** | `/pet/{id}` | GET | Encontrar por ID, 404 para inexistente |
| **Pet** | `/pet/{id}` | POST | Atualizar via form data |
| **Pet** | `/pet/{id}` | DELETE | Deletar e verificar remoção |
| **Store** | `/store/inventory` | GET | Retorno de dict com valores numéricos |
| **Store** | `/store/order` | POST | Criar pedido, verificar campos e status |
| **Store** | `/store/order/{id}` | GET | Buscar por ID, 404 para inexistente |
| **Store** | `/store/order/{id}` | DELETE | Deletar e verificar remoção |
| **User** | `/user` | POST | Criar usuário individual |
| **User** | `/user/createWithList` | POST | Criar múltiplos usuários |
| **User** | `/user/login` | GET | Login válido, token, headers |
| **User** | `/user/logout` | GET | Logout com sucesso |
| **User** | `/user/{username}` | GET | Buscar por username, 404 para inexistente |
| **User** | `/user/{username}` | PUT | Atualizar nome e email |
| **User** | `/user/{username}` | DELETE | Deletar e verificar remoção |

---

## 🛠 Tecnologias

- **Python 3.12** — linguagem principal
- **pytest** — framework de testes
- **requests** — cliente HTTP
- **pytest-html** — relatório HTML
- **pytest-json-report** — relatório JSON para CI
- **python-dotenv** — gerenciamento de variáveis de ambiente
- **GitHub Actions** — pipeline de CI/CD
