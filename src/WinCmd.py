# ==================================================================
#       文 件 名: WinCmd.py
#       概    要: 
#       作    者: IT小强 
#       创建时间: 2019/12/22 9:48
#       修改时间: 
#       copyright (c) 2016 - 2019 mail@xqitw.cn
# ==================================================================
from os.path import abspath, dirname, join
from os import popen
from re import search


class WinCmd:
    """
    WSL2 端口转发处理类
    """

    def __init__(self):
        self.scriptDir = dirname(abspath(__file__))
        self.BASH_EXE = 'bash.exe'
        self.WSCRIPT_EXE = r'C:\Windows\System32\wscript.exe'
        self.WSL_BAT_PATH = join(self.scriptDir, 'script/wsl.vbs')
        self.POWER_SHELL = 'PowerShell.exe'
        self.FireWallRuleOut = 'Outbound'
        self.FireWallRuleIn = 'Inbound'
        self.FireWallRuleDisplayName = 'WSL 2 Firewall Unlock'

    def get_wsl2_ip(self):
        """
        该方法用于获取WSL2的IP
        @return: str
        """
        pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        try:
            cmd = self.BASH_EXE + ' -c "ifconfig eth0 | grep \'inet \'"'
            result = self.read_cmd(cmd)
            wsl_ip = search(pattern, result).group(0)
        except AttributeError:
            wsl_ip = ''
        return wsl_ip

    def start_wsl(self):
        """
        启动wsl子系统
        :return:
        """
        cmd = self.WSCRIPT_EXE
        cmd += ' ' + self.WSL_BAT_PATH + ' wsl'
        return self.read_cmd(cmd)

    def port_add(self, wsl_ip, wsl_port, addr='0.0.0.0'):
        """
        添加端口转发
        @param addr: 监听地址
        @param wsl_ip: 待转发的IP地址
        @param wsl_port: 待添加端口号
        @return:
        """
        cmd = self.POWER_SHELL
        cmd += ' netsh interface portproxy add v4tov4'
        cmd += ' listenport=' + wsl_port
        cmd += ' listenaddress=' + addr
        cmd += ' connectport=' + wsl_port
        cmd += ' connectaddress=' + wsl_ip
        return self.read_cmd(cmd)

    def port_del(self, wsl_port, addr='0.0.0.0'):
        """
        删除端口转发
        @param addr: 监听地址
        @param wsl_port: 待删除的端口号
        @return:
        """
        cmd = self.POWER_SHELL
        cmd += ' netsh interface portproxy delete v4tov4 listenport=' + wsl_port + ' listenaddress=' + addr
        return self.read_cmd(cmd)

    def port_reset(self):
        """
        清除所有的端口转发
        @return:
        """
        cmd = self.POWER_SHELL
        cmd += ' netsh interface portproxy reset'
        return self.read_cmd(cmd)

    def port_info(self, is_str=False):
        """
        查看端口转发情况
        @return:
        """
        cmd = self.POWER_SHELL
        cmd += ' netsh interface portproxy show all'
        info_str = self.read_cmd(cmd)
        if is_str:
            return info_str
        return self.port_info_to_list(info_str)

    def fire_wall_rule_add(self, wsl_port, wall_type):
        """
        添加防火墙规则
        @param wsl_port: str 端口号
        @param wall_type: str 防火墙类型 Outbound | Inbound
        @return:
        """
        "New-NetFireWallRule -DisplayName 'test1008611' -Direction 'Inbound' -Action Allow -Protocol TCP"
        wall_name = self.FireWallRuleDisplayName + wall_type + wsl_port
        cmd = self.POWER_SHELL
        cmd += " New-NetFireWallRule -DisplayName '" + wall_name + "'"
        cmd += " -Direction '" + wall_type + "'"
        cmd += " -LocalPort " + wsl_port + " -Action Allow -Protocol TCP"
        return self.read_cmd(cmd)

    def fire_wall_rule_del(self, wsl_port, wall_type):
        """
        删除防火墙规则
        @param wsl_port: str 端口号
        @param wall_type: str 防火墙类型 Outbound | Inbound
        @return:
        """
        wall_name = self.FireWallRuleDisplayName + wall_type + wsl_port
        cmd = self.POWER_SHELL
        cmd += " Remove-NetFireWallRule -DisplayName '" + wall_name + "'"
        return self.read_cmd(cmd)

    def save_bat_script(self, content):
        f = open(join(self.scriptDir, 'script/wsl.bat'), 'w', encoding='utf8')
        f.write(content)
        f.close()

    def get_bat_script(self):
        f = open(join(self.scriptDir, 'script/wsl.bat'), 'r', encoding='utf8')
        content = f.read()
        f.close()
        return content

    @staticmethod
    def read_cmd(cmd):
        """
        执行命令，并返回输出结果
        :param cmd:
        :return:
        """
        f = popen(cmd)
        result = f.read().strip()
        f.close()
        return result

    @staticmethod
    def port_info_to_list(info_str):
        """
        格式化话端口信息
        :param info_str:
        :return: 以字典形式返回
        """
        info = []
        pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(.*?)(\d+)(.*?)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        for line in info_str.splitlines():
            line_info = search(pattern, line)
            if line_info:
                info.append({
                    'addr': line_info.group(1),
                    'port': line_info.group(3),
                    'ip': line_info.group(5),
                })
        return info
