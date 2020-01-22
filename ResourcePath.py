# ==================================================================
#       文 件 名: ResourcePath.py
#       概    要: 资源路径处理类
#       作    者: IT小强 
#       创建时间: 2020/1/22 14:51
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================
import sys
from os import environ, mkdir
from os.path import expanduser, expandvars, join
from pathlib import Path


class ResourcePath:
    """
    资源路径处理类
    """

    @staticmethod
    def get_user_home_path():
        """
        获取用户主目录
        :return:
        """
        user_home_path = ''
        try:
            user_home_path = environ['HOME']
        except KeyError:
            user_home_path = expanduser('~')
            if not user_home_path:
                user_home_path = expandvars('$HOME')
        finally:
            return user_home_path

    @staticmethod
    def resource_path(relative_path):
        """
        获取 资源绝对路径
        :param relative_path:
        :return:
        """
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller会创建临时文件夹temp
            # 并把路径存储在_MEIPASS中
            base_path = sys._MEIPASS
        else:
            base_path = '.'
        return join(base_path, relative_path)

    @classmethod
    def create_settings_path(cls, path_name='.wsl2_auto_port_forward'):
        """
        创建并返回配置目录
        :param path_name:
        :return:
        """
        user_home_path = cls.get_user_home_path()
        settings_path = join(user_home_path, path_name)
        if not Path(settings_path).is_dir():
            mkdir(settings_path)
        return settings_path
