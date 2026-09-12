# Backup e restauração

## Objetivo

Proteger o banco PostgreSQL e validar que os backups são restauráveis antes do lançamento.

## Política inicial

- Backup lógico diário com `pg_dump` no formato customizado.
- Criptografia e armazenamento fora do host da aplicação.
- Retenção sugerida: 7 diários, 4 semanais e 6 mensais.
- Acesso restrito à equipe técnica autorizada.
- Teste de restauração mensal em banco isolado.

## Procedimento

1. Gerar o backup com nome contendo data, ambiente e versão.
2. Validar que o arquivo não está vazio e registrar seu checksum SHA-256.
3. Criar um banco temporário isolado.
4. Restaurar com `pg_restore --clean --if-exists` exclusivamente nesse banco.
5. Executar `manage.py check`, migrations e smoke tests contra o banco restaurado.
6. Remover o banco temporário após registrar a evidência.

Nunca executar restauração sobre produção sem janela aprovada, backup prévio e confirmação explícita do banco-alvo.

