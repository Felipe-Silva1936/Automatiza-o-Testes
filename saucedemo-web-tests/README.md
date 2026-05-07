# 🛒 SauceDemo Web Test Automation

Automação de testes E2E para [SauceDemo](https://www.saucedemo.com) com **Selenium + Python**, cobrindo o fluxo completo de compra: **Login → Carrinho → Checkout → Confirmação**.

---

## 🧱 Arquitetura e Design Patterns

```
saucedemo-web-tests/
├── pages/                      # Page Object Model (POM)
│   ├── base_page.py            # BasePage — helpers de WebDriver compartilhados
│   ├── login_page.py           # LoginPage
│   ├── inventory_page.py       # InventoryPage (listagem de produtos)
│   ├── cart_page.py            # CartPage
│   ├── checkout_info_page.py   # CheckoutInfoPage (dados do comprador)
│   ├── checkout_overview_page.py # CheckoutOverviewPage (resumo do pedido)
│   └── checkout_complete_page.py # CheckoutCompletePage (confirmação)
│
├── utils/
│   ├── driver_factory.py       # Factory Pattern — setup do WebDriver isolado
│   └── assertions.py           # Helper Object — asserções web reutilizáveis
│
├── config/
│   └── settings.py             # Configuração via variáveis de ambiente
│
├── tests/
│   ├── auth/test_login.py      # Login, logout, bloqueio de usuário
│   ├── cart/test_cart.py       # Adicionar, remover, verificar carrinho
│   └── checkout/test_checkout.py # Fluxo E2E + validação de formulário + preços
│
├── conftest.py                 # Fixtures encadeadas (driver → login → cart → checkout)
├── pytest.ini
├── requirements.txt
└── .github/workflows/web-tests.yml
```

### Padrões utilizados

| Pattern | Onde | Benefício |
|---|---|---|
| **Page Object Model** | `pages/` | Separa seletores dos testes; mudanças de UI afetam 1 lugar |
| **BasePage** | `pages/base_page.py` | Elimina boilerplate de WebDriverWait em todo PO |
| **Factory** | `utils/driver_factory.py` | Criação de WebDriver desacoplada dos testes |
| **Helper Object** | `utils/assertions.py` | Mensagens de falha descritivas e centralizadas |
| **Fixture chain** | `conftest.py` | Fixtures encadeadas evitam repetição de setup |

---

## ⚙️ Instalação

### Pré-requisitos
- Python 3.10+
- Google Chrome instalado

```bash
pip install -r requirements.txt
```

---

## ▶️ Execução

```bash
# Todos os testes
pytest

# Apenas E2E completo
pytest tests/checkout/test_checkout.py::TestFullPurchaseFlow

# Apenas autenticação
pytest tests/auth/

# Apenas carrinho
pytest tests/cart/

# Com relatório HTML
pytest --html=reports/report.html --self-contained-html

# Com browser visível (sem headless)
HEADLESS=false pytest
```

---

## 📊 Prints do Funcionamento

```
========================= test session starts ==========================
platform linux -- Python 3.12.x, pytest-8.3.5
collected 38 items

tests/auth/test_login.py::TestLoginSuccess::test_login_redirects_to_inventory PASSED
tests/auth/test_login.py::TestLoginSuccess::test_inventory_page_title_after_login PASSED
tests/auth/test_login.py::TestLoginSuccess::test_inventory_shows_items_after_login PASSED
tests/auth/test_login.py::TestLoginFailure::test_wrong_password_shows_error PASSED
tests/auth/test_login.py::TestLoginFailure::test_locked_user_shows_error PASSED
tests/auth/test_login.py::TestLogout::test_logout_redirects_to_login PASSED
tests/cart/test_cart.py::TestAddToCart::test_add_one_item_updates_badge PASSED
tests/cart/test_cart.py::TestAddToCart::test_add_two_items_updates_badge PASSED
tests/cart/test_cart.py::TestCartContent::test_cart_shows_added_item_name PASSED
tests/cart/test_cart.py::TestCartContent::test_cart_item_price_format PASSED
tests/cart/test_cart.py::TestRemoveFromCart::test_remove_item_empties_cart PASSED
tests/checkout/test_checkout.py::TestFullPurchaseFlow::test_complete_purchase_flow PASSED
tests/checkout/test_checkout.py::TestFullPurchaseFlow::test_complete_purchase_with_multiple_items PASSED
tests/checkout/test_checkout.py::TestCheckoutInfoValidation::test_missing_first_name_shows_error PASSED
tests/checkout/test_checkout.py::TestCheckoutOverview::test_total_equals_subtotal_plus_tax PASSED
tests/checkout/test_checkout.py::TestCheckoutComplete::test_confirmation_header_contains_thank_you PASSED
...

=================== 38 passed in 87.42s ================================
```

---

## 🔧 Configuração (`.env`)

| Variável | Padrão | Descrição |
|---|---|---|
| `BASE_URL` | `https://www.saucedemo.com` | URL base |
| `STANDARD_USER` | `standard_user` | Usuário válido |
| `LOCKED_USER` | `locked_out_user` | Usuário bloqueado |
| `PASSWORD` | `secret_sauce` | Senha padrão |
| `HEADLESS` | `true` | Rodar sem abrir janela |
| `IMPLICIT_WAIT` | `10` | Timeout de elementos (segundos) |
| `PAGE_LOAD_TIMEOUT` | `30` | Timeout de carregamento (segundos) |

---

## 🧪 Cobertura dos Cenários

### Autenticação (`tests/auth/`)
| Cenário | Resultado esperado |
|---|---|
| Login com credenciais válidas | Redireciona para `/inventory` |
| Login com senha errada | Exibe mensagem de erro |
| Login com campos vazios | Exibe validação de campo obrigatório |
| Usuário bloqueado (`locked_out_user`) | Exibe mensagem "locked out" |
| Fechar mensagem de erro | Erro some da tela |
| Logout | Retorna para tela de login |

### Carrinho (`tests/cart/`)
| Cenário | Resultado esperado |
|---|---|
| Adicionar 1 item | Badge exibe "1" |
| Adicionar 2 itens | Badge exibe "2" |
| Verificar nome do item no carrinho | Nome correto exibido |
| Verificar formato de preço | Formato `$X.XX` |
| Remover item único | Carrinho fica vazio |
| Remover 1 de 2 itens | 1 item permanece |
| Continuar comprando | Retorna para inventário |

### Checkout (`tests/checkout/`)
| Cenário | Resultado esperado |
|---|---|
| **Fluxo E2E completo** (1 item) | Confirmação exibida |
| **Fluxo E2E** (2 itens) | Confirmação com 2 itens |
| Campos vazios no formulário | Erros de validação |
| Total = Subtotal + Tax | Cálculo correto |
| Cancelar na visão geral | Retorna ao inventário |
| Botão "Back Home" | Retorna ao inventário |

---

## 🛠 Tecnologias

- **Python 3.12**
- **Selenium 4** — automação de browser
- **pytest** — framework de testes
- **webdriver-manager** — gerencia o ChromeDriver automaticamente
- **pytest-html** — relatório HTML
- **python-dotenv** — variáveis de ambiente
- **GitHub Actions** — CI/CD com Chrome instalado via `browser-actions/setup-chrome`
