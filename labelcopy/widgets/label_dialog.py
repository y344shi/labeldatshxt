import re

from PyQt5.QtWidgets import *
from qtpy import QT_VERSION
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets

from labelme.logger import logger
import labelme.utils

QT5 = QT_VERSION[0] == "5"


# TODO(unknown):
# - Calculate optimal position so as not to go out of screen area.


class LabelQLineEdit(QtWidgets.QLineEdit):
    def setListWidget(self, list_widget):
        self.list_widget = list_widget

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Up, QtCore.Qt.Key_Down]:
            self.list_widget.keyPressEvent(e)
        else:
            super(LabelQLineEdit, self).keyPressEvent(e)


Num = 0


class LabelDialog(QtWidgets.QDialog):
    def __init__(
            self,
            text="Please enter cultural term：",
            parent=None,
            labels=None,
            sort_labels=True,
            show_text_field=True,
            completion="startswith",
            fit_to_content=None,
            flags=None,
    ):
        if fit_to_content is None:
            fit_to_content = {"row": False, "column": True}
        self._fit_to_content = fit_to_content
        ################################################################################################################
        super(LabelDialog, self).__init__(parent)

        ###combobox图层
        self.layers_Title = QLabel()
        self.layers_Title.setText("素材图层：")
        self.layers = QComboBox(self)
        self.layers.addItems(["主体物", "标题", "文案", "点缀标题", "背景"])

        ###combobox素材本身定义
        self.matDefi_Title = QLabel()
        self.matDefi_Title.setText("素材定义：")
        self.matDefi1 = QComboBox(self)
        self.matDefi1.addItems(["实物拍摄照片", "电脑生成图像"])
        self.matDefi2 = QComboBox(self)
        self.matDefi2.addItems(["人像", "动物", "植物", "工艺品", "工业产品", "食物", "衣物鞋靴", "风景"])
        self.matDefi1.currentIndexChanged.connect(self.changeIndex)

        ###combobox素材颜色
        self.colors_Title = QLabel()
        self.colors_Title.setText("素材颜色：")
        self.colors = QComboBox(self)
        self.colors.addItems(["红", "橙", "黄", "绿", "青", "蓝", "紫", "灰色系", "黑", "白", "金", "银"])

        ###shapeposision位置
        self.shapeposision_Title = QLabel()
        self.shapeposision_Title.setText("素材位置：")
        self.shapeposision = QLabel()
        # self.shapeposision.setText(shapepos)
        # self.layer.setText(self.layers.currentText())

        ###shapeForm形状
        self.shapeForm_Title = QLabel()
        self.shapeForm_Title.setText("素材形状：")
        self.shapeForm = QLabel()

        ###culture
        self.culture_Title = QLabel()
        self.culture_Title.setText("文化词汇：")
        self.culture = LabelQLineEdit()
        self.culture.setPlaceholderText(text)
        self.culture.setValidator(labelme.utils.labelValidator())
        self.culture.editingFinished.connect(self.postProcess)

        ###adj
        self.adj_Title = QLabel()
        self.adj_Title.setText("形容词语义：")
        self.checkbox_storage = {}
        self.checkbox_storage_with_themes = {}
        self.temp_dic_storage = {}
        ##################################################################################################################
        self.adjectives = ['纯洁', '诚实', '无私', '素雅', '雅致', '古朴', '沉静', '坚实', '神圣', '缅怀', '悲哀', '惨淡', '平静', '朴素', '淡薄',
                           '谦逊', '和谐',
                           '沉闷', '平凡', '中庸', '阴郁', '绝望', '力量', '严肃', '毅力', '意志', '哀悼', '黑暗', '罪恶',
                           '恐惧', '死亡', '冷淡', '热烈', '喜庆', '吉祥', '兴奋', '革命', '敬畏', '残酷', '危险', '血腥', '热情',
                           '华丽', '富裕', '成熟', '甜蜜', '冲动', '傲慢', '焦躁', '温情', '甘美', '明朗', '光明', '纯真', '活泼',
                           '轻松', '藐视', '诱惑', '任性', '明快', '泼辣', '和平', '生命', '青春', '希望', '舒适', '平庸',
                           '嫉妒', '刻薄', '新鲜', '跃动', '公平', '理智', '深邃', '博大', '永恒', '真理', '保守', '冷酷', '漠视', '忧伤',
                           '内向', '高贵', '祥瑞', '忠诚', '神秘', '庄重', '压抑', '高尚', '优雅', '优美', '消极']
        divisor = 7
        self.the_window = QVBoxLayout()
        name_index = 0
        num = 0
        Num = 0
        # find out the length of a subject manually:
        for items in self.adjectives:
            num += 1
            Num += 1
        # determining how many loops:
        num_loops = int(num / divisor)
        if num % divisor != 0:
            num_loops += 1

        # the giant loop for creating checkboxes
        index_for_atoms = 0
        for i in range(num_loops):
            j = 0
            self.partial_layout_math_controlled = QHBoxLayout()
            self.partial_layout_math_controlled.addStretch(1)

            while j < divisor and index_for_atoms < num:
                self.tep_checkbox = QCheckBox()
                self.tep_checkbox.setCheckState(False)
                self.tep_checkbox.setText(self.adjectives[index_for_atoms])
                self.tep_checkbox.clicked.connect(self.clicked)
                self.partial_layout_math_controlled.addWidget(self.tep_checkbox)
                self.checkbox_storage[self.tep_checkbox.text()] = self.tep_checkbox
                self.temp_dic_storage[self.tep_checkbox.text()] = self.tep_checkbox
                index_for_atoms += 1
                j += 1
            self.partial_layout_math_controlled.addStretch(1.8)
            self.the_window.addLayout(self.partial_layout_math_controlled)
        self.checkbox_storage_with_themes[name_index] = self.temp_dic_storage
        name_index += 1
        # self.adj =

        ######B
        if flags:
            self.culture.textChanged.connect(self.updateFlags)
        self.culture_group_id = QtWidgets.QLineEdit()
        self.culture_group_id.setPlaceholderText("Group ID")
        self.culture_group_id.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp(r"\d*"), None)
        )
        ##############################################################################################
        layout = QtWidgets.QVBoxLayout()

        if show_text_field:
            layout_shapeposition = QtWidgets.QHBoxLayout()
            layout_shapeposition.addWidget(self.shapeposision_Title, 2)
            layout_shapeposition.addWidget(self.shapeposision, 6)
            layout.addLayout(layout_shapeposition)

            layout_shapeForm = QtWidgets.QHBoxLayout()
            layout_shapeForm.addWidget(self.shapeForm_Title, 2)
            layout_shapeForm.addWidget(self.shapeForm, 6)
            layout.addLayout(layout_shapeForm)

            layout_layer = QtWidgets.QHBoxLayout()
            layout_layer.addWidget(self.layers_Title, 2)
            layout_layer.addWidget(self.layers, 6)
            layout.addLayout(layout_layer)

            layout_matDefi = QtWidgets.QHBoxLayout()
            layout_matDefi.addWidget(self.matDefi_Title, 2)
            layout_matDefi.addWidget(self.matDefi1, 3)
            layout_matDefi.addWidget(self.matDefi2, 3)
            layout.addLayout(layout_matDefi)

            layout_color = QtWidgets.QHBoxLayout()
            layout_color.addWidget(self.colors_Title, 2)
            layout_color.addWidget(self.colors, 6)
            layout.addLayout(layout_color)

            layout_culture = QtWidgets.QHBoxLayout()
            layout_culture.addWidget(self.culture_Title, 2)
            layout_culture.addWidget(self.culture, 6)
            # layout_culture.addWidget(self.culture_group_id, 2)
            layout.addLayout(layout_culture)

            # label_list
            self.labelList = QtWidgets.QListWidget()
            if self._fit_to_content["row"]:
                self.labelList.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff
                )
            if self._fit_to_content["column"]:
                self.labelList.setVerticalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff
                )
            self._sort_labels = sort_labels
            if labels:
                self.labelList.addItems(labels)
            if self._sort_labels:
                self.labelList.sortItems()
            else:
                self.labelList.setDragDropMode(
                    QtWidgets.QAbstractItemView.InternalMove
                )
            self.labelList.currentItemChanged.connect(self.labelSelected)
            self.labelList.itemDoubleClicked.connect(self.labelDoubleClicked)
            self.culture.setListWidget(self.labelList)
            layout.addWidget(self.labelList)

            #
            layout_adj = QtWidgets.QVBoxLayout()
            layout_adj.addWidget(self.adj_Title)
            layout_adj.addLayout(self.the_window)
            layout.addLayout(layout_adj)
            '''layout_adj = QtWidgets.QHBoxLayout()
            layout_adj.addWidget(CheckBoxSmart())
            layout.addLayout(layout_adj)'''

        # buttons
        self.buttonBox = bb = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self,
        )
        bb.button(bb.Ok).setIcon(labelme.utils.newIcon("done"))
        bb.button(bb.Cancel).setIcon(labelme.utils.newIcon("undo"))
        bb.accepted.connect(self.validate)
        # bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        # label_flags
        if flags is None:
            flags = {}
        self._flags = flags
        self.flagsLayout = QtWidgets.QVBoxLayout()
        self.resetFlags()
        layout.addItem(self.flagsLayout)
        self.culture.textChanged.connect(self.updateFlags)
        self.setLayout(layout)

        # completion
        completer = QtWidgets.QCompleter()
        if not QT5 and completion != "startswith":
            logger.warn(
                "completion other than 'startswith' is only "
                "supported with Qt5. Using 'startswith'"
            )
            completion = "startswith"
        if completion == "startswith":
            completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
            # Default settings.
            # completer.setFilterMode(QtCore.Qt.MatchStartsWith)
        elif completion == "contains":
            completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            completer.setFilterMode(QtCore.Qt.MatchContains)
        else:
            raise ValueError("Unsupported completion: {}".format(completion))
        completer.setModel(self.labelList.model())
        self.culture.setCompleter(completer)

    def clicked(self):
        ####################################################################################################################
        sender = self.sender().text()
        checkstate = self.checkbox_storage[sender].isChecked()
        #print(sender, checkstate)

    def reSet(self):
        for i in self.adjectives:
            self.checkbox_storage[i].setChecked(False)

    def read_boxes(self):
        str_checked = ''
        flag = 0
        for keys in self.checkbox_storage:
            if self.checkbox_storage[keys].isChecked():
                flag += 1
                # temp_keys_under_catagories.append(keys)
                if flag > 1:
                    str_checked += ", " + keys
                else:
                    str_checked += keys
        #print(str(str_checked))
        return str(str_checked)

    def reloadAdj(self, adj):
        word = ""
        adjectives = []
        for i in adj:
            if i != ",":
                if i == " ":
                    word = ""
                    continue
                word += i
            else:
                adjectives.append(word)
        adjectives.append(word)
        print(adjectives)
        for keys in adjectives:
            self.checkbox_storage[keys].setChecked(True)

    def comboBoxFunction_layer(self):
        layer = self.layers.currentText()
        return layer

    def comboBoxFunction_matdefi1(self):
        matdefi1 = self.matDefi1.currentText()
        return matdefi1

    def comboBoxFunction_matdefi2(self):
        matdefi2 = self.matDefi2.currentText()
        return matdefi2

    def comboBoxFunction_color(self):
        color = self.colors.currentText()
        return color

    def changeIndex(self):
        if self.matDefi1.currentText() == "实物拍摄照片":
            self.matDefi2.clear()
            self.matDefi2.addItems(["人像", "动物", "植物", "工艺品", "工业产品", "食物", "衣物鞋靴", "风景"])
        elif self.matDefi1.currentText() == "电脑生成图像":
            self.matDefi2.clear()
            self.matDefi2.addItems(["人像", "动物", "植物", "工艺品", "工业产品", "食物", "衣物鞋靴", "风景", "几何图形"])
        else:
            return
        return

    def getGroupId(self):
        group_id = self.culture_group_id.text()
        if group_id:
            return int(group_id)
        return None

    def addLabelHistory(self, label):
        if self.labelList.findItems(label, QtCore.Qt.MatchExactly):
            return
        self.labelList.addItem(label)
        if self._sort_labels:
            self.labelList.sortItems()

    def labelSelected(self, item):
        self.culture.setText(item.text())

    def validate(self):
        self.read_boxes()
        text = self.culture.text()
        if hasattr(text, "strip"):
            text = text.strip()
        else:
            text = text.trimmed()
        self.accept()

    def labelDoubleClicked(self, item):
        self.validate()

    def postProcess(self):
        text = self.culture.text()
        if hasattr(text, "strip"):
            text = text.strip()
        else:
            text = text.trimmed()
        self.culture.setText(text)

    def updateFlags(self, label_new):
        # keep state of shared flags
        flags_old = self.getFlags()

        flags_new = {}
        for pattern, keys in self._flags.items():
            if re.match(pattern, label_new):
                for key in keys:
                    flags_new[key] = flags_old.get(key, False)
        self.setFlags(flags_new)

    def deleteFlags(self):
        for i in reversed(range(self.flagsLayout.count())):
            item = self.flagsLayout.itemAt(i).widget()
            self.flagsLayout.removeWidget(item)
            item.setParent(None)

    def resetFlags(self, label=""):
        flags = {}
        for pattern, keys in self._flags.items():
            if re.match(pattern, label):
                for key in keys:
                    flags[key] = False
        self.setFlags(flags)

    def setFlags(self, flags):
        self.deleteFlags()
        for key in flags:
            item = QtWidgets.QCheckBox(key, self)
            item.setChecked(flags[key])
            self.flagsLayout.addWidget(item)
            item.show()

    def getFlags(self):
        flags = {}
        for i in range(self.flagsLayout.count()):
            item = self.flagsLayout.itemAt(i).widget()
            flags[item.text()] = item.isChecked()
        return flags

    def popUp(self, shapepos=None, shapeform=None, flags=None, layer=None, matdefi1=None, matdefi2=None,
              color=None, text=None, adj=None, group_id=None, move=True, Ftime=None):
        if self._fit_to_content["row"]:
            self.labelList.setMinimumHeight(
                self.labelList.sizeHintForRow(0) * self.labelList.count() + 2
            )
        if self._fit_to_content["column"]:
            self.labelList.setMinimumWidth(
                self.labelList.sizeHintForColumn(0) + 2
            )
        if Ftime:
            self.reSet()
        if layer is None:
            layer = self.comboBoxFunction_layer()
        if color is None:
            color = self.comboBoxFunction_color()
        if matdefi1 is None:
            matdefi1 = self.comboBoxFunction_matdefi1()
        elif matdefi1 == "实物拍摄照片":
            self.matDefi2.clear()
            self.matDefi2.addItems(["人像", "动物", "植物", "工艺品", "工业产品", "食物", "衣物鞋靴", "风景"])
        elif matdefi1 == "电脑生成图像":
            self.matDefi2.clear()
            self.matDefi2.addItems(["人像", "动物", "植物", "工艺品", "工业产品", "食物", "衣物鞋靴", "风景", "几何图形"])
        if matdefi2 is None:
            matdefi2 = self.comboBoxFunction_matdefi2()
        # if text is None, the previous label in self.culture is kept
        if text is None:
            text = self.culture.text()
        if (adj is not None) and (adj!="Missing Adjectives"):
            self.reSet()
            self.reloadAdj(adj)
        if flags:
            self.setFlags(flags)
        else:
            self.resetFlags(text)
        self.culture.setText(text)
        self.culture.setSelection(0, len(text))
        self.layers.setCurrentText(layer)
        self.matDefi1.setCurrentText(matdefi1)
        self.matDefi2.setCurrentText(matdefi2)
        self.colors.setCurrentText(color)
        self.shapeposision.setText(shapepos)
        self.shapeForm.setText(shapeform)
        ###
        adj = self.read_boxes()
        if group_id is None:
            self.culture_group_id.clear()
        else:
            self.culture_group_id.setText(str(group_id))
        items = self.labelList.findItems(text, QtCore.Qt.MatchFixedString)
        if items:
            if len(items) != 1:
                logger.warning("Label list has duplicate '{}'".format(text))
            self.labelList.setCurrentItem(items[0])
            row = self.labelList.row(items[0])
            self.culture.completer().setCurrentRow(row)
        self.culture.setFocus(QtCore.Qt.PopupFocusReason)
        if move:
            self.move(QtGui.QCursor.pos())
        if self.exec_():
            return self.getFlags(), self.layers.currentText(), self.matDefi1.currentText(), \
                   self.matDefi2.currentText(), self.colors.currentText(), self.culture.text(), self.read_boxes(), self.getGroupId()
        else:
            return None, None, None, None, None, None, None, None
