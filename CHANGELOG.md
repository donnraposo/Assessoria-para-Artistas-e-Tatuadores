# Changelog

Todas as alterações relevantes do projeto serão registradas neste arquivo.

## Não publicado

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
- Intervenção excepcional da Assessoria na disponibilidade do Artista (RN-008), com motivo obrigatório e auditoria dedicada.
- Auto-cadastro de Artista e Studio (RN-004 e RN-026), com atribuição de papel, validação de senha e login automático.

### Corrigido

- Criação do primeiro perfil de Artista (`PUT /api/v1/artists/me/`), que falhava com erro 500 por tentar gravar um registro em branco antes de aplicar os dados enviados.
