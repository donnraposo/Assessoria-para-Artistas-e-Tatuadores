# Design System do Frontend

> Documento de referência da camada de interface. Ele substitui a leitura do código
> para entender como a interface é construída, quais peças existem e como estendê-las.
> Atualizar sempre que um token, componente, classe ou regra responsiva mudar.

## 1. Objetivo

Garantir que os três perfis (Artist, Studio, Advisory) compreendam cada função ao
bater o olho, em desktop, tablet e celular, preservando a direção editorial definida
no ADR-018 e a centralização de estilo definida no ADR-012.

## 2. Princípios

1. **Reconhecimento, não memorização.** Todo elemento interativo carrega ícone,
   rótulo e estado. Nada depende de o usuário lembrar o significado de um código.
2. **Zero valor mágico.** Nenhuma cor, espaço, raio, duração ou dimensão é escrita
   diretamente no CSS. Tudo vem de token declarado em `tokens.css`.
3. **Cor com função semântica.** Verde, vermelho, âmbar e azul comunicam estado
   operacional. O bordô permanece exclusivo da marca e de ênfase.
4. **Responsividade real, não redução.** Cada faixa de tela recebe um padrão de
   navegação e de apresentação de dados próprio, não uma versão espremida do desktop.
5. **Um componente, uma responsabilidade.** Telas compõem; não estilizam.

## 3. Arquitetura de camadas

```text
tokens.css        decisões visuais      cor, escala, espaço, raio, sombra, motion
    |
styles.css        primitivos e composição, consome apenas tokens
    |
components/       peças reutilizáveis com responsabilidade única
    |
telas             composição; sem estilo próprio, sem regra de negócio
```

Dependências apontam sempre para baixo. Uma tela nunca declara estilo; um componente
nunca contém regra de negócio; o CSS nunca contém valor literal.

## 4. Arquivos e responsabilidades

| Arquivo | Responsabilidade |
|---|---|
| `frontend/src/app/tokens.css` | Única fonte de valores visuais |
| `frontend/src/app/styles.css` | Primitivos e composição, em 21 seções numeradas |
| `frontend/src/components/Icon.tsx` | Componente de ícone |
| `frontend/src/components/iconGlyphs.tsx` | Mapa de traços SVG, uma entrada por ícone |
| `frontend/src/components/iconName.ts` | Tipo `IconName`, contrato do vocabulário |
| `frontend/src/components/*.tsx` | Componentes compartilhados e telas |
| `frontend/src/content/dashboard.ts` | Metadados de navegação e filas |
| `frontend/src/content/workspaceCardIcon.ts` | Ícone por cartão de workspace |
| `frontend/src/content/workspaceCardHint.ts` | Descrição por cartão de workspace |
| `frontend/src/lib/format.ts` | Funções puras de formatação e tom semântico |

**Convenção:** uma unidade exportada por arquivo, conforme ADR-007. O `type XProps`
não exportado é o contrato do próprio componente e permanece junto dele. As exceções
pré-existentes (`format.ts` e `dashboard.ts`) estão registradas como DT-001 em
`docs/08-roadmap/backlog.md`.

## 5. Tokens

Declarados em `:root` de `tokens.css`. Famílias e uso pretendido:

| Família | Prefixo | Uso |
|---|---|---|
| Cor de superfície | `--color-canvas`, `--color-surface`, `--color-surface-soft`, `--color-surface-veil` | Fundos, do mais externo ao mais sutil |
| Cor de navegação | `--color-sidebar`, `--color-sidebar-active`, `--color-sidebar-hover` | Barra lateral escura |
| Cor de texto | `--color-ink`, `--color-ink-soft`, `--color-on-dark`, `--color-muted`, `--color-muted-dark` | Hierarquia tipográfica |
| Cor de marca | `--color-accent`, `--color-accent-strong`, `--color-accent-soft` | Bordô — marca e ênfase |
| Cor semântica | `--color-positive`, `--color-danger`, `--color-warning`, `--color-info` e variantes `-soft` | Estado operacional |
| Borda | `--color-border`, `--color-border-strong`, `--color-border-dark`, `--border-thin`, `--border-strong`, `--border-dark`, `--border-dashed` | Separação |
| Tipografia | `--font-sans`, `--font-display`, `--text-xs` a `--text-hero`, `--weight-*`, `--line-*`, `--tracking-*` | Escala fluida com `clamp()` |
| Espaço | `--space-0` a `--space-12`, `--space-page` | Ritmo vertical e horizontal |
| Raio | `--radius-sm` a `--radius-hero`, `--radius-round` | Arredondamento |
| Sombra | `--shadow-card`, `--shadow-raised`, `--shadow-float`, `--shadow-focus` | Elevação e foco |
| Movimento | `--transition-fast`, `--transition-slow`, `--spin-cycle`, `--lift-hover` | Animação e microinteração |
| Toque e ícone | `--touch-target`, `--icon-size`, `--icon-size-lg`, `--icon-box` | Acessibilidade física |
| Opacidade | `--opacity-hidden`, `--opacity-subtle`, `--opacity-disabled`, `--opacity-full` | Estados |

