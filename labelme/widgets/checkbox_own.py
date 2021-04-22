from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QPushButton, QMessageBox, QLabel, \
    QHBoxLayout, QVBoxLayout

import sys

class CheckBoxSmart(QWidget):
    Signal_OneParameter = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.checkbox_storage = {}
        self.checkbox_storage_with_themes = {}
        self.set_up_boxes()
        self.show()
        self.Themes = self.read_boxes()
        self.Data = None
    def set_up_boxes(self):

        ### 用于循环创造表格的数据 ###
        themes = {
            '风格': ['ps立体文字', '建议图文叠加', '极简', '写实', '卡通', '插画', '撞色', '立体主义', '欧普', '像素', '渐变', '波普', '极繁', '新丑风', '赛博朋克', '蒸汽波', '孟菲斯', '酸性风格', '图片合成', '正负形', '哥特', '故障风', '半透明叠加', '切面排列透镜', '错层阴影', '多重曝光', '长投影', '文字切片'],
            '无法识别' : ['无风格', '不是海报']              
                 }
        spotlight = {
            '主体物来源': ['电脑合成图像', '实物照片'],
            '主体物类别': ['字体','几何图形','人像','其他动物','植物','工艺品','工业品','食物','衣物鞋靴','风景','其他']
        }
        list_names = ['风格', '主体物']
        list_name_data = [themes, spotlight]

        divisor = 6

        self.the_window = QVBoxLayout()
        self.setLayout(self.the_window)

        name_index = 0

        line_shape = '-----------------------------------------------------------------------' \
                     '-----------------------------------------------------------------------'
        line_shape2 = '-----------------------------------------------------------------------' \
                      '-----------------------------------------------------------------------'
        for categories in list_name_data:
            self.label_catagory_line = QLabel(line_shape)
            self.label_catagory_line2 = QLabel(line_shape2)
            self.label_catagory = QLabel('[ ' + list_names[name_index] + ' ]')
            self.the_window.addWidget(self.label_catagory_line)
            self.the_window.addWidget(self.label_catagory)

            self.temp_dic_storage = {}

            for keys in categories:

                self.label_key = QLabel(keys)


                local_list = categories[keys]
                len_ = 0

                # find out the length of a subject manually:
                for items in local_list:
                    len_ += 1

                # determining how many loops:
                num_loops = int(len_ / divisor)

                if len_ % divisor != 0:
                    num_loops += 1



                # the giant loop for creating checkboxes
                index_for_atoms = 0
                for i in range(num_loops):

                    j = 0
                    self.partial_layout_math_controlled = QHBoxLayout()
                    if i == 0:
                        self.partial_layout_math_controlled.addWidget(self.label_key)
                    self.partial_layout_math_controlled.addStretch(1)

                    while j <  divisor and index_for_atoms < len_:
                        self.tep_checkbox = QCheckBox()
                        self.tep_checkbox.setCheckState(False)
                        self.tep_checkbox.setText(categories[keys][index_for_atoms])
                        self.tep_checkbox.clicked.connect(self.clicked)
                        self.partial_layout_math_controlled.addWidget(self.tep_checkbox)
                        self.checkbox_storage[self.tep_checkbox.text()] = self.tep_checkbox
                        self.temp_dic_storage[self.tep_checkbox.text()] = self.tep_checkbox
                        index_for_atoms += 1
                        j += 1
                #self.partial_layout.addStretch(1)
                    self.partial_layout_math_controlled.addStretch(1.8)
                #self.the_window.addLayout(self.partial_layout)
                    self.the_window.addLayout(self.partial_layout_math_controlled)

            self.checkbox_storage_with_themes[list_names[name_index]] = self.temp_dic_storage
            name_index += 1
        self.the_window.addWidget(self.label_catagory_line2)

        '''self.submit_button = QPushButton()
        self.submit_button.setText('Submit Selections & save')
        self.submit_button.clicked.connect(self.read_boxes)
        self.the_window.addWidget(self.submit_button)'''

    def emit_signal(self):
        for categories in self.checkbox_storage_with_themes:
            for keys in self.checkbox_storage_with_themes[categories]:
                if ((keys not in self.Themes[categories]) and self.checkbox_storage_with_themes[categories][keys].isChecked()) or\
                        ((keys in self.Themes[categories]) and not self.checkbox_storage_with_themes[categories][keys].isChecked()):
                    self.Signal_OneParameter.emit(True)
                    return
                else:
                    self.Signal_OneParameter.emit(False)

    def clicked(self):
        sender = self.sender().text()
        checkstate = self.checkbox_storage[sender].isChecked()
        self.emit_signal()
        print(sender, checkstate)

    def read_boxes(self):
        output_dic = {}
        str_checked = ''
        for categories in self.checkbox_storage_with_themes:
            str_checked += categories
            str_checked += ': '
            temp_keys_under_catagories = []
            for keys in self.checkbox_storage_with_themes[categories]:

                if self.checkbox_storage_with_themes[categories][keys].isChecked():
                    temp_keys_under_catagories.append(keys)
                    str_checked += keys + ', '

            output_dic[categories] = temp_keys_under_catagories
            str_checked += ' \n'
        return output_dic

    '''def changed(self, CheckBoxSmart):
        for categories in self.checkbox_storage_with_themes:
            for keys in self.checkbox_storage_with_themes[categories]:
                if self.Themes[categories][keys] != self.Data[categories][keys]:
                    return True
        return False'''

    def update_boxes(self, data_set):
        self.Data=data_set
        for catagories in data_set:
            for items in data_set[catagories]:
                self.checkbox_storage_with_themes[catagories][items].setCheckState(Qt.Checked)

    def reSet(self):
        for catagories in self.checkbox_storage_with_themes:
            for keys in self.checkbox_storage_with_themes[catagories]:
                self.checkbox_storage_with_themes[catagories][keys].setCheckState(Qt.Unchecked)

    def set_uncheckable(self, bool_state):
        for catagories in self.checkbox_storage_with_themes:
            for keys in self.checkbox_storage_with_themes[catagories]:
                self.checkbox_storage_with_themes[catagories][keys].setDisabled(bool_state)

if __name__ == '__main__':
    application = QApplication(sys.argv)
    ex = CheckBoxSmart()
    ex.show()
    sys.exit(application.exec_())
