# 🚀 Guia de Deployment - PythonAnywhere

## 📌 Resumo Rápido

1. ✅ Mudanças em `settings.py` já foram feitas (veja `DEPLOYMENT_CHANGES.md`)
2. 📋 Vamos agora:
   - Criar conta no PythonAnywhere
   - Clonar o projeto
   - Instalar dependências
   - Executar migrations
   - Configurar variáveis de ambiente

---

## 1️⃣ Criar Conta no PythonAnywhere

1. Acesse https://www.pythonanywhere.com
2. Clique em **Sign up**
3. Escolha plano **Free** (suficiente para começar)
4. Confirme email

---

## 2️⃣ Criar Web App

1. No dashboard, vá em **Web**
2. Clique **Add a new web app**
3. Escolha:
   - Domínio: `seu_username.pythonanywhere.com` (automático)
   - Python 3.10 (recomendado)
   - Framework: **Manual configuration** (deixe o Django automático para depois)
4. **Create web app**

Seu URL será: `https://seu_username.pythonanywhere.com`

---

## 3️⃣ Clonar o Projeto (via Console)

1. Na página do **Web**, procure por um link para **Console**
2. Ou vá em **Consoles** → **Bash**

No console, execute:

```bash
# Navegue para home
cd ~

# Clone seu repositório GitHub
git clone https://github.com/seu_usuario/financeiro.git

# Entre no projeto
cd financeiro
```

Se ainda **não tem no GitHub**, suba lá primeiro:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/seu_usuario/financeiro.git
git branch -M main
git push -u origin main
```

---

## 4️⃣ Criar Virtual Environment

No console PythonAnywhere:

```bash
# Criar e ativar venv seguro
mkvirtualenv --python=/usr/bin/python3.10 financeiro

# Será ativado automaticamente (vê o prefixo)
```

Instale as dependências:

```bash
pip install Django==6.0.1 django-jazzmin
```

---

## 5️⃣ Executar Migrations e Criar Superuser

```bash
# Entre no diretório do projeto
cd ~/financeiro

# Migrations
python manage.py migrate

# Criar admin
python manage.py createsuperuser
# Siga as instruções (username, email, senha)
```

---

## 6️⃣ Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

Isso cria a pasta `staticfiles/ ` com CSS, JS, imagens.

---

## 7️⃣ Configurar Variáveis de Ambiente

### No PythonAnywhere:

1. Vá em **Web**
2. Procure por seu app
3. Role até **Environment variables**
4. Clique **Edit**
5. Adicione:

```
DEBUG = False
ALLOWED_HOSTS = seu_username.pythonanywhere.com
DJANGO_SECRET_KEY = (chave segura abaixo)
```

### Gerar SECRET_KEY segura:

No console:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copie a saída e cole em `DJANGO_SECRET_KEY`.

---

## 8️⃣ Configurar Arquivo WSGI

1. Na aba **Web**, clique em **Edit configuration file**
2. Encontre a linha que começa com `import sys`
3. Edite para:

```python
import os
import sys

# MUDE ISSO PARA SEU USERNAME
path = '/home/seu_username/financeiro'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'financeiro.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## 9️⃣ Configurar Arquivos Estáticos

Na aba **Web**, seção **Static files**, clique **Edit**:

1. Delete tudo que estiver lá (padrão do PythonAnywhere)
2. Adicione:

```
URL: /static/
Directory: /home/seu_username/financeiro/staticfiles
```

Clique **Add**

---

## 🔟 Recarregar App

Na aba **Web**, procure pelo botão **Reload** (verde)

Clique para ativar as mudanças.

---

## ✅ Pronto!

Sua app está online em: **`https://seu_username.pythonanywhere.com`**

Admin em: **`https://seu_username.pythonanywhere.com/admin`**

---

## 🆘 Troubleshooting

### ❌ Erro 500

1. Vá em **Web** → **Error log**
2. Use para diagnosticar problema
3. Comandos úteis:

```bash
# Check settings (no console)
python manage.py check --deploy

# Ver logs de erro do banco
python manage.py shell
>>> from contas_pagar.models import ContaPagar
>>> ContaPagar.objects.all()
```

### ❌ Estáticos não carregam (CSS/JS não funcionam)

```bash
# Re-collected
python manage.py collectstatic --noinput --clear

# Reload app novamente
```

### ❌ Erro de conexão ao banco

```bash
# Verifique banco
python manage.py dbshell

# Se não entrar, refaça migrate
python manage.py migrate --run-syncdb
```

---

## 📱 Acessar Console Depois

Quando quiser voltar ao console PythonAnywhere:

1. Vá em **Consoles**
2. Procure seu console anterior ou crie novo
3. Ative venv:
   ```bash
   workon financeiro
   cd ~/financeiro
   ```
4. Pronto para rodar comandos!

---

## 🔐 Segurança Checklist

- ✅ `DEBUG = False` em produção
- ✅ `SECRET_KEY` diferente (gere uma nova)
- ✅ `ALLOWED_HOSTS` com seu domínio
- ✅ Senhas strong para superuser
- ✅ HTTPS ativado (PythonAnywhere faz automaticamente)

---

## 📚 Próximos Passos

1. **Domain Próprio?** Configure DNS para apontar para PythonAnywhere
2. **PostgreSQL?** PythonAnywhere oferecido grátis (upgrade pago)
3. **Email?** Configure SMTP para enviar notificações
4. **Backup?** PythonAnywhere tem backup automático (Free tem limite)

---

## 📞 Suporte

- Docs PythonAnywhere: https://help.pythonanywhere.com
- Django Deployment: https://docs.djangoproject.com/en/6.0/howto/deployment/
- Problemas? Verifique `Error log` em **Web**
