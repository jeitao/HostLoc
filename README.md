# HostLoc

HostLoc论坛《美国VPS综合讨论》版块新帖TG机器人提醒

# 使用

1. 请确保你的VPS上面已经安装了`docker`与`docker-compose`;
2. 请确保你的VPS是可以翻墙的；

```bash
$ whoami
root
$ git clone https://github.com/anshengme/HostLoc.git
$ cd HostLoc/
$ vim docker-compose.yml
......
      TELEGRAM_BOT_TOKEN: ""   # 修改为你的TG机器人TOken，如："797610865:AAHdrMSDAVxSDAV_QQOKMKCqPLKJhuEA3A8"
      CHANNEL_NAM: ""  # 修改为你的频道地址，如："@mjjhost"
......
$ docker-compose up -d  # 需要等待几分钟
```

