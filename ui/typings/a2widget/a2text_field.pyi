from a2qt import QtWidgets

class A2TextField(QtWidgets.QPlainTextEdit):
    pass

class A2CodeField(A2TextField):
    """
    Subclassed `A2TextField` with monospaced font. Auto-adjusts its height.
    """
    pass