**Regra:** ao precisar de um valor novo, criar token seguindo a convenção da família
correspondente. Nunca escrever o valor direto no seletor.

## 6. Sistema de ícones

`Icon.tsx` expõe um componente único e um tipo `IconName`. Os traços são SVG inline
de 24×24, `stroke="currentColor"`, sem dependência externa.

**Nomes disponíveis:**

`overview` · `create` · `artist` · `studio` · `proposal` · `reservation` · `lead` ·
`cancellation` · `logistics` · `schedule` · `portfolio` · `guest` · `trip` ·
`revenue` · `alert` · `approved` · `declined` · `pending` · `arrow` · `signout` ·
`bell` · `empty` · `upload` · `trash`

**Uso:** `<Icon name="guest" />`. Por padrão é decorativo (`aria-hidden`). Passar
`title` apenas quando o ícone for a única forma de comunicar a informação.

**Para adicionar:** incluir o nome em `components/iconName.ts` e a entrada
correspondente no mapa de `components/iconGlyphs.tsx`. Como o mapa é tipado como
`Record<IconName, ReactElement>`, o TypeScript passa a exigir a cobertura — esquecer
o traço quebra a compilação, não a interface em produção.

## 7. Componentes compartilhados

| Componente | Responsabilidade | Props principais |
|---|---|---|
| `Icon` | Vocabulário visual | `name`, `title?` |
| `Sidebar` | Navegação por papel, nos três modos responsivos | `name`, `role` |
| `WorkspaceHeader` | Cabeçalho da área de trabalho com saída de sessão | `eyebrow`, `title`, `onSignOut`, `children?` |
| `PageHeading` | Título de seção com sobrelinha, descrição e elemento à direita | `title`, `description?`, `eyebrow?`, `aside?` |
| `StatusBadge` | Estado operacional traduzido em cor e ícone | `status` |
| `EmptyState` | Vazio com orientação do que fazer | `title`, `hint?`, `icon?`, `action?` |
| `LoadingScreen` | Carregamento acessível com `aria-busy` | `message` |
| `ErrorScreen` | Falha com ação de recuperação | `title`, `message`, `action?` |
| `QueueCard` | Indicador com ícone, valor, estado e explicação | `label`, `detail`, `value`, `href?`, `hint?`, `icon?` |

**Regra:** uma tela nova deve compor estes componentes. Se precisar de estilo próprio,
o correto é estender o componente compartilhado, não criar CSS na tela.

## 8. Estados semânticos

`statusTone()` em `lib/format.ts` traduz o status do backend em um tom visual. É
função pura e coberta por teste.

| Tom | Classe | Status cobertos |
|---|---|---|
| `positive` | `.status-positive` | APPROVED, CONFIRMED, ACCEPTED, PAID, FINISHED, CLOSED, READY, COMPLETED, ACTIVE |
| `danger` | `.status-danger` | REJECTED, REFUSED, DECLINED, CANCELLED, CANCELED, FAILED, EXPIRED |
| `warning` | `.status-warning` | UNDER_REVIEW, PENDING, REQUESTED, CANCELLATION_REQUESTED, AWAITING_DECISION |
| `info` | `.status-info` | PLANNING, IN_CAPTURE, IN_PROGRESS, SCHEDULE_FULL, OPEN, SUBMITTED |
| `neutral` | `.status-neutral` | DRAFT, INACTIVE e qualquer valor desconhecido ou nulo |

