# STI Web Scrapper

[English version](./README.en.md)

> Projeto desenvolvido durante a faculdade, mas trata-se de uma solução real, usada em produção pela empresa em que o autor trabalhava na época. A automação foi criada para atender a um cenário operacional concreto de monitoramento de frota.

Aplicação em Python para automatizar a coleta de dados de rastreio da STI, complementar com uma planilha de frota e enviar os registros para o AppSheet.

## Visão geral

Este projeto foi desenvolvido para monitorar e atualizar em tempo real informações de veículos, incluindo:

- Veículo
- Motorista
- Carreta 1 e Carreta 2
- Status
- Velocidade
- Localização
- UF

A aplicação realiza os seguintes passos:

1. Acessa os portais da STI via Selenium
2. Coleta as informações em HTML/JavaScript
3. Lê a planilha Excel de planejamento da frota
4. Combina os dados por veículo
5. Envia os dados para tabelas do AppSheet
6. Exibe o status em uma interface gráfica desktop

## Tecnologias

- Python 3
- Selenium
- Pandas
- Tkinter + ttkbootstrap
- AppSheet API

## Requisitos

- Python 3.10 ou superior
- Google Chrome ou Chromium instalado
- Dependências do projeto instaladas

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/hugoMiquilino/sti-web-scrapper.git
cd sti-web-scrapper
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

```env
USER=seu_usuario_sti
PASSWD=sua_senha_sti
APPSHEET_APP_ID=seu_appsheet_app_id
APPSHEET_ACCESS_KEY=sua_appsheet_access_key
APPSHEET_TABLE_NAME_FROTA=nome_tabela_frota
APPSHEET_TABLE_NAME_VEICULOS=nome_tabela_veiculos
```

Essas variáveis são consumidas em:

- `src/modules/sti_module.py` para autenticação no portal STI
- `src/modules/request_module.py` para autenticação e envio ao AppSheet

## Execução

Para iniciar a aplicação:

```bash
python main.py
```

Ao executar, a aplicação:

- inicia o ciclo de coleta em segundo plano
- registra logs
- abre a interface gráfica de status
- mantem o processo em execução em loop com intervalo de atualização

## Estrutura do projeto

```text
sti-web-scrapper/
├─ gui/
│  ├─ assets/
│  ├─ base.py
│  └─ log_handler.py
├─ src/
│  ├─ docs/
│  │  └─ conversion_dict.json
│  ├─ logs/
│  │  └─ logger.py
│  ├─ modules/
│  │  ├─ __init__.py
│  │  ├─ sti_module.py
│  │  ├─ plan_module.py
│  │  └─ request_module.py
│  └─ utils/
│     └─ path.py
├─ main.py
├─ requirements.txt
├─ .gitignore
└─ README.md
```

## Fluxo da aplicação

- `main.py` inicia a aplicação e o worker em segundo plano
- `sti_module.py` acessa o portal da STI e transforma os dados em um DataFrame
- `plan_module.py` lê a planilha Excel com os dados de frota
- `request_module.py` monta o payload e envia as informações para o AppSheet
- o sistema salva também um arquivo `r.csv` com o resultado do merge para análise

## Observações importantes

- A coleta da STI depende da disponibilidade e da estrutura do portal externo.
- O projeto usa o Selenium em modo headless.
- O caminho da planilha do Excel está definido em `src/modules/plan_module.py` e pode precisar de ajuste conforme o ambiente local.
- O projeto está focado em um ambiente Windows, especialmente por causa do uso de caminhos locais e da interface desktop.

## Licença

Este projeto não possui licença definida no repositório.
