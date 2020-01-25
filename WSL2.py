# ==================================================================
#       文 件 名: WSL2.py
#       概    要: 启动文件
#       作    者: IT小强 
#       创建时间: 2020/1/22 15:52
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================
from sys import exit

from PySide2.QtWidgets import QApplication, QSystemTrayIcon

from UI import UI

if __name__ == "__main__":
    app = QApplication([])
    ui = UI(app)
    ui.ui.show()
    ui.tp.show()
    ui.tp.showMessage(
        'WSL2AutoPortForward',
        'WSL2端口自动转发工具已启动',
        QSystemTrayIcon.MessageIcon.Information
    )
    exit(app.exec_())
