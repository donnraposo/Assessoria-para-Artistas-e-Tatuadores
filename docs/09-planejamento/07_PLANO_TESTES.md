# Plano de Testes

## Estratégia

Priorizar regras de negócio, autorização, concorrência e consistência financeira. Todos os testes devem ser repetíveis em containers e independentes de serviços externos reais.

## Testes unitários

- Objetos de valor monetário, intervalos e estados.
- Transições de Proposta e Guest.
- Limites de negociação do Artista.
- Divisão financeira 20/80 e arredondamento.
- Conversão, CPL, custo por fechamento, ROAS e ocupação.
- Políticas de autorização puras.
- Regras de cancelamento já confirmadas.

## Testes de integração

- Repositórios com PostgreSQL real.
- Transações de fechamento e confirmação de agendamento.
- Restrições de conflito de agenda e reserva.
- Upload privado e geração de acesso temporário.
- Autenticação, renovação ou encerramento de sessão.
- Auditoria de alterações administrativas.
- Tarefas assíncronas com adaptadores substituídos em testes.

SQLite não substituirá PostgreSQL nos testes de comportamento transacional.

## Testes de API

- Contratos OpenAPI e validação de entrada.
- Paginação, filtros, ordenação e erros padronizados.
- Idempotência em operações críticas.
- Respostas para transições inválidas.
- Matriz de acesso positiva e negativa por perfil.
- Garantia de que Studio não acessa Ads, Leads, faturamento ou receita da Assessoria.

## Testes de segurança

- Isolamento entre usuários do mesmo perfil.
- Escalada horizontal e vertical de privilégios.
- CSRF, cookies e política de CORS.
- Limites e conteúdo real de uploads.
- Ausência de segredos e dados sensíveis em logs.
- Dependências e imagens de container vulneráveis.
- Rate limiting nos endpoints de autenticação.

## Testes de concorrência

- Duas tentativas simultâneas sobre o mesmo intervalo do Artista.
- Duas reservas concorrentes para a última bancada disponível.
- Confirmações repetidas do mesmo recebimento.
- Atualizações concorrentes de estado do Guest.

## Testes ponta a ponta

- Candidatura e aprovação do Artista.
- Cadastro e aprovação do Studio.
- Proposta, confirmação e evolução do Guest.
- Reserva de Studio pela plataforma e registro externo.
- Lead, recebimento dos 20%, fechamento e agendamento.
- Consulta de resultados e `Minha Viagem` pelo Artista.
- Solicitação de cancelamento pelo Artista.

## Testes de usuário

- Sessões de aceite com representantes da Assessoria, Artista e Studio.
- Verificação de clareza dos estados e das pendências.
- Validação de responsividade, navegação por teclado e mensagens de erro.
- Confirmação de que cada perfil visualiza somente o necessário.

## Critérios de aprovação

- Testes automatizados críticos aprovados.
- Nenhum defeito crítico ou alto aberto.
- Nenhum acesso indevido conhecido.
- Fluxo completo do Guest executado em homologação.
- Conflitos simultâneos bloqueados no banco.
- Cálculos financeiros e indicadores conferidos com exemplos de referência.
- Backup restaurado com sucesso antes do lançamento.
- Critérios de aceite vinculados à matriz de rastreabilidade.

## Evidências

O pipeline deve preservar resultados dos testes, cobertura como indicador auxiliar, relatório de segurança e evidências dos testes ponta a ponta. Cobertura numérica isolada não substitui cenários relevantes.

