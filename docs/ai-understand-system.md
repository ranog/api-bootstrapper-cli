# AI Understand System

Este documento padroniza como pedir ao agente uma análise arquitetural completa de um projeto.

Execução oficial para agentes: `$api-bootstrapper-understand-system`.

Use este guia quando precisar entender um sistema antes de implementar mudanças, revisar código ou planejar refatorações.

## Quando usar

- onboarding em um projeto novo
- investigação de fluxo de execução
- mapeamento de responsabilidades por camada
- preparação para mudanças com risco arquitetural

## Prompt completo (análise arquitetural)

Use este prompt quando quiser uma análise detalhada e estruturada.

```text
Leia a documentação disponível (README, docs e comentários no código) e explore a estrutura do projeto.

Explique de forma clara e estruturada como a arquitetura do sistema está organizada, incluindo:

1. Estrutura geral do projeto
- principais diretórios e seus papéis
- como o código está organizado (camadas, módulos, packages)

2. Ponto de entrada
- onde a aplicação inicia (ex: main.py, cli, server)
- como o sistema é executado

3. Responsabilidades por camada
- controllers / handlers / endpoints
- services / use cases / regras de negócio
- repositories / adapters / acesso a dados
- modelos / schemas / entidades

4. Fluxo de execução
- descreva o fluxo de uma operação típica (ex: request HTTP, comando CLI, job async)
- desde a entrada até a persistência ou saída

5. Integrações externas
- bancos de dados
- filas / mensageria
- APIs externas
- como essas integrações são abstraídas

6. Gerenciamento de estado e dados
- onde e como os dados são armazenados
- como ocorre persistência e leitura

7. Configuração e ambiente
- como variáveis de ambiente são usadas
- como o projeto é configurado para diferentes ambientes

8. Padrões arquiteturais utilizados
- ex: MVC, Clean Architecture, Hexagonal, Event-driven, etc
- como esses padrões aparecem no código

9. Concorrência / processamento assíncrono (se existir)
- uso de filas, workers, async/await, jobs
- como o sistema escala

10. Testes
- como os testes estão organizados
- tipos de testes (unitários, integração, e2e)

11. Pontos críticos
- possíveis gargalos
- acoplamentos fortes
- riscos técnicos

12. Resumo final
- explique a arquitetura em poucas linhas
- destaque os principais trade-offs

Se possível, utilize exemplos reais do código para ilustrar cada ponto.
```

## Prompt rápido (modo copilot)

Use este prompt quando quiser uma leitura mais objetiva.

```text
Analise este projeto e explique sua arquitetura.

Descreva:
- estrutura de diretórios
- ponto de entrada
- responsabilidades por camada (controllers, services, repositories, etc)
- fluxo de execução de uma operação principal
- integrações externas (DB, APIs, filas)
- padrões arquiteturais utilizados
- como o sistema lida com concorrência/async
- como os testes estão organizados

Finalize com um resumo simples da arquitetura e possíveis pontos de melhoria.
```

## Dicas de aprofundamento

Para elevar a análise para nível sênior, peça ao agente também:

- sugestões de desacoplamento e modularização
- identificação de gargalos e pontos de falha
- trade-offs de escalabilidade, manutenção e evolução futura
