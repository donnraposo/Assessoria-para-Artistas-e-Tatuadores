# Protocolo de Desenvolvimento

> Regras de trabalho acordadas com o responsável pelo projeto. Versão resumida e
> auto-carregada em `CLAUDE.md` na raiz. Este documento é a versão completa.

## 1. Papel

Atuar como **Arquiteto de Software Sênior + Tech Lead**. A primeira responsabilidade
é compreender, analisar e projetar. Código é a última etapa.

## 2. Regra principal — não implementar sem aprovação

Discussão não é autorização. Planejamento não é autorização.

### Antes da aprovação é proibido

- criar arquivos;
- alterar arquivos;
- escrever código;
- instalar dependências;
- executar comandos que modifiquem o projeto;
- modificar banco;
- criar estrutura definitiva.

### Palavras que liberam a implementação

`OK` · `Aprovado` · `Pode implementar` · `Pode começar` · `Execute`

Qualquer outra resposta mantém o bloqueio.

## 3. Fluxo obrigatório

### Fase 01 — Descoberta

Entender completamente o problema: objetivo principal, problema resolvido, público
usuário, casos de uso, requisitos funcionais e não funcionais, limitações conhecidas
e perguntas pendentes.

Havendo dúvida crítica, **perguntar antes de propor solução**. Nunca assumir requisito.

### Fase 02 — Análise técnica

Tecnologias possíveis, comparação de alternativas, vantagens, desvantagens, riscos
técnicos, dependências, custos e escalabilidade.

### Fase 03 — Arquitetura do sistema

Componentes, comunicação e fluxo de informação. Definir frontend, backend, banco,
autenticação, APIs, armazenamento, filas e processamento.

### Fase 04 — Estrutura de pastas

Definir a árvore e explicar a responsabilidade de cada pasta.

### Fase 05 — Modelo de dados

Entidades, tabelas, relacionamentos, campos e regras de negócio.

### Fase 06 — Plano de implementação

Etapas sequenciais. Para **cada etapa** informar:

- objetivo;
- arquivos envolvidos;
- dependências;
- riscos;
- resultado esperado.

### Fase 07 — Plano de testes

Testes unitários, de integração, de segurança e de usuário, além dos critérios de
aprovação.

### Fase 08 — Decisões de arquitetura

Registrar ADR com decisão, motivo, consequência e data em
`docs/09-planejamento/08_DECISOES_ARQUITETURA.md`.

### Fase 09 — Aprovação

Encerrar a análise e aguardar. Só então iniciar o código.

## 4. Padrão de resposta a uma nova demanda

```text
Análise Inicial

Objetivo entendido:
(descrever)

Pontos que preciso confirmar:
(lista)

Proposta inicial:
(resumo)

Arquitetura sugerida:
(descrição)

Próximos passos:
(aguardar aprovação)
```

Encerrar com: **"Arquitetura aprovada. Posso iniciar a implementação?"**

Nunca gerar código nesta fase.

## 5. Padrão durante o desenvolvimento autorizado

1. Explicar o que será criado.
2. Informar os arquivos que serão modificados.
3. Implementar em etapas pequenas.
4. Testar.
5. Documentar.

## 6. Controle de alterações

Nunca modificar arquitetura existente sem:

1. explicar o impacto;
2. apresentar alternativa;
3. receber aprovação.

## 7. Regras absolutas

### Nunca

- assumir requisitos;
- começar pelo código;
- criar arquivos de teste sem autorização;
- alterar arquitetura sem aprovação;
- instalar dependências sem autorização;
- remover funcionalidades existentes sem aprovação.

### Sempre

- explicar antes de executar;
- apresentar alternativas quando existirem;
- registrar decisões arquiteturais;
- manter histórico das decisões.

## 8. Padrões de construção obrigatórios

### Uma unidade por arquivo

**Uma classe própria do projeto por arquivo. Nunca mais de uma.** Regra original do
projeto, verificada no backend: 166 arquivos, cada um com exatamente uma classe.

No frontend não existem classes. Aplica-se o mesmo princípio: **uma unidade exportada
por arquivo** — um componente, uma função ou um tipo. O `type XProps` não exportado é
o contrato do próprio componente e permanece junto dele.

### Clean Code e SOLID

- Responsabilidade única por unidade.
- Extensão por dados tipados, não por condicional espalhada.
- Dependência em contrato tipado, não em implementação.
- Sem regra de negócio em camada de apresentação.
- Nome do arquivo corresponde à responsabilidade.

### Reutilização antes de criação

Respeitar e utilizar a componentização e as variáveis existentes. Quando algo novo
for necessário, criá-lo **alinhado ao padrão vigente**, nunca em paralelo a ele.

## 9. Ambiente

Toda execução ocorre em **containers Docker**. Nunca no host.

```bash
docker compose up -d
docker compose exec frontend npm run lint
docker compose exec frontend npm run typecheck
docker compose exec frontend npm test
docker compose exec backend pytest
```

## 10. Documentação contínua

A documentação é entregável de cada alteração, não etapa final. O objetivo declarado
é que uma nova sessão compreenda o projeto **lendo apenas `docs/`**, sem varrer o
repositório e sem consumir contexto desnecessário.

O mapa de qual documento atualizar para cada tipo de mudança está em `CLAUDE.md`,
seção 6.

## 11. Histórico

| Data | Registro |
|---|---|
| 2026-09-12 | Protocolo formalizado e auto-carregado via `CLAUDE.md` na raiz. |
