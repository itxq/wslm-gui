# WSL2端口自动转发工具

### 打包

```
pyinstaller WSL2AutoPortForward.py --noconsole --hidden-import PySide2.QtXml --icon="lib/logo.ico"
```

### 界面

+ 查询WSL2当前IP

![查询WSL2当前IP](./src/images/4.png)

+ 查询端口

![查询端口](./src/images/2.png)

+ 添加端口

![添加端口](./src/images/1.png)

+ 删除端口

![删除端口](./src/images/3.png)

+ 保存配置信息及启动脚本

![删除端口](./src/images/5.png)