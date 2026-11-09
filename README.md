# NEI Events API

API de inscrições em eventos do NEI, em Python com FastAPI e SQLite. Gere eventos, participantes e as inscrições de cada participante num evento, com regras de lotação e de duplicados. A criação de eventos exige um token de administrador no header `X-Admin-Token`.

Os exercícios do workshop que usa esta aplicação estão em https://github.com/sebastiaoteixeira/workshop-claude.

## Pré-requisitos

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/)
- `make`

## Começar

```bash
uv sync
make test
make run
```

`make run` arranca o servidor em http://127.0.0.1:8000, com a documentação interativa em `/docs`.

## Comandos

| Comando | O que faz |
|---|---|
| `uv sync` | Cria o `.venv` e instala as dependências |
| `make test` | Corre a suite pytest |
| `make lint` | `ruff check` e `ruff format --check` |
| `make run` | Servidor de desenvolvimento com reload |
| `make seed` | Recria `data/workshop.db` com um conjunto de dados fixo e reprodutível |

`make run` e `make seed` leem o `.env` se existir (ver `.env.example`). Variáveis reconhecidas: `ADMIN_TOKEN` (por omissão `dev-token`) e `DATABASE_PATH` (por omissão `data/workshop.db`).

## Estrutura

```
app/                 API FastAPI
  main.py            Criação da app e registo dos routers
  routes/            Handlers HTTP, sem SQL
  repositories/      Todo o SQL
  schemas.py         Modelos Pydantic de entrada e saída
migrations/          Esquema SQLite, aplicado por ordem no arranque
data/workshop.db     Base de dados de exemplo
scripts/seed.py      Gera data/workshop.db (make seed)
tests/               Suite pytest
```

## Autores

Sebastião Teixeira e Vicente Barros.

## Licença

MIT, ver [LICENSE](LICENSE).
