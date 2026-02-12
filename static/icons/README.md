# Gerador de Ícones PWA

Este script gera todos os ícones necessários para o PWA a partir de uma imagem base.

## Pré-requisitos
```bash
pip install Pillow
```

## Como usar

1. Crie uma imagem quadrada de alta resolução (pelo menos 512x512px) com o ícone do seu app
2. Salve como `icon-base.png` nesta mesma pasta
3. Execute o script:

```bash
python gerar_icones.py
```

Os ícones serão criados automaticamente na pasta `icons/`.

## Alternativa: Usar ferramenta online

Se preferir, use: https://www.pwabuilder.com/imageGenerator

1. Faça upload da sua imagem
2. Baixe o pacote de ícones
3. Extraia na pasta `static/icons/`
