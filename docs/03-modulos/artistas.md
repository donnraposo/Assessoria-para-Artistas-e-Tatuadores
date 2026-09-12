# Módulo de Artistas

## 1. Objetivo

Gerenciar candidatura, avaliação, perfil, portfólio, parâmetros comerciais e disponibilidade do Artista.

## 2. Funcionalidades iniciais

- Cadastro e envio para análise.
- Aprovação ou reprovação pela Assessoria.
- Perfil e portfólio.
- Disponibilidade por data e horário.
- Consulta de Guests, agenda, resultados e `Minha Viagem`.

## 3. Estado da implementação

- Perfil, candidatura, avaliação, portfólio e disponibilidade disponíveis na API.
- Jornada de candidatura e avaliação disponível na interface: o Artista preenche o perfil
  e envia, a Assessoria tria a fila, abre o detalhe e decide com motivo auditado.
- Intervenção excepcional da Assessoria na disponibilidade disponível na API, com motivo
  obrigatório e histórico auditado.
- A aprovação da candidatura passou a ser exigida para o Artista entrar em Proposta de Guest.
- Emissão de URL assinada do portfólio permanece pendente da escolha do provedor S3.

## 4. Regras relacionadas

RN-001 a RN-008 e RN-016 a RN-025.

## 5. Pontos em aberto

- Critérios eliminatórios e conteúdo exibido na reprovação.
- Reenvio após reprovação: hoje o envio exige rascunho, então uma candidatura reprovada
  não pode ser reenviada. A interface comunica o estado; a regra depende de decisão.
