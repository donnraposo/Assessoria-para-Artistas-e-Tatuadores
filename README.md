# Plataforma de Assessoria para Tatuadores

Sistema operacional para selecionar artistas, planejar operações de Guest, organizar Studios, agenda, marketing, finanças e logística.

## Documentação

Toda a documentação oficial está em [`docs/`](docs/), exclusivamente em Markdown.

O planejamento técnico para construção do MVP está em [`docs/09-planejamento/`](docs/09-planejamento/).

## Estrutura

- `docs/`: visão, negócio, requisitos, módulos, fluxos, arquitetura, API, UX/UI e roadmap.
- `backend/`: API Django organizada por módulos e camadas.
- `frontend/`: aplicação Next.js e sistema visual baseado em tokens.
- `infrastructure/`: imagens e configuração dos containers.
- `tests/`: testes transversais futuros.

## Estado

Sprints 01 a 08 concluídas no backend. A Sprint 09 já entrega autenticação web,
dashboards isolados por perfil, filas administrativas, notificações persistentes,
imagens de produção e runbooks. As telas transacionais completas e a homologação
visual/manual permanecem como gate antes de declarar o MVP pronto para lançamento.

Decisões e execução estão documentadas em `docs/01-negocio/regras-de-negocio.md`,
`docs/09-planejamento/` e `docs/10-operacao/`.
