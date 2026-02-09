# Financeiro - Sistema de Gestão Financeira

Sistema Django para gestão de contas a pagar, contas a receber e plano de contas.

## 🚀 Quick Start

### Desenvolvimento Local

```bash
# 1. Clone ou entre na pasta
cd financeiro

# 2. Crie virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# ou source venv/bin/activate (Mac/Linux)

# 3. Instale dependências
pip install -r requirements.txt

# 4. Migre banco de dados
python manage.py migrate

# 5. Crie superuser (admin)
python manage.py createsuperuser
# Username: admin
# Email: seu_email@example.com
# Password: 123456

# 6. Rode server
python manage.py runserver
```

Acesse:
- 🌐 App: http://localhost:8000
- 🔐 Admin: http://localhost:8000/admin

---

## 📦 Dependências

- Django 6.0.1
- django-jazzmin (admin bonito)

```bash
pip install -r requirements.txt
```

---

## 🔐 LOGIN

**Usuário padrão:** admin  
**Senha padrão:** 123456

---

## ✨ Features

- **(Contas a Pagar)**
  - Criar/Editar/Deletar contas
  - Baixa em lote
  - **Copiar com edição de valores/datas**
  - Recorrência automática

- **(Contas a Receber)**
  - Criar/Editar/Deletar contas
  - Recebimento em lote

- **(Plano de Contas)**
  - CRUD completo
  - Hierarquia (Grupo/Conta pai)

- **(Empresas)**
  - CRUD de fornecedores/clientes

- **(Admin)**
  - Interface Jazzmin (bonita!)
  - Registros customizados

---

## 🌍 Deploy no PythonAnywhere

### ⚠️ Antes de Deployer

Leia **ANTES de fazer nada**:

1. **[DEPLOYMENT_CHANGES.md](DEPLOYMENT_CHANGES.md)** - Mudanças no settings (ANTES → DEPOIS)
2. **[PYTHONANYWHERE_SETUP.md](PYTHONANYWHERE_SETUP.md)** - Passo a passo completo

### ⚡ Resumo Rápido

```bash
# 1. No PythonAnywhere (Bash console)
cd ~/financeiro
python manage.py migrate
python manage.py collectstatic --noinput

# 2. No dashboard PythonAnywhere:
# - Web → seu app → Edit configuration
# - Adicione variáveis: DEBUG=False, ALLOWED_HOSTS=sua_url, DJANGO_SECRET_KEY=novo_valor
# - Web → Reload

# 3. Acesse: https://seu_username.pythonanywhere.com
```

---

## 📋 Estrutura

```
financeiro/
├── contas_pagar/          # Contas a pagar (models, views, forms, etc)
├── contas_receber/        # Contas a receber
├── empresa/               # Empresas (fornecedores/clientes)
├── accounts/              # Usuários customizados
├── login/                 # Auto login/logout
├── templates/             # HTML base
├── requirements.txt       # Dependências
├── manage.py              # Django CLI
├── DEPLOYMENT_CHANGES.md  # 📌 MUDANÇAS NO SETTINGS (importante!)
├── PYTHONANYWHERE_SETUP.md # 📌 GUIA PASSO A PASSO (importante!)
└── README.md              # Este arquivo
```

---

## 🔧 Ambiente (Development)

Para desenvolvimento local, opcionalmente crie `.env`:

```bash
cp .env.example .env
# Edite conforme necessário (padrão já funciona)
```

---

## 📱 Usuário de Teste

```
Username: admin
Senha:    123456
```

Crie um ao seu gosto:
```bash
python manage.py createsuperuser
```

---

## 🚀 Próximos Passos

1. **Customize:** Adicione suas empresas, contas, etc
2. **Deploy:** Siga [PYTHONANYWHERE_SETUP.md](PYTHONANYWHERE_SETUP.md)
3. **Domínio:** Aponte seu domínio para PythonAnywhere
4. **PostgreSQL:** Migre de SQLite para DB melhor (depois)

---

## 🆘 Ajuda

- 📚 Docs Django: https://docs.djangoproject.com/en/6.0/
- 🎨 Jazzmin Docs: https://github.com/farridav/django-jazzmin
- 🚀 PythonAnywhere: https://help.pythonanywhere.com

---

## 📝 Licença

Projeto pessoal - Free to use

---

**Desenvolvido com ❤️ em Django**
