from dataclasses import dataclass, field
from collections import deque as Queue
from typing import Protocol

class Operation(Protocol):
    def execute(self) -> str:
        ...

    def get_opposite_operation(self, text: str) -> 'Operation':
        ...

class Insert(Operation):
    def __init__(self, text_to_insert: str):
        self.text_to_insert = text_to_insert

    def execute(self, text: str) -> str:
        return text + self.text_to_insert
    
    def get_opposite_operation(self, text: str) -> 'Delete':
        return Delete(num_chars=len(self.text_to_insert))

class Delete(Operation):
    def __init__(self, num_chars: int):
        self.num_chars = num_chars

    def execute(self, text: str) -> str:
        return text[:-self.num_chars]
    
    def get_opposite_operation(self, text: str) -> 'Insert':
        return Insert(text[-self.num_chars:])

@dataclass
class TextEditor:
    text: str = ""
    _queue_undo: Queue = field(default_factory=Queue, init=False)
    _queue_redo: Queue = field(default_factory=Queue, init=False)

    def insert(self, text: str) -> None:
        operation = Insert(text)
        self._do(operation)

    def delete(self, num_chars: int) -> None:
        operation = Delete(num_chars)
        self._do(operation)

    def _do(self, operation: Operation) -> None:
        opposite_operation = operation.get_opposite_operation(self.text)
        self._execute_operation(operation)
        self._queue_undo.append(opposite_operation)
        self._empty_queue(self._queue_redo)

    def undo(self) -> None:
        operation = self._get_from_queue(self._queue_undo)
        if operation:
            opposite_operation = operation.get_opposite_operation(self.text)
            self._execute_operation(operation)
            self._queue_redo.append(opposite_operation)

    def redo(self) -> None:
        operation = self._get_from_queue(self._queue_redo)
        if operation:
            opposite_operation = operation.get_opposite_operation(self.text)
            self._execute_operation(operation)
            self._queue_undo.append(opposite_operation)

    def _execute_operation(self, operation: Operation) -> None:
        self.text = operation.execute(self.text)

    def print_text(self) -> None:
        print(self.text)

    def _get_from_queue(self, queue: Queue) -> Operation | None:
        if queue:
            return queue.pop()
        else:
            None

    def _empty_queue(self, queue: Queue) -> None:
        while queue:
            queue.pop()


def main() -> None:
    # Test the text editor
    editor = TextEditor()

    # Since there is no text, these commands should do nothing
    editor.undo()
    editor.redo()

    editor.insert("Hello")
    editor.insert(" World!")
    editor.print_text()  # Output: Hello World!

    editor.delete(6)
    editor.print_text()  # Output: Hello

    editor.undo()
    editor.print_text()  # Output: Hello World!

    editor.redo()
    editor.print_text()  # Output: Hello

    editor.insert("!!!")
    editor.print_text()  # Output: Hello!!!

    editor.undo()
    editor.undo()
    editor.print_text()  # Output: Hello World!


if __name__ == "__main__":
    main()
