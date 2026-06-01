/**
 * Cofre Binário Karatsuba - Script Frontend
 * Gerencia interações do jogo, validação de entrada e renderização de resultados
 */

// Elementos do DOM
const answerInput = document.getElementById('answer-input');
const checkBtn = document.getElementById('check-btn');
const errorMessage = document.getElementById('error-message');
const loadingDiv = document.getElementById('loading');
const feedbackSection = document.getElementById('feedback-section');
const feedbackCard = document.getElementById('feedback-card');
const scoreSpan = document.getElementById('score');
const phaseSpan = document.getElementById('phase-number');

// Habilitar/desabilitar botão baseado na entrada
if (answerInput) {
    answerInput.addEventListener('input', function() {
        errorMessage.style.display = 'none';
        checkBtn.disabled = this.value.trim() === '';
    });

    // Permitir enviar com Enter
    answerInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !checkBtn.disabled) {
            checkBtn.click();
        }
    });
}

// Botão de verificação
if (checkBtn) {
    checkBtn.addEventListener('click', submitAnswer);
}

/**
 * Valida se a entrada contém apenas 0 e 1
 */
function isValidBinary(str) {
    return /^[01]+$/.test(str);
}

/**
 * Envia a resposta para o servidor
 */
async function submitAnswer() {
    const resposta = answerInput.value.trim();

    // Validar entrada
    if (!resposta) {
        showError('Por favor, digite uma resposta.');
        return;
    }

    if (!isValidBinary(resposta)) {
        showError('A resposta deve conter apenas 0 e 1 (sem espaços ou outros caracteres).');
        return;
    }

    // Mostrar carregamento
    loadingDiv.style.display = 'block';
    checkBtn.disabled = true;
    answerInput.disabled = true;
    errorMessage.style.display = 'none';

    try {
        const response = await fetch('/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ resposta: resposta })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.erro || 'Erro ao processar resposta');
        }

        const data = await response.json();

        // Renderizar feedback
        renderFeedback(data);

        // Remover reload automático - agora o usuário clica no botão

    } catch (error) {
        showError(error.message);
        checkBtn.disabled = false;
        answerInput.disabled = false;
    } finally {
        loadingDiv.style.display = 'none';
    }
}

/**
 * Exibe mensagem de erro
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

/**
 * Renderiza o feedback da resposta
 */
