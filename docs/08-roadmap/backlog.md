# Backlog

## 1. Objetivo

Registrar itens candidatos sem convertê-los automaticamente em compromisso de entrega.

## 2. A priorizar

- Detalhar critérios de candidatura e aprovação.
- Definir políticas completas de cancelamento.
- Definir permissões internas da Assessoria.
- Especificar cálculo e registro de custos adicionais.
- Detalhar pagamento e conciliação do Studio.
- Definir tratamento de valores em moeda secundária.
- Especificar notificações e auditoria.

## 3. Dívida técnica registrada

### DT-001 — Módulos multi-export no frontend

`frontend/src/lib/format.ts` (6 exports) e `frontend/src/content/dashboard.ts`
(5 exports) agrupam várias funções e tipos no mesmo arquivo, divergindo da regra de
uma unidade por arquivo definida no ADR-007.

**Origem:** ambos são anteriores à reformulação de interface de 2026-09-12; a regra
foi aplicada estritamente apenas aos arquivos criados naquela entrega.

**Decisão:** dividir em sprint própria, por envolver arquitetura vigente e atualização
ampla de imports. Registrado em 2026-09-12 com aprovação do responsável.

**Impacto se não tratado:** inconsistência de convenção entre backend e frontend.

## 4. Critério de priorização

Valor operacional, risco, dependências e aderência ao ciclo principal do MVP.
