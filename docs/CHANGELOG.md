# Histórico de Alterações

## 2026-09-12 — Tela de registro

- Adicionadas a tela `/register` e a função `register()` em `lib/api.ts`,
  cobrindo o auto-cadastro de Artista ou Studio (`POST /api/v1/auth/register/`)
  que já existia apenas na API.
- Adicionado seletor de papel (Artist/Studio) reutilizando os ícones já
  existentes, seguindo a composição de `.login-shell`/`.login-card` da tela
  de login.
- Adicionado link "Create an account" na tela de login e "Sign in" na tela
  de registro, com nova classe `.login-switch` em `styles.css` (seção 18,
  apenas tokens existentes).
- Validado com `npm run lint`, `npm run typecheck`, `npm test` e teste real
  de ponta a ponta (Playwright) do fluxo de cadastro de Studio até o
  workspace autenticado; suíte backend (81 testes) revalidada sem regressão.

## 2026-09-12 — Regras de negócio pendentes e correções de API

- Adicionado auto-cadastro de Artista e Studio (`POST /api/v1/auth/register/`),
  com atribuição de papel, validação de senha e login automático (RN-004, RN-026).
- Adicionada intervenção excepcional da Assessoria na disponibilidade do Artista
  (`POST /api/v1/artists/{artist_id}/availability/override/`), com motivo
  obrigatório e auditoria (RN-008).
- Adicionadas edição e remoção de disponibilidade pelo próprio Artista
  (`PATCH|DELETE /api/v1/artists/me/availability/{id}/`), bloqueadas para janelas
  geridas pela Assessoria e protegidas contra remoção/redução com agendamento
  confirmado no intervalo (RN-007).
- Adicionadas recusa e cancelamento de Proposta de Guest com motivo obrigatório
  (`POST /api/v1/guests/proposals/{id}/transition/`) (RN-010).
- Adicionados Studios adicionais por Guest com bloqueio de sobreposição de
  horário (`GET|POST /api/v1/guests/{id}/studios/`) (RN-015).
- Adicionado registro pela Assessoria de negociação de reserva de Studio fechada
  por canal externo (`POST /api/v1/studios/booking-requests/{id}/external-response/`)
  (RN-032).
- Adicionada atualização do status de pagamento do Studio, `Pendente` ou `Pago`
  (`PATCH /api/v1/studios/bookings/{id}/payment/`) (RN-033).
- Adicionada API de bancadas, preços e disponibilidade do Studio
  (`GET|POST /api/v1/studios/me/{workstations,prices,availability}/`), antes
  existentes apenas como modelos sem exposição via API (RN-029).
- Adicionada API de Finance: resumo de saldo por Guest e confirmação de
  recebimento externo do Artista ou de devolução, encerrando o estado "previsto"
  quando confirmado (`GET /api/v1/finance/guests/{id}/summary/`,
  `POST /api/v1/finance/entries/{id}/confirm/`) (RN-025, RN-040).
- Corrigida a confirmação de reserva de Studio, que tratava o Studio inteiro
  como uma única bancada e não protegia contra confirmações concorrentes da
  mesma janela; agora considera a bancada informada (ou a capacidade do Studio)
  e trava a confirmação por Studio (RN-020).
- Corrigida a criação do primeiro perfil de Artista (`PUT /api/v1/artists/me/`),
  que falhava com erro 500 por gravar um registro em branco antes de aplicar os
  dados enviados.

## 2026-09-12 — Reformulação de experiência e design system

- Substituída a numeração editorial da navegação por sistema de ícones SVG inline,
  sem dependência externa.
- Removidos os índices decorativos `A/01` do hero dos dashboards e da tela de login.
- Adicionado tom semântico de estado: aprovado, recusado, pendente, em andamento e
  neutro passam a ter cor e ícone próprios.
- Convertidas as tabelas operacionais em cartões empilhados abaixo de 48rem,
  eliminando a rolagem horizontal no celular.
