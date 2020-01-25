# ==================================================================
#       文 件 名: Auto.py
#       概    要: 开机启动脚本
#       作    者: IT小强 
#       创建时间: 2020/1/25 22:51
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================
from SettingsManage import SettingsManage
from WinCmd import WinCmd

if __name__ == "__main__":
    # 实例化配置管理类
    settings_manage = SettingsManage()
    settings = settings_manage.get()

    # 获取需要转发的端口
    ports = settings.get('ports', [])

    # 实例化windows命令处理类
    win_cmd = WinCmd()

    # 获取wsl2 IP
    wsl2_ip = win_cmd.get_wsl2_ip()

    # 端口转发处理
    port_str = ''
    for port in ports:
        port_str += (',' + port if port_str else port)
        # 删除端口
        win_cmd.port_del(wsl_port=port, exec_run=True)
        # 添加端口
        win_cmd.port_add(wsl_ip=wsl2_ip, wsl_port=port, exec_run=True)

    # 清除防已有火墙
    win_cmd.fire_wall_rule_del(wall_type=win_cmd.FireWallRuleIn, exec_run=True)
    win_cmd.fire_wall_rule_del(wall_type=win_cmd.FireWallRuleOut, exec_run=True)

    # 添加新的防火墙
    win_cmd.fire_wall_rule_add(wsl_port=port_str, wall_type=win_cmd.FireWallRuleIn, exec_run=True)
    win_cmd.fire_wall_rule_add(wsl_port=port_str, wall_type=win_cmd.FireWallRuleOut, exec_run=True)

    # 启动wsl2
    win_cmd.start_wsl(exec_run=True)
