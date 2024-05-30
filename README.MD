# Integracao-ChatGPT

Este projeto integra o ChatGPT com uma aplicação web utilizando Flask no backend e uma interface simples em HTML e JavaScript.

## Descrição

O projeto cria um assistente (assistant) usando a API da OpenAI e para cada interação com o usuário, cria uma nova thread para gerenciar a conversa. A estrutura do projeto é composta por um servidor Flask que gerencia as requisições e uma interface web que permite ao usuário interagir com o assistente.

## Funcionalidades

- Criação de um assistente ao iniciar o servidor.
- Criação de uma nova thread para cada interação do usuário.
- Adição de mensagens a threads existentes.
- Execução do assistente para responder às mensagens do usuário.

## Estrutura do Projeto

- `servidor.py`: Arquivo principal do servidor Flask que gerencia as requisições e interações com a API da OpenAI.
- `static/`: Pasta contendo arquivos estáticos, como HTML, CSS e JavaScript.

## Melhorias
Agora pode reaproveitar um ID de um Assistant já criado, evitando que toda vez que inicia o servidor, ele crie um novo Assistant desnecessario, basta colocar o ID do Assistant na pasta `assistant_id.txt`.

`prompt.tx` - Para melhor legibilidade do codigo, o prompt completo pode ser escrito nesse arquivo, e sendo usado na linha 36 de `servidor.py`.
