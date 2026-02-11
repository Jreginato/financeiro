# Configurações de Ambiente - Django

Este projeto possui **duas configurações separadas** para evitar confusão entre desenvolvimento e produção.

## 📁 Arquivos de Configuração

### ⚙️ `settings.py` - DESENVOLVIMENTO LOCAL
- **Uso**: Desenvolvimento local no seu computador
- **DEBUG**: `True` (mostra erros detalhados)
- **Banco**: SQLite local (`db.sqlite3`)
- **ALLOWED_HOSTS**: `localhost, 127.0.0.1`
- **Segurança**: Relaxada para facilitar desenvolvimento

**Como usar:**
```bash
# Rodar servidor local (usa settings.py por padrão)
python manage.py runserver

# Migrations
python manage.py migrate

# Criar superuser
python manage.py createsuperuser
```

---

### 🚀 `settings_2.py` - PRODUÇÃO (PythonAnywhere)
- **Uso**: Produção no PythonAnywhere
- **DEBUG**: `False` (não mostra erros sensíveis)
- **Banco**: SQLite ou MySQL (configurável)
- **ALLOWED_HOSTS**: Domínio do PythonAnywhere
- **Segurança**: Completa (HTTPS, cookies seguros, etc.)

**Como usar:**

#### 1. Antes do Deploy - Configure o arquivo:
```python
# Em settings_2.py, altere:

SECRET_KEY = 'gere-uma-nova-chave-secreta'  # Use o comando abaixo para gerar
ALLOWED_HOSTS = ['seuusername.pythonanywhere.com']  # Seu domínio real
```

**Gerar SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### 2. No PythonAnywhere - Configure o WSGI:

Edite o arquivo `/var/www/seuusername_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

# Adicione o caminho do projeto
path = '/home/seuusername/financeiro'
if path not in sys.path:
    sys.path.append(path)

# IMPORTANTE: Use settings_2 para produção
os.environ['DJANGO_SETTINGS_MODULE'] = 'financeiro.settings_2'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 3. Collectstatic (arquivos CSS/JS):
```bash
python manage.py collectstatic --settings=financeiro.settings_2
```

#### 4. Migrations em Produção:
```bash
python manage.py migrate --settings=financeiro.settings_2
```

#### 5. Criar Superuser em Produção:
```bash
python manage.py createsuperuser --settings=financeiro.settings_2
```

---

## 🔧 Diferenças Principais

| Configuração | settings.py (DEV) | settings_2.py (PROD) |
|--------------|-------------------|----------------------|
| **DEBUG** | `True` | `False` |
| **SECRET_KEY** | Padrão (insegura) | Única e secreta |
| **ALLOWED_HOSTS** | localhost | Domínio PythonAnywhere |
| **HTTPS** | Não obrigatório | Obrigatório |
| **Validação de Senha** | Desabilitada | Habilitada (mín. 8 caracteres) |
| **Logging** | Console | Arquivo + Console |
| **Static Files** | Desenvolvimento | Collectstatic |

---

## ⚠️ IMPORTANTE - Checklist de Deploy

Antes de fazer deploy no PythonAnywhere:

- [ ] Alterar `SECRET_KEY` em `settings_2.py`
- [ ] Configurar `ALLOWED_HOSTS` com seu domínio
- [ ] Se usar MySQL, configurar credenciais do banco
- [ ] Atualizar `wsgi.py` para usar `settings_2`
- [ ] Executar `collectstatic`
- [ ] Executar `migrate` em produção
- [ ] Criar superuser em produção
- [ ] Testar login e funcionalidades básicas
- [ ] Verificar que DEBUG está False

---

## 🆘 Troubleshooting

### Erro: "DisallowedHost"
- Configure `ALLOWED_HOSTS` em `settings_2.py` com seu domínio exato

### Erro: "Static files not found"
- Execute `collectstatic` em produção
- Configure mapeamento na aba Web do PythonAnywhere:
  - URL: `/static/`
  - Directory: `/home/seuusername/financeiro/staticfiles`

### Erro: "SECRET_KEY not secure"
- Gere uma nova chave única para produção
- Nunca compartilhe a SECRET_KEY de produção

---

## 📝 Comandos Úteis

### Testar com settings de produção localmente:
```bash
python manage.py runserver --settings=financeiro.settings_2
```

### Ver qual settings está sendo usado:
```bash
python manage.py diffsettings --settings=financeiro.settings_2 | grep SETTINGS_MODULE
```

---

**Dica**: Sempre use `settings.py` para desenvolvimento local e `settings_2.py` apenas em produção!
