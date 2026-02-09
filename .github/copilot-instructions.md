## Resumo rápido

Projeto Django (Django 6) monolítico com 3 apps principais: `accounts`, `contas_pagar`, `empresa`.
Banco local: SQLite (`db.sqlite3`). Admin usa `jazzmin` (tema). Template base em `templates/base.html`.

## Arquitetura e padrões importantes
- **Camadas**: `views` -> `forms` (validação) -> `services` (lógica de negócio) -> `models`.
- **Serviços**: ver `contas_pagar/services/pagamento_service.py` — é aqui que ficam regras operacionais (ex.: `PagamentoService.baixar_em_lote`).
- **Formulários**: `contas_pagar/forms.py` faz validações compostas (ex.: exigência de `quantidade_recorrencias` quando `recorrencia` é diferente de `nenhuma`).
- **Modelos**: `contas_pagar/models.py` contém `ContaPagar` e `PlanoDeContas` — enumerações de `Status` e `Recorrencia` são usadas frequentemente nas views e templates.
- **Usuário**: `AUTH_USER_MODEL` está em `accounts.models.User` (modelo customizado).

## Fluxos e exemplos concretos
- Lançamento -> `conta_pagar_criar` (view) -> salva `ContaPagar` -> se houver recorrência e `quantidade_recorrencias` redireciona para `contas_pagar_recorrencia_previa` (ver [contas_pagar/views.py](contas_pagar/views.py#L1-L120)).
- Baixa em lote: a template [contas_pagar/baixa_tabela.html](contas_pagar/templates/contas_pagar/baixa_tabela.html#L1-L120) gera inputs nomeados como `valor_pago_{id}` e `data_pagamento_{id}`; o service os consome em `PagamentoService.baixar_em_lote` (veja [contas_pagar/services/pagamento_service.py](contas_pagar/services/pagamento_service.py#L1-L80)).
- Formato de moeda/data: front-end usa máscara jQuery (`000.000.000,00`) — o backend converte vírgula para ponto ao parsear valores em `pagamento_service.py`.

## Convenções do projeto
- Strings de escolha (enums) nos modelos são fundamentais — filtre por `ContaPagar.Status` e `ContaPagar.Recorrencia` nas queries.
- Nomeação de rotas: prefixo `contas-pagar/`; nomes de URL principais: `contas_pagar_lista`, `conta_pagar_criar`, `conta_pagar_editar`, `contas_pagar_baixa_confirmar` (veja [contas_pagar/urls.py](contas_pagar/urls.py#L1-L40)).
- Templates por app em `contas_pagar/templates/contas_pagar/` e template global em `templates/base.html`.

## Comandos de desenvolvimento (rápido)
- Criar e ativar virtualenv (sugestão): `python -m venv .venv && .venv\Scripts\activate` (Windows).
- Instalar dependências: `pip install django==6.0.1 jazzmin` (adapte conforme requirements locais).
- Migrar banco: `python manage.py migrate`.
- Superuser: `python manage.py createsuperuser`.
- Rodar servidor: `python manage.py runserver`.

## Pontos de atenção para PRs e mudanças
- Evite colocar lógica complexa diretamente em views; siga o padrão `services` para regras de negócio.
- Ao alterar campos de modelo (especialmente enums), verifique views, forms e templates por usos literais.
- Internacionalização: settings usam `pt-BR` e timezone `America/Sao_Paulo`. Formatos de moeda esperam vírgula decimal.

## Locais a consultar primeiro (rápido)
- [financeiro/settings.py](financeiro/settings.py#L1-L120)
- [contas_pagar/models.py](contas_pagar/models.py#L1-L200)
- [contas_pagar/views.py](contas_pagar/views.py#L1-L220)
- [contas_pagar/services/pagamento_service.py](contas_pagar/services/pagamento_service.py#L1-L200)
- [contas_pagar/templates/contas_pagar/baixa_tabela.html](contas_pagar/templates/contas_pagar/baixa_tabela.html#L1-L120)

Se algo ficou ambíguo ou você quer que eu inclua exemplos de PRs ou checagens automáticas (tests/pre-commit), diga qual formato prefere e eu atualizo.
