"""
Algoritmo de Karatsuba em Números Binários
Implementa multiplicação rápida usando Dividir e Conquistar
"""

from utils import normalize_binary, equal_length_binary, bin_add, bin_sub, shift_left_binary, decimal_to_binary

# Variável global para armazenar o rastreamento de passos
steps_trace = []


def karatsuba_binary(x, y, level=0):
    """
    Implementa o algoritmo de Karatsuba em strings binárias.
    
    FÓRMULA UTILIZADA:
    xy = 2^n · x1·y1 + 2^(n/2) · ((x1+x0)(y1+y0) - x1·y1 - x0·y0) + x0·y0
    
    Onde:
    - x1, x0 são as metades superior e inferior de x
    - y1, y0 são as metades superior e inferior de y
    - n é o tamanho total (n = 2m)
    - 2^n é deslocamento para ac (x1·y1)
    - 2^(n/2) é deslocamento para o termo do meio
    
    Retorna: resultado (string binária do produto)
    
    Parâmetros:
    - x, y: strings binárias
    - level: nível de profundidade recursiva (para rastreamento)
    """
    global steps_trace
    
    # Normalizar e igualar tamanho
    x = normalize_binary(x)
    y = normalize_binary(y)
    x, y = equal_length_binary(x, y)
    
    n = len(x)
    
    # Caso base: tamanho 1 → multiplicação direta
    if n == 1:
        result = decimal_to_binary(int(x, 2) * int(y, 2))
        step = {
            'level': level,
            'x': x,
            'y': y,
            'is_base_case': True,
            'result': result,
            'type': 'base_case'
        }
        steps_trace.append(step)
        return result
    
    # Se tamanho for ímpar, adicionar zero à esquerda para deixar par
    if n % 2 == 1:
        x = '0' + x
        y = '0' + y
        n = len(x)
    
    m = n // 2
    
    # PASSO 1: DIVIDIR
    # x = x1 | x0 (onde | significa concatenação)
    # y = y1 | y0
    x1 = x[:m]      # metade superior de x
    x0 = x[m:]      # metade inferior de x
    y1 = y[:m]      # metade superior de y
    y0 = y[m:]      # metade inferior de y
    
    # PASSO 2: CONQUISTAR (3 multiplicações recursivas em vez de 4)
    # x1·y1: multiplicação das metades superiores
    x1y1 = karatsuba_binary(x1, y1, level + 1)
    
    # x0·y0: multiplicação das metades inferiores
    x0y0 = karatsuba_binary(x0, y0, level + 1)
    
    # Termo do meio: (x1+x0)·(y1+y0) - x1·y1 - x0·y0
    soma_x = bin_add(x1, x0)      # x1 + x0
    soma_y = bin_add(y1, y0)      # y1 + y0
    meio_bruto = karatsuba_binary(soma_x, soma_y, level + 1)
    meio_ajustado = bin_sub(bin_sub(meio_bruto, x1y1), x0y0)
    
    # PASSO 3: COMBINAR (Fórmula do Karatsuba)
    # xy = 2^n · x1y1 + 2^(n/2) · meio_ajustado + x0y0
    # onde 2^n = deslocamento de 2m posições
    #       2^(n/2) = deslocamento de m posições
    x1y1_shifted = shift_left_binary(x1y1, 2 * m)      # x1·y1 << (2m)
    meio_shifted = shift_left_binary(meio_ajustado, m) # meio << m
    
    resultado = bin_add(bin_add(x1y1_shifted, meio_shifted), x0y0)
    resultado = normalize_binary(resultado)
    
    # Registrar passo detalhado para visualização
    step = {
        'level': level,
        'x': x,
        'y': y,
        # Divisão
        'a': x1,
        'b': x0,
        'c': y1,
        'd': y0,
        'm': m,
        # Multiplicações recursivas
        'ac': x1y1,
        'bd': x0y0,
        'soma_ab': soma_x,
        'soma_cd': soma_y,
        'meio': meio_bruto,
        'meio_ajustado': meio_ajustado,
        # Deslocamentos (combinação)
        'ac_shifted': x1y1_shifted,
        'meio_shifted': meio_shifted,
        'resultado': resultado,
        'is_base_case': False,
        'type': 'recursive'
    }
    steps_trace.append(step)
    
    return resultado


def karatsuba_solve(x, y):
    """
    Wrapper para chamar karatsuba_binary e retornar resultado + trace.
    
    Retorna um dicionário com:
    - resultado: string binária do produto
    - trace: lista de dicionários com todos os passos recursivos
    """
    global steps_trace
    steps_trace = []  # limpar trace anterior
    
    x = normalize_binary(x)
    y = normalize_binary(y)
    
    resultado = karatsuba_binary(x, y, level=0)
    
    return {
        'resultado': resultado,
        'trace': steps_trace
    }
