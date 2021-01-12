# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'a2settings_advanced.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2path_field import A2PathField
from a2widget.a2slider import A2Slider


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")

        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.a2scroll_area_background = QWidget()
        self.a2scroll_area_background.setObjectName(u"a2scroll_area_background")
        self.a2scroll_area_background.setGeometry(QRect(0, 0, 815, 769))
        self.formLayout_3 = QFormLayout(self.a2scroll_area_background)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.ui_scale_label = QLabel(self.a2scroll_area_background)
        self.ui_scale_label.setObjectName(u"ui_scale_label")
        self.ui_scale_label.setText(u"UI Scale:")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.ui_scale_label)

        self.ui_scale_slider = A2Slider(self.a2scroll_area_background)
        self.ui_scale_slider.setObjectName(u"ui_scale_slider")
        self.ui_scale_slider.setDecimals(2)
        self.ui_scale_slider.setMinimum(0.500000000000000)
        self.ui_scale_slider.setMaximum(2.000000000000000)
        self.ui_scale_slider.setSingleStep(0.050000000000000)
        self.ui_scale_slider.setValue(1.000000000000000)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.ui_scale_slider)

        self.hotkey_box = QGroupBox(self.a2scroll_area_background)
        self.hotkey_box.setObjectName(u"hotkey_box")
        self.hotkey_box.setTitle(u"Hotkey Dialog")
        self.formLayout_4 = QFormLayout(self.hotkey_box)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setContentsMargins(-1, 25, -1, -1)
        self.label_7 = QLabel(self.hotkey_box)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setText(u"Style:")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_7)

        self.hk_dialog_style = QComboBox(self.hotkey_box)
        self.hk_dialog_style.setObjectName(u"hk_dialog_style")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.hk_dialog_style)

        self.label_13 = QLabel(self.hotkey_box)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setText(u"Keyboard Layout:")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_13)

        self.hk_dialog_layout = QComboBox(self.hotkey_box)
        self.hk_dialog_layout.setObjectName(u"hk_dialog_layout")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.hk_dialog_layout)


        self.formLayout_3.setWidget(2, QFormLayout.SpanningRole, self.hotkey_box)

        self.dev_box = QGroupBox(self.a2scroll_area_background)
        self.dev_box.setObjectName(u"dev_box")
        self.dev_box.setTitle(u"a2 dev mode")
        self.dev_box.setCheckable(True)
        self.verticalLayout_3 = QVBoxLayout(self.dev_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 25, -1, -1)
        self.dev_widget = QWidget(self.dev_box)
        self.dev_widget.setObjectName(u"dev_widget")
#if QT_CONFIG(accessibility)
        self.dev_widget.setAccessibleDescription(u"")
