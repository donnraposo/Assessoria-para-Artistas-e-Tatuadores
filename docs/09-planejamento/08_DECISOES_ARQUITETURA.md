# Decisões de Arquitetura

## ADR-001 — Backend Django

**Decisão:** utilizar Python, Django e Django REST Framework.

**Motivo:** produtividade, segurança, ORM relacional, ecossistema maduro e suporte administrativo adequado ao MVP.

**Consequência:** regras devem permanecer fora de views e serializers para não acoplar o domínio ao framework.

**Data:** 2026-09-11.

## ADR-002 — Monólito modular

**Decisão:** iniciar com um único backend implantável, separado internamente por módulos de domínio.

**Motivo:** reduzir custo operacional e preservar consistência transacional sem impedir evolução.

**Consequência:** módulos não podem acessar detalhes internos uns dos outros; comunicação passa por contratos e casos de uso explícitos.

**Data:** 2026-09-11.

## ADR-003 — PostgreSQL

**Decisão:** adotar PostgreSQL como banco oficial.

**Motivo:** integridade relacional, transações, restrições e controle de concorrência necessários para agenda e finanças.

**Consequência:** testes de integração usarão PostgreSQL, não SQLite como substituto comportamental.

**Data:** 2026-09-11.

## ADR-004 — REST e OpenAPI

**Decisão:** expor API REST versionada e documentada por OpenAPI.

**Motivo:** contrato simples, interoperável e capaz de gerar cliente tipado para o frontend.

**Consequência:** mudanças incompatíveis exigem estratégia explícita de versionamento.

**Data:** 2026-09-11.

## ADR-005 — Next.js e TypeScript

**Decisão:** utilizar Next.js no frontend web responsivo.

**Motivo:** tipagem, organização por funcionalidades e experiência adequada às áreas de Artista, Studio e Assessoria.

**Consequência:** Django permanece autoridade do domínio e da identidade; frontend não duplica regras críticas.

**Data:** 2026-09-11.

## ADR-006 — Docker

**Decisão:** containerizar frontend, backend e workers, usando Docker Compose no desenvolvimento.

**Motivo:** reprodutibilidade e paridade entre ambientes.

**Consequência:** PostgreSQL deve ser gerenciado em produção; segredos não entram nas imagens; containers executam com menor privilégio.

**Data:** 2026-09-11.

## ADR-007 — Clean Architecture, SOLID e uma classe por arquivo

**Decisão:** organizar cada módulo nas camadas de domínio, aplicação, infraestrutura e apresentação; cada classe própria do projeto terá arquivo exclusivo.

**Motivo:** explicitar responsabilidades, reduzir acoplamento e facilitar testes e evolução.

**Consequência:** abstrações serão criadas somente em fronteiras úteis para evitar complexidade cerimonial. Migrações geradas seguem o padrão do Django.

**Data:** 2026-09-11.

## ADR-008 — Armazenamento de arquivos

**Decisão:** manter arquivos em serviço compatível com S3, privados por padrão, e somente metadados no PostgreSQL.

**Motivo:** escalabilidade, controle de acesso e separação entre dados transacionais e binários.

**Consequência:** ambiente local poderá usar MinIO; produção usará S3 ou R2 conforme decisão de infraestrutura.

**Data:** 2026-09-11.

## ADR-009 — Processamento assíncrono sob demanda

**Decisão:** introduzir Celery e Redis somente quando houver casos de uso assíncronos implementados.

**Motivo:** evitar infraestrutura prematura sem bloquear e-mails, notificações e rotinas futuras.

**Consequência:** confirmações financeiras e de agenda permanecem síncronas e transacionais.

**Data:** 2026-09-11.

## ADR-010 — Dinheiro e tempo

**Decisão:** usar decimal com moeda obrigatória; armazenar instantes em UTC e preservar o fuso operacional quando necessário.

**Motivo:** impedir cálculos imprecisos, soma indevida de moedas e ambiguidades de agenda.

**Consequência:** conversão cambial somente ocorrerá mediante taxa e origem registradas em evolução aprovada.

**Data:** 2026-09-11.

## ADR-011 — Autorização em múltiplas dimensões

**Decisão:** combinar papéis, propriedade do recurso e escopo operacional.

**Motivo:** os três perfis possuem limites diferentes e o Studio não pode visualizar dados comerciais privados.

**Consequência:** cada endpoint e caso de uso crítico terá testes positivos e negativos de acesso.

**Data:** 2026-09-11.

## ADR-012 — Design tokens e componentes configuráveis

**Decisão:** estilos reutilizáveis serão derivados de variáveis CSS centralizadas; componentes receberão conteúdo, estado e variações por propriedades ou estruturas tipadas.

**Motivo:** garantir consistência visual, manutenção simples, temas futuros e reutilização.

**Consequência:** cores, tipografia, espaçamento, raios, sombras e movimento devem nascer como tokens semânticos; valores operacionais não ficarão fixos dentro de componentes reutilizáveis.

