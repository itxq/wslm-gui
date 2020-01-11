# ==================================================================
#       文 件 名: WSL2AutoPortForward.py
#       概    要: 
#       作    者: IT小强 
#       创建时间: 2019/12/22 9:51
#       修改时间: 
#       copyright (c) 2016 - 2019 mail@xqitw.cn
# ==================================================================
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMessageBox
from SettingsManage import SettingsManage
from WinCmd import WinCmd


class WSL2AutoPortForward:
    """
    WSL2 端口自动转发
    """

    def __init__(self):
        # 实例化配置管理类
        self.settings_manage = SettingsManage()
        self.__setting = self.settings_manage.get()

        # 实例化windows命令处理类
        self.wsl2 = WinCmd()

        # 加载UI文件
        self.ui = QUiLoader().load('lib/wsl2.ui')

        # 设置界面图标
        app_icon = QIcon("lib/logo.ico")
        self.ui.setWindowIcon(app_icon)

        # 设置选中状态
        self.ui.auto_start_wsl.setChecked(self.__setting.get('auto_start_wsl', False))
        self.ui.fire_wall_open.setChecked(self.__setting.get('fire_wall_open', False))
        self.ui.fire_wall_close.setChecked(self.__setting.get('fire_wall_close', False))

        # 设置文本框的值
        self.ui.port_text.appendPlainText('\n'.join(self.__setting.get('ports', [])))
        self.ui.bat_text.appendPlainText(self.wsl2.get_bat_script())

        # 按钮监听
        self.ui.get_wsl2_ip.clicked.connect(self.__get_wsl2_ip)
        self.ui.port_add.clicked.connect(self.__port_add)
        self.ui.port_del.clicked.connect(self.__port_del)
        self.ui.port_info.clicked.connect(self.__port_info)
        self.ui.port_reset.clicked.connect(self.__port_reset)
        self.ui.start_wsl.clicked.connect(self.__start_wsl)
        self.ui.save_settings.clicked.connect(self.__save_settings)

        if self.ui.auto_start_wsl.isChecked():
            self.__start_wsl()

    def __get_wsl2_ip(self):
        wsl2_ip_info = self.wsl2.get_wsl2_ip()
        if not wsl2_ip_info:
            # 未查询到端口转发信息提示
            QMessageBox.information(self.ui, '系统提示', '未查询到IP信息!')
        else:
            wsl2_ip_info = 'WSL2当前IP为：' + wsl2_ip_info
            self.ui.result_text.setPlainText(wsl2_ip_info)

    def __port_add(self):
        wsl2_ip_info = self.wsl2.get_wsl2_ip()
        if not wsl2_ip_info:
            # 未查询到端口转发信息提示
            QMessageBox.information(self.ui, '系统提示', '未查询到IP信息!')
        else:
            self.ui.result_text.clear()
            ports = self.ui.port_text.toPlainText()
            for port in ports.splitlines():
                if not port.strip():
                    continue
                self.wsl2.port_add(wsl2_ip_info, port)
                self.ui.result_text.appendPlainText('>>> 添加端口：【' + port + '】...')
                if self.ui.fire_wall_open.isChecked():
                    self.wsl2.fire_wall_rule_add(port, self.wsl2.FireWallRuleIn)
                    self.ui.result_text.appendPlainText('>>> 添加防火墙：【' + port + '】【' + self.wsl2.FireWallRuleIn + '】...')
                    self.wsl2.fire_wall_rule_add(port, self.wsl2.FireWallRuleOut)
                    self.ui.result_text.appendPlainText('>>> 添加防火墙：【' + port + '】【' + self.wsl2.FireWallRuleOut + '】...')
            self.ui.result_text.appendPlainText('Succeed!')

    def __port_del(self):
        self.ui.result_text.clear()
        ports = self.ui.port_text.toPlainText()
        for port in ports.splitlines():
            if not port.strip():
                continue
            self.__port_del_one(port)
        self.ui.result_text.appendPlainText('Succeed!')

    def __port_reset(self):
        port_info = self.wsl2.port_info()
        self.ui.result_text.clear()
        for port in port_info:
            self.__port_del_one(port['port'])
        self.ui.result_text.appendPlainText('Succeed!')

    def __port_info(self):
        info_str = self.wsl2.port_info(True)
        if not info_str:
            # 未查询到端口转发信息提示
            QMessageBox.information(self.ui, '系统提示', '未查询到端口转发信息!')
        else:
            self.ui.result_text.setPlainText(info_str)

    def __port_del_one(self, port):
        self.wsl2.port_del(port)
        self.ui.result_text.appendPlainText('>>> 删除端口：【' + port + '】...')
        if self.ui.fire_wall_close.isChecked():
            self.wsl2.fire_wall_rule_del(port, self.wsl2.FireWallRuleIn)
            self.ui.result_text.appendPlainText('>>> 删除防火墙：【' + port + '】【' + self.wsl2.FireWallRuleIn + '】...')
            self.wsl2.fire_wall_rule_del(port, self.wsl2.FireWallRuleOut)
            self.ui.result_text.appendPlainText('>>> 删除防火墙：【' + port + '】【' + self.wsl2.FireWallRuleOut + '】...')

    def __wsl2_auto_port_forward(self):
        """
        一键自动转发
        @return:
        """

        self.__port_del()
        self.__port_add()

    def __start_wsl(self):
        """
        启动wsl
        :return:
        """
        self.wsl2.start_wsl()
        self.__wsl2_auto_port_forward()

    def __save_settings(self):
        """
        保存全部配置
        :return:
        """
        # 保存脚本
        self.__save_bat_script()

        # 保存配置信息
        self.settings_manage.set('fire_wall_open', self.ui.fire_wall_open.isChecked())
        self.settings_manage.set('fire_wall_close', self.ui.fire_wall_close.isChecked())
        self.settings_manage.set('auto_start_wsl', self.ui.auto_start_wsl.isChecked())
        self.settings_manage.set('ports', self.ui.port_text.toPlainText().splitlines())

        # 保存成功提示
        QMessageBox.information(self.ui, '系统提示', '配置保存成功!')

    def __save_bat_script(self):
        """
        保存启动脚本
        :return:
        """
        content = self.ui.bat_text.toPlainText()
        self.wsl2.save_bat_script(content)


if __name__ == "__main__":
    app = QApplication([])
    wsl2_auto_port_forward = WSL2AutoPortForward()
    wsl2_auto_port_forward.ui.show()
    app.exec_()
