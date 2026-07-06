"""
AI CODE REVIEW ASSISTANT - Premium Claude/GPT Style UI
Run with: python main.py
"""

import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# ============================================================
# ✅ YOUR API KEY
# ============================================================

GROQ_API_KEY = "" 

# ============================================================
# Code Review Worker (Thread)
# ============================================================

class CodeReviewWorker(QThread):
    finished = pyqtSignal(str, str)
    
    def __init__(self, code, category, prompt):
        super().__init__()
        self.code = code
        self.category = category
        self.prompt = prompt
    
    def run(self):
        try:
            from groq import Groq
            import httpx
            
            client = Groq(
                api_key=GROQ_API_KEY,
                http_client=httpx.Client(timeout=30.0)
            )
            
            full_prompt = f"""
            Review this code for {self.prompt}:
            
            {self.code}
            
            Be specific. Point to exact lines.
            Give actionable feedback.
            Keep it short and direct.
            Format with bullet points using •.
            """
            
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.3,
                max_tokens=400
            )
            
            result = response.choices[0].message.content
            self.finished.emit(self.category, result)
            
        except Exception as e:
            self.finished.emit(self.category, f"❌ Error: {str(e)}")

# ============================================================
# Main Window - Claude Style
# ============================================================

class CodeReviewAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeHawk")
        self.setGeometry(100, 100, 1400, 850)
        self.setMinimumSize(1200, 700)
        self.setStyleSheet("""
            QMainWindow {
                background: #0d0d1a;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #2a2a3e;
                border-radius: 3px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3a3a5e;
            }
            QScrollBar:horizontal {
                background: transparent;
                height: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:horizontal {
                background: #2a2a3e;
                border-radius: 3px;
                min-width: 30px;
            }
        """)
        
        self.workers = []
        self.init_ui()
    
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ============================================================
        # LEFT PANEL - Code Input (60%)
        # ============================================================
        
        left_panel = QWidget()
        left_panel.setStyleSheet("""
            QWidget {
                background: #0d0d1a;
                border-right: 1px solid #1a1a2e;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(30, 30, 30, 30)
        left_layout.setSpacing(15)
        
        # Header
        header = QHBoxLayout()
        header.setSpacing(10)
        
        icon_label = QLabel("📝")
        icon_label.setStyleSheet("font-size: 24px;")
        header.addWidget(icon_label)
        
        title_label = QLabel("Code Input")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e2e2f0;
            font-family: 'Segoe UI', sans-serif;
        """)
        header.addWidget(title_label)
        header.addStretch()
        
        # Language selector
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Ruby", "PHP", "Swift"])
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background: #1a1a2e;
                color: #a0a0b8;
                border: 1px solid #2a2a3e;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
                min-width: 120px;
            }
            QComboBox:hover {
                border-color: #6c63ff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QComboBox QAbstractItemView {
                background: #1a1a2e;
                color: #e2e2f0;
                border: 1px solid #2a2a3e;
                selection-background-color: #6c63ff;
                padding: 4px;
            }
        """)
        header.addWidget(self.lang_combo)
        
        left_layout.addLayout(header)
        
        # Code input area with line numbers (simulated)
        code_container = QFrame()
        code_container.setStyleSheet("""
            QFrame {
                background: #111122;
                border: 1px solid #1a1a2e;
                border-radius: 12px;
            }
        """)
        code_layout = QVBoxLayout(code_container)
        code_layout.setContentsMargins(0, 0, 0, 0)
        
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("""
// Paste your code here...
// AI will review it for bugs, performance,
// quality, security, and improvements.

