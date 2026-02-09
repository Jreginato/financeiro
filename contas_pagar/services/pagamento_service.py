from datetime import datetime
from contas_pagar.models import ContaPagar

class PagamentoService:

    @staticmethod
    def baixar_conta(conta, valor_pago, data_pagamento):
        valor_pago = float(str(valor_pago).replace(".", "").replace(",", "."))
        if valor_pago <= 0:
            return

        conta.valor_pago = valor_pago
        conta.data_pagamento = data_pagamento
        conta.status = ContaPagar.Status.PAGA
        conta.save()

    @staticmethod
    def baixar_em_lote(contas, dados):
        for conta in contas:
            valor = dados.get(f"valor_pago_{conta.id}")
            data = dados.get(f"data_pagamento_{conta.id}")

            if not valor or not data:
                continue

            PagamentoService.baixar_conta(
                conta,
                valor_pago=valor,
                data_pagamento=datetime.strptime(data, "%Y-%m-%d").date()
            )

    @staticmethod
    def copiar_conta(conta_original, descricao, valor, data_vencimento):
        """Cria uma nova conta a pagar baseada em uma existente."""
        nova_conta = ContaPagar(
            descricao=descricao,
            fornecedor=conta_original.fornecedor,
            plano_conta=conta_original.plano_conta,
            valor=valor,
            data_vencimento=data_vencimento,
            status=ContaPagar.Status.PENDENTE,
            recorrencia=ContaPagar.Recorrencia.NENHUMA,
        )
        nova_conta.save()
        return nova_conta

    @staticmethod
    def copiar_em_lote(contas, dados):
        """Copia múltiplas contas com novos valores e datas."""
        for conta in contas:
            descricao = dados.get(f"descricao_{conta.id}", conta.descricao)
            valor = dados.get(f"valor_{conta.id}")
            data = dados.get(f"data_vencimento_{conta.id}")

            if not valor or not data:
                continue

            valor = float(str(valor).replace(".", "").replace(",", "."))
            if valor <= 0:
                continue

            PagamentoService.copiar_conta(
                conta,
                descricao=descricao,
                valor=valor,
                data_vencimento=datetime.strptime(data, "%Y-%m-%d").date()
            )