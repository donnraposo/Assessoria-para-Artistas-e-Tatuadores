# Regras de Negócio

## 1. Objetivo

Consolidar as regras confirmadas da plataforma e separar decisões ainda não tomadas.

## 2. Convenções

- `Confirmada`: decisão expressamente aceita na definição do produto.
- `Em aberto`: tema citado ou recomendado, mas ainda não decidido.
- A numeração abaixo substitui rascunhos anteriores e organiza as regras por domínio.

## 3. Regras confirmadas

### 3.1 Atores e acesso

#### RN-001 — Tipos de usuário

Artista, Studio e Assessoria/Administração terão acesso autenticado e áreas distintas.

#### RN-002 — Cliente final sem área

O Cliente final não terá login nem área própria. Leads e clientes serão tratados pela equipe da Assessoria/Marketing.

#### RN-003 — Separação de informações

Cada perfil visualizará somente as informações necessárias à sua atuação. O Studio não acessará investimento em Ads, leads, conversão ou receita da Assessoria.

### 3.2 Artista

#### RN-004 — Candidatura

O Artista realiza cadastro e envia dados profissionais, experiência e portfólio para avaliação.

#### RN-005 — Avaliação humana

A equipe interna da Assessoria avalia o nível do trabalho e aprova ou reprova a candidatura. O cadastro, por si só, não autoriza o uso completo dos serviços.

#### RN-006 — Perfil e portfólio

O cadastro do Artista deve permitir registrar dados pessoais e profissionais, anos de experiência, estilos e portfólio necessários à avaliação.

#### RN-007 — Disponibilidade

O Artista administra sua disponibilidade por dia e intervalo de horário.

#### RN-008 — Intervenção da Assessoria

A Assessoria pode alterar a disponibilidade em situação excepcional, mantendo histórico da alteração, responsável e motivo.

### 3.3 Guest

#### RN-009 — Centralidade do Guest

O Guest representa uma operação de um Artista em determinada localidade e período e relaciona agenda, Studios, marketing, fechamentos, finanças e logística.

#### RN-010 — Proposta e confirmação

A Proposta de Guest precede o Guest confirmado. Seus estados são `Rascunho`, `Em planejamento`, `Pronta para confirmação`, `Confirmada`, `Recusada` ou `Cancelada`.

#### RN-011 — Condições de confirmação

Para confirmação do Guest devem estar definidos cidade, datas, Studio, Ads e valores das tattoos. Viagem e acomodação não são pré-requisitos de confirmação.

#### RN-012 — Estados do Guest

O Guest confirmado pode evoluir por `Em captação`, `Agenda completa`, `Em andamento` e `Finalizado`, com `Cancelado` como saída excepcional.

#### RN-013 — Moeda principal

Toda Proposta de Guest deve possuir uma moeda principal definida antes da confirmação.

#### RN-014 — Consolidação monetária

Valores do Guest devem ser apresentados e consolidados na moeda principal, sem somar moedas diferentes como equivalentes.

#### RN-015 — Múltiplos Studios

Um Guest pode utilizar mais de um Studio, inclusive na mesma localidade, desde que os horários não sejam incompatíveis.

### 3.4 Valores e negociação

#### RN-016 — Valores informados pelo Artista

O Artista explicita valor mínimo da tattoo, ticket esperado e, quando aplicável, valor da sessão diária.

#### RN-017 — Autonomia comercial

A Assessoria pode negociar e melhorar a proposta dentro da faixa autorizada pelo Artista, sem fechar abaixo do valor mínimo.

#### RN-018 — Consulta no valor mínimo

Quando a negociação chegar ao valor mínimo, a Assessoria deve contatar o Artista antes de concluir o fechamento nesse valor.

### 3.5 Agenda e ocupação

#### RN-019 — Granularidade da agenda

Disponibilidade, reserva de Studio e agendamento devem considerar data e intervalo de horário.

#### RN-020 — Conflitos

O sistema deve impedir reservas de Studio ou agendamentos incompatíveis para o mesmo Artista no mesmo intervalo.

#### RN-021 — Ocupação

A ocupação do Guest será medida tanto por dias quanto por horas efetivamente disponíveis para tatuar.

#### RN-022 — Meta não é limite

A meta de ocupação não interrompe a captação. O objetivo operacional continua sendo ocupar até 100% da disponibilidade comercial.

#### RN-023 — Confirmação do agendamento

Um agendamento só é confirmado após o recebimento, pela Assessoria, dos 20% do valor final da tattoo.

#### RN-024 — Cancelamento pelo Artista

O Artista não cancela diretamente um agendamento confirmado; ele solicita o cancelamento à Assessoria.

#### RN-025 — Devolução por responsabilidade do Artista

Se o cancelamento for de responsabilidade do Artista, ele devolve à Assessoria os 20% recebidos no fechamento para restituição ao Cliente.

### 3.6 Studios

#### RN-026 — Solicitação de entrada

Qualquer Studio pode criar conta, preencher seus dados e solicitar entrada na plataforma.

