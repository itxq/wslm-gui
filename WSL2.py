# ==================================================================
#       文 件 名: WSL2.py
#       概    要: 启动文件
#       作    者: IT小强 
#       创建时间: 2020/1/22 15:52
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================
from sys import exit, argv

from PySide2.QtWidgets import QApplication

from UI import UI

if __name__ == "__main__":
    app = QApplication([])
    ui = UI(app)
    if (len(argv) == 2 and argv[1] == 'start') or ui.ui.auto_start_wsl.isChecked():
        ui.start_wsl_all()
    else:
        ui.ui.show()
    exit(app.exec_())
