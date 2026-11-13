---
name: changelog
description: Notas de release, changelog, "o que mudou desde" a última versão. Gera a próxima secção do CHANGELOG.md a partir do git log, no formato da equipa, quando alguém pede notas de release ou pergunta o que mudou desde uma tag ou versão.
argument-hint: [tag ou intervalo de commits]
---

Gera a secção da próxima versão no `CHANGELOG.md` a partir dos commits ainda não documentados.

## Procedimento

1. Intervalo. Se `$ARGUMENTS` tiver valor, usa-o tal como está (`v0.3.0` significa `v0.3.0..HEAD`; um intervalo `a..b` é usado literalmente). Senão, começa na última tag de versão (`git describe --tags --match 'v*' --abbrev=0`); se não existir, no último commit que tocou no `CHANGELOG.md` (`git log -1 --format=%h -- CHANGELOG.md`).
2. Commits: `git log --format='%h %s' <intervalo>..HEAD`.
3. Classifica cada commit pelo prefixo: `feat` em `### Adicionado`, `fix` em `### Corrigido`, `refactor` e `chore` em `### Alterado`. `docs` e `test` ficam de fora. Commits sem prefixo convencional são classificados pelo que descrevem.
4. Versão: lê a última secção do `CHANGELOG.md` e sobe o minor (`0.3.0` passa a `0.4.0`); sobe o patch se só houver `### Corrigido`. A data é a de hoje.
5. Escreve a secção nova logo abaixo do parágrafo introdutório do `CHANGELOG.md`, antes da secção mais recente. Não faz commit.

## Formato

Cada bullet é uma frase curta em português, substantivada, que diz o que mudou para quem usa a API, e termina com o hash curto entre parênteses. Secções sem bullets não aparecem.

```markdown
## [0.4.0] - 2026-11-13

### Adicionado

- Lista de espera por evento, com promoção do primeiro da fila (1a20555)

### Corrigido

- Deslocamento da paginação calculado a partir da página 1 (f5dcd69)

### Alterado

- Hooks de lint e de proteção de ficheiros nas edições do Claude Code (58ce512)
```