#### RN-027 — Aprovação do Studio

A Assessoria realiza avaliação humana e aprova ou reprova o Studio. Somente Studios aprovados aparecem nas pesquisas e podem ser usados em Guests.

#### RN-028 — Modelo de cobrança

O Studio define livremente suas modalidades e condições de cobrança, como hora, diária, semana, percentual ou valor negociado.

#### RN-029 — Capacidade e disponibilidade

O Studio informa capacidade de bancadas e disponibilidade por data e horário.

#### RN-030 — Solicitação de reserva

A Assessoria pode solicitar reserva pela plataforma; o Studio pode aceitar ou recusar.

#### RN-031 — Confirmação da reserva

A confirmação operacional da reserva é responsabilidade da Assessoria.

#### RN-032 — Negociação externa

A Assessoria pode negociar por canais externos e registrar manualmente a reserva e sua forma de confirmação.

#### RN-033 — Pagamento do Studio

O pagamento do Studio é responsabilidade do Artista, ocorre fora da plataforma e tem status operacional `Pendente` ou `Pago`.

### 3.7 Marketing e Ads

#### RN-034 — Responsabilidade por Ads

O investimento em Ads é custeado pelo Artista.

#### RN-035 — Funil do MVP

O funil oficial do MVP acompanha apenas `Leads -> Fechamentos`; etapas intermediárias permanecem nas ferramentas externas da equipe.

#### RN-036 — Dados manuais

A equipe registra por Guest os Leads gerados e o valor efetivamente gasto em Ads.

#### RN-037 — Dados calculados

Fechamentos, faturamento vendido, receita da Assessoria, conversão, CPL, custo por fechamento, ROAS e ocupação devem ser calculados a partir dos dados disponíveis, evitando duplicidade de entrada.

### 3.8 Financeiro 20/80

#### RN-038 — Divisão financeira

Sobre o valor final de cada tattoo, 20% são pagos pelo Cliente à Assessoria e os 80% restantes são destinados ao Artista.

#### RN-039 — Receita da Assessoria

A receita da Assessoria é calculada automaticamente como 20% do valor final fechado da tattoo.

#### RN-040 — Saldo previsto do Artista

Os 80% devem ser apresentados como saldo previsto para o Artista enquanto o recebimento externo não estiver confirmado.

#### RN-041 — Controle operacional

A plataforma registra e acompanha valores, mas não foi definida como intermediadora de todos os pagamentos no MVP.

### 3.9 Logística, viagem e acomodação

#### RN-042 — Princípio de responsabilidade

A Assessoria organiza e administra Studio, viagem e acomodação; o Artista arca com esses custos, assim como com Ads.

#### RN-043 — Viagem externa

A plataforma pode registrar informações da viagem vinculada ao Guest. Contratação e pagamento ocorrem externamente e são custeados pelo Artista.

#### RN-044 — Acomodação independente

A acomodação não precisa pertencer ao Studio utilizado no Guest.

#### RN-045 — Oferta por Studio

O Studio pode informar que possui acomodação disponível para Artistas.

#### RN-046 — Sem reserva automática

A disponibilidade informada pelo Studio não gera reserva automática de acomodação.

#### RN-047 — Intermediação da acomodação

A Assessoria intermedeia e administra o processo de acomodação entre Studio e Artista; o Artista paga o custo.

#### RN-048 — Minha Viagem

Cada Guest confirmado disponibiliza ao Artista a área `Minha Viagem`, consolidando viagem, acomodação, Studios, agenda e custos relacionados.

#### RN-049 — Gestão e consulta da viagem

A Assessoria administra e atualiza os dados de `Minha Viagem`; o Artista os acompanha.

## 4. Pontos em aberto

- Critérios eliminatórios, estados finais e comunicação do motivo de reprovação do Artista.
- Contrato, plano, mensalidade ou cobranças adicionais da Assessoria.
- Natureza jurídica/contábil e nomenclatura definitiva dos 20%.
- Políticas para cancelamento pelo Cliente, Studio, viagem, remarcação e no-show.
- Confirmação e rastreabilidade detalhadas do pagamento ao Studio.
- Tratamento de valores originalmente cobrados em moeda diferente da moeda principal e taxa de conversão manual.
- Escopo exato de custos adicionais e cálculo do resultado estimado do Guest no MVP.
- Campos obrigatórios e estados detalhados de viagem e acomodação.
- Dados mínimos da acomodação oferecida pelo Studio.
- Regras de garantia comercial de agenda cheia.
- Perfis e permissões internas da Assessoria.
- Metas de ocupação e faturamento por Guest.

## 5. Fora do MVP ou evolução futura

- Integração com Google Calendar, sem dependência do MVP.
- Conversão cambial automática.
- Marketplace autônomo de Studios e acomodações.
- Emissão de passagens ou processamento integral de pagamentos.
- CRM completo de leads.

## 6. Histórico de alterações

| Data | Alteração |
|---|---|
| 2026-09-11 | Consolidação inicial das decisões já confirmadas. |
