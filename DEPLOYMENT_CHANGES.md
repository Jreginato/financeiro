# 📋 Documentação das Mudanças para Deployment

Este arquivo documenta **TODAS as mudanças** necessárias para publicar no PythonAnywhere.

## ✅ Mudanças Realizadas

### 1. **financeiro/settings.py**

#### Linha 14 - Import `os`
```python
# ANTES: 
  from pathlib import Path

# DEPOIS:
  import os
  from pathlib import Path
```
**Por quê?** Para ler variáveis de ambiente.

---

#### Linha 23-28 - SECRET_KEY
```python
# ANTES:
  SECRET_KEY = 'django-insecure-c&xg5cyk9k($p04+ay7=ho#cq2knt5-n#trswxhc91ajhtum6)'

# DEPOIS:
  SECRET_KEY = os.environ.get(
      'DJANGO_SECRET_KEY', 
      'django-insecure-c&xg5cyk9k($p04+ay7=ho#cq2knt5-n#trswxhc91ajhtum6)'
  )
```
**Por quê?** Em produção, a chave vem de variável de ambiente (mais seguro).  
**Para voltar:** Use a linha simples `SECRET_KEY = '...'`

---

#### Linha 31-33 - DEBUG
```python
# ANTES:
  DEBUG = True

# DEPOIS:
  DEBUG = os.environ.get('DEBUG', 'True') == 'True'
```
**Por quê?** Em produção será `DEBUG=False` via variável de ambiente.  
**Para voltar:** Use `DEBUG = True`

---

#### Linha 35-37 - ALLOWED_HOSTS
```python
# ANTES:
  ALLOWED_HOSTS = []

# DEPOIS:
  ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```
**Por quê?** Permite localhost em dev, e seu domínio em produção.  
**Para voltar:** Use `ALLOWED_HOSTS = []`

---

#### Linha ~115-117 - STATIC_ROOT
```python
# ANTES:
  STATIC_URL = 'static/'

# DEPOIS:
  STATIC_URL = 'static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```
**Por quê?** Necessário para coletar arquivos estáticos em produção.  
**Para voltar:** Delete a linha `STATIC_ROOT = ...`

---

## 🔄 Como Reverter para Estado Original

### Opção 1: Reverter tudo
```bash
git checkout financeiro/settings.py
```

### Opção 2: Manual
Desfaça as 5 mudanças acima (segue o ANTES em cada seção).

---

## 🚀 Próximos Passos em Produção

### No PythonAnywhere, na aba **Web App** → **Edit configuration**:

Adicione estas variáveis de ambiente:
```
DEBUG = False
ALLOWED_HOSTS = seu_username.pythonanywhere.com
DJANGO_SECRET_KEY = (gere uma nova chave segura)
```

### Gerar nova SECRET_KEY:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## 📝 Resumo das Variáveis de Ambiente

| Variável | Desenvolvimento | Produção |
|----------|-----------------|----------|
| `DEBUG` | `True` | `False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | `seu_username.pythonanywhere.com` |
| `DJANGO_SECRET_KEY` | Inclusa no arquivo | Defina no PythonAnywhere |

---

## ⚠️ Importante

- **Nunca** deixe `DEBUG=True` em produção
- **Sempre** mude a `SECRET_KEY` em produção
- **ALLOWED_HOSTS** deve ter seu domínio real
- Depois de fazer as mudanças, teste localmente com `DEBUG=False`