**Data:** 2026-09-11.

## ADR-013 — Idioma da aplicação

**Decisão:** todo conteúdo visível da aplicação, incluindo mensagens da API, será escrito em inglês. A documentação interna permanece em português.

**Data:** 2026-09-11.

## ADR-014 — Cálculo e ausência de métricas

**Decisão:** indicadores serão calculados a partir dos registros operacionais. Conversão representa fechamentos sobre Leads e ROAS representa faturamento vendido sobre gasto em Ads. Quando o denominador for zero, o indicador será retornado como `null`.

**Motivo:** impedir duplicidade de entrada e evitar resultados matematicamente enganosos.

**Data:** 2026-09-11.

## ADR-015 — Documentos logísticos privados

**Decisão:** persistir somente a chave privada do documento. Respostas comuns da API expõem apenas a existência do documento, nunca sua chave ou URL pública.

**Motivo:** reduzir exposição de passagens, reservas e dados pessoais.

**Data:** 2026-09-11.

## ADR-016 — Notificações persistentes sem broker no MVP

**Decisão:** armazenar notificações no PostgreSQL e processá-las por worker Django
independente, com idempotência e limite de três tentativas.

**Motivo:** oferecer recuperação de falha e rastreabilidade sem introduzir Redis e
Celery antes de existir volume ou latência que os justifique.

**Consequência:** a entrega não participa das transações críticas; o worker pode ser
substituído por uma fila dedicada sem alterar os casos de uso.

**Data:** 2026-09-11.

## ADR-017 — Dashboards segregados por papel

**Decisão:** manter dashboard global exclusivo da Assessoria e workspaces próprios
para Artista e Studio.

**Motivo:** impedir que indicadores comerciais e financeiros globais sejam expostos
a usuários externos.

**Consequência:** novas métricas exigem consulta com escopo explícito e teste negativo
de acesso antes de serem exibidas.

**Data:** 2026-09-11.

## ADR-018 — Direção visual editorial para tatuagem

**Decisão:** adotar identidade editorial urbana de alto contraste, com fotografia
original do processo artístico, navegação responsiva e componentes derivados de
tokens CSS semânticos.

**Motivo:** traduzir a linguagem visual de referência para o mercado de tatuagem sem
copiar marca, conteúdo ou elementos do produto automotivo original.

**Consequência:** as jornadas dos três perfis compartilham a mesma base visual; ativos
rasterizados do produto devem ser originais e mantidos no projeto.

**Data:** 2026-09-11.

## ADR-019 — Interface orientada a reconhecimento

**Decisão:** todo elemento interativo passa a comunicar sua função por ícone, rótulo
e estado simultaneamente. A numeração editorial usada na navegação (`01`, `02`) foi
substituída por ícones SVG inline, e os índices decorativos `A/01` do hero e do login
foram removidos.

**Motivo:** a numeração não comunicava função. Em telas de até 64rem os rótulos eram
ocultados e restavam apenas algarismos, tornando a navegação ininteligível em tablet.
Os índices decorativos ocupavam área nobre sem transmitir informação.

**Consequência:** `Icon.tsx` concentra o vocabulário visual, sem dependência externa.
Novos itens de navegação exigem ícone declarado; o tipo `IconName` garante cobertura
em tempo de compilação.

**Data:** 2026-09-12.

## ADR-020 — Cor como portadora de estado operacional

**Decisão:** o estado de um registro é comunicado por tom semântico derivado do
status, através da função pura `statusTone()`. Status desconhecido resolve para tom
neutro.

**Motivo:** o selo de estado era sempre âmbar, de modo que aprovado, rejeitado e
pendente tinham aparência idêntica. Os tokens semânticos já existiam, mas não eram
aplicados a estado.

**Consequência:** a leitura de uma fila deixa de exigir leitura textual célula a
célula. Novos status exigem mapeamento e teste; a ausência de mapeamento degrada
para neutro sem quebrar a interface.

**Data:** 2026-09-12.

## ADR-021 — Padrão responsivo por faixa, não por redução

**Decisão:** cada faixa de tela recebe um padrão próprio: barra lateral completa em
desktop, trilho de ícones com tooltip em tablet e barra inferior flutuante em celular.
Tabelas operacionais convertem-se em cartões empilhados abaixo de 48rem, usando o
atributo `data-label` de cada célula.

**Motivo:** a tabela possuía largura mínima de 46rem, forçando rolagem horizontal em
qualquer tela menor. As filas operacionais são a superfície mais usada pela Assessoria.

**Consequência:** toda célula de tabela operacional deve declarar `data-label`, pois
é ele que preserva a legibilidade no celular. Alvos de toque passam a observar o
mínimo de 2.75rem.

**Data:** 2026-09-12.

## Processo de alteração

Uma decisão aceita somente poderá ser substituída após registro do contexto, alternativas, impacto, migração necessária e aprovação do usuário.
