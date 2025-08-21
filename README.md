# Dose Certa - Controle de Estoque Inteligente 🎯

### Sobre o Projeto

O **Dose Certa** é um aplicativo de controle de estoque projetado especificamente para bares, restaurantes e estabelecimentos similares. Desenvolvido com **Python** e a framework **Flet**, o objetivo é oferecer uma ferramenta intuitiva, eficiente e acessível para gerenciar inventários, reduzir desperdícios e otimizar o processo de compra.

A aplicação contará com duas versões:

- **Versão Gratuita (Trial):** Funcionalidades essenciais com armazenamento de dados local via banco de dados **SQLite**.
- **Versão Paga (Premium):** Todos os recursos, com armazenamento em nuvem via **Firebase**, permitindo a recuperação de dados e o uso em múltiplos dispositivos através do login com a conta Google.

### ✨ Funcionalidades Planejadas

- **Login Seguro:** Autenticação de usuários com opção de login via conta Google na versão Premium.
- **Dashboard Intuitivo:** Visualização rápida das informações mais importantes do estoque.
- **Cadastro Simplificado:**
  - Cadastro de itens (bebidas, insumos).
  - Cadastro de locais de contagem (Ex: Estoque Principal, Bar da Frente).
  - Cadastro de unidades de medida.
- **Contagem de Estoque:** Ferramenta otimizada para realizar contagens de forma rápida e precisa.
- **Lançamento de Compras:** Módulo para registrar a entrada de novos itens no estoque.
- **Relatórios Detalhados:** Geração de relatórios de contagens, movimentação de itens e auditoria.
- **Personalização:** Temas claro e escuro para melhor experiência do usuário (UX).

### 🛠️ Tecnologias Utilizadas

| Tecnologia    | Propósito                                                                      |
| :------------ | :----------------------------------------------------------------------------- |
| **Python** | Linguagem principal de desenvolvimento do backend e lógica da aplicação.        |
| **Flet** | Framework para a construção da interface gráfica (UI) para desktop, web e mobile. |
| **SQLite** | Banco de dados local para a versão gratuita (trial).                           |
| **Firebase** | Banco de dados em nuvem e sistema de autenticação para a versão paga.            |
| **Git & GitHub** | Sistema de controle de versão e hospedagem do código-fonte.                   |
| **Fly.io** | Plataforma de deploy para a versão web da aplicação.                           |

### 🚀 Roadmap de Desenvolvimento

O projeto seguirá um roadmap dividido em fases, utilizando a metodologia SCRUM para garantir entregas incrementais e de valor. Veja o roadmap detalhado [aqui](#).

### 📦 Instalação e Execução

*(Esta seção será atualizada conforme o desenvolvimento avança)*

# 1. Clone o repositório

```
git clone https://github.com/atnzpe/dose-certa
```

# 2. Navegue até o diretório do projeto

```
cd dose-certa
```

# 3. Crie e ative um ambiente virtual

```
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

# 4. Instale as dependências

```
pip install -r requirements.txt
```

# 5. Execute a aplicação

```
flet run main.py
```

### 🤝 ContribuiçãoContribuições são bem-vindas

Para sugestões, correções de bugs ou novas funcionalidades, por favor, abra uma Issue neste repositório.

(Esta seção será detalhada com um guia de contribuição)

### 📄 Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
