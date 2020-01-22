# ==================================================================
#       文 件 名: wsl2.py
#       概    要: 启动文件
#       作    者: IT小强 
#       创建时间: 2020/1/22 15:52
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================
from PySide2.QtWidgets import QApplication, QSystemTrayIcon

from wsl2.WSL2AutoPortForward import WSL2AutoPortForward

if __name__ == "__main__":
    app = QApplication([])
    wsl2_auto_port_forward = WSL2AutoPortForward(app)
    wsl2_auto_port_forward.ui.show()
    wsl2_auto_port_forward.tp.show()
    wsl2_auto_port_forward.tp.showMessage(
        'WSL2AutoPortForward',
        'WSL2端口自动转发工具已启动',
        QSystemTrayIcon.MessageIcon.Information
    )
    app.exec_()
