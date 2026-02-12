# 📱 Guia de Instalação - PWA (Progressive Web App)

## O que é PWA?

PWA permite que você instale o sistema financeiro no seu celular como se fosse um aplicativo nativo, com:
- ✅ Ícone na tela inicial
- ✅ Funciona sem conexão (cache offline)
- ✅ Visual em tela cheia (sem barra do navegador)
- ✅ Notificações push (futuro)
- ✅ Carregamento mais rápido

---

## 🎨 Passo 1: Gerar Ícones

### Opção A: Script Python (Recomendado)

1. Instale Pillow:
```bash
pip install Pillow
```

2. Crie uma imagem quadrada 512x512px com o logo do app e salve como `icon-base.png` em `static/`

3. Execute o gerador:
```bash
cd static
python gerar_icones.py
```

### Opção B: Ferramenta Online

1. Acesse: https://www.pwabuilder.com/imageGenerator
2. Faça upload de uma imagem quadrada (512x512px)
3. Baixe o pacote e extraia em `static/icons/`

---

## 🚀 Passo 2: Configurar o Servidor

### Para desenvolvimento local:

O Django já está configurado para servir arquivos estáticos em desenvolvimento.

### Para produção:

Certifique-se de que `settings.py` tem:

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

Execute:
```bash
python manage.py collectstatic
```

---

## 📲 Passo 3: Instalar no Celular

### Android (Chrome/Edge):

1. Abra o site no Chrome/Edge
2. Espere aparecer o banner "Adicionar à tela inicial" ou:
3. Toque no menu (⋮) > "Instalar app" ou "Adicionar à tela inicial"
4. Confirme a instalação
5. O app aparecerá na tela inicial e gaveta de apps

### iOS (Safari):

1. Abra o site no Safari
2. Toque no botão de compartilhar (□↑)
3. Role para baixo e selecione "Adicionar à Tela de Início"
4. Personalize o nome se quiser
5. Toque em "Adicionar"

---

## 🔧 Passo 4: Configurações Adicionais (Opcional)

### HTTPS é obrigatório em produção

Service Workers só funcionam em HTTPS (exceto localhost). Para produção:

1. Use Cloudflare, Let's Encrypt ou certificado SSL
2. Configure redirecionamento HTTP → HTTPS

### Testar PWA

1. Chrome DevTools > Application > Manifest
2. Verifique se todos os ícones carregaram
3. Application > Service Workers > Verifique se está ativo

---

## 🎯 URLs Importantes

- Manifest: `/static/manifest.json`
- Service Worker: `/static/service-worker.js`
- Ícones: `/static/icons/icon-*x*.png`

---

## 🐛 Solução de Problemas

### "Adicionar à tela inicial" não aparece

- Verifique se está usando HTTPS (ou localhost)
- Confirme que manifest.json está acessível
- Verifique se os ícones existem
- Limpe cache do navegador

### Service Worker não registra

- Abra DevTools > Console para ver erros
- Verifique se o caminho está correto
- Service Worker precisa estar na raiz ou acima das páginas

### Ícones não aparecem

- Verifique se os arquivos existem em `static/icons/`
- Execute `python manage.py collectstatic` em produção
- Verifique URLs no manifest.json

---

## 🔄 Atualizar PWA

Quando fizer mudanças:

1. Atualize a versão no `service-worker.js`:
```javascript
const CACHE_NAME = 'financeiro-v2'; // Incrementar versão
```

2. O service worker detectará automaticamente e atualizará

---

## 📊 Recursos Adicionais

### Adicionar mais páginas ao cache offline

Edite `service-worker.js`:

```javascript
const urlsToCache = [
  '/',
  '/login/',
  '/contas-pagar/',
  '/contas-receber/',
  '/empresa/dashboard/',
  // Adicione mais URLs aqui
];
```

### Personalizar comportamento offline

Você pode criar uma página customizada de "offline" e servir quando não houver conexão.

---

## ✅ Checklist Final

- [ ] Ícones gerados (72x72 até 512x512)
- [ ] manifest.json configurado
- [ ] service-worker.js criado
- [ ] Meta tags adicionadas no base.html
- [ ] HTTPS configurado (produção)
- [ ] Testado no Chrome DevTools
- [ ] Instalado e testado no celular

---

## 🎉 Pronto!

Seu sistema agora é um PWA completo! Os usuários podem instalar direto do navegador e usar como app nativo.

Para mais informações: https://web.dev/progressive-web-apps/
