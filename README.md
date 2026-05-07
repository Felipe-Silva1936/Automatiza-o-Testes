
<h2>8. README.md</h2>

# Automação de Testes - API e Web

## Descrição
Este repositório contém automações de teste para duas aplicações:
- **Petstore API Tests**: Testes de API REST para a Petstore API, cobrindo operações de pets, usuários e loja.
- **SauceDemo Web Tests**: Testes E2E para o site SauceDemo usando Selenium e Page Object Model, simulando fluxo completo de compra.

## Pré-requisitos
- Python 3.11+ (recomendado 3.13)
- Git
- Navegador Chrome (para testes web)

## Instalação e Execução

### 1. Clone o repositório
```bash
git clone <seu-repo>
cd Automatiza-o-Testes
```

### 2. Testes de API (Petstore)
Navegue para a pasta do projeto de API e instale as dependências:
copie o caminho da pasta usando botão direito e copiando caminho no arquivo petstore-api-tests
```bash
cd <caminho copiado>
pip install -r requirements.txt
```

#### Executar testes:
- **Todos os testes**:
  ```bash
  pytest
  ```
- **Testes por módulo**:
  ```bash
  pytest tests/pet/      # Testes relacionados a pets
  pytest tests/store/    # Testes relacionados à loja
  pytest tests/user/     # Testes relacionados a usuários
  ```
- **Arquivo específico**:
  ```bash
  pytest tests/pet/test_pet.py
  ```
- **Teste específico (classe e método)**:
  ```bash
  pytest tests/pet/test_pet.py::TestPetCreate::test_add_pet_returns_200
  ```
- **Com relatórios**:
  ```bash
  pytest --html=reports/report.html --json-report --json-report-file=reports/report.json
  ```

### 3. Testes Web (SauceDemo)
Navegue para a pasta do projeto web e instale as dependências:
copie o caminho da pasta usando botão direito e copiando caminho no arquivo saucedemo-web-tests
```bash
cd <caminho copiado>
pip install -r requirements.txt
```

#### Executar testes:
- **Todos os testes**:
  ```bash
  pytest tests/ -v --html=report.html
  ```
- **Arquivo específico**:
  ```bash
  pytest tests/test_caso_2.py
  ```
- **Com verbosidade e relatórios**:
  ```bash
  pytest tests/ -v -s --html=report.html --json-report
  ```

## Estrutura do Projeto
```
Automatiza-o-Testes/
├── petstore-api-tests/          # Testes de API
│   ├── clients/                 # Clientes para APIs
│   ├── models/                  # Modelos de dados
│   ├── tests/                   # Casos de teste
│   │   ├── pet/
│   │   ├── store/
│   │   └── user/
│   ├── utils/                   # Utilitários
│   └── requirements.txt
├── SauceDemo-web-tests/         # Testes web
│   ├── pages/                   # Page Objects
│   ├── tests/                   # Casos de teste
│   └── requirements.txt
└── README.md
```

## Tecnologias Utilizadas
- **Python**: Linguagem principal
- **Pytest**: Framework de testes
- **Requests**: Para testes de API
- **Selenium**: Para automação web
- **Webdriver Manager**: Gerenciamento de drivers
- **Allure/Pytest-HTML**: Relatórios de teste

## Notas
- Para testes web, certifique-se de que o ChromeDriver está instalado automaticamente via webdriver-manager.
- Relatórios são salvos na pasta `reports/` (para API) ou na raiz (para web).
- Use `pytest --collect-only` para listar todos os testes sem executá-los.