# Modelo de Dados

## Princípios

- PostgreSQL como fonte transacional oficial.
- UUID para identificadores públicos.
- Integridade reforçada por chaves, restrições e transações.
- Dinheiro armazenado como decimal acompanhado de moeda ISO 4217.
- Datas persistidas em UTC; fuso operacional registrado quando relevante.
- Histórico financeiro não muda retroativamente.
- Dados pessoais e comerciais expostos pelo menor privilégio.

## Entidades iniciais

### Identidade

- `User`: id, e-mail, senha, estado, último acesso e datas de controle.
- `Role`: papel de Artista, Studio ou Assessoria.
- `UserRole`: associação entre usuário, papel e escopo.
- `InternalPermission`: permissões e alçadas internas, após definição do negócio.

### Artistas

- `Artist`: usuário, dados pessoais e profissionais, experiência, estado e parâmetros comerciais.
- `ArtistApplication`: envio, estado, parecer, responsável e datas.
- `PortfolioItem`: artista, arquivo, descrição, estilo, ordem e visibilidade.
- `ArtistAvailability`: artista, início, fim, fuso e estado.

### Studios

- `Studio`: conta, nome, localização, estrutura, estado de aprovação e acomodação disponível.
- `StudioApplication`: envio, avaliação, responsável e parecer.
- `Workstation`: Studio, identificação, capacidade e estado.
- `StudioPrice`: modalidade, valor, moeda, vigência e condições.
- `StudioAvailability`: Studio ou bancada, início, fim e capacidade.
- `StudioBookingRequest`: Guest, Studio, período, estado e resposta.
- `StudioBooking`: solicitação, Guest, período, confirmação e pagamento operacional.

### Guests

- `GuestProposal`: artista, cidade, período, moeda principal, Ads, valores, estado e versão.
- `Guest`: proposta confirmada, artista, localidade, período, moeda, estado e fuso.
- `GuestStudio`: Guest, Studio, período e condições operacionais.
- `GuestGoal`: metas opcionais de ocupação e faturamento.

Proposta e Guest permanecerão separados para preservar o histórico do planejamento confirmado.

### Agenda e vendas

- `Appointment`: Guest, artista, cliente externo, início, fim, valor, moeda e estado.
- `Lead`: Guest, referência externa, origem, dados mínimos permitidos e datas.
- `Closing`: Lead, Appointment, valor final, moeda, data e responsável.
- `AgencyReceipt`: Closing, valor de 20%, estado, referência e confirmação.
- `CancellationRequest`: alvo, solicitante, responsabilidade, motivo e estado.

O agendamento somente alcança o estado confirmado quando o recebimento de 20% for confirmado na mesma operação transacional.

### Marketing

- `Campaign`: Guest, canal, orçamento autorizado, período e estado.
- `AdSpend`: campanha, valor, moeda, período e origem do registro.
- Métricas como conversão, CPL, custo por fechamento, ROAS e ocupação serão calculadas, não duplicadas como entrada manual.

### Financeiro

- `FinancialEntry`: Guest, tipo, beneficiário, valor, moeda, competência, estado e referência de origem.
- `GuestCost`: Guest, categoria, valor, moeda, responsável e estado.
- O valor da Assessoria será 20% do fechamento; 80% será saldo previsto do Artista até confirmação externa.

### Logística

- `Travel`: Guest, tipo, origem, destino, datas, estado, custo e referência externa.
- `Accommodation`: Guest, Studio opcional, período, endereço, estado e custo.
- `TravelUpdate`: item logístico, mensagem, responsável e data.

### Auditoria e notificações

- `AuditEvent`: ator, ação, recurso, identificador, antes/depois permitido, motivo e data.
- `Notification`: destinatário, categoria, canal, estado e data.

## Relacionamentos centrais

```text
Artist 1 ── N GuestProposal 1 ── 0..1 Guest
Guest 1 ── N GuestStudio N ── 1 Studio
Guest 1 ── N Appointment
Guest 1 ── N Campaign ── N AdSpend
Lead 1 ── 0..1 Closing 1 ── 1 AgencyReceipt
Guest 1 ── N FinancialEntry
Guest 1 ── N Travel
Guest 1 ── N Accommodation
```

## Restrições críticas

- E-mail de usuário único após normalização.
- Apenas Studios aprovados podem ser associados a novos Guests.
- Intervalos devem possuir fim posterior ao início.
- Reservas e agendamentos incompatíveis do mesmo Artista devem ser impedidos.
- Guest possui exatamente uma moeda principal antes da confirmação.
- Não somar moedas distintas sem conversão registrada.
- Transições de estado passam por casos de uso autorizados.
- Alteração excepcional da disponibilidade exige ator e motivo.

## Pendências antes das migrations definitivas

- Dados mínimos do cliente externo e base legal de tratamento.
- Políticas de cancelamento e retenção.
- Estrutura exata de endereços internacionais.
- Subpapéis da Assessoria.
- Regras para valores em moeda secundária.
- Campos obrigatórios de viagem, acomodação e comprovantes.

