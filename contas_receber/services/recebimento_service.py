from datetime import datetime
from contas_receber.models import ContaReceber


class RecebimentoService:

    @staticmethod
    def receber_conta(conta, valor_recebido, data_recebimento):
        valor_recebido = float(str(valor_recebido).replace(".", "").replace(",", "."))
        if valor_recebido <= 0:
            return

        conta.valor_recebido = valor_recebido
        conta.data_recebimento = data_recebimento
        conta.status = ContaReceber.Status.RECEBIDA
        conta.save()

    @staticmethod
    def receber_em_lote(contas, dados):
        for conta in contas:
            valor = dados.get(f"valor_recebido_{conta.id}")
            data = dados.get(f"data_recebimento_{conta.id}")

            if not valor or not data:
                continue

            RecebimentoService.receber_conta(
                conta,
                valor_recebido=valor,
                data_recebimento=datetime.strptime(data, "%Y-%m-%d").date()
            )
