import a2ctrl.connect
from a2qt import QtWidgets
from a2element import DrawCtrl, EditCtrl
from a2widget.a2text_field import A2TextField


class Draw(DrawCtrl):
    """
    The frontend widget visible to the user with options
    to change the default behavior of the element.
    """

    def __init__(self, *args):
        super(Draw, self).__init__(*args)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        text = self.cfg.get('text', 'Nothing yet').replace('\n', '<br>')

        # TODO: This might be used in other places. Make it a DrawCtrl method?
        if '%module_path%' in text:
            text = text.replace('%module_path%', self.mod.path)

        self.label = QtWidgets.QLabel(text, self)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(True)
        self.main_layout.addWidget(self.label)
        self.setLayout(self.main_layout)


class Edit(EditCtrl):
    """
    The background widget that sets up how the user can edit the element,
    visible when editing the module.
    """

    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg)

        self.mainLayout.addWidget(QtWidgets.QLabel('Some text to show in the module frontend:'))
        self.text_field = A2TextField()
        self.mainLayout.addWidget(self.text_field)
        a2ctrl.connect.control(self.text_field, 'text', self.cfg)

    @staticmethod
    def element_name():
        """The elements display name shown in UI"""
        return 'Label'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.text


def get_settings(module_key, cfg, db_dict, user_cfg):
    pass
