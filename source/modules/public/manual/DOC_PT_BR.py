from dataclasses import dataclass


@dataclass(frozen=True)
class ManualDetails:
    summary: str
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()


@dataclass(frozen=True)
class ManualSection:
    id: str
    title: str
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()
    details: tuple[ManualDetails, ...] = ()

def normalize_language(lang: str | None) -> str:
    if not lang:
        return "pt_BR"

    v = lang.strip().replace("-", "_").lower()
    if v in ("pt_br", "pt"):
        return "pt_BR"

    if v in ("en_us", "en"):
        return "en_US"

    return "pt_BR"

def get_manual_document(lang: str | None = None) -> tuple[ManualSection, ...]:
    lang = normalize_language(lang)
    if lang == "en_US":
        try:
            from . import DOC_EN_US
            return getattr(DOC_EN_US, "_DOC_EN_US", tuple())

        except Exception:
            return tuple()

    return _DOC_PT_BR

# ----------------------------
# Conteúdo do manual (texto)
# ----------------------------

_DOC_PT_BR: tuple[ManualSection, ...] = (
    ManualSection(
        id="visao-geral",
        title="Visão Geral",
        paragraphs=(
            "Lúmen é uma suíte de ferramentas para estudo composta por módulos principais: Leitor Acessível, Gestão de Tempo "
            "(Pomodoro e gerenciador de tarefas), Mapas Mentais, Método Feynman e Matriz de Eisenhower. "
            "A interface é organizada em abas; cada aba contém controles e ferramentas específicas ao módulo.",
        ),
    ),
    ManualSection(
        id="requisitos-basicos-usuario",
        title="Requisitos básicos (usuário)",
        bullets=(
            "Windows (testado).",
            "Conexão à Internet para Edge TTS (opcional).",
        ),
    ),
    ManualSection(
        id="como-iniciar-o-aplicativo",
        title="Como iniciar o aplicativo",
        bullets=(
            "Abra a aplicação e selecione a aba do módulo que deseja usar.",
            "No Leitor: carregue um documento ou cole um texto na área de leitura, ajuste fonte e zoom.",
            "Para ouvir: use o botão Ler para iniciar TTS; use Pausar ou Parar conforme necessário.",
            "Em Gestão de Tempo: crie tarefas, inicie Pomodoro para foco e registre progressos.",
            "Em Mapas Mentais e Feynman: crie, edite e salve seus projetos.",
            "Em Eisenhower: categorize tarefas e reorganize por prioridade.",
        ),
    ),
    ManualSection(
        id="abertura-e-controles-globais",
        title="Abertura e controles globais",
        paragraphs=(
            "Ao abrir o Lúmen você verá a janela principal com abas e uma barra de menus (Arquivo, Configurações, Idiomas, Vozes, Sobre). "
            "A barra de status exibe informações contextuais.",
        ),
    ),
    ManualSection(
        id="modulos",
        title="Módulos (detalhados por aba)",
        details=(
            ManualDetails(
                summary="Leitor Acessível — Aba 1",
                paragraphs=(
                    "O Leitor Acessível foi feito para que qualquer pessoa possa abrir, ler e ouvir documentos sem conhecimentos técnicos."
                    " Use-o para ler PDFs, colar textos ou abrir arquivos de texto, ouvir o conteúdo com vozes naturais e acompanhar a leitura com destaques visuais.",
                    "O fluxo de uso é direto: abra ou cole o texto, escolha a voz (se desejar), ajuste volume e velocidade e pressione 'Ler'. Durante a reprodução você pode pausar, retomar ou parar a leitura, além de visualizar o texto destacado conforme a fala.",
                ),
                bullets=(
                    "Abrir arquivo: vá em Arquivo → Abrir (ou pressione Ctrl+O) e selecione um PDF ou arquivo de texto. O conteúdo será carregado na área de leitura.",
                    "Colar texto: cole diretamente na área de leitura se preferir ouvir um trecho copiado de outro lugar.",
                    "Selecionar voz: abra o menu Vozes e escolha a voz desejada; vozes neurais costumam soar mais naturais.",
                    "Iniciar leitura: clique em ▶️ Ler (ou use o atalho) para começar a ouvir o texto atual.",
                    "Pausar/continuar: use ⏸️ Pausar para interromper temporariamente e clique novamente para retomar do mesmo ponto.",
                    "Parar: ⏹️ Parar interrompe a leitura e reinicia a fila; para ouvir novamente pressione Ler.",
                    "Velocidade e volume: ajuste os controles deslizantes para deixar a voz mais lenta/rápida e definir o volume desejado.",
                    "Destaque de fala: ao ouvir, as palavras ou sentenças podem ser realçadas no texto para facilitar o acompanhamento visual.",
                    "Régua de Foco: ative a régua para isolar uma linha ou área da página — útil para leitura em voz alta ou concentração; feche com ESC ou pelo botão da régua.",
                    "Zoom e fonte: ajuste o tamanho da fonte e o zoom da área de leitura para maior conforto visual; as preferências são lembradas pelo aplicativo.",
                    "Busca no texto: use o campo Buscar (Ctrl+F) para localizar palavras ou frases dentro do documento carregado.",
                    "Selecionar e salvar: selecione texto para copiar ou use 'Salvar Como' para exportar o texto lido em formato de texto (.txt).",
                    "PDFs sem texto: se um PDF for apenas imagem (ex.: digitalizado), o aplicativo pode não extrair o texto automaticamente — nesses casos é necessário OCR externo.",
                    "Exportar áudio: é possível gerar arquivos de áudio (quando disponível) para ouvir offline ou compartilhar; remova arquivos temporários pelo gestor de áudio do aplicativo.",
                    "Dicas rápidas: foque em trechos curtos se estiver estudando, aumente a velocidade para revisão e use a régua para acompanhar linha a linha.",
                ),
            ),
            ManualDetails(
                summary="Gestão de Tempo — Aba 2",
                paragraphs=(
                    "A aba Gestão de Tempo combina um temporizador Pomodoro configurável com um gerenciador de tarefas em estilo Kanban.",
                    "Use este módulo para planejar sessões de estudo ou trabalho, focar em uma única tarefa por vez e registrar seu progresso de forma simples e visual.",
                ),
                bullets=(
                    "Adicionar tarefa: digite o título no campo indicado e clique em '➕ Adicionar' ou pressione Enter.",
                    "Definir prioridade: escolha a prioridade pela lista (círculos coloridos) para organizar o que é mais urgente ou importante.",
                    "Organizar com Kanban: arraste tarefas entre as colunas 'Todo', 'Doing' e 'Done' para refletir o estado atual do trabalho.",
                    "Iniciar sessão: selecione a tarefa que quer trabalhar (na coluna 'Doing') e clique em '▶️ Iniciar' para começar um Pomodoro.",
                    "Pausar e retomar: use o mesmo botão para pausar; clique novamente para retomar a contagem sem perder o progresso.",
                    "Pular ou resetar: use '⏭️ Pular' para avançar para o próximo ciclo ou '⏱️ Resetar Relógio' para reiniciar o temporizador atual.",
                    "Ajustar durações: altere os minutos de foco e descanso nas configurações rápidas — as mudanças valem para os ciclos seguintes.",
                    "Registro automático: ao terminar um ciclo de foco com uma tarefa selecionada, o sistema registra um Pomodoro para essa tarefa, ajudando a acompanhar produtividade.",
                    "Contagem de progresso: verifique quantos Pomodoros foram completados por tarefa na lista ou no histórico de sessões.",
                    "Concluir tarefa: quando terminar o trabalho, mova a tarefa para 'Done' ou use o menu de contexto para marcar como concluída.",
                    "Integração opcional: ative a integração com a Matriz de Eisenhower para enviar/receber tarefas entre módulos e manter a agenda sincronizada.",
                    "Alertas e som: o módulo pode avisar com som e notificações ao fim de ciclos — verifique volume e permissões do sistema se não ouvir alerta.",
                    "Dicas rápidas: foque em uma tarefa por Pomodoro, faça pequenas pausas regulares e ajuste os tempos conforme seu ritmo pessoal.",
                ),
            ),
            ManualDetails(
                summary="Mapas Mentais — Aba 3",
                paragraphs=(
                    "Mapas Mentais é uma área visual onde você organiza ideias em nós ligados por linhas."
                    " Use-o para capturar pensamentos, estruturar projetos, planejar estudos e lembrar conceitos de forma visual.",
                ),
                bullets=(
                    "Criar novo mapa: inicie um mapa vazio para começar do zero.",
                    "Adicionar ideias: clique em 'Adicionar nó' ou no botão correspondente para inserir um novo item; dê um título curto e claro.",
                    "Editar texto: clique duas vezes sobre um nó para alterar o conteúdo; mantenha frases curtas para melhorar a leitura.",
                    "Conectar nós: use a opção 'Conectar' ou arraste de um nó ao outro para criar relações visuais entre ideias.",
                    "Reorganizar: arraste os nós com o mouse para reposicionar; solte quando estiver satisfeito com a disposição.",
                    "Zoom e movimentação: aproxime/afaste para ver detalhes e arraste o espaço em branco para mover o mapa pelo canvas.",
                    "Salvar projeto: use 'Arquivo → Salvar' ou 'Salvar Como' para persistir seu mapa e poder retomá-lo depois.",
                    "Exportar imagem: escolha 'Exportar' para gerar um PNG do mapa e compartilhar ou incluir em documentos.",
                    "Desfazer/refazer: utilize os botões de desfazer/refazer para corrigir alterações acidentais.",
                    "Excluir/editar conexões: selecione uma ligação para removê-la ou edite rótulos quando disponíveis.",
                    "Navegação por hierarquia: expanda/contraia grupos de nós para focar em partes específicas do mapa.",
                    "Boas práticas: comece com um nó central representando o tema principal; mantenha os ramos curtos e use palavras-chave em vez de frases longas.",
                ),
            ),
            ManualDetails(
                summary="Método Feynman — Aba 4",
                paragraphs=(
                    "Ferramenta pensada para ajudá-lo a aprender qualquer tema explicando-o com suas próprias palavras. "
                    "O fluxo guia você por passos simples: explique de forma acessível, identifique o que você não entendeu, pesquise e então simplifique novamente.",
                    "Tudo é construído para ser usado sem conhecimento técnico: só escreva, revise e salve. Seus conceitos ficam listados para consulta posterior.",
                ),
                bullets=(
                    "➕ Novo: clique para criar um novo conceito; comece dando um título claro (Ex: 'Tensão de Cisalhamento').",
                    "1️⃣ Conceito: no campo de título escreva o nome do tema que quer aprender.",
                    "2️⃣ Explique com Simplicidade: escreva a explicação como se estivesse ensinando para alguém sem conhecimento prévio; use exemplos do dia a dia e frases curtas.",
                    "3️⃣ Lacunas Identificadas: anote onde você ficou em dúvida ou não soube explicar — esses pontos guiam sua pesquisa.",
                    "4️⃣ Revisão: depois de pesquisar, reescreva a explicação de forma mais clara e completa; esse é o momento de consolidar o aprendizado.",
                    "📊 Nível de Domínio: selecione o nível que representa seu domínio (Iniciante / Intermediário / Avançado) para acompanhar progresso.",
                    "💾 Salvar Conceito: use o botão '💾 Salvar Conceito' para persistir o conceito; ele aparecerá na lista à esquerda.",
                    "Lista de Conceitos: selecione um item para abrir e editar seu conteúdo; a lista mostra um marcador de domínio (cores) para identificar seu progresso rapidamente.",
                    "🗑️ Deletar: apague conceitos que não precisar mais usando o botão '🗑️ Deletar' (há confirmação antes de remover).",
                    "Redefinir Nível: clique com o botão direito sobre um conceito na lista para '🎯 Redefinir Nível de Domínio' e ajustar sem abrir o item.",
                    "Dicas práticas: seja específico no título, use analogias simples, foque em explicar sem jargões e reveja conceitos periodicamente.",
                ),
            ),
            ManualDetails(
                summary="Matriz de Eisenhower — Aba 5",
                paragraphs=(
                    "A Matriz de Eisenhower ajuda você a priorizar tarefas dividindo-as em quatro quadrantes com base em urgência e importância. "
                    "Nesta aba você pode criar, agendar, mover e concluir tarefas de forma visual e simples, sem necessidade de conhecimentos técnicos.",
                ),
                bullets=(
                    "Adicionar tarefa: digite a tarefa no campo 'Adicione uma tarefa...' e clique em 'Adicionar Tarefa'.",
                    "Vincular data e horário: marque 'Vincular data' (e 'Vincular horário' se desejar) antes de adicionar para agendar a tarefa em uma data/horário específicos.",
                    "Escolher quadrante: selecione o quadrante apropriado no seletor antes de adicionar; caso contrário, mova a tarefa depois para o quadrante correto.",
                    "Mover tarefas: arraste e solte entre quadrantes para reorganizar, ou use o menu de contexto (clique com o botão direito) para opções rápidas.",
                    "Marcar como concluída: marque a caixa de seleção ao lado da tarefa para movê-la para a lista 'Concluídas' correspondente; desmarque para restaurá-la.",
                    "Editar tarefa: abra o menu de contexto sobre uma tarefa para editar texto, data, horário, descrição ou anexar/abrir arquivos vinculados.",
                    "Remover tarefa: escolha 'Remover' no menu de contexto; haverá confirmação para evitar exclusões acidentais.",
                    "Placeholders e dicas: listas vazias mostram textos orientativos (ex.: '1º Quadrante') para indicar onde adicionar tarefas.",
                    "Painel de calendário: use o botão 'Calendário' para ver todas as tarefas agendadas por data; clique em uma data para visualizar e abrir tarefas vinculadas do dia.",
                    "Salvar e exportar: as tarefas são persistidas pelo aplicativo; use 'Salvar Como' quando quiser exportar em formatos suportados (JSON/Excel/PDF).",
                    "Boas práticas: mantenha cada tarefa curta e objetiva, use datas apenas para compromissos reais e reveja a matriz regularmente para atualizar prioridades.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="menus-e-acoes-rapidas",
        title="Menus e ações rápidas",
        bullets=(
            "Arquivo: carregar e salvar projetos, exportar mapas, importar tarefas (quando disponível).",
            "Configurações: idioma, vozes e fonte padrão.",
            "Idiomas: muda idioma da interface e das strings.",
            "Ajuda: versão e documentação rápida.",
        ),
    ),
    ManualSection(
        id="sugestoes-de-uso-combinadas",
        title="Sugestões de uso combinadas",
        bullets=(
            "Leitura e Pomodoro: abra material no Leitor, ative régua de foco, vincule uma tarefa e inicie a sessão.",
            "Mapas e Feynman: transforme nós em explicações e revise depois.",
            "Eisenhower: priorize semanalmente e planeje pomodoros para o que importa.",
        ),
    ),
    ManualSection(
        id="novas-funcionalidades",
        title="Novas funcionalidades (como usar)",
        details=(
            ManualDetails(
                summary="Pomodoro mais inteligente no dia a dia",
                bullets=(
                    "Use o botão principal do timer normalmente: ele muda entre Iniciar, Pausar e Continuar conforme o momento do estudo.",
                    "Se você atingir a meta de ciclos do dia, o aplicativo avisa e bloqueia novos ciclos de foco até você aumentar a meta.",
                    "Você pode usar 'Pular' para encerrar o período atual e ir para o próximo, ou 'Resetar Relógio' para recomeçar o período do zero.",
                    "Ao terminar um foco, você recebe confirmação de progresso com a contagem de ciclos concluídos.",
                ),
            ),
            ManualDetails(
                summary="Alterar tempos sem perder o que já foi feito",
                bullets=(
                    "Durante o uso do timer, você pode ajustar minutos de foco, descanso e quantidade de ciclos.",
                    "Ao mudar essas configurações, o tempo já cumprido no ciclo atual é preservado para você não perder andamento.",
                    "Se necessário, ajuste para pelo menos 1 ciclo para manter o fluxo funcionando corretamente.",
                ),
            ),
            ManualDetails(
                summary="Integração automática entre Pomodoro e tarefas",
                bullets=(
                    "Mantenha a tarefa que você está executando na coluna 'Em Progresso'.",
                    "Quando um ciclo de foco termina, o contador de Pomodoros dessa tarefa é atualizado automaticamente.",
                    "Quando a tarefa atingir a meta de ciclos definida, ela pode ser concluída automaticamente, conforme seu fluxo.",
                    "Use o botão de reset de contagem quando quiser zerar apenas os contadores, sem apagar tarefas.",
                ),
            ),
            ManualDetails(
                summary="Mover tarefas com mais rapidez",
                bullets=(
                    "Arraste tarefas entre listas para atualizar o status com poucos cliques.",
                    "Ao arrastar sobre as abas, a aba de destino pode abrir sozinha para facilitar a movimentação.",
                    "Você também pode clicar com o botão direito e escolher para qual lista ou prioridade enviar a tarefa.",
                    "Na criação de tarefas, pressione Enter para adicionar rapidamente.",
                ),
            ),
            ManualDetails(
                summary="Matriz de Eisenhower com uso mais prático",
                bullets=(
                    "No painel da matriz, use o botão de calendário para alternar entre mostrar e recolher o calendário lateral.",
                    "Com o calendário aberto, selecione uma data para ver as tarefas daquele dia.",
                    "Com o calendário recolhido, você ganha mais espaço para organizar os quadrantes.",
                    "No menu da tarefa (clique com o botão direito), você pode mover rapidamente para outro quadrante.",
                ),
            ),
            ManualDetails(
                summary="Compartilhar tarefas da Matriz para o Pomodoro",
                bullets=(
                    "Na tarefa da matriz, abra o menu com clique direito e escolha compartilhar com a Gestão de Tempo.",
                    "A tarefa aparece no fluxo de Pomodoro para você estudar com foco e registrar progresso.",
                    "Você pode compartilhar uma tarefa por vez ou várias tarefas em sequência.",
                ),
            ),
            ManualDetails(
                summary="Método Feynman com material de apoio e visão rápida",
                bullets=(
                    "Vincule arquivos de apoio aos seus conceitos para manter tudo no mesmo lugar.",
                    "Passe o mouse sobre um conceito para ver um resumo rápido antes de abrir.",
                    "Se o arquivo tiver sido movido ou apagado, o aplicativo mostra um aviso para você corrigir o vínculo.",
                ),
            ),
            ManualDetails(
                summary="Mapa Mental -> Método Feynman sem retrabalho",
                bullets=(
                    "No Mapa Mental, preencha o conceito e use o botão de integração para enviar ao Método Feynman.",
                    "Ao abrir o Método Feynman, o conteúdo já chega organizado para você revisar.",
                    "Se o conceito já existir, o aplicativo atualiza o conteúdo em vez de criar duplicado.",
                ),
            ),
            ManualDetails(
                summary="Tema e idioma atualizados em tempo real",
                bullets=(
                    "Você pode trocar idioma e tema com o aplicativo aberto.",
                    "Textos, títulos e botões são atualizados na hora, sem necessidade de reiniciar.",
                    "As telas de tempo, tarefas, Pomodoro e matriz acompanham a mudança automaticamente.",
                ),
            ),
            ManualDetails(
                summary="Som do Pomodoro configurável",
                bullets=(
                    "Acesse Configurações -> Som para escolher a campainha do Pomodoro.",
                    "Use '▶️ Tocar' para testar o áudio antes de salvar.",
                    "Ajuste o intervalo de repetição; ao fim do ciclo, o alerta toca na hora e repete até você fechar o aviso.",
                    "As preferências ficam salvas para os próximos usos.",
                ),
            ),
            ManualDetails(
                summary="Proteção extra ao abrir e recuperar conteúdo",
                bullets=(
                    "Ao abrir conteúdos com informações incompletas, o aplicativo tenta recuperar o máximo possível automaticamente.",
                    "Em casos de inconsistência, você recebe aviso em vez de perder tudo sem perceber.",
                    "Essa proteção reduz risco de interrupção durante estudo e organização.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="solucao-de-problemas",
        title="Solução de problemas",
        details=(
            ManualDetails(
                summary="Sem som",
                bullets=(
                    "Verifique volume do sistema e do aplicativo.",
                    "Se estiver usando Edge TTS, confirme a conexão com a Internet.",
                ),
            ),
            ManualDetails(
                summary="PDF sem texto",
                bullets=(
                    "O PDF pode ser baseado em imagem; será necessário OCR.",
                    "Se aplicável, verifique bibliotecas como pdfplumber e pypdf.",
                ),
            ),
            ManualDetails(
                summary="Vozes não listadas",
                bullets=("Recarregue vozes ou reinicie o aplicativo.",),
            ),
            ManualDetails(
                summary="Erro ao salvar ou ler",
                bullets=(
                    "Verifique permissões da pasta de dados.",
                    "Consulte os logs para detalhes.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="logs-e-diagnostico",
        title="Logs e diagnóstico",
        bullets=("O LogManager gera logs; verifique a pasta AppData\\Local\\Lumen\\logs (no Windows).",),
    ),
    ManualSection(
        id="armazenamento",
        title="Armazenamento e arquivos persistentes (resumo)",
        bullets=(
            "Tarefas: JSON (por exemplo, tarefas.json).",
            "Mapas: projeto (por exemplo, .map ou .json).",
            "Conceitos Feynman: conceitos.json.",
            "Configurações: config.json.",
            "Local sugerido: AppData\\Local\\Lumen (no Windows).",
        ),
    ),
    ManualSection(
        id="boas-praticas",
        title="Boas práticas de uso",
        bullets=(
            "Salve mapas e conceitos regularmente.",
            "Faça backups periódicos.",
            "Mantenha o aplicativo e dependências atualizados.",
        ),
    ),
    ManualSection(
        id="atalhos",
        title="Resumo rápido de atalhos",
        bullets=(
            "Ctrl+1 — 📖 Leitor Acessível  ",
            "Ctrl+2 — ⏱️ Gestão de Tempo",
            "Ctrl+3 — 🧠 Mapas Mentais",
            "Ctrl+4 — 🎓 Método Feynman",
            "Ctrl+5 — 🗂️ Matriz Eisenhower",
            "Ctrl+O — 📂 Carregar PDF",
            "Ctrl+R — ▶️ Ler",
            "Ctrl+P — ⏸️ Pausar",
            "Ctrl+T — ➕ Adicionar",
            "Ctrl+N — ➕ Adicionar Conceito",
            "Ctrl+S — 💾 Salvar",
            "Ctrl+L — 📂 Carregar",
            "Ctrl+F — 🔎 Buscar",
            "Ctrl+Shift+F — 🔤 Fonte",
            "Ctrl+Shift+S — 🔔 Som",
            "Ctrl+Q — ❌ Sair",
            "F1 — ❓ Ajuda",
        ),
    ),
    ManualSection(
        id="faq",
        title="Perguntas frequentes (FAQ)",
        details=(
            ManualDetails(
                summary="Como deixar a voz mais natural?",
                paragraphs=("Use Edge TTS (vozes neurais) e ajuste velocidade e volume.",),
            ),
            ManualDetails(
                summary="Onde meus dados são salvos?",
                paragraphs=("No diretório de dados do app (Windows: AppData\\Local\\Lumen).",),
            ),
        ),
    ),
    ManualSection(
        id="suporte",
        title="Como obter ajuda e suporte",
        bullets=(
            "Use o menu Ajuda para versão e documentação.",
            "Para problemas técnicos, anexe logs ao abrir um issue. Contato: linceu_lighthouse@outlook.com.",
        ),
    ),
)

__all__ = ["_DOC_PT_BR"]
