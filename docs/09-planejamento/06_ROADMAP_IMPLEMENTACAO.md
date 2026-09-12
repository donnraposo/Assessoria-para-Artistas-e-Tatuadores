# Roadmap de Implementação

Cada sprint será entregue em mudança pequena, testada e documentada. Os nomes de arquivos concretos serão confirmados ao iniciar a sprint, preservando uma classe por arquivo.

O checklist operacional completo está em `09_PLANO_EXECUCAO_DETALHADO.md`.

## Sprint 01 — Fundação técnica

**Objetivo:** criar os projetos Django e Next.js, containers, configuração por ambiente, PostgreSQL, verificações de qualidade e CI inicial.

**Arquivos:** configuração raiz, `backend/config`, `frontend`, `infrastructure/docker`, `compose.yaml`, exemplos de ambiente e documentação de execução.

**Dependências:** versões suportadas de Python, Django, Node.js, Next.js e PostgreSQL.

**Riscos:** divergência entre desenvolvimento e produção; exposição de segredos.

**Resultado esperado:** aplicações e banco iniciam de forma reproduzível e executam verificações básicas.

## Sprint 02 — Identidade e autorização

**Objetivo:** implementar usuário, autenticação, recuperação de acesso, papéis e base de auditoria.

**Arquivos:** módulos `identity` e `audit`, endpoints e testes.

**Dependências:** decisão final entre sessão e tokens conforme topologia de domínios.

**Riscos:** escalada de privilégio e exposição entre perfis.

**Resultado esperado:** Artista, Studio e Assessoria autenticam-se e recebem acesso isolado.

## Sprint 03 — Artistas e candidaturas

**Objetivo:** cadastrar perfil, portfólio, disponibilidade e avaliação humana.

**Arquivos:** módulo `artists`, integração de arquivos, telas e testes.

**Dependências:** armazenamento compatível com S3 e dados obrigatórios da candidatura.

**Riscos:** dados pessoais, upload malicioso e critérios de reprovação indefinidos.

**Resultado esperado:** candidatura percorre envio, análise e decisão com auditoria.

## Sprint 04 — Studios e reservas

**Objetivo:** cadastrar e aprovar Studios, bancadas, preços, disponibilidade e solicitações de reserva.

**Arquivos:** módulos `studios` e `bookings`, telas e testes.

**Dependências:** modalidades de cobrança e informações mínimas da acomodação.

**Riscos:** conflitos por capacidade e confirmação externa inconsistente.

**Resultado esperado:** Assessoria encontra Studio aprovado, solicita e confirma uma reserva.

## Sprint 05 — Propostas e Guests

**Objetivo:** implementar planejamento, validação, confirmação e estados do Guest.

**Arquivos:** módulo `guests`, telas e testes de transição.

**Dependências:** Artistas e Studios aprovados; moeda e fuso definidos.

**Riscos:** alterações retroativas e estados inválidos.

**Resultado esperado:** proposta válida gera Guest confirmado e rastreável.

## Sprint 06 — Agenda, vendas e financeiro

**Objetivo:** implementar disponibilidade, Leads, fechamento, recebimento de 20%, agendamento e divisão 20/80.

**Arquivos:** módulos `scheduling`, `sales` e `finance`, telas e testes concorrentes.

**Dependências:** Guest confirmado e política mínima de cancelamento.

**Riscos:** dupla reserva, arredondamento e operações parcialmente confirmadas.

**Resultado esperado:** fechamento confirmado atualiza agenda e financeiro atomicamente.

## Sprint 07 — Marketing e indicadores

**Objetivo:** registrar campanhas, Ads e Leads e calcular métricas do Guest.

**Arquivos:** módulo `marketing`, consultas, dashboards e testes matemáticos.

**Dependências:** vendas, agenda e critérios das métricas.

**Riscos:** duplicidade de dados calculados e divisão por zero.

**Resultado esperado:** Assessoria e Artista visualizam indicadores autorizados e consistentes.

## Sprint 08 — Logística e Minha Viagem

**Objetivo:** registrar viagem, acomodação, custos e visão consolidada do Artista.

**Arquivos:** módulo `logistics`, telas e testes de acesso.

**Dependências:** campos mínimos e políticas de edição.

**Riscos:** dados incompletos e exposição indevida de documentos.

**Resultado esperado:** Guest confirmado apresenta viagem, hospedagem, Studios, agenda e custos.

## Sprint 09 — Administração, segurança e lançamento

**Estado:** em execução. Filas administrativas, dashboards por papel, notificações
persistentes, logs estruturados, endurecimento de segurança, imagens de produção,
backup/restauração e smoke tests foram implementados. Restam as telas transacionais
completas e a homologação visual/manual das jornadas para o aceite final.

**Objetivo:** concluir filas operacionais, observabilidade, backup, recuperação, segurança e aceite do MVP.

**Arquivos:** áreas administrativas, infraestrutura, runbooks e testes ponta a ponta.

**Dependências:** módulos anteriores e provedor de produção.

**Riscos:** lacunas operacionais, restauração não testada e permissões excessivas.

**Resultado esperado:** ciclo completo do Guest aprovado em homologação e pronto para implantação controlada.

## Regra de avanço

Cada sprint exige critérios de aceite atendidos, testes proporcionais ao risco e atualização das decisões afetadas antes da seguinte.
