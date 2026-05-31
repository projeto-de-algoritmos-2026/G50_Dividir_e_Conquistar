"""
Cofre Binário Karatsuba - Jogo Educativo sobre o Algoritmo de Karatsuba em Binário
Aplicação Flask principal com rotas e gerenciamento de sessão.
"""

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import secrets

from karatsuba import karatsuba_solve
from utils import normalize_binary, binary_to_decimal
from game import initialize_session, generate_new_numbers, process_answer

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# ========================= ROTAS FLASK =========================

@app.route('/')
def index():
    """Página inicial."""
    return render_template('index.html')


@app.route('/game')
def game():
    """Tela do jogo."""
    # Verificar se a sessão foi inicializada
    if 'fase' not in session:
        initialize_session()
    
    if session.get('jogo_acabou', False):
        # Se jogo acabou, redirecionar para resultado final
        return render_template('result.html',
                             fase=session['fase'],
                             pontuacao=session['pontuacao'],
                             jogo_acabou=True)
    
    x, y = session.get('numeros_atuais', ['0', '0'])
    fase = session.get('fase', 1)
    pontuacao = session.get('pontuacao', 0)
    
    return render_template('game.html',
                         x=x,
                         y=y,
                         fase=fase,
                         pontuacao=pontuacao)


@app.route('/check', methods=['POST'])
def check():
    """
    Recebe a resposta do jogador, valida e calcula o resultado com Karatsuba.
    Retorna JSON com resultado, trace e feedback.
    """
    data = request.get_json()
    resposta_jogador = data.get('resposta', '').strip()
    
    # Validar entrada
    if not resposta_jogador:
        return jsonify({
            'erro': 'Por favor, digite uma resposta.'
        }), 400
    
    if not all(c in '01' for c in resposta_jogador):
        return jsonify({
            'erro': 'A resposta deve conter apenas 0 e 1.'
        }), 400
    
    # Obter números atuais
    x, y = session.get('numeros_atuais', ['0', '0'])
    
    # Resolver com Karatsuba
    solucao = karatsuba_solve(x, y)
    resposta_correta = solucao['resultado']
    trace = solucao['trace']
    
    # Normalizar para comparação
    resposta_jogador_norm = normalize_binary(resposta_jogador)
    resposta_correta_norm = normalize_binary(resposta_correta)
    
    # Verificar se acertou
    acertou = resposta_jogador_norm == resposta_correta_norm
    
    # Processar resposta (atualizar sessão)
    game_status = process_answer(resposta_correta_norm, acertou)
    
    # Preparar resposta
    return jsonify({
        'acertou': acertou,
        'x': x,
        'y': y,
        'resposta_jogador': resposta_jogador_norm,
        'resposta_jogador_decimal': binary_to_decimal(resposta_jogador_norm),
        'resposta_correta': resposta_correta_norm,
        'x_decimal': binary_to_decimal(x),
        'y_decimal': binary_to_decimal(y),
        'resultado_decimal': binary_to_decimal(resposta_correta),
        'pontuacao': game_status['pontuacao'],
        'fase': game_status['fase'],
        'jogo_acabou': game_status['jogo_acabou'],
        'trace': trace
    })


@app.route('/reset')
def reset():
    """Reinicia o jogo."""
    session.clear()
    return redirect(url_for('index'))


# ========================= EXECUTAR =========================

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
