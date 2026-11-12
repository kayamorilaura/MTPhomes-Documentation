# MTPHomes — Documentação da operação de alojamentos

Repositório de referência para o processo de revisão de anúncios e fotografias da MTPHomes, incluindo exports do **n8n**, scripts **Tampermonkey**, exemplos de auditoria e folhas de apoio.

> **Estado:** arquivo técnico e documentação de passagem. Os ficheiros representam versões guardadas do projeto, não garantem que os workflows estejam ativos ou que todas as publicações tenham sido revalidadas em produção.

## 📁 Estrutura

| Caminho | Conteúdo |
| --- | --- |
| [`dev/n8nversions/versoes_n8n/`](dev/n8nversions/versoes_n8n) | Quatro exports dos workflows n8n (fotos/Groq, recuperação de incompletos, estado parcial e propostas Airbnb) |
| [`dev/n8nversions/versoes_groq/`](dev/n8nversions/versoes_groq) | Ficheiros de referência relativos ao Groq |
| [`dev/n8nversions/gpt/`](dev/n8nversions/gpt) | Guia técnico do gestor de fotografias e materiais de geração |
| [`dev/tappermonkey/`](dev/tappermonkey) | Scripts para o Avantio e o Airbnb, incluindo auditoria, exportação e gestor em lote |
| [`dev/fotoszip/`](dev/fotoszip) | Exemplos de ZIPs de fotografias pendentes, para cruzamento visual e identificação dos IDs |
| [`Lista Alojamentos MTPHomes.xlsx`](Lista%20Alojamentos%20MTPHomes.xlsx) | Folha de alojamentos e informação de apoio |
| [`Lista_alojamentos.xlsx`](Lista_alojamentos.xlsx) | Segunda versão da folha de alojamentos — confirmar qual é a fonte atual antes de usar |

## 🔄 Como funciona

1. **Notion:** escolher o alojamento e confirmar o link/identificador MTPHomes, as observações e o progresso guardado.
2. **Avantio:** abrir a galeria correta e executar o script de auditoria de fotografias.
3. **Fotografias pendentes:** usar o script de exportação para obter um ZIP com imagens e `manifest.json`, preservando IDs e ordem.
4. **n8n + Groq:** gerar os metadados em **PT, ES, EN e FR**. Cada fotografia recebe **título, descrição e ALT** (12 campos de texto).
5. **Recuperação:** em caso de rate limit ou falha, guardar o estado `PARCIAL` e retomar apenas as imagens em falta. Não regenerar nem apagar as já validadas.
6. **Gestor em Lote:** importar o JSON correspondente à galeria e validar o mapa entre imagem e ID Avantio. **Testar uma fotografia primeiro.**
7. **Guardar e reauditar:** usar «Validar e guardar dados» no Avantio e voltar a executar a auditoria. Só considerar tecnicamente completa uma galeria confirmada com **0 fotografias a rever e 0 não verificáveis**.
8. **Airbnb:** comparar anúncios e detalhes essenciais. Não assumir que a descrição pública é idêntica, palavra por palavra, ao texto de referência.

### Scripts relevantes

- **Avantio Fotos — Gestor em Lote 2.3.5:** `dev/tappermonkey/Avantio Fotos - Gestor em Lote-2.3.5.txt`
- **Avantio — Auditoria de Fotos 2.0.0:** `dev/tappermonkey/Avantio — Auditoria de Fotos-2.0.0.txt`
- **Exportar Fotos da Auditoria 1.0:** `dev/tappermonkey/MTPHomes - Exportar Fotos da Auditoria-1.0.txt`
- **Airbnb Autofill (revisão segura) 0.1.0:** `dev/tappermonkey/MTPHomes - Airbnb Autofill (revisão segura)-0.1.0.txt`

Para instalar um userscript, copiar o seu conteúdo para um novo script no Tampermonkey, verificar o domínio `@match` e autorizações, e testar em ambiente controlado. Os scripts não substituem uma auditoria manual do anúncio.

## 🧩 Os principais workflows n8n

| Workflow exportado | Responsabilidade |
| --- | --- |
| `MTPHomes - Recuperar UM Incompleto v4 - Groq original` | Retoma da análise de uma unidade, validação de snapshot e escrita protegida no Notion |
| `MTPHomes \| APENAS erro GROQ → PARCIAL/PENDENTE → Notion PS` | Registo de erro e progresso parcial para retoma |
| `MTPHomes \| Atualizar fotos no avantio (GROQ)` | Processamento de fotografias, preparação de JSON e atualização do Notion |
| `MTPHomes \| Airbnb v2 - download para proposta (com resposta JSON)` | Preparação de uma proposta de conteúdos para revisão/importação Airbnb |

São **exports de versões**: verificar nomes de nós, ligações, credenciais, triggers e lógica antes de ativar. A propriedade `active` num export não confirma que o serviço esteja atualmente em execução.

## ⚠️ Exceções e integridade dos dados

- **Os checks do Notion podem representar fecho administrativo**, não necessariamente uma prova de publicação ou verificação real.
- Os casos não acessíveis no Airbnb/Avantio devem manter a respetiva observação e ser submetidos à equipa com acesso.
- **Eva Andorinha:** não confundir os anúncios **684095 (5Pax, 20 fotografias de referência)** e **695899 (2Pax, 16 fotografias na galeria 4122475)**. Validar a correspondência antes de reutilizar JSON.
- Alguns alojamentos foram concluídos por importadores diretos no Avantio, embora o JSON histórico no Notion ainda esteja `PARCIAL`.
- **Não** substituir metadados já preenchidos sem uma decisão explícita e um backup dos dados originais.

## 🔐 Segurança e manutenção

**Este repositório é público.** Antes de o partilhar, confirmar a autorização para publicar as folhas Excel, imagens dos alojamentos, URLs internas e informação de operação. Se contiver dados não públicos, alterar a visibilidade para **privado** e restringir o acesso.

Nunca fazer commit de chaves Groq, tokens Notion, credenciais Avantio/Airbnb, cookies, ficheiros `.env` ou dados pessoais. Em exports n8n, as referências a credenciais têm de ser configuradas na instalação de destino; não exportar segredos.

A pasta `node_modules/` está versionada neste arquivo, mas **não deve fazer parte de futuros commits**. Adicionar `.gitignore` e remover os ficheiros já rastreados do índice Git quando a estrutura do projeto for revista.

---

**Manual de passagem:** consultar a documentação operacional MTPHomes mantida no Notion pela equipa. Os procedimentos e exceções do Notion são a referência para as decisões de negócio.
