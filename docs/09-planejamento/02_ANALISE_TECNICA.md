# Análise Técnica

## Tecnologias escolhidas

| Área | Escolha | Motivo |
|---|---|---|
| Backend | Python, Django e Django REST Framework | Produtividade, ORM relacional, segurança e administração |
| Frontend | Next.js e TypeScript | Aplicação responsiva, tipagem e boa experiência para três perfis |
| Banco | PostgreSQL | Transações, integridade, relacionamentos e controle de concorrência |
| Contrato | REST e OpenAPI | Simplicidade, versionamento e geração de cliente TypeScript |
| Arquivos | API compatível com S3 | Armazenamento privado e escalável fora do banco |
| Assíncrono | Celery e Redis, quando necessário | E-mails, notificações e tarefas demoradas |
| Containers | Docker e Docker Compose | Reprodutibilidade entre ambientes |
| Testes | Pytest e Playwright | Cobertura do domínio, API e jornadas críticas |

## Alternativas consideradas

### Backend

- Laravel: alta produtividade, mas não foi a stack escolhida.
- NestJS: compartilharia TypeScript com o frontend, porém Django oferece ORM, autenticação e administração mais convenientes para este MVP.
- FastAPI: API enxuta e rápida, mas exigiria compor mais recursos administrativos e de domínio.

### Arquitetura

- Microsserviços: rejeitados no MVP pelo custo operacional e pela necessidade prematura de comunicação distribuída.
- Backend embutido no Next.js: rejeitado pela complexidade transacional e modular do domínio.
- Monólito modular: escolhido por combinar velocidade, consistência e separação evolutiva.

### Autenticação

- Sessão Django com cookie seguro: preferência quando frontend e API puderem compartilhar o mesmo site.
- Access token curto e refresh token em cookie seguro: alternativa para origens separadas.
- Tokens persistidos em `localStorage`: rejeitados por ampliar exposição a XSS.

## Dependências previstas

- Banco PostgreSQL.
- Serviço de e-mail transacional.
- Armazenamento compatível com S3.
- Redis apenas quando filas ou cache forem introduzidos.
- Plataforma capaz de executar containers e banco gerenciado em produção.

As bibliotecas e versões exatas serão fixadas somente na etapa de configuração, após validação de compatibilidade e suporte.

## Custos

Os custos recorrentes serão concentrados em aplicação, banco gerenciado, armazenamento, e-mail e observabilidade. No início, uma única implantação web e um banco pequeno são suficientes; workers e Redis devem ser adicionados por demanda comprovada.

## Escalabilidade

- Escala horizontal dos containers stateless.
- PostgreSQL como fonte oficial, com índices orientados às consultas reais.
- Arquivos fora do banco.
- Filas para tarefas demoradas.
- Extração futura de módulos somente diante de limites mensuráveis.

## Riscos técnicos

- Corridas em reservas e agendamentos: mitigar com transações e restrições no banco.
- Vazamento entre perfis: autorização por papel, propriedade e testes negativos.
- Estados inconsistentes: transições explícitas por casos de uso.
- Erros monetários: `Decimal`, moeda obrigatória e snapshots históricos.
- Complexidade acidental da Clean Architecture: criar abstrações somente em fronteiras úteis.
- Fragmentação por uma classe por arquivo: manter convenção de nomes e navegação consistente.
- Operação do banco em container local: usar PostgreSQL gerenciado em produção.

