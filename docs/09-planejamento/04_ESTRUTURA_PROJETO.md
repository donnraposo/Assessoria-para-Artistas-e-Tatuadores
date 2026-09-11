# Estrutura do Projeto

## Estrutura geral

```text
projeto/
├── backend/
│   ├── config/
│   ├── shared/
│   ├── modules/
│   ├── tests/
│   └── manage.py
├── frontend/
│   ├── src/
│   └── tests/
├── infrastructure/
│   ├── docker/
│   └── environments/
├── docs/
├── scripts/
├── compose.yaml
└── README.md
```

## Responsabilidades

- `backend/config`: configuração, inicialização e rotas globais do Django.
- `backend/shared`: primitivas técnicas realmente compartilhadas, sem regras específicas de módulos.
- `backend/modules`: módulos de negócio independentes dentro do monólito.
- `backend/tests`: testes transversais e de arquitetura.
- `frontend/src`: interface web, contratos, componentes e áreas por perfil.
- `infrastructure/docker`: imagens, pontos de entrada e configurações de containers.
- `infrastructure/environments`: exemplos e documentação de variáveis por ambiente, sem segredos.
- `docs`: documentação oficial e decisões arquiteturais.
- `scripts`: automações explícitas de desenvolvimento e operação.

## Estrutura padrão de um módulo Django

```text
modules/guests/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── enums/
│   ├── services/
│   └── repositories/
├── application/
│   ├── use_cases/
│   ├── commands/
│   ├── queries/
│   └── dto/
├── infrastructure/
│   ├── persistence/
│   ├── repositories/
│   └── integrations/
├── presentation/
│   └── api/
│       ├── serializers/
│       ├── views/
│       ├── permissions/
│       └── urls.py
└── apps.py
```

## Convenções obrigatórias

- Uma classe própria do projeto por arquivo.
- Nome do arquivo correspondente à responsabilidade da classe.
- Sem regras de negócio em views, serializers, signals ou tarefas assíncronas.
- Sem importação direta da camada de apresentação por camadas internas.
- Casos de uso delimitam transações e orquestram dependências.
- Migrations são artefatos gerados pelo Django e seguem a convenção do framework.
- Testes espelham a estrutura dos módulos e mantêm uma classe por arquivo quando utilizarem classes.
- `__init__.py` não deve esconder dependências por meio de reexportações extensas.

## Frontend

O frontend será organizado por funcionalidades e não por uma coleção global de tipos técnicos:

```text
frontend/src/
├── app/
├── features/
│   ├── auth/
│   ├── artists/
│   ├── studios/
│   ├── guests/
│   ├── scheduling/
│   ├── finance/
│   └── logistics/
├── shared/
└── generated/
```

`generated` conterá contratos derivados do OpenAPI e não receberá edição manual.

