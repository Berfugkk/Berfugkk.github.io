Dicionário — catálogo estático

Este projeto agora inclui 3.502 entradas em 17 categorias. As primeiras entradas são o núcleo curado; a camada adicional amplia o catálogo com conceitos descritivos marcados como tal para não fingir que toda expressão é um lema fixo do idioma.

# Dicionário

Um dicionário exploratório em português brasileiro para sentimentos, emoções, estados mentais, relações humanas, experiências, sensações, memória, tempo, comportamentos e conceitos difíceis de explicar.

## Stack

- HTML5
- CSS3
- JavaScript puro
- Nenhum backend
- Nenhuma dependência de build
- `data.js` separado da interface

## Como executar

A forma mais simples: abra `index.html` no navegador.

Para usar as rotas limpas (`/palavras/saudade`, `/categoria/Sentimentos` etc.) localmente, use o servidor incluído:

```bash
python server.py
```

Depois abra `http://127.0.0.1:8765`.

Também é possível abrir `index.html` diretamente; nesse caso a navegação usa URLs com hash (`#/palavras/saudade`) para continuar funcionando sem servidor.

## Estrutura

```text
dicionario/
├── index.html
├── styles.css
├── app.js
├── data.js
├── README.md
├── server.py
└── assets/
```

## Conteúdo

O banco inicial contém 3.400 entradas distribuídas em 17 categorias, com 200 entradas por categoria. As definições e situações de reconhecimento foram escritas para este projeto; termos estrangeiros/contemporâneos são marcados na própria entrada.

### Adicionando palavras

Edite os arrays em `CATEGORY_CATALOGS` dentro de `data.js`. A interface gera automaticamente:

- página individual;
- categoria;
- busca por nome/definição/categoria/conexões;
- palavras relacionadas;
- contrastes;
- navegação anterior/próxima;
- histórico local.

Para entradas especialmente importantes, o objeto `polish` em `data.js` permite substituir definição, reconhecimento e relações com texto mais específico.

## Recursos

- busca global com suporte a frases;
- busca por nome, definição, categoria, relacionados e reconhecimento;
- botão “Me surpreenda”;
- rotas individuais;
- links entre palavras;
- histórico no navegador;
- copiar link;
- anterior/próxima com setas do teclado;
- menu lateral responsivo no celular;
- página Sobre;
- contador de entradas;
- suporte a `file://` e a hospedagem estática.

## Observações

O estilo foi desenvolvido a partir da linguagem visual de documentação técnica escura usada como referência, mas a identidade, textos, organização e componentes são próprios deste projeto.


## GitHub Pages

O projeto é estático e inclui `404.html` para preservar as rotas de palavras quando o site for publicado no GitHub Pages.

1. Suba o conteúdo desta pasta para um repositório.
2. Em **Settings → Pages**, selecione a branch e a pasta publicada.
3. Aguarde a publicação.

No GitHub Pages, a interface usa URLs com hash (`#/palavras/saudade`, `#/categoria/Sentimentos`) para evitar o 404 de SPA. O `404.html` também converte acessos diretos a rotas antigas/limpas para o fallback interno.
