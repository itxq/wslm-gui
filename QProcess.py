# ==================================================================
#       文 件 名: QProcess.py
#       概    要: QProcess 封装
#       作    者: IT小强 
#       创建时间: 2020/1/22 21:37
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================
from PySide2.QtCore import QProcess as PySide2QProcess


class QProcess:
    """
    QProcess 封装
    """

    @staticmethod
    def get_out_put(cmd):
        """
        执行命令，并返回结果
        :param cmd: 要执行的命令
        :return:
        """
        process = PySide2QProcess()
        process.start(cmd)
        process.waitForFinished()
        out_put = process.readAllStandardOutput()
        out_put = out_put.data()
        try:
            out_put = out_put.decode('utf-8')
        except UnicodeDecodeError:
            out_put = out_put.decode('gbk')
        finally:
            return out_put
