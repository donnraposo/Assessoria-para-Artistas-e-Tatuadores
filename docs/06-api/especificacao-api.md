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
- `POST /api/v1/auth/register/`: auto-cadastro de Artista ou Studio, com login automático.
- `POST /api/v1/auth/login/` e `POST /api/v1/auth/logout/`.
- `GET /api/v1/auth/me/`: usuário e papéis correntes.
- `GET /api/v1/operations/dashboard/`: visão global exclusiva da Assessoria.
- `GET /api/v1/operations/queues/{queue_name}/`: fila administrativa paginada.
- `GET /api/v1/operations/workspace/`: visão isolada de Artist ou Studio.
- `GET /api/v1/notifications/` e `POST /api/v1/notifications/{id}/read/`.

## 5. Endpoints operacionais implementados

- `POST /api/v1/artists/{artist_id}/availability/override/`: intervenção excepcional da Assessoria na disponibilidade do Artista, com motivo obrigatório e auditoria.
- `POST /api/v1/guests/proposals/{proposal_id}/transition/`: recusa ou cancelamento de Proposta com motivo obrigatório.
- `GET|POST /api/v1/guests/{guest_id}/studios/`: Studios adicionais do Guest, com bloqueio de sobreposição de horário.
- `POST /api/v1/studios/booking-requests/{request_id}/external-response/`: registro pela Assessoria de negociação de reserva fechada por canal externo.
- `PATCH /api/v1/studios/bookings/{booking_id}/payment/`: atualização do status de pagamento do Studio (`Pendente`/`Pago`).
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
