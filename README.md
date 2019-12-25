# WSL2端口自动转发工具

### 打包

```
# 进入 src 目录后执行
pyinstaller WSL2AutoPortForward.py --noconsole --hidden-import PySide2.QtXml --icon="lib/logo.ico"
```

### 界面

+ 查询WSL2当前IP

![查询WSL2当前IP](./src/lib/images/4.png)

+ 查询端口

![查询端口](./src/lib/images/2.png)

+ 添加端口

![添加端口](./src/lib/images/1.png)

+ 删除端口

![删除端口](./src/lib/images/3.png)