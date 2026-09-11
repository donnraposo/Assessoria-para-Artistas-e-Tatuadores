# Arquitetura do Sistema

## Visão geral

A solução será uma aplicação web com frontend Next.js e API Django REST Framework. O backend será um monólito modular organizado por domínio. PostgreSQL será a fonte oficial dos dados e um armazenamento compatível com S3 guardará mídia e documentos.

```text
Artista ─┐
Studio ──┼── Next.js ── API REST ── Django modular ── PostgreSQL
Assessoria┘                 │              │
                            │              ├── Armazenamento S3
                            │              ├── E-mail
                            │              └── Celery/Redis (quando necessário)
                            └── OpenAPI
```

## Componentes e comunicação

- O navegador acessa o frontend por HTTPS.
- O frontend consome a API REST versionada.
- A API autentica, autoriza, valida o contrato e executa casos de uso.
- Casos de uso coordenam domínio, persistência e integrações.
- Eventos assíncronos não decidem confirmações financeiras ou de agenda.
- OpenAPI documenta o contrato e poderá gerar o cliente TypeScript.

## Módulos principais

- Identidade e acesso.
- Artistas e candidaturas.
- Studios, bancadas e reservas.
- Propostas e Guests.
- Disponibilidade, agenda e agendamentos.
- Leads, fechamentos e cancelamentos.
- Marketing e Ads.
- Financeiro.
- Logística e `Minha Viagem`.
- Auditoria e notificações.

## Camadas internas

```text
Presentation -> Application -> Domain
                       |
                       v
                Infrastructure
```

- `domain`: entidades, objetos de valor, regras e contratos independentes de HTTP.
- `application`: casos de uso, comandos, consultas e DTOs.
- `infrastructure`: ORM Django, repositórios e integrações.
- `presentation`: views, serializers, permissões e rotas da API.

Dependências apontam para o domínio. Cada classe própria do projeto terá arquivo exclusivo.

## Autenticação e autorização

- Django será a autoridade de identidade.
- Preferência por sessão ou token de curta duração protegido por cookie `HttpOnly`.
- Autorização combinará papel, propriedade e escopo operacional.
- Cliente final não terá autenticação.
- Alterações administrativas relevantes gerarão auditoria.

## Dados e armazenamento

- PostgreSQL para dados transacionais.
- UUID como identificador público.
- Valores usando decimal e código de moeda.
- Datas armazenadas em UTC com fuso operacional preservado quando necessário.
- Arquivos privados em S3/R2; MinIO poderá simular o serviço localmente.

## Infraestrutura

- Docker para frontend, backend e workers.
- Docker Compose no desenvolvimento.
- Banco gerenciado em produção.
- Configuração por ambiente e segredos externos às imagens.
- TLS, health checks, logs estruturados, backups e monitoramento.

## Fluxo crítico de fechamento

```text
Lead -> negociação externa -> recebimento dos 20%
     -> caso de uso transacional -> fechamento
     -> agendamento confirmado -> métricas recalculadas
```

O registro do recebimento, o fechamento e a confirmação do agendamento deverão permanecer consistentes dentro de uma transação.