- Adicionado padrão responsivo por faixa: barra lateral completa, trilho de ícones
  com tooltip e barra inferior flutuante.
- Adicionados componentes compartilhados de cabeçalho, título, estado vazio,
  carregamento e erro, eliminando duplicação em oito telas.
- Adicionada orientação de próxima ação a todos os estados vazios.
- Corrigido o indicador de carregamento, que não possuía animação.
- Ajustados alvos de toque para o mínimo de 2.75rem e contraste de texto auxiliar
  para atender AA.
- Adicionados `aria-current`, `aria-busy`, `role="alert"` e suporte a
  `prefers-reduced-motion`.
- Substituído `100vh` por `100dvh`, corrigindo corte de conteúdo em navegador móvel.
- Documentado o design system em `docs/07-ux-ui/design-system.md`.
- Aplicada a regra de uma unidade por arquivo aos arquivos criados: vocabulário de
  ícones dividido em `iconName.ts`, `iconGlyphs.tsx` e `Icon.tsx`; cartões de
  workspace divididos em `workspaceCardIcon.ts` e `workspaceCardHint.ts`.
- Registrada a dívida DT-001 para os módulos multi-export pré-existentes.
- Formalizado o protocolo de desenvolvimento em `CLAUDE.md` na raiz, carregado
  automaticamente a cada sessão, e detalhado em
  `docs/11-processo/protocolo-de-desenvolvimento.md`.

## 2026-09-12 — Portfólio privado

- Integrado armazenamento privado compatível com S3, com MinIO no ambiente Docker local.
- Implementado fluxo de solicitação, upload direto, inspeção real, confirmação, acesso temporário e remoção.
- Removida a exposição de `object_key` das respostas do portfólio.
- Adicionada galeria privada com upload e exclusão na área do Artist.
- Adicionadas auditoria e proteção de propriedade para o ciclo do portfólio.

## 2026-09-11 — Sprint 09 em execução

- Redesenhado o frontend com direção editorial urbana voltada ao universo da tatuagem.
- Adicionado ativo visual original, navegação mobile flutuante e composição responsiva de alto contraste.
- Migrada a paleta, tipografia, dimensões, imagens e animações para tokens CSS centralizados.
- Adicionada bancada transacional da Assessoria para propostas, reservas, Leads, agendamentos e campanhas.
- Adicionados formulários transacionais de trechos de viagem e acomodações à bancada da Assessoria.
- Adicionados testes de contrato e autorização para criação logística pela API.
- Adicionado endpoint seguro de dados de referência para os formulários administrativos.
- Adicionadas navegação real e telas paginadas para as sete filas da Assessoria.
- Adicionadas aprovação e reprovação de candidaturas de Artist e Studio pela interface.
- Adicionadas transições de propostas, confirmação de reservas e decisões de cancelamento nas filas.
- Adicionado fechamento transacional de Leads pela interface, com idempotência e confirmação explícita.
- Adicionada área do Artist com perfil, candidatura e disponibilidade.
- Adicionada área do Studio com perfil, submissão e resposta a solicitações próprias de reserva.
- Adicionadas áreas do Artist para Guests, My Trip, agenda, cancelamento e consulta de portfólio.
- Adicionado contrato da fila logística sem exposição de documentos privados.
- Adicionadas filas e visão operacional da Assessoria.
- Adicionados workspaces com isolamento de dados para Artist e Studio.
- Adicionadas notificações persistentes, idempotentes e processadas por worker.
- Adicionados CSRF explícito, readiness de banco, logs JSON e controles de segurança.
- Adicionados login e dashboards responsivos em inglês, baseados em design tokens.
- Adicionadas imagens e composição Docker de produção.
- Adicionados runbooks de deploy, rollback, backup e restauração.
- Executada restauração real em banco temporário e smoke test dos serviços.
- Mantido aberto o aceite final de interface e jornadas transacionais.
