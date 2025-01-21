# plataforma-hackathon

## Intro
Esse prjeto foi criado como a intenção de ser educativo e realizado com 3 times diferentes, cada um lidando com uma parte do projeto.

## Parte 1: Customer e Products (nível básico)
### Customer - Time 1
Precisa deixar o projeto funcionando para seus clientes, existem vários pontos que devem ser implementados no código para que ele atenda as chamadas

Vocês serão responsáveis por entregar os dados de produtos para a aplicação de Orders.
```mermaid
---
title: Serviço de Customer
---
graph LR
C-API{{Customer API}} --> C-SVC[[Customer Service]]
C-DOMAIN([Customer Domain]) --> C-SVC
C-DOMAIN --> C-API
C-DOMAIN --> C-DB
C-DB[(Customer Storage)] --> C-SVC
```

### Products - Time 2
Muito parecido com o projeto de Customer, é preciso implementar parte das integrações com SQL, melhorar alguns pontos, todos descritos no começo de cada arquivo fonte. 

Vocês serão responsáveis por entregar os dados de produtos para a aplicação de Orders.

```mermaid
---
title: Serviço de Products
---
graph LR
P-API{{Products API}} --> P-SVC[[Products Service]]
P-DOMAIN([Products Domain]) --> P-SVC
P-DOMAIN --> P-API
P-DOMAIN --> P-DB
P-DB[(Products Storage)] --> P-SVC
```

## Parte 2: Orders (nível intermediário)
Nesse projeto além de ter que implementar alguns pontos que estão faltando, ainda é preciso consumnir dados dos outros dois projetos, Customer e Products. Sem eles, essa API não vai funcionar corretamente.

```mermaid
---
title: Serviço de Orders
---
graph LR
O-API{{Orders API}} --> O-SVC[[Orders Service]]
O-DOMAIN([Orders Domain]) --> O-SVC
O-DOMAIN --> O-API
O-DOMAIN --> O-DB
O-DB[(Orders Storage)] --> O-SVC
O-SVC --> O-CUS-CLI>Customer Client]
O-SVC --> O-PRO-CLI>Products Client]
O-CUS-CLI --> O-CUS-CLI-CACHE[(Customer Cache)]
O-PRO-CLI --> O-PRO-CLI-CACHE[(Products Cache)]
O-PRO-DOM([Products Client Domain]) --> O-CUS-CLI
O-CUS-DOM([Customer Client Domain]) --> O-PRO-CLI
```


## Visão geral

```mermaid
---
title: Diagrama de integração
---
graph LR
O-API{{Orders API}} --> O-SVC[[Orders Service]]
O-DOMAIN([Orders Domain]) --> O-SVC
O-DOMAIN --> O-API
O-DOMAIN --> O-DB
O-DB[(Orders Storage)] --> O-SVC
O-SVC --> O-CUS-CLI>Customer Client]
O-SVC --> O-PRO-CLI>Products Client]

O-CUS-CLI --> O-CUS-CLI-CACHE[(Customer Cache)]
O-CUS-DOM([Customer Client Domain]) --> O-PRO-CLI

O-PRO-CLI --> O-PRO-CLI-CACHE[(Products Cache)]
O-PRO-DOM([Products Client Domain]) --> O-CUS-CLI
O-CUS-CLI --> C-API{{Customer API}}
O-PRO-CLI --> P-API{{Products API}}
C-API --> C-SVC[[Customer Service]]
P-API --> P-SVC[[Products Service]]
C-SVC --> C-DB[(Customer Storage)]
C-DOMAIN([Customer Domain]) --> C-SVC
C-DOMAIN --> C-API
C-DOMAIN --> C-DB
P-SVC --> P-DB[(Products Storage)]
P-DOMAIN([Products Domain]) --> P-SVC
P-DOMAIN --> P-API
P-DOMAIN --> P-DB
```
