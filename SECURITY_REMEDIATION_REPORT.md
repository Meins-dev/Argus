# Relatório de correção de segurança

**Data:** 2026-10-03
**Projeto:** Argus (checkout `e2fff67`, correções ainda locais)
**Escopo:** revisão de código e dependências, testes selecionados da API e build do frontend.

## Achados críticos corrigidos

1. **Execução arbitrária de código no modo hospedado.** `code_helper` estava exposto pela lista `CLOUD_SAFE_ACTIONS`, embora seu fluxo possa executar código gerado. Removi a ferramenta dessa lista; a proteção do executor hospedado também rejeita ações fora dela. A implementação local/desktop permanece disponível. Acrescentei uma regressão que verifica que a API hospedada não anuncia `code_helper`.

2. **Next.js vulnerável a três RCEs críticas.** O lockfile tinha Next.js 16.3.1, faixa afetada pelas falhas em servidores Windows, otimização AVIF e `next/og ImageResponse`. Fixei Next.js em 16.3.8 e atualizei `package-lock.json`. As versões corrigidas publicadas pelos mantenedores começam em 16.3.3 ou 16.3.6, conforme a falha ([advisórios oficiais do Next.js](https://github.com/vercel/next.js/security/advisories)). O `npm audit` após a atualização reporta **0 críticas**.

## Validação

- `npm ci --ignore-scripts`: concluído.
- `npm run typecheck`: concluído.
- `npm run build`: concluído com Next.js 16.3.8.
- `npm audit --omit=dev`: **0 vulnerabilidades** nas dependências de produção.
- `npm audit`: **0 críticas; 7 altas**, limitadas ao conjunto de ferramentas de desenvolvimento/lint.
- `HostedApiTests.test_status_and_cloud_actions_are_authenticated`: passou, incluindo a nova asserção para `code_helper`.
- A suíte `test_hosted_api.py`: 6 de 7 testes passaram. O WebSocket ainda falha porque remove oito caracteres do prefixo `Argus: `, que tem sete, resultando em `cho:` em vez de `Echo:`. É um defeito funcional fora dos achados críticos desta correção.
- `git diff --check`: passou.

## Itens de segurança ainda pendentes

Os itens abaixo não foram classificados como críticos nesta revisão e não foram alterados:

- SSRF possível ao fornecer URLs a `create_presentation` (o fetch aceita endereços privados e segue redirecionamentos).
- Logout não invalida imediatamente o token já emitido; o prazo padrão observado é de 24 horas.
- `open_app` usa `shell=True` no Windows com o nome de aplicativo recebido.
- A validação de `JWT_SECRET` não impõe entropia mínima forte.
- O frontend mantém sete avisos altos em dependências de desenvolvimento. As dependências de produção passaram em `npm audit --omit=dev`.
- As dependências Python não têm lockfile. O scan consultou dependências diretas e reportou advisórios condicionais para `cryptography==48.0.0` em Darwin com Python >=3.14; dependências transitivas não puderam ser confirmadas.
- A licença MIT e variáveis locais de trial/bloqueio não constituem, por si só, um serviço de licenciamento comercial com validação confiável no servidor. O modelo de licenciamento ainda precisa ser projetado antes da comercialização.

## Limitações

Não foi possível executar DAST contra uma implantação: o Docker daemon não estava acessível no ambiente. A revisão não equivale a uma certificação ou pentest externo. A cópia de trabalho corrigida está em `Documentos/Argus`; o site institucional em `Documentos/argus` não foi alterado e suas mudanças locais foram preservadas.
