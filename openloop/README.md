## OpenLoop脚本 我的邀请码ole268190

![微信截图_20241130162931](https://github.com/user-attachments/assets/20a509e2-a1ed-44c1-a6ae-28ea829b2808)

## OpenLoop Network 是一个去中心化的无线网络，旨在增强互联网服务的交付，使其更高效、可访问性更强，并为每个人带来更多回报。

- 官方网站 [https://openloop.so/](https://openloop.so/)
- 官方推特 [@openloop_so](https://x.com/openloop_so)

## **功能**

- **自动注册**
- **加载现有Token**：如果你已经注册了账户，可以在脚本内选2登录来读取Token。
- **自动Ping**
- **自动推荐**
- **支持多账户**
- **支持代理**

## **要求**

- **Python环境**：确保已安装python环境

## **如果使用代理的话请确保账户数量和代理数量一致 不使用代理无视这条**

如果你已经有账户，请把账号密码以格式为`example1@email.com,password1`的方式放入`accounts.txt`

将你的代理放入`proxy.txt`文件中，格式为`http://username:pass@ip:port`


## 设置

1. 克隆此仓库：
   ```bash
   git clone https://github.com/Gzgod/openloop.git
   cd openloop
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行脚本创建账户或直接获取Token：
   ```bash
   python bot.py 或 python3 bot.py
   ```
**运行后选择2注册或获取Token 注意！要把你需要注册或者登录的账号密码写入`accounts.txt`内 格式为`example1@email.com,password1`**

4. 运行脚本安装节点：
   ```bash
   python bot.py 或 python3 bot.py
   ```
**运行后选择1运行节点 如选择代理后无法运行 请选择不使用代理 如不使用代理成功 那就是你代理的问题 请更换代理**
