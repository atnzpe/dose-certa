<!--
  Arquivo: CLAUDE.md
  Para que serve: as regras que o Claude Code segue ao trabalhar neste repositório (Dose Certa).
  É lido em toda conversa: fica curto e muda quando uma decisão mudar.
-->

# CLAUDE.md · Dose Certa

- **O que é:** controle de estoque de bebidas para bares e adegas, em Python + Flet, que **funciona sem internet** (SQLite):
  itens, locais de estoque, movimentação, contagem, cardápio para WhatsApp e relatórios.
- **Rumo (15/11/2026):** virar **app Android simples** (celular e TV) para **contar pela balança, vender e ver um relatório do dia**.
  A mesma regra de contagem vai virar o módulo Contagem do Sofi OS (outro produto). O APK sai depois do Quiz SFPC.
- **Pessoas:** Gleyson Atanazio (desenvolvedor e Scrum Master) e a PO e QA do time, que testa cada APK antes de publicar.
- **Autonomia:** o Claude cria branch, commit, push e PR sem pedir. O merge, a publicação e a limpeza do histórico do Git são do Gleyson.
- **Idioma:** tudo em português do Brasil, em linguagem simples, com todo termo técnico explicado.

## A regra de contagem (fonte única; o Sofi OS segue a mesma)

- **Doses que restam na garrafa** = (peso na balança − peso da garrafa vazia) ÷ ml da dose. Considera 1 g = 1 ml, como a planilha original.
- **Doses de uma garrafa cheia** = ml da garrafa ÷ ml da dose.
- **Erro** quando o peso na balança é menor ou igual ao peso vazio (garrafa errada ou balança errada).
- **Casos de teste:** Gin 750 ml, vazia 535 g, dose 50 ml, balança 1.258 g → **14,46 doses**; balança igual ao peso vazio → **erro**; Gin 750 ml, vazia 425 g, balança 1.135 g → **14,2 doses**.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| Código | `app/` e `main.py` |
| Documentação antiga | `Documentation/` e `ROADMAP.pdf` |
| O que falta fazer | [ROADMAP.md](ROADMAP.md) |
| O que aprendi | [APRENDIZADO.md](APRENDIZADO.md) |

## Regras que não mudam

- **LGPD:** banco com dados de usuário **nunca** no Git (o `.gitignore` barra `*.db`). Em 15/11/2026 o `dose_certa.db` saiu do repositório e de todo o histórico.
  O app cria o banco vazio no primeiro uso (`initialize_database`).
- **Nenhuma senha, chave ou token** (Firebase incluído) no repositório nem dentro do APK. Senha sempre com hash (bcrypt).
- **Código comentado para qualquer pessoa entender** (regra inegociável do Gleyson): vale para todo arquivo criado ou alterado.
