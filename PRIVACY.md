# Política de privacidade do Argus

**Modelo de política, baseado no código em 2 de outubro de 2026. Precisa ser
revisado por um advogado antes de qualquer uso comercial.** Este documento
descreve o comportamento encontrado no repositório; não afirma que um serviço
hospedado específico esteja operando.

## Telemetria

O repositório não inclui SDK de analytics, telemetria de produto, coleta de
crash reports nem envio periódico de métricas. Não há telemetria de produto a
desativar. As chamadas normais a Gemini, pesquisa, e-mail e outros provedores
acontecem apenas quando o usuário inicia os recursos correspondentes; elas são
necessárias para esses recursos e não são analytics do Argus.

## Dados processados

### Aplicativo desktop

- Ao usar voz, texto, captura de tela, câmera, arquivos ou pesquisa, o conteúdo
  escolhido para a ação é enviado ao Gemini ou ao serviço externo daquela
  ação. Áudio de sessão Live é transmitido ao Gemini. O código não grava áudio
  em um arquivo nem em um banco de dados próprio.
- O usuário pode pedir ao assistente que guarde fatos em memória. A memória
  local fica em `memory/long_term.json` no diretório de dados do Argus, sem
  expiração automática; o código limita o arquivo a cerca de 2.200 caracteres.
  Histórico de tarefas fica em `memory/task_history.json`, limitado às 100
  entradas mais recentes. Respostas elegíveis ficam em
  `memory/answer_cache.json`, limitado a 200 itens.
- Configurações da interface e alguns parâmetros locais ficam em arquivos JSON
  no diretório do usuário. A chave Gemini da tela de configuração só é
  lembrada quando essa opção é escolhida: usa o chaveiro do sistema quando
  disponível e, sem backend de chaveiro, fica apenas em memória no processo.
  Se o usuário colocar `GEMINI_API_KEY` no `.env`, ela fica como texto nesse
  arquivo local, sujeito às permissões e backups do sistema.
  `memory/config_manager.py` ainda contém uma função legada que pode escrever
  `config/api_keys.json`; não há chamada a essa função na interface atual.
- Tokens OAuth do Gmail são guardados pelo chaveiro do sistema. Arquivos que o
  usuário gera ou baixa são salvos no local selecionado pela ação.
- A interface mantém mensagens de diagnóstico durante a execução e o programa
  também escreve algumas mensagens em stdout. Os logs de ferramenta incluem o
  nome e os parâmetros da ação e um trecho de até 80 caracteres do resultado;
  erros podem incluir detalhes adicionais. Não há logger de arquivo próprio,
  mas o terminal ou a plataforma que inicia o programa pode reter stdout.

As rotas e arquivos locais relevantes incluem `main.py`, `ui.py`,
`core/secret_store.py`, `memory/memory_manager.py`, `memory/task_history.py`,
`memory/answer_cache.py` e `actions/email_control.py`.

### Serviço web

Quando o serviço é implantado e usado, o banco guarda endereço de e-mail,
nome de exibição e hash de senha scrypt; configuração e memória por usuário; chaves
Gemini cifradas; conversas enviadas ao endpoint de chat; transcrições de texto
da sessão Live; histórico de tarefas e cache de respostas. As definições estão
em `api/models.py`, e a gravação de conversa em `api/server.py` e
`api/websocket_client.py`. Áudio Live é encaminhado ao Gemini, mas não é salvo
no banco pelo código. A lista de conexões WebSocket ativas e seus buffers de
trabalho ficam em memória enquanto a conexão permanece aberta. O cliente web
guarda o token de acesso em `localStorage`; tokens têm validade padrão de 1.440
minutos e são stateless, e o endpoint de logout não revoga um token já emitido.

Os logs HTTP padrão do Uvicorn vão para stdout e podem incluir endereço remoto,
rota e status; não há logger de arquivo ou política de retenção própria no
código. Redis mantém chaves de quota com expiração. Se Redis não estiver disponível e
for permitido pelo ambiente, o limitador usa memória do processo. O servidor
escreve logs operacionais em stdout; a retenção desses logs depende do
container, host ou provedor que os coleta.

O padrão `ARGUS_DATA_RETENTION_DAYS=90` apaga, durante a inicialização e depois
uma vez por dia, somente mensagens de chat, registros de tarefas e entradas de
cache web com mais de 90 dias. O valor pode ser configurado como inteiro maior
que zero. Contas, hashes de senha, memória, configuração e segredos cifrados
não são removidos por essa rotina e permanecem no banco até exclusão manual do
banco ou implementação de uma ferramenta própria de exclusão. Veja
`api/config.py`, `api/retention.py` e `api/server.py`.

## Destinatários externos

Gemini recebe conteúdo necessário à conversa e às ferramentas baseadas no
modelo. Dependendo da ação escolhida e de sua configuração, o código também
envia termos de busca a Google Search/Gemini ou DuckDuckGo, acessa páginas web
e URLs fornecidas para pesquisa/apresentações, lê ou envia e-mails pelo Gmail,
e envia texto a OpenAI, ElevenLabs ou Edge TTS quando esses provedores de voz
são selecionados. Gmail usa OAuth; uma mensagem preparada passa por revisão e
confirmação antes do envio. Os provedores externos têm seus próprios termos e
políticas, que o Argus não controla.

## Configuração de domínio

O site Astro usa `PUBLIC_ARGUS_SITE_URL` como única URL base do domínio público;
deixe-a vazia até escolher o domínio e configure-a no build/deploy. O endereço
base dos links do repositório é `PUBLIC_ARGUS_REPOSITORY_URL`. No cliente Next.js,
`NEXT_PUBLIC_API_BASE_URL` é a URL base da API, e a URL WebSocket é derivada
dela. Consulte os arquivos `.env.example` correspondentes antes de publicar.

## Contato e exclusão

Este modelo ainda precisa ser completado com o controlador responsável,
endereço de contato, processo de pedidos de titulares e procedimentos de
exclusão antes de uso público ou comercial. No estado atual do código, não há
uma rota web para excluir uma conta inteira.
