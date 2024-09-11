# 后端代码配置说明：

**<u>*前提：以下配置基于Windows系统，其它系统命令会有所不同*</u>**

## 克隆后端代码

​	通过HTTPS进行克隆

```bash
git clone https://github.com/shady0501/RetrievalSystem.git
```

​	或者通过SSH进行克隆，前提为GitHub上已配置SSH密钥，可从 user ---> settings ---> SSH and GPG keys 中查看是否已配置

```bash
git clone git@github.com:shady0501/RetrievalSystem.git
```



## 创建虚拟环境

通过 PyCharm / VSCode 进入克隆后的文件夹，通过终端使用 `venv` 创建 Python 虚拟环境

```bash
python -m venv .venv
```



## 激活创建好的虚拟环境

```bash
myenv\Scripts\activate
```



## 安装项目所需要的依赖包

```bash
pip install -r requirements.txt
```

​	***<u>注意：这里的依赖库可能会有冲突，安装 zhipuai 会自动把 PyJWT 等依赖库会删掉，可以运行代码后再安装缺失的依赖包</u>***（可以尝试先安装 zhipuai 再安装其他依赖库）



## 更改代码中MySQL密码、数据库名称

- 更改 config.py 文件中数据库配置中的MySQL密码与数据库名称为实际内容
- 更改 services/backup_records.py 文件中数据库配置中的 MySQL 密码与数据库名称为实际内容



## 更改 IP 

如果前后端大模型部署在一台设备上，必须更改调用大模型 IP 为自己本机 IPv4 的地址，端口是否更改需要根据大模型的设置决定

（前端更改 IP ：前端在 IP 配置中也同样需要将 IP 改为本机 IPv4 的地址）

 

## 更改基础配置

app.py 文件中启动 Flask 应用部分：

​	如果是使用 PyCharm 专业版，可以在编译器基础配置中开启 debug 模式，设置应用将在所有可用的网络接口上运行，运行配置中附加命令行选项填写如下内容：

```
--host=0.0.0.0 --port=8000
```

​	如果是使用 PyCharm 社区版，则需要在 app.run() 中配置代码如下：

```python
app.run(host="0.0.0.0", debug=True)
```



## 注意文件存储位置

1. 当前代码中默认图片、数据库备份等存储主路径为 D:/code/RetrievalSystemBackend ，根据备份内容不同会进一步细分子文件夹如 /avatar 、 /backup 等，如果路径不存在会自动创建新文件夹
2. 使用图片搜索文本或者文本搜索图片功能前，必须配置正确图片所在的文件夹，必须将基础数据集中的图片存放在D:/code/RetrievalSystemBackend/images 中，或者在源代码中更改存储路径（因为数据库中只是存放图片路径，从数据库中得到路径但是在具体文件夹中未找到不会返回图片）



## 附录——前端及大模型GitHub仓库

- 前端仓库：https://github.com/lst555ProMax/RetrievalSystem-Front
- 大模型仓库：https://github.com/GodTheHands/ITR
