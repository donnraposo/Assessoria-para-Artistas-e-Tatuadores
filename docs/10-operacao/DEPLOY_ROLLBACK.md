# Implantação e rollback

## Implantação

1. Fixar versões das imagens e revisar variáveis obrigatórias, incluindo endpoint,
   bucket, região e credenciais S3 privadas.
2. Gerar e verificar backup do banco.
3. Construir as imagens de produção.
4. Aplicar migrations antes de liberar tráfego.
5. Verificar `/api/v1/health/`, `/api/v1/ready/`, autenticação e jornada crítica.
6. Liberar o frontend e acompanhar logs estruturados e indicadores.
7. Executar upload, leitura assinada e remoção de um objeto descartável de homologação.

## Rollback

- Reverter primeiro a imagem da aplicação para a versão anterior conhecida.
- Não reverter migrations destrutivas automaticamente.
- Quando houver incompatibilidade de esquema, executar o plano específico da migration aprovado antes da implantação.
- Restaurar banco somente como último recurso e após confirmação explícita do alvo.

## Critérios de interrupção

- Falha de autenticação ou autorização.
- Erro na confirmação transacional 20/80.
- Conflito de agenda não bloqueado.
- Indisponibilidade persistente do banco ou aumento relevante de erros HTTP 5xx.
- Bucket público, URL assinada inválida ou falha de remoção do armazenamento privado.