**Para adicionar um status:** incluir no mapa `statusTones` e cobrir com teste. Um
status não mapeado cai em `neutral` sem quebrar a interface.

## 9. Responsividade

Três faixas, cada uma com padrão próprio de navegação e de dados.

| Faixa | Dispositivo | Navegação | Tabelas | Grades |
|---|---|---|---|---|
| ≥ 64rem (1024px) | Desktop | Barra lateral completa, ícone + rótulo | Tabela | Múltiplas colunas |
| 48–64rem | Tablet | Trilho de ícones, rótulo em tooltip ao focar | Tabela com rolagem contida | Colunas reduzidas |
| < 48rem (768px) | Celular | Barra inferior flutuante, ícone + rótulo curto | **Cartões empilhados** | Coluna única |

**Transformação da tabela no celular.** Cabeçalho é ocultado e cada célula vira uma
linha rotulada, usando `content: attr(data-label)`. Por isso **toda célula precisa do
atributo `data-label`** — é o que preserva a legibilidade sem rolagem horizontal.

**Barra inferior.** Rolagem horizontal com `scroll-snap`, barra de rolagem oculta,
cada item com largura mínima de `--sidebar-collapsed`. Suporta os 9 itens do perfil
Advisory sem perder legibilidade.

## 10. Acessibilidade

| Item | Implementação |
|---|---|
| Página atual | `aria-current="page"` no item ativo da navegação |
| Alvo de toque | Mínimo `--touch-target` (2.75rem ≈ 44px) em todo controle |
| Foco visível | `--shadow-focus` via `:focus-visible`, nunca removido |
| Contraste | `--color-muted` ajustado para atender AA em texto pequeno |
| Movimento | `prefers-reduced-motion` neutraliza animações e deslocamentos |
| Carregamento | `aria-busy` e `role="status"` |
| Erro | `role="alert"` |
| Ícone decorativo | `aria-hidden` por padrão |
| Viewport | `100dvh` em vez de `100vh`, evitando corte sob a barra de endereço |

## 11. Mapa das seções do `styles.css`

| # | Seção | # | Seção |
|---|---|---|---|
| 1 | Base | 12 | Tabelas |
| 2 | Primitivo de ícone | 13 | Controles de ação |
| 3 | Shell da aplicação | 14 | Formulários |
| 4 | Barra lateral e navegação | 15 | Painéis e listas de registro |
| 5 | Topbar | 16 | Guests, viagem e portfólio |
| 6 | Títulos | 17 | Cartões de criação |
| 7 | Hero | 18 | Login |
| 8 | Cartões | 19 | Tablet — trilho de ícones |
| 9 | Atividade | 20 | Celular — barra inferior e empilhamento |
| 10 | Selos de estado | 21 | Preferência de movimento |
| 11 | Estados: vazio, carregando, erro | | |

## 12. Como estender

| Necessidade | Procedimento |
|---|---|
| Nova cor, espaço ou dimensão | Criar token em `tokens.css` na família correspondente |
| Novo ícone | Nome em `iconName.ts` e traço em `iconGlyphs.tsx` |
| Novo status | Adicionar ao mapa `statusTones` em `format.ts` e cobrir com teste |
| Nova tela | Compor `Sidebar`, `WorkspaceHeader`, `PageHeading` e os componentes de estado |
| Nova coluna de fila | Declarar em `content/dashboard.ts`; o `data-label` é gerado automaticamente |
| Novo cartão de workspace | Ícone em `workspaceCardIcon.ts` e texto em `workspaceCardHint.ts` |

## 13. Validação

Executar sempre dentro do container, nunca no host:

```bash
docker compose exec frontend npm run lint
docker compose exec frontend npm run typecheck
docker compose exec frontend npm test
```

**Atenção:** não executar `npm run build` enquanto o `npm run dev` estiver ativo no
mesmo container. Ambos usam o diretório `.next` e o build de produção substitui o
estado incremental do servidor de desenvolvimento, que passa a servir páginas
estáticas obsoletas. Caso ocorra, `docker compose restart frontend` restaura.

## 14. Pontos em aberto

- Homologação visual manual nos três perfis, em navegador real.
- Tema escuro: fora do escopo atual; a estrutura de tokens já o comporta.
- Skeleton de carregamento progressivo por tela.
- Revisão de contraste com ferramenta automatizada.
