# 🚀 Deploy Rápido - PythonAnywhere

## Passo a Passo para Publicar

### 1️⃣ Preparar o Projeto Localmente

```bash
# 1. Certifique-se que tudo está commitado
git status
git add .
git commit -m "Preparando para deploy"
git push origin main
```

### 2️⃣ Configurar settings_2.py

```bash
# 2. Gere uma SECRET_KEY nova
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Edite `financeiro/settings_2.py`:
```python
SECRET_KEY = 'cole-a-chave-gerada-aqui'
ALLOWED_HOSTS = ['seuusername.pythonanywhere.com']
```

### 3️⃣ No PythonAnywhere Console

```bash
# 3. Clone o repositório (primeira vez apenas)
cd ~
git clone https://github.com/seuusername/financeiro.git
cd financeiro

# 4. Crie o ambiente virtual
python3.10 -m venv venv
source venv/bin/activate

# 5. Instale as dependências
pip install -r requirements.txt

# 6. Configure o banco de dados
python manage.py migrate --settings=financeiro.settings_2

# 7. Colete arquivos estáticos
python manage.py collectstatic --settings=financeiro.settings_2 --noinput

# 8. Crie o superuser
python manage.py createsuperuser --settings=financeiro.settings_2
```

### 4️⃣ Configurar WSGI no PythonAnywhere

Na aba **Web** do PythonAnywhere, clique em **"WSGI configuration file"** e edite:

```python
import os
import sys

# Caminho do projeto
path = '/home/seuusername/financeiro'
if path not in sys.path:
    sys.path.append(path)

# Ativar ambiente virtual
os.environ['VIRTUAL_ENV'] = '/home/seuusername/financeiro/venv'

# IMPORTANTE: Use settings_2 para PRODUÇÃO
os.environ['DJANGO_SETTINGS_MODULE'] = 'financeiro.settings_2'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5️⃣ Configurar Arquivos Estáticos

Na aba **Web**, seção **Static files**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/seuusername/financeiro/staticfiles` |

### 6️⃣ Recarregar a Aplicação

Clique no botão verde **"Reload seuusername.pythonanywhere.com"**

---

## 🔄 Atualizações Futuras

Quando fizer mudanças no código:

```bash
# No PythonAnywhere Console
cd ~/financeiro
source venv/bin/activate

# Puxar atualizações do GitHub
git pull origin main

# Se tiver novas dependências
pip install -r requirements.txt

# Se tiver novas migrations
python manage.py migrate --settings=financeiro.settings_2

# Se tiver mudanças em CSS/JS
python manage.py collectstatic --settings=financeiro.settings_2 --noinput

# Recarregar na aba Web (botão verde)
```

---

## ✅ Checklist de Deploy

- [ ] `settings_2.py` configurado com SECRET_KEY única
- [ ] `ALLOWED_HOSTS` configurado com domínio correto
- [ ] Git push feito
- [ ] Repositório clonado no PythonAnywhere
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Migrations executadas
- [ ] Collectstatic executado
- [ ] Superuser criado
- [ ] WSGI configurado para usar `settings_2`
- [ ] Static files mapeados
- [ ] Aplicação recarregada
- [ ] Testado: consegue acessar o site
- [ ] Testado: consegue fazer login no admin

---

## 🆘 Problemas Comuns

### Site não carrega (500 Error)
1. Verifique o **Error Log** na aba Web
2. Confirme que `WSGI` está usando `settings_2`
3. Verifique se `ALLOWED_HOSTS` está correto

### Admin sem CSS
1. Execute `collectstatic` novamente
2. Verifique mapeamento de `/static/` na aba Web
3. Recarregue a aplicação

### Erro de Database
1. Execute `migrate --settings=financeiro.settings_2`
2. Verifique permissões do arquivo `db.sqlite3`

### Mudanças não aparecem
1. Sempre faça `git pull` no PythonAnywhere
2. Recarregue a aplicação (botão verde)
3. Limpe cache do navegador (Ctrl+Shift+R)

---

## 📞 Comandos Úteis

```bash
# Ver logs de erro
tail -n 50 /var/log/seuusername.pythonanywhere.com.error.log

# Testar se settings_2 está funcionando
python manage.py check --settings=financeiro.settings_2

# Shell com settings de produção
python manage.py shell --settings=financeiro.settings_2
```

---

**Última atualização**: 11/02/2026
