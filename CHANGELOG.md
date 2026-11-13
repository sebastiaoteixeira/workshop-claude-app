# Changelog

Todas as alterações relevantes da API de eventos ficam registadas aqui, uma secção por versão, da mais recente para a mais antiga.

## [0.4.0] - 2026-11-13

### Adicionado

- Guia do projeto em `CLAUDE.md`, cancelamento de inscrições e lugares disponíveis no detalhe do evento (feaf8b3)
- Lista de espera por evento, com promoção do primeiro da fila (1a20555)
- Subagent de revisão de código só de leitura (c9c967f)

### Corrigido

- Deslocamento da paginação calculado a partir da página 1 (f5dcd69)

### Alterado

- Hooks de lint e de proteção de ficheiros nas edições do Claude Code (58ce512)

## [0.3.0] - 2026-10-15

### Adicionado

- Validação de capacidade positiva na criação de eventos (81b16d5)
- Limite de 100 para `page_size` (3847491)

### Corrigido

- Eventos ordenados pela data de início (12bbfec)

### Alterado

- Erros de domínio tratados por um único handler (047a134)
- Dependência de ligação partilhada pelos routers (4cabc19)
- Páginas construídas no repositório de eventos (8f8dd0b)

## [0.2.0] - 2026-09-25

### Adicionado

- Paginação em `GET /events` com `page` e `page_size` (b38ad69)

### Corrigido

- Chaves estrangeiras ativas em todas as ligações (bafd796)

## [0.1.0] - 2026-09-18

### Adicionado

- Listagem e criação de eventos (89640dc)
- Criação de eventos protegida por token de administrador (08b90df)
- Detalhe de um evento por id (d9dbd94)
- Inscrição de participantes com regras de lotação e de duplicados (3240699)
- Listagem das inscrições de um evento (4194ada)
- Base de dados de exemplo e script de seed (ae27a03)
