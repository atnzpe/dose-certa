<!--
  Arquivo: ROADMAP.md
  Para que serve: o caminho do Dose Certa até o app Android simples (contar, vender e relatório), em ordem.
  Atualizado em 15/11/2026.
-->

# Roadmap · Dose Certa

## Já feito (no computador)

- [x] Login, cadastro de itens e locais de estoque
- [x] Movimentação (entrada, saída, perda) e contagem de inventário
- [x] Cardápio digital para pedidos pelo WhatsApp e relatórios
- [x] Funciona sem internet (SQLite)

## Agora: preparar o app

1. [x] **LGPD (15/11/2026):** `dose_certa.db` tirado do repositório e de todo o histórico; o app cria o banco vazio no primeiro uso; `.gitignore` para `*.db`
2. [ ] Conferir as issues abertas (#4 locais de estoque, #5 unidades, #6 fichas técnicas, #7 e #8 navegação)

## Versão 1 no celular: contar, vender, relatório

3. [ ] **Tela da balança:** escolher a bebida, digitar o peso e ver as doses que restam (regra e casos de teste no [CLAUDE.md](CLAUDE.md))
4. [ ] Cadastro de cada bebida com peso cheio, peso vazio, ml e ml da dose (e o peso vazio calculado quando faltar: peso cheio − ml)
5. [ ] **Venda rápida:** registrar doses vendidas
6. [ ] **Relatório do dia:** doses vendidas, doses que restam e valor
7. [ ] APK pelo GitHub Actions (`flet build apk`) e teste no celular e na TV

## Depois

8. [ ] Fator de densidade opcional por bebida (destilado pesa cerca de 0,95 g por ml), se o Gleyson decidir
9. [ ] Publicar nas Releases do GitHub; Play Store só se fizer sentido
