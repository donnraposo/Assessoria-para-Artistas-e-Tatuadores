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

## ADR-018 — Camadas do frontend

**Decisão:** aplicar ao frontend a mesma separação da ADR-007. `lib/http` concentra o
cliente HTTP e a tradução de falhas, `lib/types` os contratos da API, `lib/services` um
serviço por módulo do backend, `lib/<módulo>` as regras de apresentação e validação, e
`components` apenas composição visual. Cada classe ocupa arquivo exclusivo.

**Motivo:** o cliente de API vinha crescendo como módulo único com tipos, transporte e
chamadas, e as telas repetiam tratamento de erro e mapeamento de dados.

**Consequência:** componentes não chamam `fetch` nem inspecionam código HTTP; o
tratamento de 404 e de sessão expirada pertence ao serviço e a `RequestFailure`. Regras
já garantidas pelo backend só são replicadas no frontend como orientação de interface,
nunca como autoridade.

**Data:** 2026-09-12.

## ADR-019 — Navegação por `Link`

**Decisão:** navegação interna entre telas usa o componente `Link` do Next.js.

**Motivo:** âncoras simples descartam o estado do cliente e recarregam a aplicação
inteira a cada troca de área, além de dispensarem o prefetch da rota.

**Consequência:** rotas internas novas devem ser declaradas na navegação por papel, não
em âncoras soltas dentro de componentes.

**Data:** 2026-09-12.

## ADR-020 — Aprovação e piso comercial como pré-condição da Proposta

**Decisão:** a Proposta de Guest só atinge `Pronta para confirmação` quando a candidatura
do Artista está aprovada e quando o valor mínimo da proposta é maior ou igual ao declarado
pelo Artista em seu perfil. A comparação vive em `ArtistCommercialFloor`, no domínio de
Guests, e é aplicada na criação e novamente na preparação.

**Motivo:** RN-005 determina que o cadastro, por si só, não autoriza o uso dos serviços, e
RN-016 e RN-017 tornam o valor declarado pelo Artista o piso da negociação. Sem o vínculo,
o piso podia ser rebaixado na origem e o fechamento validaria contra um mínimo já reduzido.

**Consequência:** o Artista continua sendo a autoridade sobre seu próprio piso; elevá-lo
invalida propostas ainda não confirmadas, que precisarão ser corrigidas antes de avançar.
Propostas já confirmadas preservam o snapshot, conforme RN-009.

**Data:** 2026-09-12.

## Processo de alteração

Uma decisão aceita somente poderá ser substituída após registro do contexto, alternativas, impacto, migração necessária e aprovação do usuário.