#endif // QT_CONFIG(accessibility)
        self.formLayout_2 = QFormLayout(self.dev_widget)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_4 = QLabel(self.dev_widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setText(u"Author Name:")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.author_name = QLineEdit(self.dev_widget)
        self.author_name.setObjectName(u"author_name")
        self.author_name.setText(u"")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.author_name)

        self.label_6 = QLabel(self.dev_widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setText(u"Author Homepage:")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_6)

        self.author_url = QLineEdit(self.dev_widget)
        self.author_url.setObjectName(u"author_url")
        self.author_url.setText(u"")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.author_url)

        self.label_5 = QLabel(self.dev_widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setText(u"Default Code Editor:")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.code_editor = A2PathField(self.dev_widget)
        self.code_editor.setObjectName(u"code_editor")
        self.code_editor.setText(u"")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.code_editor)

        self.label_8 = QLabel(self.dev_widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setText(u"Autohotkey Executable:")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_8)

        self.autohotkey = A2PathField(self.dev_widget)
        self.autohotkey.setObjectName(u"autohotkey")
        self.autohotkey.setEnabled(False)
        self.autohotkey.setText(u"")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.autohotkey)

        self.line = QFrame(self.dev_widget)
        self.line.setObjectName(u"line")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QSize(100, 0))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.formLayout_2.setWidget(10, QFormLayout.SpanningRole, self.line)

        self.label_2 = QLabel(self.dev_widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setText(u"User Data:")

        self.formLayout_2.setWidget(11, QFormLayout.LabelRole, self.label_2)

        self.data_folder = A2PathField(self.dev_widget)
        self.data_folder.setObjectName(u"data_folder")
        self.data_folder.setEnabled(False)
        self.data_folder.setText(u"")

        self.formLayout_2.setWidget(11, QFormLayout.FieldRole, self.data_folder)

        self.label_10 = QLabel(self.dev_widget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setText(u"Python Executable:")

        self.formLayout_2.setWidget(14, QFormLayout.LabelRole, self.label_10)

        self.python_executable = A2PathField(self.dev_widget)
        self.python_executable.setObjectName(u"python_executable")
        self.python_executable.setEnabled(False)
        self.python_executable.setText(u"")

        self.formLayout_2.setWidget(14, QFormLayout.FieldRole, self.python_executable)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.button_set_user_dir_standard = QPushButton(self.dev_widget)
        self.button_set_user_dir_standard.setObjectName(u"button_set_user_dir_standard")
        self.button_set_user_dir_standard.setText(u"Set Standard Dir")

        self.horizontalLayout_4.addWidget(self.button_set_user_dir_standard)

        self.button_set_user_dir_custom = QPushButton(self.dev_widget)
        self.button_set_user_dir_custom.setObjectName(u"button_set_user_dir_custom")
        self.button_set_user_dir_custom.setText(u"Set Override Path")

        self.horizontalLayout_4.addWidget(self.button_set_user_dir_custom)


        self.formLayout_2.setLayout(12, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.portable_label = QLabel(self.dev_widget)
        self.portable_label.setObjectName(u"portable_label")
        self.portable_label.setWordWrap(True)

        self.formLayout_2.setWidget(13, QFormLayout.FieldRole, self.portable_label)

        self.json_indent = QSpinBox(self.dev_widget)
        self.json_indent.setObjectName(u"json_indent")
        self.json_indent.setMaximumSize(QSize(70, 16777215))

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.json_indent)

        self.label_9 = QLabel(self.dev_widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setText(u"JSON Indent:")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_9)

        self.auto_reload = QCheckBox(self.dev_widget)
        self.auto_reload.setObjectName(u"auto_reload")
        self.auto_reload.setText(u"Auto-Reload Runtime On Script Changes")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.auto_reload)


        self.verticalLayout_3.addWidget(self.dev_widget)


        self.formLayout_3.setWidget(5, QFormLayout.SpanningRole, self.dev_box)

        self.proxy_box = QGroupBox(self.a2scroll_area_background)
        self.proxy_box.setObjectName(u"proxy_box")
        self.proxy_box.setTitle(u"Use a Proxy")
        self.proxy_box.setCheckable(True)
        self.proxy_box.setChecked(False)
        self.verticalLayout_4 = QVBoxLayout(self.proxy_box)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 25, -1, -1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.proxy_http = QComboBox(self.proxy_box)
        self.proxy_http.addItem(u"http://")
        self.proxy_http.addItem(u"https://")
        self.proxy_http.setObjectName(u"proxy_http")
        self.proxy_http.setProperty("currentText", u"http://")

        self.horizontalLayout_2.addWidget(self.proxy_http)

        self.proxy_user = QLineEdit(self.proxy_box)
        self.proxy_user.setObjectName(u"proxy_user")
        self.proxy_user.setPlaceholderText(u"user name")

        self.horizontalLayout_2.addWidget(self.proxy_user)

        self.label = QLabel(self.proxy_box)
        self.label.setObjectName(u"label")
        self.label.setText(u":")

        self.horizontalLayout_2.addWidget(self.label)

        self.proxy_pass = QLineEdit(self.proxy_box)
        self.proxy_pass.setObjectName(u"proxy_pass")
        self.proxy_pass.setEchoMode(QLineEdit.Password)
        self.proxy_pass.setPlaceholderText(u"password")

        self.horizontalLayout_2.addWidget(self.proxy_pass)

        self.label_14 = QLabel(self.proxy_box)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setText(u"@")

        self.horizontalLayout_2.addWidget(self.label_14)

        self.proxy_server = QLineEdit(self.proxy_box)
        self.proxy_server.setObjectName(u"proxy_server")
        self.proxy_server.setPlaceholderText(u"server")

        self.horizontalLayout_2.addWidget(self.proxy_server)

        self.label_15 = QLabel(self.proxy_box)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setText(u":")

        self.horizontalLayout_2.addWidget(self.label_15)

        self.proxy_port = QLineEdit(self.proxy_box)
        self.proxy_port.setObjectName(u"proxy_port")
        self.proxy_port.setPlaceholderText(u"port")

        self.horizontalLayout_2.addWidget(self.proxy_port)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.formLayout_3.setWidget(6, QFormLayout.SpanningRole, self.proxy_box)

        self.startup_tooltips = QCheckBox(self.a2scroll_area_background)
        self.startup_tooltips.setObjectName(u"startup_tooltips")
        self.startup_tooltips.setText(u"Enable Startup Tooltips")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.startup_tooltips)

        self.scrollArea.setWidget(self.a2scroll_area_background)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        self.portable_label.setText(QCoreApplication.translate("Form", u"a2 runs in portable mode! The data path is in the main directory and cannot be changed!", None))

        self.proxy_server.setText("")
        pass
    # retranslateUi

