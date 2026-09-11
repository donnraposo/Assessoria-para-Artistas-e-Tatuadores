# Especificação da API

## 1. Objetivo

Documentar a API após definição da arquitetura e do modelo de dados.

## 2. Recursos candidatos

- Autenticação e usuários.
- Artistas e candidaturas.
- Studios, disponibilidades e reservas.
- Propostas de Guest e Guests.
- Agenda, fechamentos e cancelamentos.
- Marketing, Ads e métricas.
- Financeiro, viagem e acomodação.

## 3. Convenções a definir

- Versionamento, autenticação, paginação, erros, idempotência e auditoria.

## 4. Pontos em aberto

- Estilo da API, contratos e política de compatibilidade.

## 5. Endpoints implementados na Sprint 06

- `GET|POST /api/v1/schedule/appointments/`: agenda autorizada e criação administrativa.
- `GET /api/v1/schedule/guests/{guest_id}/occupancy/`: ocupação por horas e dias.
- `POST /api/v1/schedule/appointments/{appointment_id}/cancellation-requests/`: solicitação do Artista.
- `POST /api/v1/schedule/cancellation-requests/{cancellation_id}/decide/`: decisão da Assessoria.
- `GET|POST /api/v1/sales/leads/`: registro e consulta administrativa de Leads.
- `POST /api/v1/sales/leads/{lead_id}/close/`: recebimento e fechamento transacional 20/80.
