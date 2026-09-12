# Plano de Execução Detalhado do MVP

## Regras de execução

- Implementar uma tarefa por vez, mantendo uma classe própria por arquivo.
- Atualizar contrato OpenAPI, testes, documentação e changelog junto da funcionalidade.
- Não avançar com testes críticos, migrations ou análise de segurança falhando.
- Aplicar Clean Architecture, SOLID, design tokens e componentes configuráveis.
- Tratar PostgreSQL como comportamento oficial; Docker como ambiente padrão.

## Sprint 01 — Fundação técnica

### S01.01 — Estrutura

- Criar projetos `backend`, `frontend` e `infrastructure`.
- Separar configurações Django de desenvolvimento, teste e produção.
- Criar estrutura modular e endpoint `/api/v1/health/`.
- Preparar Next.js, TypeScript estrito, lint e testes.
- **Arquivos:** configurações raiz, `backend/config`, `backend/modules/health`, `frontend/src/app`.
- **Aceite:** Django e Next.js iniciam sem erro; health retorna HTTP 200.

### S01.02 — Containers

- Criar imagens multi-stage para backend e frontend.
- Criar Compose com frontend, backend e PostgreSQL.
- Executar containers sem privilégios em produção.
- Configurar health checks, volumes e variáveis sem guardar segredos.
- **Aceite:** build reproduzível; serviços iniciam e se comunicam.

### S01.03 — Qualidade e CI

- Configurar Ruff, Pytest, ESLint, TypeScript e testes do frontend.
- Fixar dependências em lockfiles.
- Criar pipeline para lint, testes, build e auditoria.
- **Aceite:** pipeline local equivalente aprovado; nenhuma vulnerabilidade crítica conhecida.

## Sprint 02 — Identidade, acesso e auditoria

**Estado:** concluída. Usuário, papéis, login, logout, consulta da sessão, recuperação de senha, limitação de tentativas, políticas por papel e auditoria implementados e testados.

### S02.01 — Modelo de identidade

- Criar `User` com UUID, e-mail normalizado, estado e timestamps.
- Criar enums e perfis de Artista, Studio e Assessoria.
- Configurar `AUTH_USER_MODEL` antes das migrations de domínio.
- **Migration:** tabelas de usuário, papel e associação de escopo.
- **Testes:** unicidade de e-mail, senha, estados e criação de superusuário.

### S02.02 — Autenticação

- Implementar login, logout, sessão segura, recuperação e redefinição de senha.
- Aplicar CSRF, cookies seguros, rate limit e mensagens neutras.
- **Endpoints:** `/auth/login`, `/auth/logout`, `/auth/me`, `/auth/password/*`.
- **Telas:** entrar, recuperar senha, redefinir senha e sessão expirada.
- **Aceite:** sessão revogável e nenhum token persistido em `localStorage`.

### S02.03 — Autorização e auditoria

- Implementar políticas por papel, propriedade e escopo.
- Criar evento de auditoria append-only com ator, ação, alvo, motivo e data.
- **Testes:** matriz positiva e negativa para todos os perfis.
- **Aceite:** Studio nunca acessa Ads, Leads, faturamento ou receita da Assessoria.

## Sprint 03 — Artistas e candidaturas

**Estado:** concluída. Perfil, candidatura, avaliação, portfólio privado com URL
assinada e disponibilidade sem sobreposição foram implementados e integrados à interface.

### S03.01 — Perfil e candidatura

- Modelar Artista, candidatura, estilos, parâmetros comerciais e estados.
- Implementar criação, edição de rascunho, envio, análise, aprovação e reprovação.
- **Endpoints:** `/artists`, `/artist-applications`, ações `/submit`, `/approve`, `/reject`.
- **Telas:** candidatura, perfil, fila de avaliação e detalhe administrativo.
- **Testes:** transições, campos obrigatórios, propriedade e auditoria.

### S03.02 — Portfólio

- Integrar armazenamento compatível com S3 e URLs assinadas.
- Validar extensão, MIME real, tamanho, quantidade, ordem e privacidade.
- **Endpoints:** solicitação de upload, confirmação, listagem e remoção.
- **Aceite:** binários fora do banco e acesso privado temporário.

**Implementado:** MinIO no Docker local, adaptador S3 compatível, solicitação temporária,
upload direto, inspeção de assinatura MIME, confirmação idempotente, leitura assinada,
remoção, auditoria e isolamento por Artist. O limite máximo de imagens permanece sem
valor arbitrário até definição explícita da regra de negócio.

### S03.03 — Disponibilidade

- Modelar intervalos com UTC e fuso operacional.
- Implementar inclusão, alteração e bloqueio de sobreposição.
- Permitir intervenção excepcional da Assessoria com motivo obrigatório.
- **Aceite:** histórico identifica antes, depois, responsável e justificativa.