function renderFeedback(data) {
    const acertou = data.acertou;
    const feedbackHTML = [];

    // Header do feedback
    const headerHTML = `
        <div class="feedback-header">
            <span class="feedback-icon">${acertou ? '✅' : '❌'}</span>
            <div>
                <div class="feedback-status ${acertou ? 'correct' : 'incorrect'}">
                    ${acertou ? 'Cofre Aberto com Sucesso! 🎉' : 'Código Binário Incorreto!'}
                </div>
            </div>
        </div>
    `;
    feedbackHTML.push(headerHTML);

    // Informações da multiplicação
    feedbackHTML.push(`
        <div class="section">
            <h3>📝 Detalhes da Multiplicação</h3>
            <table class="result-table">
                <tr>
                    <th>Descrição</th>
                    <th>Binário</th>
                    <th>Decimal</th>
                </tr>
                <tr>
                    <td>Número 1</td>
                    <td class="binary">${data.x ? data.x : '❌ Erro'}</td>
                    <td class="decimal">${data.x_decimal}</td>
                </tr>
                <tr>
                    <td>Número 2</td>
                    <td class="binary">${data.y ? data.y : '❌ Erro'}</td>
                    <td class="decimal">${data.y_decimal}</td>
                </tr>
                <tr style="background: rgba(0, 255, 255, 0.2);">
                    <td><strong>Sua Resposta</strong></td>
                    <td class="binary"><strong>${data.resposta_jogador}</strong></td>
                    <td class="decimal"><strong>${data.resposta_jogador_decimal}</strong></td>
                </tr>
                <tr style="background: rgba(0, 255, 0, 0.2);">
                    <td><strong>Resposta Correta</strong></td>
                    <td class="binary"><strong>${data.resposta_correta}</strong></td>
                    <td class="decimal"><strong>${data.resultado_decimal}</strong></td>
                </tr>
            </table>
        </div>
    `);

    // Pontuação
    feedbackHTML.push(`
        <div class="section" style="margin-top: 20px; text-align: center;">
            <h3>⭐ Pontuação Atual: <span class="correct">${data.pontuacao}</span> pontos</h3>
        </div>
    `);

    // Se errou, mostrar os passos do Karatsuba
    if (!acertou && data.trace && data.trace.length > 0) {
        feedbackHTML.push(renderKaratsubaSteps(data.trace));
    }

    // Botão para próxima fase ou fim de jogo
    if (data.jogo_acabou) {
        feedbackHTML.push(`
            <div style="text-align: center; margin-top: 30px;">
                <h2>🏆 Parabéns! Você Completou o Jogo!</h2>
                <p style="font-size: 1.2rem; margin: 15px 0;">
                    Pontuação Final: <strong class="correct">${data.pontuacao} / 50</strong>
                </p>
                <a href="/" class="btn btn-primary btn-large" style="display: inline-block;">
                    🎮 Jogar Novamente
                </a>
                <a href="/" class="btn btn-secondary" style="display: inline-block; margin-left: 10px;">
                    🏠 Voltar ao Início
                </a>
            </div>
        `);
    } else {
        feedbackHTML.push(`
            <div style="text-align: center; margin-top: 30px;">
                <p style="color: var(--text-secondary); margin-bottom: 20px;">
                    🎯 Próximo desafio aguardando!
                </p>
                <a href="/game" class="btn btn-primary btn-large" style="display: inline-block;">
                    ➡️ Próxima Fase
                </a>
            </div>
        `);
    }

    // Renderizar no DOM
    feedbackCard.innerHTML = feedbackHTML.join('');
    feedbackSection.style.display = 'block';

    // Fazer scroll até feedback
    feedbackSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Renderiza os passos do algoritmo Karatsuba
 */
function renderKaratsubaSteps(trace) {
    if (!trace || trace.length === 0) return '';

    let html = `
        <div class="karatsuba-section">
            <h3 class="karatsuba-title">
                📊 Como o Algoritmo Karatsuba Resolveu
            </h3>
            <p style="margin-bottom: 15px; color: var(--text-secondary);">
                Clique em cada passo para ver os detalhes da divisão recursiva:
            </p>
    `;

    // Agrupar passos por nível
    const stepsByLevel = {};
    trace.forEach(step => {
        const level = step.level;
        if (!stepsByLevel[level]) {
            stepsByLevel[level] = [];
        }
        stepsByLevel[level].push(step);
    });

    // Renderizar cada nível
    Object.keys(stepsByLevel).sort((a, b) => parseInt(a) - parseInt(b)).forEach(level => {
        const levelSteps = stepsByLevel[level];
        
        levelSteps.forEach((step, index) => {
            const stepId = `step-${level}-${index}`;
            const isBaseCase = step.is_base_case;
            const headerClass = isBaseCase ? 'base-case' : '';
            
            let headerText = '';
            if (isBaseCase) {
                headerText = `Nível ${level} (BASE): ${step.x} × ${step.y} = ${step.result}`;
            } else {
                headerText = `Nível ${level}: ${step.x} × ${step.y}`;
            }

            html += `
                <div class="step-container">
                    <div class="step-header ${headerClass}" onclick="toggleStep('${stepId}')">
                        <strong>${headerText}</strong>
                        <span style="float: right;">▼</span>
                    </div>
                    <div class="step-content" id="${stepId}">
            `;

            if (isBaseCase) {
                html += `
                    <div class="step-info">
                        <div class="step-field">
                            <label>Multiplicação Direta:</label>
                            <value>${step.x} × ${step.y} = ${step.result}</value>
                        </div>
                    </div>
                `;
            } else {
                html += `
                    <div class="step-info">
                        <div class="step-field">
                            <label>X = a|b (dividido):</label>
                            <value>${step.a} | ${step.b}</value>
                        </div>
                        <div class="step-field">
                            <label>Y = c|d (dividido):</label>
                            <value>${step.c} | ${step.d}</value>
                        </div>
                        <div class="step-field">
                            <label>Tamanho da metade (m):</label>
                            <value>${step.m}</value>
                        </div>
                    </div>

                    <div style="margin: 15px 0; padding: 15px; background: rgba(187, 134, 252, 0.1); border-radius: 4px;">
                        <strong style="color: var(--accent-purple);">Cálculos Recursivos:</strong>
                        <div class="step-info" style="margin-top: 10px;">
                            <div class="step-field">
                                <label>ac = a × c:</label>
                                <value>${step.ac}</value>
                            </div>
                            <div class="step-field">
                                <label>bd = b × d:</label>
                                <value>${step.bd}</value>
                            </div>
                            <div class="step-field">
                                <label>a + b:</label>
                                <value>${step.soma_ab}</value>
                            </div>
                            <div class="step-field">
                                <label>c + d:</label>
                                <value>${step.soma_cd}</value>
                            </div>
                            <div class="step-field">
                                <label>meio = (a+b) × (c+d):</label>
                                <value>${step.meio}</value>
                            </div>
                            <div class="step-field">
                                <label>meio ajustado = meio - ac - bd:</label>
                                <value>${step.meio_ajustado}</value>
                            </div>
                        </div>
                    </div>

                    <div style="margin: 15px 0; padding: 15px; background: rgba(0, 255, 0, 0.1); border-radius: 4px;">
                        <strong style="color: var(--accent-green);">Combinação (Deslocamentos):</strong>
                        <div class="step-info" style="margin-top: 10px;">
                            <div class="step-field">
                                <label>ac << (2×${step.m}):</label>
                                <value>${step.ac_shifted}</value>
                            </div>
                            <div class="step-field">
                                <label>meio_ajustado << ${step.m}:</label>
                                <value>${step.meio_shifted}</value>
                            </div>
                            <div class="step-field">
                                <label>Resultado Final:</label>
                                <value><strong>${step.resultado}</strong></value>
                            </div>
                        </div>
                    </div>
                `;
            }

            html += `
                    </div>
                </div>
            `;
        });
    });

    html += `
        </div>
    `;

    return html;
}

/**
 * Alterna visibilidade de um passo
 */
function toggleStep(stepId) {
    const stepContent = document.getElementById(stepId);
    if (stepContent) {
        stepContent.classList.toggle('active');
    }
}
