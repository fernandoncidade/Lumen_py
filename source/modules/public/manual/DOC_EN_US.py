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
    if lang == "pt_BR":
        try:
            from . import DOC_PT_BR
            return getattr(DOC_PT_BR, "_DOC_PT_BR", tuple())

        except Exception:
            return tuple()

    return _DOC_EN_US

# ----------------------------
# Conteúdo do manual (texto)
# ----------------------------

_DOC_EN_US: tuple[ManualSection, ...] = (
    ManualSection(
        id="overview",
        title="Overview",
        paragraphs=(
            "Lúmen is a study tool suite composed of core modules: Accessible Reader, Time Management (Pomodoro and task manager), "
            "Mind Maps, Feynman Method, and Eisenhower Matrix. The interface is organized into tabs; each tab contains controls "
            "and tools specific to its module.",
        ),
    ),
    ManualSection(
        id="basic-requirements-user",
        title="Basic Requirements (User)",
        bullets=(
            "Windows (tested).",
            "Internet connection for Edge TTS (optional).",
        ),
    ),
    ManualSection(
        id="how-to-start-the-application",
        title="How to Start the Application",
        bullets=(
            "Open the application and select the tab of the module you want to use.",
            "In the Reader: load a document or paste text into the reading area; adjust font and zoom.",
            "To listen: use the Read button to start TTS; use Pause or Stop as needed.",
            "In Time Management: create tasks, start Pomodoro for focus, and log progress.",
            "In Mind Maps and Feynman: create, edit, and save your projects.",
            "In Eisenhower: categorize tasks and reorganize by priority.",
        ),
    ),
    ManualSection(
        id="startup-and-global-controls",
        title="Startup and Global Controls",
        paragraphs=(
            "When opening Lúmen, you will see the main window with tabs and a menu bar (File, Settings, Languages, Voices, About). "
            "The status bar displays contextual information.",
        ),
    ),
    ManualSection(
        id="modules",
        title="Modules (Detailed by Tab)",
        details=(
            ManualDetails(
                summary="Accessible Reader — Tab 1",
                paragraphs=(
                    "The Accessible Reader is designed so anyone can open, read and listen to documents without technical knowledge."
                    " Use it to read PDFs, paste text, or open text files, listen to content with natural voices, and follow along with visual highlights.",
                    "The workflow is straightforward: open or paste the text, choose a voice (optional), adjust volume and speed, and press 'Read'. During playback you can pause, resume or stop reading, and see the text highlighted as it is spoken.",
                ),
                bullets=(
                    "Open file: go to File → Open (or press Ctrl+O) and select a PDF or text file. The content will load into the reading area.",
                    "Paste text: paste directly into the reading area if you prefer to listen to a copied excerpt.",
                    "Select voice: open the Voices menu and choose the desired voice; neural voices usually sound more natural.",
                    "Start reading: click ▶️ Read (or use the shortcut) to begin listening to the current text.",
                    "Pause/resume: use ⏸️ Pause to temporarily stop and click again to resume from the same point.",
                    "Stop: ⏹️ Stop halts reading and clears the queue; to listen again press Read.",
                    "Speed and volume: use the sliders to make the voice slower/faster and set the desired volume.",
                    "Speech highlighting: while listening, words or sentences can be highlighted in the text to help follow along visually.",
                    "Focus ruler: enable the ruler to isolate a line or area of the page — useful for reading aloud or concentrating; close with ESC or the ruler button.",
                    "Zoom and font: adjust font size and zoom in the reading area for visual comfort; preferences are remembered by the app.",
                    "Text search: use the Find field (Ctrl+F) to locate words or phrases within the loaded document.",
                    "Select and save: select text to copy or use 'Save As' to export the read text as a .txt file.",
                    "PDFs without text: if a PDF is image-based (e.g., scanned), the app may not extract text automatically — OCR from external tools may be required.",
                    "Export audio: it's possible to generate audio files (when available) to listen offline or share; remove temporary files using the app's audio manager.",
                    "Quick tips: focus on short passages when studying, increase speed for review, and use the ruler to follow line by line.",
                ),
            ),
            ManualDetails(
                summary="Time Management — Tab 2",
                paragraphs=(
                    "The Time Management tab combines a configurable Pomodoro timer with a Kanban-style task manager.",
                    "Use this module to plan study or work sessions, focus on a single task at a time, and track your progress in a simple, visual way.",
                ),
                bullets=(
                    "Add task: type the title in the field and click '➕ Add' or press Enter.",
                    "Set priority: choose from the priority list (colored circles) to organize what is most urgent or important.",
                    "Organize with Kanban: drag tasks between the 'Todo', 'Doing' and 'Done' columns to reflect current work status.",
                    "Start a session: select the task you want to work on (in the 'Doing' column) and click '▶️ Start' to begin a Pomodoro.",
                    "Pause and resume: use the same button to pause; click again to resume the timer without losing progress.",
                    "Skip or reset: use '⏭️ Skip' to move to the next cycle or '⏱️ Reset Clock' to restart the current timer.",
                    "Adjust durations: change focus and break minutes in the quick settings — changes apply to subsequent cycles.",
                    "Automatic logging: when a focus cycle ends with a selected task, the system logs a Pomodoro for that task to help track productivity.",
                    "Progress count: check how many Pomodoros have been completed per task in the list or session history.",
                    "Complete a task: when finished, move the task to 'Done' or use the context menu to mark it as completed.",
                    "Optional integration: enable integration with the Eisenhower Matrix to send/receive tasks between modules and keep your schedule synchronized.",
                    "Alerts and sound: the module can notify with sound and notifications at cycle end — check system volume and permissions if you don't hear an alert.",
                    "Quick tips: focus on one task per Pomodoro, take short regular breaks, and adjust times to match your personal rhythm.",
                ),
            ),
            ManualDetails(
                summary="Mind Maps — Tab 3",
                paragraphs=(
                    "Mind Maps is a visual area where you organize ideas as nodes connected by lines."
                    " Use it to capture thoughts, structure projects, plan study sessions, and recall concepts visually.",
                ),
                bullets=(
                    "Create new map: start an empty map to begin from scratch.",
                    "Add ideas: click 'Add node' or the corresponding button to insert a new item; give it a short, clear title.",
                    "Edit text: double-click a node to change its content; keep sentences short to improve readability.",
                    "Connect nodes: use the 'Connect' option or drag from one node to another to create visual relationships between ideas.",
                    "Reorganize: drag nodes with the mouse to reposition them; release when you are satisfied with the layout.",
                    "Zoom and pan: zoom in/out to see details and drag empty space to move the map across the canvas.",
                    "Save project: use 'File → Save' or 'Save As' to persist your map and resume it later.",
                    "Export image: choose 'Export' to generate a PNG of the map for sharing or inserting into documents.",
                    "Undo/redo: use the undo/redo buttons to correct accidental changes.",
                    "Delete/edit connections: select a link to remove it, or edit labels when available.",
                    "Hierarchy navigation: expand/collapse groups of nodes to focus on specific parts of the map.",
                    "Best practices: start with a central node representing the main theme; keep branches short and use keywords instead of long sentences.",
                ),
            ),
            ManualDetails(
                summary="Feynman Method — Tab 4",
                paragraphs=(
                    "A tool designed to help you learn any topic by explaining it in your own words. ",
                    "The workflow guides you through simple steps: explain accessibly, identify what you don't understand, research, and then simplify again.",
                    "Everything is built to be used without technical knowledge: just write, review, and save. Your concepts are stored in a list for later reference.",
                ),
                bullets=(
                    "➕ New: click to create a new concept; start by giving it a clear title (e.g., 'Shear Stress').",
                    "1️⃣ Concept: in the title field, write the name of the topic you want to learn.",
                    "2️⃣ Explain Simply: write the explanation as if teaching someone with no prior knowledge; use everyday examples and short sentences.",
                    "3️⃣ Identified Gaps: note where you had doubts or couldn't explain — these points guide your research.",
                    "4️⃣ Review: after researching, rewrite the explanation more clearly and completely; this is when you consolidate learning.",
                    "📊 Mastery Level: choose the level that represents your command (Beginner / Intermediate / Advanced) to track progress.",
                    "💾 Save Concept: use the '💾 Save Concept' button to persist the concept; it will appear in the list on the left.",
                    "Concept List: select an item to open and edit its content; the list shows a domain marker (colors) to quickly identify your progress.",
                    "🗑️ Delete: remove concepts you no longer need using the '🗑️ Delete' button (a confirmation is shown before removal).",
                    "Reset Level: right-click a concept in the list for '🎯 Reset Mastery Level' and adjust it without opening the item.",
                    "Practical tips: be specific in the title, use simple analogies, avoid jargon, and review concepts periodically.",
                ),
            ),
            ManualDetails(
                summary="Eisenhower Matrix — Tab 5",
                paragraphs=(
                    "The Eisenhower Matrix helps you prioritize tasks by dividing them into four quadrants based on urgency and importance. "
                    "In this tab you can create, schedule, move, and complete tasks visually and simply, without needing technical knowledge.",
                ),
                bullets=(
                    "Add task: type the task in the 'Add a task...' field and click 'Add Task'.",
                    "Link date and time: check 'Link date' (and 'Link time' if desired) before adding to schedule the task on a specific date/time.",
                    "Choose quadrant: select the appropriate quadrant in the selector before adding; otherwise, move the task later to the correct quadrant.",
                    "Move tasks: drag and drop between quadrants to reorganize, or use the context menu (right-click) for quick options.",
                    "Mark as completed: check the box next to the task to move it to the corresponding 'Completed' list; uncheck to restore it.",
                    "Edit task: open the context menu on a task to edit text, date, time, description, or attach/open linked files.",
                    "Remove task: choose 'Remove' in the context menu; a confirmation will appear to prevent accidental deletions.",
                    "Placeholders and tips: empty lists show guidance text (e.g., '1st Quadrant') to indicate where to add tasks.",
                    "Calendar panel: use the 'Calendar' button to view all scheduled tasks by date; click a date to view and open tasks linked to that day.",
                    "Save and export: tasks are persisted by the app; use 'Save As' when you want to export in supported formats (JSON/Excel/PDF).",
                    "Best practices: keep each task short and focused, use dates only for real commitments, and review the matrix regularly to update priorities.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="menus-and-quick-actions",
        title="Menus and Quick Actions",
        bullets=(
            "File: load and save projects, export maps, import tasks (when available).",
            "Settings: language, voices, and default font.",
            "Languages: changes UI language and strings.",
            "Help: version and quick documentation.",
        ),
    ),
    ManualSection(
        id="combined-usage-suggestions",
        title="Combined Usage Suggestions",
        bullets=(
            "Reading and Pomodoro: open material in the Reader, enable focus ruler, link a task, and start a session.",
            "Mind Maps and Feynman: turn nodes into explanations and review later.",
            "Eisenhower: prioritize weekly and plan Pomodoros for what matters.",
        ),
    ),
    ManualSection(
        id="new-features",
        title="New Features (How to Use)",
        details=(
            ManualDetails(
                summary="Mind Map Integration -> Feynman Method",
                bullets=(
                    "In Mind Maps, double-click a node to open editing and fill in concept notes/review.",
                    "Click '➕ Integrate into Feynman Method' to send the node content automatically.",
                    "Open the Feynman Method tab and confirm the concept in the list; if it already exists, the app merges content without duplicating the title.",
                    "When you update a node and integrate again, review and complementary fields are preserved in the existing concept.",
                ),
            ),
            ManualDetails(
                summary="Linked Files in Feynman (Preview and Open)",
                bullets=(
                    "Link a file to the concept (in node editing or in the concept flow) to keep supporting material with your study.",
                    "Hover over the concept in the list to see a structured preview (Concept, Explain, Gaps, Review, and linked file).",
                    "Use CTRL + double-click on the node (Mind Maps) to quickly open the linked file.",
                    "If the file was moved/deleted, the app shows a warning instead of failing silently; relink the correct path.",
                ),
            ),
            ManualDetails(
                summary="Time Management with Enhanced Drag and Drop",
                bullets=(
                    "Drag tasks between columns and also over tabs: the destination tab can open automatically during drag.",
                    "Drop the task on the tab header to move it without losing the item, including when there is a single selection.",
                    "In the new task field, you can press Enter to add immediately.",
                    "You can also drag and drop files/text into the task field when supported by the system.",
                ),
            ),
            ManualDetails(
                summary="Collapsible Calendar Panel (Eisenhower)",
                bullets=(
                    "In the Eisenhower Matrix, use the calendar button to switch between 'Show Calendar' and 'Collapse Calendar'.",
                    "With the panel open, select a date to list tasks linked to that day.",
                    "With the panel collapsed, you get more space to prioritize tasks in the quadrants.",
                ),
            ),
            ManualDetails(
                summary="Configurable Pomodoro Sound",
                bullets=(
                    "Go to Settings -> Sound to choose the Pomodoro bell.",
                    "Use '▶️ Play' to test the audio before saving.",
                    "Adjust the interval between repeats; when a cycle ends, the alert plays immediately and repeats until you close the window.",
                    "Sound and interval preferences are saved for upcoming cycles.",
                ),
            ),
            ManualDetails(
                summary="Automatic Mind Map Backup",
                bullets=(
                    "Edit your map normally and save your project; automatic backup starts protecting changes in the background.",
                    "If there is no real change in the map, the app automatically avoids unnecessary rewrites.",
                    "When loading maps with partial/invalid data, the system tries to recover as much as possible instead of aborting everything.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="troubleshooting",
        title="Troubleshooting",
        details=(
            ManualDetails(
                summary="No sound",
                bullets=(
                    "Check system and application volume.",
                    "If using Edge TTS, confirm Internet connectivity.",
                ),
            ),
            ManualDetails(
                summary="PDF without text",
                bullets=(
                    "The PDF may be image-based; OCR may be required.",
                    "If applicable, check libraries such as pdfplumber and pypdf.",
                ),
            ),
            ManualDetails(
                summary="Voices not listed",
                bullets=("Reload voices or restart the app.",),
            ),
            ManualDetails(
                summary="Error saving or reading",
                bullets=(
                    "Check data folder permissions.",
                    "See logs for details.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="logs-and-diagnostics",
        title="Logs and Diagnostics",
        bullets=("LogManager generates logs; check the app data folder at AppData\\Local\\Lumen\\logs (on Windows).",),
    ),
    ManualSection(
        id="storage",
        title="Storage / Persistent Files (Summary)",
        bullets=(
            "Tasks: JSON (for example, tasks.json).",
            "Maps: project files (for example, .map or .json).",
            "Feynman concepts: concepts.json.",
            "Settings: config.json.",
            "Suggested location: AppData\\Local\\Lumen (on Windows).",
        ),
    ),
    ManualSection(
        id="best-practices",
        title="Best Practices",
        bullets=(
            "Save maps and concepts regularly.",
            "Perform periodic backups.",
            "Keep the app and dependencies up to date.",
        ),
    ),
    ManualSection(
        id="shortcuts",
        title="Quick Shortcut Summary",
        bullets=(
            "Ctrl+1 — 📖 Accessible Reader ",
            "Ctrl+2 — ⏱️ Time Management ",
            "Ctrl+3 — 🧠 Mind Maps",
            "Ctrl+4 — 🎓 Feynman Method",
            "Ctrl+5 — 🗂️ Eisenhower Matrix",
            "Ctrl+O — 📂 Load PDF",
            "Ctrl+R — ▶️ Read",
            "Ctrl+P — ⏸️ Pause",
            "Ctrl+T — ➕ Add",
            "Ctrl+N — ➕ Add Concept",
            "Ctrl+S — 💾 Save",
            "Ctrl+L — 📂 Load",
            "Ctrl+F — 🔎 Search",
            "Ctrl+Shift+F — 🔤 Font...",
            "Ctrl+Shift+S — 🔔 Sound...",
            "Ctrl+Q — ❌ Exit",
            "F1 — ❓ Help",
        ),
    ),
    ManualSection(
        id="faq",
        title="FAQ (Frequently Asked Questions)",
        details=(
            ManualDetails(
                summary="How do I make the voice more natural?",
                paragraphs=("Use Edge TTS (neural voices) and adjust speed and volume.",),
            ),
            ManualDetails(
                summary="Where are my data saved?",
                paragraphs=("In the app data directory (Windows: AppData\\Local\\Lumen).",),
            ),
        ),
    ),
    ManualSection(
        id="support",
        title="How to Get Help / Support",
        bullets=(
            "Use the Help menu for version and documentation.",
            "For technical issues, attach logs when opening an issue. Contact: linceu_lighthouse@outlook.com.",
        ),
    ),
)

__all__ = ["_DOC_EN_US"]
