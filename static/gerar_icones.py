"""
Script para gerar ícones PWA em todos os tamanhos necessários
"""
from PIL import Image
import os

# Tamanhos necessários para PWA
TAMANHOS = [72, 96, 128, 144, 152, 192, 384, 512]

def gerar_icones(imagem_base):
    """Gera todos os ícones necessários para PWA"""
    
    # Criar pasta icons se não existir
    os.makedirs('icons', exist_ok=True)
    
    # Abrir imagem base
    img = Image.open(imagem_base)
    
    # Converter para RGBA se necessário
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Gerar cada tamanho
    for tamanho in TAMANHOS:
        # Redimensionar mantendo qualidade
        img_redimensionada = img.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
        
        # Salvar
        nome_arquivo = f'icons/icon-{tamanho}x{tamanho}.png'
        img_redimensionada.save(nome_arquivo, 'PNG', optimize=True)
        print(f'✓ Criado: {nome_arquivo}')
    
    print(f'\n✅ {len(TAMANHOS)} ícones criados com sucesso!')

if __name__ == '__main__':
    # Verificar se existe imagem base
    if not os.path.exists('wallet.png'):
        print('❌ Erro: Arquivo wallet.png não encontrado!')
        print('\nCrie uma imagem quadrada (pelo menos 512x512px) e salve como "wallet.png"')
        print('Ou use: https://www.pwabuilder.com/imageGenerator')
    else:
        gerar_icones('wallet.png')
