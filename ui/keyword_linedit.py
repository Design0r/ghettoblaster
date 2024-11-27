from typing import Iterable
from Qt.QtWidgets import QLineEdit, QAction, QMenu
from Qt.QtCore import Qt
from functools import partial


class KeywordLineedit(QLineEdit):
    def __init__(self, keywords: Iterable[str], parent=None) -> None:
        super().__init__(parent)
        self.keywords = keywords

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self, point) -> None:
        pop_menu = QMenu(self)

        for i in self.keywords:
            description = (
                f"Insert {i.replace('<', '').replace('>', '').lower()} name {i}"
            )
            action = QAction(description, self)
            action.triggered.connect(partial(self.insert_keyword, i))
            pop_menu.addAction(action)

        pop_menu.exec_(self.mapToGlobal(point))

    def insert_keyword(self, keyword: str) -> None:
        curr_text = self.text()
        cursor_pos = self.cursorPosition()
        right, left = curr_text[cursor_pos:], curr_text[:cursor_pos]

        new_text = f"{left}{keyword}{right}"
        self.setText(new_text)
