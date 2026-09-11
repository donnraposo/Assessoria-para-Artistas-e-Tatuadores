# Arquitetura do Sistema

## 1. Objetivo

Definir a arquitetura técnica após a consolidação do MVP.

## 2. Contextos de domínio

- Identidade e acesso.
- Artistas.
- Guests.
- Studios e reservas.
- Agenda e fechamentos.
- Marketing e Ads.
- Financeiro.
- Logística.
- Administração e auditoria.

## 3. Princípios iniciais

- Separação de responsabilidades por domínio.
- Guest como agregador operacional, sem misturar entidades distintas.
- Agenda interna como fonte oficial no MVP.
- Integrações externas desacopladas.
- Valores monetários sempre acompanhados de moeda.

## 4. Pontos em aberto

- Stack, implantação, autenticação, observabilidade e estratégia de integração.
