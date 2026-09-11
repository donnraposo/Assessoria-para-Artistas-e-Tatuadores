# Visão do Projeto

## Objetivo principal

Centralizar a operação da Assessoria para selecionar Artistas e Studios, planejar e executar Guests, captar e fechar clientes, controlar agenda, resultados, finanças e logística.

## Problema resolvido

A operação hoje depende de informações distribuídas entre conversas e ferramentas externas. A plataforma estabelecerá uma fonte operacional única, com responsabilidades, estados, indicadores e histórico claros.

## Usuários

- Artista: candidata-se, administra perfil e disponibilidade e acompanha Guests, agenda, resultados e viagem.
- Studio: mantém estrutura, preços e disponibilidade e responde a reservas.
- Assessoria/Administração: avalia cadastros e coordena toda a operação.
- Cliente final: participa da negociação e dos pagamentos, mas não possui acesso ao sistema.

## Casos de uso centrais

- Avaliar candidaturas de Artistas e Studios.
- Planejar, confirmar, acompanhar e finalizar um Guest.
- Controlar disponibilidade, reservas e conflitos de agenda.
- Registrar Leads, Ads, fechamentos e indicadores.
- Registrar o recebimento de 20% e calcular o saldo previsto de 80% do Artista.
- Organizar viagem, acomodação, Studios e custos em `Minha Viagem`.
- Auditar intervenções e alterações administrativas relevantes.

## Requisitos funcionais

Adotar RF-001 a RF-010 definidos em `docs/02-requisitos/requisitos-funcionais.md`, com prioridade para o ciclo completo do Guest.

## Requisitos não funcionais

- Isolamento de dados por perfil, organização e propriedade.
- Transações e restrições para preservar agenda e valores.
- Auditoria de ações administrativas relevantes.
- API versionada e documentada.
- Aplicação web responsiva e acessível.
- Ambientes reproduzíveis e containerizados.
- Backups, logs, monitoramento e recuperação compatíveis com o risco.
- Código modular, testável e orientado a Clean Architecture e SOLID.
- Uma classe própria do projeto por arquivo.

## Limitações conhecidas do MVP

- Sem área do Cliente final.
- Sem CRM comercial completo.
- Sem dependência do Google Calendar.
- Sem gateway para todos os pagamentos.
- Sem conversão cambial automática.
- Sem reserva automática de viagem ou acomodação.

## Perguntas pendentes

- Países, idiomas, moedas e fusos do lançamento.
- Papéis e alçadas internas da Assessoria.
- Políticas completas de cancelamento, remarcação e no-show.
- Retenção de dados, documentos obrigatórios e requisitos legais.
- Volume inicial, orçamento e provedor de infraestrutura.
- Regras definitivas para moeda secundária e custos adicionais.

