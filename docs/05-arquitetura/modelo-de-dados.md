# Modelo de Dados

## 1. Entidades candidatas

- Usuário, papel e permissão.
- Artista, candidatura e portfólio.
- Studio, bancada, preço e disponibilidade.
- Proposta de Guest e Guest.
- Disponibilidade do Artista, reserva de Studio e agendamento.
- Campanha, métricas de Ads, Lead e fechamento.
- Registro financeiro, pagamento e custo.
- Viagem e acomodação.
- Histórico de alteração.

## 2. Relações centrais

- Um Artista pode ter vários Guests.
- Um Guest pode usar vários Studios por data e horário.
- Um Guest pode ter vários agendamentos e campanhas.
- Cada Guest possui uma moeda principal.

## 3. Pontos em aberto

- Atributos, cardinalidades, retenção, dados pessoais e estados persistidos.