## Sprint 04 — Studios e reservas

**Estado:** concluída no backend. Cadastro, aprovação, bancadas, preços, disponibilidade e fluxo transacional de reserva foram implementados. A reserva já utiliza relacionamento com o Guest criado na Sprint 05.

### S04.01 — Cadastro e aprovação

- Modelar Studio, endereço, estrutura, bancada, preço e candidatura.
- Implementar solicitação, avaliação, aprovação, reprovação e inativação permitida.
- **Telas:** cadastro do Studio e fila administrativa.
- **Aceite:** somente Studio aprovado aparece na pesquisa operacional.

### S04.02 — Oferta e disponibilidade

- Registrar capacidade, bancadas, modalidades de cobrança e intervalos.
- Registrar oferta de acomodação sem criar reserva automática.
- **Testes:** validade de períodos, capacidade e isolamento comercial.

### S04.03 — Reserva

- Implementar pesquisa, solicitação, aceite, recusa e confirmação da Assessoria.
- Implementar registro manual de negociação externa.
- Registrar pagamento externo como `Pendente` ou `Pago`.
- **Testes concorrentes:** última bancada e conflito do Artista.

## Sprint 05 — Propostas e Guests

**Estado:** concluída no backend. Proposta, validações confirmatórias, snapshot do Guest, Studio principal, múltiplos Studios, metas e transições auditadas foram implementados. Reservas agora possuem chave estrangeira real para Guest.

### S05.01 — Proposta

- Modelar cidade, datas, fuso, moeda, Studios, Ads e valores comerciais.
- Implementar estados Rascunho, Em planejamento, Pronta, Confirmada, Recusada e Cancelada.
- Validar pré-condições de confirmação.
- **Endpoints/telas:** CRUD e ações de transição com histórico.

### S05.02 — Guest

- Gerar Guest a partir de snapshot imutável da proposta confirmada.
- Implementar estados Em captação, Agenda completa, Em andamento, Finalizado e Cancelado.
- Associar múltiplos Studios por período sem conflito.
- **Aceite:** Guest confirmado habilita agenda, marketing e Minha Viagem.

## Sprint 06 — Agenda, vendas e financeiro

**Estado:** concluída no backend. Agenda vinculada à disponibilidade do Artista e ao Studio do Guest, ocupação por horas e dias, Leads, fechamento transacional 20/80, idempotência, prevenção concorrente de conflitos e cancelamento solicitado pelo Artista foram implementados. Políticas de cancelamento ainda não aprovadas permanecem bloqueadas.

### S06.01 — Agenda

- Modelar agendamento, bloqueio e intervalo disponível.
- Calcular ocupação por dias e horas sem interromper captação na meta.
- Criar calendário da Assessoria e visão do Artista.
- **Testes:** bordas de intervalo, fusos e concorrência.

### S06.02 — Leads e negociação

- Registrar Lead mínimo vinculado ao Guest e origem externa.
- Registrar valor negociado, mínimo autorizado e consulta ao Artista no mínimo.
- **Aceite:** fechamento abaixo do mínimo é impossível.

### S06.03 — Fechamento 20/80

- Registrar recebimento, comprovante/referência e idempotência.
- Em uma transação: confirmar recebimento, criar fechamento, confirmar agendamento e lançamentos 20/80.
- Preservar snapshot do valor e moeda.
- **Testes:** arredondamento, repetição, rollback e concorrência.

### S06.04 — Cancelamentos confirmados

- Artista somente solicita; Assessoria decide.
- Registrar responsabilidade e devolução dos 20% quando atribuída ao Artista.
- Manter demais origens bloqueadas até política aprovada.

## Sprint 07 — Marketing e indicadores

**Estado:** concluída no backend. Campanhas e gastos de Ads na moeda principal do Guest, auditoria e métricas derivadas de Leads, fechamentos, lançamentos financeiros e ocupação foram implementados. Métricas sem denominador retornam valor indefinido, sem divisão artificial por zero.

### S07.01 — Campanhas e Ads

- Registrar orçamento, campanha, período, canal e gasto efetivo.
- Impedir soma entre moedas sem conversão registrada.
- **Telas:** lançamento administrativo e visão autorizada do Artista.

### S07.02 — Métricas

- Calcular Leads, fechamentos, faturamento, receita, conversão, CPL, custo por fechamento, ROAS e ocupação.
- Definir resultados seguros para denominador zero e dados incompletos.
- **Aceite:** métricas derivadas não exigem duplicidade de entrada.

## Sprint 08 — Logística e Minha Viagem

