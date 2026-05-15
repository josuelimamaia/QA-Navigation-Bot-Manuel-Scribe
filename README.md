# QA Navigation Bot - Manuel Scribe 🤖

Este é um projeto de **Automação de Testes (Quality Assurance)** desenvolvido em Python utilizando a biblioteca **Selenium**. O objetivo principal do robô é navegar de forma autônoma pelo site [Manuel Scribe](https://www.manuel-scribe.com.br), simulando o comportamento de um usuário real para identificar possíveis erros na interface ou no sistema (como links quebrados ou erros de servidor).

## 🚀 O que ele faz?

*   **Login Automático:** Acessa a página do sistema e realiza o login automaticamente utilizando credenciais pré-configuradas.
*   **Mapeamento e Interação:** Procura por elementos interativos na tela (botões, links) e clica neles de forma sequencial (limitado a 30 cliques por ciclo).
*   **Segurança (Filtro de Ações):** Possui um mecanismo inteligente que ignora botões com palavras de risco (como "sair", "deletar", "apagar"), evitando que o robô faça logout acidental ou exclua dados reais durante o teste.
*   **Monitoramento de Erros:** Captura erros invisíveis ao usuário comum:
    *   Erros no Console (JavaScript).
    *   Erros de Requisição de Rede (HTTP 404, 500, 422).
*   **Geração de Relatórios:** Tira *screenshots* (capturas de tela) a cada ação ou erro encontrado e gera arquivos de log em texto com o histórico completo de tudo que aconteceu durante a execução.

---

## 🛠️ Como rodar o projeto

### 1. Pré-requisitos

Para rodar este bot na sua máquina, você vai precisar de:
*   **[Python](https://www.python.org/downloads/)** instalado na sua máquina (verifique digitando `python --version` no terminal).
*   **Navegador Google Chrome** instalado.

### 2. Instalação

Abra o seu terminal (Prompt de Comando ou PowerShell), navegue até a pasta deste projeto e instale a dependência do Selenium executando o comando:

```bash
pip install selenium
```

### 3. Configuração de Credenciais

Antes de executar, você precisa informar os dados de acesso para que o robô possa fazer o login no sistema.
Abra o arquivo **`bot.py`** e, logo nas primeiras linhas de configuração (embaixo de `CONFIGURAÇÕES GERAIS`), altere as variáveis com os dados válidos:

```python
# ==========================================
# CONFIGURAÇÕES GERAIS
# ==========================================
EMAIL = "seu_email_real@exemplo.com"
SENHA = "sua_senha_real"
```
*(Dica: É altamente recomendável usar uma conta de "teste" do sistema para não impactar ou misturar com os dados do seu usuário pessoal).*

### 4. Executando o Bot

Com a biblioteca instalada e as credenciais configuradas, basta executar o script com o seguinte comando no terminal (ainda dentro da pasta do projeto):

```bash
python bot.py
```

Uma janela automatizada do Google Chrome irá abrir sozinha e o robô começará a agir. Você poderá acompanhar o passo a passo e o status do teste pelo que estiver sendo impresso no próprio terminal.

---

## 📂 Estrutura de Pastas e Arquivos

Ao rodar o bot pela primeira vez, se elas ainda não existirem, ele criará as seguintes pastas no diretório:

*   📁 `logs/`: Armazena arquivos `.txt` com todo o relatório de passos executados, cliques realizados e alertas/erros detectados. Organizados por data e hora.
*   📁 `screenshots/`: Armazena imagens (`.png`) da tela salvas logo após cada interação ou em momentos em que um erro crítico for capturado.