Example:
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
        """.strip())
        self.code_input.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                color: #d4d4e8;
                font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                padding: 20px;
                line-height: 1.8;
            }
            QTextEdit:focus {
                border: none;
            }
        """)
        code_layout.addWidget(self.code_input)
        
        left_layout.addWidget(code_container, stretch=1)
        
        # Bottom buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.review_btn = QPushButton("🔍 Review Code")
        self.review_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6c63ff, stop:1 #8b7cf7);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px 32px;
                font-size: 15px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c73ff, stop:1 #9b8cf7);
            }
            QPushButton:disabled {
                background: #2a2a3e;
                color: #6a6a80;
            }
        """)
        self.review_btn.clicked.connect(self.start_review)
        btn_layout.addWidget(self.review_btn)
        
        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #8a8aa0;
                border: 1px solid #2a2a3e;
                border-radius: 10px;
                padding: 14px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #1a1a2e;
                color: #e2e2f0;
                border-color: #4a4a5e;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_all)
        btn_layout.addWidget(self.clear_btn)
        
        btn_layout.addStretch()
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            color: #6a6a80;
            font-size: 13px;
            font-weight: 500;
        """)
        btn_layout.addWidget(self.status_label)
        
        left_layout.addLayout(btn_layout)
        
        # ============================================================
        # RIGHT PANEL - Review Results (40%)
        # ============================================================
        
        right_panel = QWidget()
        right_panel.setStyleSheet("""
            QWidget {
                background: #0d0d1a;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(25, 30, 30, 30)
        right_layout.setSpacing(15)
        
        # Header
        result_header = QHBoxLayout()
        result_header.setSpacing(10)
        
        result_icon = QLabel("📊")
        result_icon.setStyleSheet("font-size: 24px;")
        result_header.addWidget(result_icon)
        
        result_title = QLabel("Review Results")
        result_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e2e2f0;
            font-family: 'Segoe UI', sans-serif;
        """)
        result_header.addWidget(result_title)
        result_header.addStretch()
        
        right_layout.addLayout(result_header)
        
        # Tab widget for results
        self.results_tabs = QTabWidget()
        self.results_tabs.setStyleSheet("""
            QTabWidget::pane {
                background: #111122;
                border: 1px solid #1a1a2e;
                border-radius: 12px;
                padding: 4px;
            }
            QTabBar::tab {
                background: transparent;
                color: #8a8aa0;
                padding: 10px 18px;
                margin: 2px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: #1a1a2e;
                color: #e2e2f0;
            }
            QTabBar::tab:hover {
                background: #1a1a2e;
                color: #e2e2f0;
            }
        """)
        
        self.results = {}
        categories = [
            ("🐛 Bugs", "bugs", "#ef4444"),
            ("⚡ Performance", "performance", "#f59e0b"),
            ("📝 Quality", "quality", "#3b82f6"),
            ("🔒 Security", "security", "#8b5cf6"),
            ("💡 Improvements", "improvements", "#22c55e")
        ]
        
        for label, key, color in categories:
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(12, 12, 12, 12)
            
            # Header with icon and color
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 0, 0, 8)
            
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 18px;")
            header_layout.addWidget(dot)
            
            cat_label = QLabel(label)
            cat_label.setStyleSheet(f"""
                color: {color};
                font-size: 14px;
                font-weight: 700;
            """)
            header_layout.addWidget(cat_label)
            header_layout.addStretch()
            
            container_layout.addWidget(header_widget)
            
            # Text area
            text = QTextEdit()
            text.setReadOnly(True)
            text.setPlaceholderText(f"{label} analysis will appear here...")
            text.setStyleSheet("""
                QTextEdit {
                    background: transparent;
                    border: none;
                    color: #d4d4e8;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 13px;
                    line-height: 1.8;
                    padding: 4px;
                }
                QTextEdit:focus {
                    border: none;
                }
            """)
            container_layout.addWidget(text)
            
            self.results_tabs.addTab(container, label)
            self.results[key] = text
        
        right_layout.addWidget(self.results_tabs, stretch=1)
        
        # ============================================================
        # Add panels to main layout
        # ============================================================
        
        main_layout.addWidget(left_panel, 6)  # 60%
        main_layout.addWidget(right_panel, 4)  # 40%
        
        # Set focus to code input
        self.code_input.setFocus()
    
    def start_review(self):
        code = self.code_input.toPlainText().strip()
        if not code:
            QMessageBox.warning(self, "Error", "Please paste some code first!")
            return
        
        # Clear previous results
        for key, widget in self.results.items():
            widget.clear()
        
        self.review_btn.setEnabled(False)
        self.status_label.setText("⏳ AI is reviewing...")
        
        reviews = [
            ("bugs", "Find ALL bugs. Point to exact lines. Be specific and direct."),
            ("performance", "Find performance issues. Point to exact lines. Be specific."),
            ("quality", "Analyze code quality. Suggest improvements for readability."),
            ("security", "Find security vulnerabilities. Be specific."),
            ("improvements", "Suggest specific improvements with code examples.")
        ]
        
        self.workers = []
        
        for key, prompt in reviews:
            worker = CodeReviewWorker(code, key, prompt)
            worker.finished.connect(lambda k, r, kk=key: self.show_result(kk, r))
            worker.finished.connect(self.on_worker_done)
            worker.start()
            self.workers.append(worker)
    
    def show_result(self, key, result):
        self.results[key].setHtml(f"""
            <div style='padding: 4px;'>
                <pre style='color: #d4d4e8; font-family: Segoe UI, sans-serif; font-size: 13px; 
                           line-height: 1.8; white-space: pre-wrap; margin: 0;'>
{result}
                </pre>
            </div>
        """)
    
    def on_worker_done(self):
        all_done = all(not w.isRunning() for w in self.workers)
        if all_done:
            self.review_btn.setEnabled(True)
            self.status_label.setText("✅ Review complete!")
            self.workers = []
            
            # Switch to first tab
            self.results_tabs.setCurrentIndex(0)
    
    def clear_all(self):
        self.code_input.clear()
        for key, widget in self.results.items():
            widget.clear()
        self.status_label.setText("Ready")
        if self.workers:
            for w in self.workers:
                w.terminate()
            self.workers = []
        self.review_btn.setEnabled(True)
        self.code_input.setFocus()

# ============================================================
# Run
# ============================================================

def main():
    app = QApplication(sys.argv)
    
    # Set application icon and style
    app.setStyle("Fusion")
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = CodeReviewAssistant()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()