"""
Funções Auxiliares para Operações com Números Binários
"""


def normalize_binary(s):
    """
    Remove zeros à esquerda, mantendo pelo menos um dígito.
    Exemplo: "00101" -> "101", "0000" -> "0"
    """
    s = str(s).strip()
    s_stripped = s.lstrip('0')
    return s_stripped if s_stripped else '0'


def binary_to_decimal(binary_str):
    """
    Converte uma string binária para decimal.
    Exemplo: "1011" -> 11
    """
    binary_str = normalize_binary(binary_str)
    return int(binary_str, 2)


def decimal_to_binary(decimal_num):
    """
    Converte um número decimal para string binária sem '0b'.
    Exemplo: 11 -> "1011"
    """
    if decimal_num == 0:
        return "0"
    return bin(decimal_num)[2:]


def bin_add(a, b):
    """
    Soma dois números binários (strings).
    Exemplo: "101" + "011" = "1000" (5 + 3 = 8)
    """
    a = normalize_binary(a)
    b = normalize_binary(b)
    result = int(a, 2) + int(b, 2)
    return decimal_to_binary(result)


def bin_sub(a, b):
    """
    Subtrai dois números binários (strings). a - b
    Se resultado for negativo, retorna "0".
    Exemplo: "1011" - "0101" = "0110" (11 - 5 = 6)
    """
    a = normalize_binary(a)
    b = normalize_binary(b)
    result = int(a, 2) - int(b, 2)
    return decimal_to_binary(max(0, result))


def shift_left_binary(s, k):
    """
    Desloca uma string binária para a esquerda k posições.
    Equivalente a multiplicar por 2^k.
    Exemplo: "101" << 2 = "10100"
    """
    if k <= 0:
        return normalize_binary(s)
    s = normalize_binary(s)
    return s + '0' * k


def equal_length_binary(x, y):
    """
    Iguala o tamanho de duas strings binárias adicionando zeros à esquerda.
    Exemplo: ("101", "11") -> ("101", "011")
    """
    x = normalize_binary(x)
    y = normalize_binary(y)
    max_len = max(len(x), len(y))
    x = x.zfill(max_len)
    y = y.zfill(max_len)
    return x, y
