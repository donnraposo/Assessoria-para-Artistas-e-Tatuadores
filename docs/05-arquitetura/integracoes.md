# Integrações

## 1. Objetivo

Catalogar integrações externas sem tornar o núcleo do domínio dependente delas.

## 2. Futuras

### Armazenamento S3 — implementado

O portfólio usa contrato compatível com S3, bucket privado, upload direto por URL
assinada e acesso temporário. MinIO atende desenvolvimento; produção deve fornecer
endpoint e credenciais próprios de S3 ou R2.

### Google Calendar

Integração futura para sincronização de disponibilidade e agendamentos. A plataforma permanece como fonte oficial no MVP.

### Câmbio

Conversão automática é futura; o tratamento manual de outra moeda ainda precisa ser definido.

### Pagamentos

Não há gateway definido. Pagamentos externos são registrados operacionalmente quando aplicável.

## 3. Pontos em aberto

- Fornecedores, direção de sincronização, autenticação, falhas e conciliação.
