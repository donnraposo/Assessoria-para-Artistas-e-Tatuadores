# Histórico de Alterações

## 1. Objetivo

Registrar todas as alterações relevantes do projeto. Nenhuma versão foi publicada; o
acumulado da seção 2 descreve o que o produto já entrega e a seção 3 registra as entregas
por data.

## 2. Não publicado

### Adicionado

- Estrutura inicial do projeto e da documentação.
- Consolidação inicial das regras de negócio já confirmadas.
- Planejamento completo do MVP: visão, análise técnica, arquitetura, estrutura, modelo de dados, roadmap, testes e decisões arquiteturais.
- Plano operacional detalhado de todas as tarefas, migrations, endpoints, telas, testes e gates do MVP.
- Fundação containerizada com Django, PostgreSQL e Next.js, endpoint de saúde, pipeline de qualidade e dashboard responsivo baseado em design tokens.
- Base de identidade com usuário customizado, papéis, autenticação por sessão e eventos de auditoria.
- Recuperação segura de senha, limitação de tentativas e políticas reutilizáveis por papel.
- Perfil, candidatura, avaliação, portfólio e disponibilidade de Artistas com auditoria e prevenção de sobreposição.
- Studios, bancadas, preços, disponibilidade, aprovação e reservas transacionais com prevenção de conflito.
- Propostas e Guests com confirmação transacional, múltiplos Studios, metas e ciclo de estados auditado.
- Interface, metadados, rótulos e mensagens públicas da API padronizados em inglês; documentação interna mantida em português.
- Agenda e ocupação de Guests com validação de disponibilidade, período e Studio.
- Leads e fechamento transacional com recebimento externo, idempotência, divisão financeira 20/80 e proteção concorrente de agenda.
- Solicitação de cancelamento pelo Artista, decisão da Assessoria e registro do valor de restituição devido.
- Campanhas, orçamento e gastos de Ads com moeda consistente e auditoria.
- Indicadores derivados de Leads, fechamentos, faturamento, receita, Ads e ocupação.
- Viagens e acomodações administradas pela Assessoria, com moeda consistente e documentos privados.
- Visão `My Trip` para consolidar logística, Studios, agenda e custos do Guest.
- Jornada de candidatura do Artista e avaliação pela Assessoria disponível na interface,
  com fila triável, detalhe da candidatura e decisão auditada.
- Camadas explícitas no frontend, separando transporte HTTP, contratos, serviços por
  módulo, regras de apresentação e componentes.

### Corrigido

- Primeira gravação do perfil do Artista, que respondia HTTP 500 por inserir o registro
  antes de validar os campos obrigatórios.
- Respostas HTTP 404 no lugar de erro interno quando o Artista ainda não possui perfil ou
  candidatura, e quando a candidatura consultada pela Assessoria não existe.

## 3. Registro por data

### 2026-09-11 — Sprint 09 em execução

- Adicionadas filas e visão operacional da Assessoria.
- Adicionados workspaces com isolamento de dados para Artist e Studio.
- Adicionadas notificações persistentes, idempotentes e processadas por worker.
- Adicionados CSRF explícito, readiness de banco, logs JSON e controles de segurança.
- Adicionados login e dashboards responsivos em inglês, baseados em design tokens.
- Adicionadas imagens e composição Docker de produção.
- Adicionados runbooks de deploy, rollback, backup e restauração.
- Executada restauração real em banco temporário e smoke test dos serviços.
- Mantido aberto o aceite final de interface e jornadas transacionais.

### 2026-09-12 — Primeira jornada transacional

- Adicionada a jornada de candidatura do Artista e avaliação pela Assessoria na interface.
- Adicionado o detalhe administrativo da candidatura, com perfil, contato e portfólio.
- Adicionada triagem da fila de candidaturas por nome, estilos e experiência.
- Adicionadas as decisões ADR-018 e ADR-019 sobre camadas e navegação do frontend.
- Corrigida a primeira gravação do perfil do Artista e os erros internos por ausência de
  perfil ou candidatura.
- Mantidos abertos os gates de homologação visual, jornadas restantes e provedor de produção.

## 4. Manutenção

Atualizar o acumulado e o registro por data na mesma alteração que entrega a
funcionalidade, conforme o gate obrigatório por tarefa.
