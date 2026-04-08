<!-- Multilanguage README.md for Lúmen -->

<p align="center">
  <b>Selecione o idioma / Select language:</b><br>
  <a href="#ptbr">🇧🇷 Português (BR)</a> |
  <a href="#enus">🇺🇸 English (US)</a>
</p>

---

## <a id="ptbr"></a>🇧🇷 Português (BR)

> **Observação:** Este repositório refere-se à versão **v2026.2.21.0** do 📚 Projeto Lúmen. Apoie o projeto e adquira a versão paga através do link: [Instalar via Microsoft Store](https://apps.microsoft.com/detail/9N70CLLMVRPN)

<details>
<summary>Clique para expandir o README em português</summary>

# 📚 Lúmen

Versão: v2026.2.21.0
Autor: Fernando Nillsson Cidade

- Manual de Utilização (PT‑BR): [MANUAL.md — Português](./MANUAL.md#ptbr)

Aplicativo de estudo personalizado para pessoas neurodivergentes (Dislexia, TDAH, TEA).

## 🎯 Objetivo
Fornecer uma ferramenta desktop configurável que reduza barreiras de leitura, atenção e organização para jovens e adultos neurodivergentes, oferecendo TTS local, ajustes tipográficos, gestores de tarefa e recursos para revisão ativa (mapas mentais / Método Feynman).

## 🎯 Funcionalidades principais

### 📖 Leitor Acessível
- Conversão de texto em fala (TTS) com seleção de voz, controle de velocidade e volume.
- Extração de texto de PDFs (quando disponível).
- Régua de foco para leitura linha a linha.
- Controles persistentes de fonte e tamanho.

### ⏱️ Gestão de Tempo e Tarefas
- Timer Pomodoro customizável.
- Matriz de Eisenhower para priorização.
- Rastreamento de sessões e pomodoros por tarefa.

### 🧠 Mapas Mentais e Método Feynman
- Editor de mapas mentais e conectividade entre ideias.
- Espaço guiado para explicação/auto‑teste (Método Feynman).
- Exportação de dados e imagens.

### Outros
- Importação/exportação local: PDF, JSON e formatos de texto.
- Localização: pt-BR e en-US (arquivos .ts incluídos; gerar .qm antes do empacotamento).
- Armazenamento local por padrão (privacidade).

## ✅ Evolução completa de funcionalidades e recursos

### 📖 Leitor Acessível (TTS)
- Correção da pausa para garantir que a leitura permaneça realmente pausada, sem avanço automático inesperado.
- Melhor controle da fila de áudio em textos longos, com retomada mais previsível ao continuar a leitura.
- Maior robustez no fluxo de troca de voz e no tratamento de arquivos temporários de áudio.

### ⏱️ Pomodoro e Gestão de Tempo
- Fluxo do timer reforçado com estados mais claros de **Iniciar / Pausar / Continuar**.
- Bloqueio de novos ciclos de foco quando o limite configurado é atingido, com aviso contextual.
- Preservação do progresso atual ao alterar tempos de foco/descanso durante o uso.
- Recursos de **pular ciclo** e **resetar relógio** com comportamento mais consistente.
- Configuração de som do Pomodoro com escolha de campainha, prévia de áudio e intervalo de repetição.
- Alerta sonoro ao fim de ciclo com reprodução imediata e repetição até o fechamento do aviso.
- Integração automática com tarefas em andamento para registrar pomodoros concluídos.

### 🗂️ Gestão de Tarefas e Kanban
- Melhorias no arrastar e soltar entre colunas e abas, com sincronização de status mais confiável.
- Melhorias de menu de contexto para edição, movimentação e ações em lote.
- Redução de duplicidade de tarefas ao integrar fluxos entre módulos.
- Contadores e listas com atualização visual mais consistente no uso diário.

### 📌 Matriz de Eisenhower
- Integração bidirecional com Gestão de Tempo com vínculo de tarefa mais estável.
- Evolução do calendário da matriz com suporte a visão anual, filtro por ano e melhor organização por períodos.
- Melhorias em remoção múltipla com menos interrupções e confirmação final consolidada.
- Salvamento e carregamento com mais segurança, incluindo cópias automáticas de backup.
- Importação/exportação mais robusta em **JSON, Excel e PDF**, com validações de estrutura e maior confiabilidade de reimportação.

### 🧠 Mapas Mentais
- Integração aprimorada com o Método Feynman para enviar conceitos com menos retrabalho.
- Melhor robustez de persistência com backup automático e redução de gravações redundantes.
- Carregamento mais defensivo para recuperar o máximo possível mesmo com dados parcialmente inconsistentes.
- Melhorias no manuseio de arquivos vinculados e no fluxo de uso visual do mapa.

### 🎓 Método Feynman
- Recebimento de conceitos vindos de Mapas Mentais com normalização e mesclagem para evitar duplicação.
- Pré-visualização mais rica de conceitos e arquivos vinculados para revisão rápida.
- Abertura de arquivos vinculados com mais compatibilidade entre ambientes.
- Melhor estabilidade de recursos internos durante abertura/fechamento de fluxos.

### 🗓️ Calendário e planejamento
- Expansão da experiência de calendário com visão mensal e anual.
- Melhor leitura da agenda com agrupamentos por período e informações contextuais aprimoradas.
- Destaques visuais para facilitar orientação da data atual e navegação de tarefas.

### 🌐 Idioma, tema, interface e plataforma
- Troca dinâmica de idioma com atualização imediata de textos e rótulos em múltiplas telas.
- Melhor sincronização visual com tema/paleta da aplicação em tempo real.
- Ajustes de locale e formato de data/hora para reduzir ambiguidades na edição de tarefas.
- Inicialização mais estável no Windows, com melhorias de ícone e consistência visual.
- Proteções adicionais na interface para evitar falhas em cenários de ciclo de vida de componentes.

### 🛡️ Integridade de dados e confiabilidade geral
- Padronização de identidade única de tarefas para reduzir tarefas “espelho” entre módulos.
- Backups automáticos antes de operações críticas de escrita.
- Validações mais rígidas em importação/carregamento para reduzir risco de corrupção silenciosa.
- Melhor experiência de recuperação e continuidade em cenários de inconsistência.

### 🧪 Checklist funcional completo (validação manual)
1. Criar tarefas, mover entre Kanban/Eisenhower e validar ausência de duplicidade inesperada.
2. Executar ciclos de Pomodoro com pausa/continuação/pulo/reset e confirmar persistência do progresso.
3. Configurar som do Pomodoro, validar prévia e repetição de alerta ao fim do ciclo.
4. Alternar calendário entre visão mensal/anual e validar filtro por ano e listagem por período.
5. Exportar e reimportar tarefas (JSON/Excel/PDF) para validar consistência de dados.
6. Integrar conceito de Mapa Mental para Feynman e confirmar atualização sem duplicação indevida.
7. Trocar idioma/tema com app aberto e verificar atualização imediata da interface.
8. Reiniciar aplicativo e confirmar persistência normal dos dados.

### 🧩 Consolidação histórica de funcionalidades e recursos (v2025.11.26.0 → v2026.2.19.0)
- Evolução contínua do Leitor Acessível com TTS local, controles tipográficos persistentes, régua de foco, extração de texto e maior estabilidade em pausa/retomada da leitura.
- Gestão de Tempo ampliada com Pomodoro configurável (foco/descanso/ciclos), bloqueios por limite, alertas sonoros configuráveis e registro automático de progresso nas tarefas.
- Gestão de Tarefas/Kanban reforçada com melhorias de edição, arrastar e soltar, ações em lote, atualização visual mais previsível e integração mais confiável com outros recursos.
- Matriz de Eisenhower expandida com sincronização bidirecional, deduplicação por identidade de tarefa, calendário mensal/anual, filtros por ano e operações de remoção em massa mais limpas.
- Importação/exportação e persistência fortalecidas com validações estruturais mais rígidas, suporte consistente em JSON/Excel/PDF e backups automáticos antes de gravações críticas.
- Integração Mapa Mental + Método Feynman consolidada com fluxo de envio de conceitos, redução de duplicidades, melhor revisão guiada e tratamento mais estável de arquivos vinculados.
- Plataforma e interface amadurecidas com tradução dinâmica em tempo real, sincronização de tema/paleta, ajustes de locale de data/hora, inicialização mais robusta e melhor consistência visual no Windows.
- Confiabilidade geral elevada com proteções defensivas adicionais na interface, prevenção de estados inválidos e continuidade operacional mais segura em cenários de inconsistência.

## 🚀 Instalação (Windows — desenvolvimento)
Requisitos mínimos:
- Python 3.10+
- Git (opcional)

Passos (PowerShell recomendado):
1. Clonar repositório:
   git clone <URL-do-repositório>
2. Criar ambiente virtual:
   python -m venv .venv
3. Ativar (PowerShell):
   .\.venv\Scripts\Activate.ps1
   (ou no CMD: .\.venv\Scripts\activate.bat)
4. Instalar dependências:
   pip install -r requirements.txt
5. Executar em desenvolvimento:
   python main.py

Observação: se o sistema exige permissões de execução do PowerShell, ajuste a política de execução conforme necessário.

## 📦 Empacotamento para distribuição (Windows)
- Recomendado: PyInstaller (ou Nuitka). Incluir assets/ e language/translations/ nas 'datas' do .spec.
- Gerar arquivos de tradução .qm com:
  pyside6-lrelease language/translations/*.ts
- Incluir arquivos de licença/aviso no bundle:
  assets/EULA/, assets/NOTICES/, assets/COPYRIGHT/, assets/CLC/, assets/PRIVACY_POLICY/
- Se empacotar PySide6, documente conformidade LGPL conforme assets/NOTICES/NOTICE_pt_BR.txt.
- Testar a pasta do executável quanto a DLLs substituíveis e procedimentos de redistribuição (LGPL).

## ⚙️ Dependências (principais)
- PySide6, PySide6_Essentials, PySide6_Addons e shiboken6 — interface gráfica desktop (Qt).
- pyttsx3 e edge-tts — síntese de voz (TTS).
- pdfplumber, pypdfium2, pypdf e PyPDF2 — leitura e processamento de PDFs.
- openpyxl e pandas — importação/exportação de dados e planilhas.
- reportlab — geração/exportação de documentos PDF.
- python-docx e docx2pdf — manipulação e conversão de documentos.
- spacy, sentence-transformers, transformers e torch — recursos de linguagem/IA.
- numpy e scikit-learn — base numérica e apoio a processamento/modelos.
Consulte a lista completa (com versões) em [`requirements.txt`](./requirements.txt).

## 🛠️ Notas técnicas
- Logging: utils/LogManager.py (logs em %LOCALAPPDATA%\TEA_TDAH_Dislexia).
- Dados de usuário (tarefas, mapas, histórico, configurações, arquivos temporários e logs) são salvos em:
  %LOCALAPPDATA%\TEA_TDAH_Dislexia
- Traduções: arquivos .ts em language/translations/ — gerar .qm antes do empacotamento.
- Recomenda‑se adicionar testes unitários para TTS, exportação e gerenciamento de tarefas.

## ⚠️ Limitações e recomendações
- Versão inicial: alfa/experimental — pode conter stubs e fluxos incompletos.
- Faça backup dos dados antes de atualizar ou alterar bibliotecas do executável.
- Validação de entradas (formatos numéricos, campos obrigatórios) pode precisar de reforço em algumas telas.

## 🔒 Privacidade e licença
- O aplicativo opera localmente por padrão e não envia telemetria automática.
- Para detalhes sobre tratamento de dados e consentimento, consulte:
  assets/PRIVACY_POLICY/Privacy_Policy_pt_BR.txt
- Termos de uso e restrições: assets/EULA/EULA_pt_BR.txt
- Avisos de terceiros e licenças: assets/NOTICES/NOTICE_pt_BR.txt
- Direitos autorais e marca: assets/COPYRIGHT/AVISO DE COPYRIGHT E MARCA REGISTRA_pt_BR.txt
- Contratos comerciais: assets/CLC/CLC_pt_BR.txt

## 🔗 Atalhos úteis
- Ctrl+1 — Leitor Acessível
- Ctrl+2 — Gestão de Tempo
- Ctrl+3 — Mapas Mentais
- Ctrl+4 — Método Feynman
- ESC — Fechar régua de foco

## 🧪 Testes e contribuição
- Bugs e contribuições: abrir issue / pull request no repositório (ver README online).
- Sugerido: incluir testes automatizados e CI para builds e empacotamento.

## 📞 Contato
Autor: Fernando Nillsson Cidade  
E‑mail (privacidade/licenças): linceu_lighthouse@outlook.com

## 📄 Versão e notas de lançamento
Consulte assets/RELEASE/RELEASE\ NOTES_pt_BR.txt e assets/RELEASE/RELEASE\ NOTES_en_US.txt para histórico de versões e mudanças importantes.
- Notas avançadas (detalhamento técnico):
  - assets/RELEASE/RELEASE NOTES_pt_BR_Avancado.txt

---

</details>

## <a id="enus"></a>🇺🇸 English (US)

> **Note:** This repository refers to the **v2026.2.21.0** version of the 📚 Lúmen Project. Support the project and purchase the paid version through the link: [Instalar via Microsoft Store](https://apps.microsoft.com/detail/9N70CLLMVRPN)

<details>
<summary>Click to expand the README in English</summary>

# 📚 Lúmen

Version: v2026.2.21.0
Author: Fernando Nillsson Cidade

- User Manual (EN‑US): [MANUAL.md — English](./MANUAL.md#enus)

Personalized study application for neurodivergent people (Dyslexia, ADHD, ASD).

## 🎯 Objective
Provide a configurable desktop tool that reduces barriers to reading, attention and organization for neurodivergent youth and adults, offering local TTS, typographic adjustments, task managers and resources for active review (mind maps / Feynman Technique).

## 🎯 Main features

### 📖 Accessible Reader
- Text‑to‑speech (TTS) conversion with voice selection, speed and volume control.
- PDF text extraction (when available).
- Focus ruler for line‑by‑line reading.
- Persistent font and size controls.

### ⏱️ Time and Task Management
- Customizable Pomodoro timer.
- Eisenhower Matrix for prioritization.
- Session and pomodoro tracking per task.

### 🧠 Mind Maps and Feynman Technique
- Mind‑map editor and connectivity between ideas.
- Guided space for explanation/self‑test (Feynman Technique).
- Data and image export.

### Others
- Local import/export: PDF, JSON and text formats.
- Localization: pt‑BR and en‑US (.ts files included; generate .qm before packaging).
- Local storage by default (privacy).

## ✅ Complete evolution of features and resources

### 📖 Accessible Reader (TTS)
- Pause behavior fixed to ensure playback truly stays paused, without unexpected auto-advance.
- Better audio queue control for long texts, with more predictable resume behavior.
- Stronger robustness in voice-switch flow and temporary audio file handling.

### ⏱️ Pomodoro and Time Management
- Timer flow reinforced with clearer **Start / Pause / Resume** states.
- New focus-cycle blocking when configured limits are reached, with contextual warning.
- Current progress is preserved when changing focus/break times while running.
- **Skip cycle** and **reset clock** behaviors are now more consistent.
- Pomodoro sound configuration with bell selection, audio preview, and repeat interval.
- End-of-cycle alert now plays immediately and repeats until the warning dialog is closed.
- Automatic integration with active tasks to register completed Pomodoros.

### 🗂️ Task Management and Kanban
- Drag-and-drop improvements across columns and tabs, with more reliable status synchronization.
- Context menu enhancements for editing, moving, and batch actions.
- Reduced task duplication when integrating flows across modules.
- More consistent visual refresh for counters and lists in daily usage.

### 📌 Eisenhower Matrix
- Bidirectional integration with Time Management using more stable task linkage.
- Calendar evolution with yearly view support, year filter, and better period organization.
- Improved multi-removal flow with fewer interruptions and consolidated final feedback.
- Safer save/load behavior, including automatic backup copies.
- More robust **JSON, Excel, and PDF** import/export with structure validation and more reliable reimport.

### 🧠 Mind Maps
- Improved integration with the Feynman Method to transfer concepts with less rework.
- Stronger persistence robustness with automatic backup and reduced redundant writes.
- More defensive loading to recover as much content as possible from partially inconsistent data.
- Better linked-file handling and overall visual workflow.

### 🎓 Feynman Method
- Incoming concepts from Mind Maps are normalized and merged to avoid duplication.
- Richer concept and linked-file previews for faster review.
- Better linked-file opening compatibility across environments.
- Improved stability of internal resources during open/close workflows.

### 🗓️ Calendar and planning
- Expanded calendar experience with monthly and yearly views.
- Better schedule readability through period grouping and richer contextual information.
- Visual highlights to improve orientation for current date and task navigation.

### 🌐 Language, theme, interface, and platform
- Dynamic language switching with immediate text/label updates across screens.
- Better real-time visual synchronization with the application theme/palette.
- Locale and date/time formatting improvements to reduce ambiguity when editing tasks.
- More stable startup on Windows, including icon and visual consistency improvements.
- Additional interface protections to avoid failures in component lifecycle scenarios.

### 🛡️ Data integrity and overall reliability
- Standardized unique task identity to reduce cross-module “mirror tasks”.
- Automatic backups before critical write operations.
- Stricter import/load validations to reduce silent corruption risks.
- Better recovery and continuity experience in inconsistent-data scenarios.

### 🧪 Full functional checklist (manual validation)
1. Create tasks, move them across Kanban/Eisenhower, and verify no unexpected duplicates.
2. Run Pomodoro cycles with pause/resume/skip/reset and confirm progress persistence.
3. Configure Pomodoro sound, validate preview, and alert repetition at cycle end.
4. Switch calendar between monthly/yearly views and validate year filter and period grouping.
5. Export and reimport tasks (JSON/Excel/PDF) to validate data consistency.
6. Send a Mind Map concept to Feynman and confirm update without unintended duplication.
7. Change language/theme while the app is open and verify immediate UI updates.
8. Restart the app and confirm normal data persistence.

### 🧩 Consolidated feature and resource evolution (v2025.11.26.0 → v2026.2.19.0)
- Continuous evolution of the Accessible Reader with local TTS, persistent typography controls, focus ruler, text extraction, and stronger pause/resume stability.
- Expanded Time Management with configurable Pomodoro (focus/break/cycles), cycle-limit blocking, configurable sound alerts, and automatic task progress registration.
- Reinforced Task/Kanban management with editing improvements, drag-and-drop refinements, batch actions, more predictable visual refresh, and more reliable integration with other resources.
- Expanded Eisenhower Matrix with bidirectional sync, task-identity-based deduplication, monthly/yearly calendar views, year filters, and cleaner bulk-removal flows.
- Stronger import/export and persistence with stricter structural validation, consistent JSON/Excel/PDF support, and automatic backups before critical writes.
- Consolidated Mind Map + Feynman integration with concept handoff flow, reduced duplication, better guided review, and more stable linked-file handling.
- Matured platform and interface with dynamic runtime translation, theme/palette synchronization, locale date/time refinements, more robust startup, and better visual consistency on Windows.
- Improved overall reliability with additional defensive UI protections, invalid-state prevention, and safer operational continuity under inconsistent-data scenarios.

## 🚀 Installation (Windows — development)
Minimum requirements:
- Python 3.10+
- Git (optional)

Steps (PowerShell recommended):
1. Clone the repository:
   git clone <repository-URL>
2. Create virtual environment:
   python -m venv .venv
3. Activate (PowerShell):
   .\.venv\Scripts\Activate.ps1
   (or in CMD: .\.venv\Scripts\activate.bat)
4. Install dependencies:
   pip install -r requirements.txt
5. Run in development:
   python main.py

Note: if the system requires PowerShell execution permissions, adjust the execution policy as needed.

## 📦 Packaging for distribution (Windows)
- Recommended: PyInstaller (or Nuitka). Include assets/ and language/translations/ in the .spec 'datas'.
- Generate .qm translation files with:
  pyside6-lrelease language/translations/*.ts
- Include license/notice files in the bundle:
  assets/EULA/, assets/NOTICES/, assets/COPYRIGHT/, assets/CLC/, assets/PRIVACY_POLICY/
- If bundling PySide6, document LGPL compliance procedures according to assets/NOTICES/NOTICE_pt_BR.txt.
- Test the executable folder for replaceable DLLs and redistribution procedures (LGPL).

## ⚙️ Main dependencies
- PySide6, PySide6_Essentials, PySide6_Addons, and shiboken6 — desktop GUI (Qt).
- pyttsx3 and edge-tts — text-to-speech (TTS).
- pdfplumber, pypdfium2, pypdf, and PyPDF2 — PDF reading and processing.
- openpyxl and pandas — data/spreadsheet import and export.
- reportlab — PDF generation/export.
- python-docx and docx2pdf — document handling and conversion.
- spacy, sentence-transformers, transformers, and torch — language/AI capabilities.
- numpy and scikit-learn — numerical foundation and model-processing support.
See the complete pinned dependency list in [`requirements.txt`](./requirements.txt).

## 🛠️ Technical notes
- Logging: utils/LogManager.py (logs at %LOCALAPPDATA%\TEA_TDAH_Dislexia).
- User data (tasks, maps, history, settings, temporary files and logs) are saved at:
  %LOCALAPPDATA%\TEA_TDAH_Dislexia
- Translations: .ts files in language/translations/ — generate .qm before packaging.
- It is recommended to add unit tests for TTS, export and task management.

## ⚠️ Limitations and recommendations
- Initial release: alpha/experimental — may contain stubs and incomplete flows.
- Back up your data before updating or changing executable libraries.
- Input validation (numeric formats, required fields) may need strengthening in some screens.

## 🔒 Privacy and license
- The application runs locally by default and does not send telemetry automatically.
- For details on data handling and consent, see:
  assets/PRIVACY_POLICY/Privacy_Policy_pt_BR.txt
- Terms of use and restrictions: assets/EULA/EULA_pt_BR.txt
- Third‑party notices and licenses: assets/NOTICES/NOTICE_pt_BR.txt
- Copyright and trademark: assets/COPYRIGHT/AVISO DE COPYRIGHT E MARCA REGISTRA_pt_BR.txt
- Commercial agreements: assets/CLC/CLC_pt_BR.txt

## 🔗 Useful shortcuts
- Ctrl+1 — Accessible Reader
- Ctrl+2 — Time Management
- Ctrl+3 — Mind Maps
- Ctrl+4 — Feynman Technique
- ESC — Close focus ruler

## 🧪 Testing and contribution
- Bugs and contributions: open an issue / pull request in the repository (see online README).
- Recommended: add automated tests and CI for builds and packaging.

## 📞 Contact
Author: Fernando Nillsson Cidade  
Email (privacy/licenses): linceu_lighthouse@outlook.com

## 📄 Version and release notes
See assets/RELEASE/RELEASE NOTES_pt_BR.txt and assets/RELEASE/RELEASE NOTES_en_US.txt for version history and important changes.
- Advanced notes (technical deep dive):
  - assets/RELEASE/RELEASE NOTES_en_US_Advanced.txt

---

</details>
