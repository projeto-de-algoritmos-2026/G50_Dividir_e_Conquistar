"""
Lógica de Gerenciamento do Jogo e Sessão
"""

import random
from flask import session


def get_bits_for_phase(phase):
    """Retorna o número de bits para cada fase."""
    phase_bits = {
        1: 4,
        2: 5,
        3: 6,
        4: 7,
        5: 8
    }
    return phase_bits.get(phase, 4)


def get_random_binary(bits):
    """
    Gera um número binário aleatório com 'bits' bits.
    Garante que não comece com 0 (exceto para o número 0 em si).
    """
    # Gerar um número entre 2^(bits-1) e 2^bits - 1
    min_val = 2 ** (bits - 1)
    max_val = 2 ** bits - 1
    num = random.randint(min_val, max_val)
    return bin(num)[2:]


def initialize_session():
    """Inicializa a sessão do jogo."""
    session['fase'] = 1
    session['pontuacao'] = 0
    session['jogo_acabou'] = False
    generate_new_numbers()


def generate_new_numbers():
    """Gera novos números binários para a fase atual."""
    phase = session.get('fase', 1)
    bits = get_bits_for_phase(phase)
    x = get_random_binary(bits)
    y = get_random_binary(bits)
    session['numeros_atuais'] = [x, y]
    session.modified = True


def process_answer(resposta_correta, acertou):
    """
    Processa a resposta do jogador e avança a fase se necessário.
    
    Retorna um dicionário com:
    - pontuacao: pontuação atual
    - fase: fase atual
    - jogo_acabou: boolean indicando se o jogo terminou
    """
    # Atualizar pontuação
    if acertou:
        session['pontuacao'] = session.get('pontuacao', 0) + 10
    
    # Avançar de fase ou finalizar jogo
    fase_atual = session.get('fase', 1)
    if acertou:
        if fase_atual < 5:
            session['fase'] = fase_atual + 1
            generate_new_numbers()
        else:
            session['jogo_acabou'] = True
    
    session.modified = True
    
    return {
        'pontuacao': session['pontuacao'],
        'fase': session['fase'],
        'jogo_acabou': session.get('jogo_acabou', False)
    }