**Estado:** concluída no backend. Trechos, acomodações externas ou vinculadas a Studio, referências documentais privadas, custos e a visão consolidada `My Trip` foram implementados. A Assessoria altera os dados e o Artista consulta somente os próprios Guests.

### S08.01 — Viagem e acomodação

- Modelar trechos, origem, destino, horários, referências, estado e custos.
- Modelar acomodação independente ou oferecida por Studio.
- Implementar atualização exclusiva da Assessoria e consulta do Artista.

### S08.02 — Minha Viagem

- Consolidar viagem, acomodação, Studios, agenda e custos por Guest.
- Implementar estados vazio, pendente, atualizado e indisponível.
- **Testes:** acesso, documentos privados, moeda e consistência com agenda.

## Sprint 09 — Administração e lançamento

**Estado:** em execução. S09.01, S09.02 e a parcela técnica de S09.03 estão
implementadas. S09.04 permanece aberta até que as jornadas transacionais estejam
disponíveis no frontend e a homologação visual/manual seja registrada.

### S09.01 — Operação administrativa

- Criar filas de candidaturas, reservas, propostas, fechamentos e logística.
- Criar filtros, paginação, estados vazios, erros e confirmação de ações críticas.
- Restringir Django Admin a suporte técnico controlado.

**Implementado:** dashboard Advisory, sete filas paginadas, atividade auditada,
workspaces isolados para Artist e Studio e ações de revisão, proposta, reserva,
cancelamento e fechamento financeiro. Adicionadas nas filas `guest_proposals` e
`studio_reservations` as ações de recusa/cancelamento de proposta (RN-010) e de
registro de negociação externa de reserva (RN-032). O Django Admin permanece
reservado à operação técnica autenticada. RN-033 (status de pagamento do
Studio) ainda não tem local na interface, pois atua sobre a reserva já
confirmada, fora das filas atuais — avaliação pendente na Fase C. Criação e
edição completa dos demais registros ainda serão entregues nas áreas
transacionais de cada perfil.

### S09.02 — Notificações e tarefas

- Introduzir Celery/Redis somente para casos aprovados.
- Implementar e-mails e lembretes idempotentes, retries e registro de falha.
- Manter decisões financeiras e de agenda fora da fila.

**Implementado:** caixa persistente, leitura, idempotência, até três tentativas e
worker independente. Celery/Redis não foram introduzidos porque o volume atual não
justifica essa dependência.

### S09.03 — Segurança e operação

- Configurar TLS, headers, secrets, logs estruturados, monitoramento e alertas.
- Configurar backup, retenção e executar restauração real.
- Verificar dependências e imagens; remover privilégios desnecessários.

**Implementado:** cookies e CSRF seguros, headers, redirecionamento TLS configurável,
HSTS conservador, logs JSON, readiness com banco, imagens sem usuário root, stack de
produção, runbooks e restauração real em banco temporário.

### S09.04 — Aceite e implantação

- Executar jornadas ponta a ponta dos três perfis.
- Validar responsividade, teclado, contraste e textos operacionais.
- Executar smoke test em homologação e plano de rollback.
- **Aceite final:** Guest planejado, confirmado, preenchido, executado e acompanhado sem área do Cliente final.

**Em andamento:** a Assessoria já possui filas, decisões principais e uma bancada
transacional para criar propostas, reservas, Leads, agendamentos, campanhas e Studio
adicional em um Guest (RN-015); Artist já possui perfil, candidatura, disponibilidade
com edição e remoção (RN-007) e tela de auto-cadastro (RN-004/026); Studio já possui
perfil, submissão, resposta a reservas e cadastro próprio de bancadas, preços e
disponibilidade (RN-029). Artist também consulta Guests, agenda, cancelamentos, My
Trip e metadados do portfólio. O design system foi atualizado para uma linguagem
editorial urbana própria do universo da tatuagem, mantendo tokens CSS centralizados.
A criação de viagem e acomodação também está disponível na bancada. O upload privado
do portfólio foi concluído. Permanecem teste visual responsivo/teclado/contraste e
homologação manual ponta a ponta, além da interface financeira (saldo do Artist e
confirmação pela Assessoria) e de RN-033 (status de pagamento do Studio), avaliadas
na Fase C por exigirem um local novo na interface. Login, dashboards, API e smoke
HTTP já passaram.

## Gate obrigatório por tarefa

1. Regra e critério de aceite identificados.
2. Contrato e autorização definidos.
3. Migration revisada, quando aplicável.
4. Implementação pequena e coesa.
5. Testes unitários, integração e acesso proporcionais ao risco.
6. Lint, tipos, testes e build aprovados.
7. OpenAPI, rastreabilidade, ADR e changelog atualizados quando afetados.
8. Evidência de homologação registrada antes de concluir a sprint.
