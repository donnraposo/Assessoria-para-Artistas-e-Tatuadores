# Homologação da Sprint 09

## Evidências aprovadas em 2026-09-11

- Backend: Ruff aprovado, 36 testes aprovados, Django Check sem problemas e nenhuma
  migração pendente.
- Frontend: ESLint, TypeScript, 2 testes unitários e build Next.js aprovados.
- Containers: imagens de produção construídas; backend e frontend executados sem
  usuário root; PostgreSQL sem porta pública na composição de produção.
- Saúde: frontend e backend responderam HTTP 200; readiness confirmou banco
  disponível; headers defensivos foram verificados.
- Recuperação: dump restaurado em banco temporário e 37 migrações consultadas; banco
  temporário e dump foram removidos após o teste, sem alterar o banco principal.

## Evidências aprovadas em 2026-09-12

- Jornada de candidatura e avaliação de Artista disponível na interface, cobrindo perfil,
  envio, fila triável, detalhe e decisão auditada.
- Backend: Ruff aprovado, 43 testes aprovados em PostgreSQL real, Django Check sem
  problemas e nenhuma migração pendente.
- Frontend: ESLint, TypeScript, 19 testes unitários e build Next.js aprovados.
- Conformidade: aprovação do Artista, piso comercial declarado e intervenção auditada da
  Assessoria na disponibilidade passaram a ser exigidos e cobertos por testes (53 no total).

## Gates ainda abertos

- Homologação visual responsiva, teclado e contraste em navegador real.
- Telas transacionais restantes: Studio, proposta/Guest, agenda, Leads, fechamento e
  logística.
- Homologação manual ponta a ponta com usuários dos três papéis.
- Definição do provedor de produção, TLS na borda, monitoramento e alertas externos.

O ambiente validado é técnico/local. Esta evidência não autoriza declarar produção
nem elimina os gates acima.
