# Atria — Diretrizes Permanentes do Projeto

> Este arquivo é carregado automaticamente no início de toda sessão.
> Ele é a fonte das regras de trabalho. Leia-o antes de qualquer ação.

## 0. Leia a documentação, não o código

Para entender o projeto, **consulte `docs/` — não varra o repositório**. A
documentação é mantida atualizada a cada alteração exatamente para evitar isso.

| Preciso entender | Leia |
|---|---|
| O que é o produto, regras de negócio | `docs/00-visao-geral/`, `docs/01-negocio/regras-de-negocio.md` |
| Arquitetura e decisões | `docs/09-planejamento/03_ARQUITETURA_SISTEMA.md`, `08_DECISOES_ARQUITETURA.md` |
| Estrutura de pastas e convenções | `docs/09-planejamento/04_ESTRUTURA_PROJETO.md` |
| Modelo de dados | `docs/09-planejamento/05_MODELO_DADOS.md` |
| Contrato da API | `docs/06-api/especificacao-api.md` |
| **Frontend: tokens, componentes, responsividade** | **`docs/07-ux-ui/design-system.md`** |
| Estado atual e o que falta | `docs/09-planejamento/09_PLANO_EXECUCAO_DETALHADO.md` |
| O que mudou e quando | `docs/CHANGELOG.md` |
| Protocolo de trabalho detalhado | `docs/11-processo/protocolo-de-desenvolvimento.md` |

## 1. MODO ARQUITETO — regra principal

**Não implementar sem aprovação.** Discutir não é autorizar. Planejar não é autorizar.

Antes de aprovação explícita é **proibido**: criar arquivos, alterar arquivos,
escrever código, instalar dependências, executar comandos que modifiquem o projeto,
alterar o banco.

Só iniciar desenvolvimento após o usuário responder claramente: **OK**, **Aprovado**,
**Pode implementar**, **Pode começar** ou **Execute**.

### Fluxo obrigatório

1. **Descoberta** — entender objetivo, usuários, casos de uso, requisitos, restrições,
   riscos, dependências e lacunas.
2. **Análise técnica** — alternativas, vantagens, desvantagens, riscos, custos.
3. **Arquitetura** — componentes, comunicação, fluxo de dados.
4. **Estrutura** — pastas e responsabilidades.
5. **Modelo de dados** — entidades, relacionamentos, regras.
6. **Plano de implementação** — etapas com objetivo, arquivos, dependências e riscos.
7. **Plano de testes** — unitário, integração, segurança, usuário, critérios.
8. **Decisões** — registrar ADR.
9. **Aprovação** — encerrar perguntando e aguardar.

Havendo dúvida crítica, **perguntar antes de propor solução**.

### Padrão de resposta a uma nova demanda

```text
Análise Inicial
Objetivo entendido:
Pontos que preciso confirmar:
Proposta inicial:
Arquitetura sugerida:
Próximos passos: (aguardar aprovação)
```

Encerrar com: **"Arquitetura aprovada. Posso iniciar a implementação?"**

## 2. Regras absolutas

**Nunca:**
- assumir requisitos;
- começar pelo código;
- criar testes sem autorização;
- alterar arquitetura existente sem explicar impacto, apresentar alternativa e obter aprovação;
- instalar dependências sem autorização;
- remover funcionalidade existente sem aprovação.

**Sempre:**
- explicar antes de executar;
- informar quais arquivos serão modificados;
- implementar em etapas pequenas;
- testar;
- documentar;
- registrar decisões arquiteturais e manter o histórico.

## 3. Clean Code e SOLID

Obrigatórios em tudo que for escrito, conforme ADR-007.

- **Uma classe própria do projeto por arquivo. Nunca mais de uma.**
  No frontend, onde não há classes, vale a mesma ideia: **uma unidade exportada por
  arquivo** — um componente, uma função, um tipo. O `type XProps` não exportado é o
  contrato do próprio componente e permanece junto dele.
- Nome do arquivo corresponde à responsabilidade da unidade.
- Sem regra de negócio em views, serializers, signals, tarefas assíncronas ou
  componentes de apresentação.
- Camadas internas não importam a camada de apresentação.
- Casos de uso delimitam transação e orquestram dependências.
- `__init__.py` não esconde dependência com reexportação extensa.
- Extensão por dados tipados (mapas `Record<Chave, Valor>`), não por condicional
  espalhada.

## 4. Frontend — componentização e variáveis

**Respeitar e reutilizar o que já existe.** Ao precisar de algo novo, criar seguindo
o padrão vigente — nunca em paralelo a ele.

- Todo valor visual vem de token em `frontend/src/app/tokens.css`. **Zero valor
  mágico no CSS** (ADR-012).
- Token novo entra na família existente, seguindo a mesma convenção de nome.
- Tela nova compõe os componentes compartilhados (`Sidebar`, `WorkspaceHeader`,
  `PageHeading`, `StatusBadge`, `EmptyState`, `LoadingScreen`, `ErrorScreen`,
  `QueueCard`). Tela não declara estilo próprio.
- Ícone novo entra em `components/iconGlyphs.tsx` e no tipo `components/iconName.ts`.
- Status novo entra no mapa de `lib/format.ts` e recebe teste.
- Idioma da interface e das mensagens da API: **inglês** (ADR-013).
  Documentação interna: **português**.
- Detalhes completos em `docs/07-ux-ui/design-system.md`.

## 5. Execução — tudo em containers Docker

Nunca executar no host. Serviços: `postgres`, `backend`, `frontend`, `minio`.

```bash
docker compose up -d
docker compose exec frontend npm run lint
docker compose exec frontend npm run typecheck
docker compose exec frontend npm test
docker compose exec backend pytest
docker compose exec backend python manage.py migrate
```

**Armadilha conhecida:** não rodar `npm run build` enquanto o `npm run dev` estiver
ativo no mesmo container. Ambos usam `.next`; o build de produção substitui o estado
incremental e o dev server passa a servir páginas estáticas obsoletas. Recuperação:
`docker compose restart frontend`.

## 6. Documentação é entregável, não etapa final

Toda alteração atualiza a documentação na mesma entrega, de modo que uma nova sessão
entenda o projeto **sem ler código**.

| Mudou | Atualize |
|---|---|
| Qualquer coisa | `docs/CHANGELOG.md` |
| Decisão de arquitetura | `docs/09-planejamento/08_DECISOES_ARQUITETURA.md` |
| Token, componente, classe CSS, responsividade | `docs/07-ux-ui/design-system.md` |
| Endpoint | `docs/06-api/especificacao-api.md` |
| Entidade ou campo | `docs/09-planejamento/05_MODELO_DADOS.md` |
| Regra de negócio | `docs/01-negocio/regras-de-negocio.md` |
| Progresso de sprint | `docs/09-planejamento/09_PLANO_EXECUCAO_DETALHADO.md` |
| Dívida técnica identificada | `docs/08-roadmap/backlog.md` |

## 7. Gate por tarefa

1. Regra e critério de aceite identificados.
2. Contrato e autorização definidos.
3. Migration revisada, quando aplicável.
4. Implementação pequena e coesa.
5. Testes proporcionais ao risco.
6. Lint, tipos, testes e build aprovados **dentro do container**.
7. OpenAPI, rastreabilidade, ADR e changelog atualizados.
8. Evidência de homologação registrada.
