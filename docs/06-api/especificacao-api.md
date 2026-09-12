# Especificação da API

## 1. Objetivo

Registrar o contrato HTTP versionado implementado pelo MVP.

## 2. Recursos

- Autenticação e usuários.
- Artistas e candidaturas.
- Studios, disponibilidades e reservas.
- Propostas de Guest e Guests.
- Agenda, fechamentos e cancelamentos.
- Marketing, Ads e métricas.
- Financeiro, viagem e acomodação.

## 3. Convenções

- Prefixo `/api/v1/`.
- Autenticação por sessão e proteção CSRF para operações mutáveis.
- Respostas e mensagens visíveis em inglês.
- Filas operacionais paginadas por `page` e `page_size`.
- Fechamentos e notificações protegidos por chave de idempotência.
- Decisões críticas registradas em auditoria append-only.

## 4. Saúde, identidade e operação

- `GET /api/v1/health/`: vida do processo.
- `GET /api/v1/ready/`: prontidão do processo e banco.
- `GET /api/v1/auth/csrf/`: token CSRF.
- `POST /api/v1/auth/login/` e `POST /api/v1/auth/logout/`.
- `GET /api/v1/auth/me/`: usuário e papéis correntes.
- `GET /api/v1/operations/dashboard/`: visão global exclusiva da Assessoria.
- `GET /api/v1/operations/queues/{queue_name}/`: fila administrativa paginada.
- `GET /api/v1/operations/workspace/`: visão isolada de Artist ou Studio.
- `GET /api/v1/notifications/` e `POST /api/v1/notifications/{id}/read/`.

## 5. Artistas e candidaturas

- `GET|PUT /api/v1/artists/me/`: perfil do próprio Artista. O `PUT` cria o perfil e abre a
  candidatura em `DRAFT`; enquanto o perfil não existir, o `GET` responde HTTP 404.
- `GET|POST /api/v1/artists/me/application/`: consulta e envio da própria candidatura.
  O envio exige rascunho e ao menos um estilo declarado, respondendo HTTP 409 caso contrário.
- `GET|POST /api/v1/artists/me/portfolio/`: metadados do portfólio do próprio Artista.
- `GET|POST /api/v1/artists/me/availability/`: disponibilidade sem sobreposição.
- `GET /api/v1/artists/applications/{application_id}/`: detalhe da candidatura para a
  Assessoria, com perfil, contato e portfólio ordenado. Exclusivo do papel Advisory.
- `POST /api/v1/artists/applications/{application_id}/review/`: aprovação ou reprovação
  auditada. A reprovação exige motivo e responde HTTP 409 quando ele está ausente.

A fila `artist-applications` devolve, além dos identificadores, `professional_name`,
`years_experience` e `styles`, permitindo triagem sem abrir cada candidatura.

## 6. Endpoints operacionais implementados

- `GET|POST /api/v1/schedule/appointments/`: agenda autorizada e criação administrativa.
- `GET /api/v1/schedule/guests/{guest_id}/occupancy/`: ocupação por horas e dias.
- `POST /api/v1/schedule/appointments/{appointment_id}/cancellation-requests/`: solicitação do Artista.
- `POST /api/v1/schedule/cancellation-requests/{cancellation_id}/decide/`: decisão da Assessoria.
- `GET|POST /api/v1/sales/leads/`: registro e consulta administrativa de Leads.
- `POST /api/v1/sales/leads/{lead_id}/close/`: recebimento e fechamento transacional 20/80.
- `GET|POST /api/v1/marketing/campaigns/`: campanhas e orçamento autorizado.
- `POST /api/v1/marketing/campaigns/{campaign_id}/spend/`: gasto efetivo de Ads.
- `GET /api/v1/marketing/guests/{guest_id}/metrics/`: indicadores derivados do Guest.
- `GET|POST /api/v1/logistics/guests/{guest_id}/travel-segments/`: trechos da viagem.
- `PATCH /api/v1/logistics/travel-segments/{segment_id}/`: atualização administrativa do trecho.
- `GET|POST /api/v1/logistics/guests/{guest_id}/accommodations/`: acomodações do Guest.
- `PATCH /api/v1/logistics/accommodations/{accommodation_id}/`: atualização administrativa da acomodação.
- `GET /api/v1/logistics/guests/{guest_id}/my-trip/`: visão consolidada autorizada.
