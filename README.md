<div align="center">

[![logo](https://raw.githubusercontent.com/Darknights-master/Darknights-server/main/assets/icon-192x192.png)](https://github.com/Darknights-master)
# Darknights - Darknights Server
*More than a gacha simulator*
</div>

Darknights 服务器，目前只实现中国大陆CN服务器

主要功能：服务器登录,模拟抽卡及作战等.

实现原理：通过分析Arknights客户端与服务器交互信息,模拟服务端进程.

主流程：Arknights客户端 -> Mitmproxy代理 -> Internet -> Nginx -> Bottle框架

![flow.png](https://i.loli.net/2021/09/19/la9fr5dkCOLYvZU.png)

由于开发者精力(能力)有限，大部分游戏内功能目前*并未实现*.

如果您有好的想法或建议，或者想参与到开发中，欢迎提交[issue](https://github.com/Darknights-master/Darknights-server/issues)或[pull request](https://github.com/Darknights-master/Darknights-server/pulls)


[开发讨论Discord](https://discord.gg/SmuB88RR5W)


## License

本Project在[Apache-2.0 License](https://github.com/Darknights-master/Darknights-server/blob/main/LICENSE)下开源

⚠**严禁**利用本Project内全部或部分代码作任何形式的商业用途

⚠**Prohibit** any form of commercial use

⚠いかなる形の商業的使用も禁止されています

项目icon inspired by [Texas](https://www.pixiv.net/artworks/87060370)

本Project与 **上海鹰角网络科技有限公司(HYPERGRYPH)** 及其旗下手游 **明日方舟(Arknights)** 无任何直接或间接的关联

## 部署

### requirements
```
python 3.x
mongodb
nginx
bottle >= 0.13
pymongo >= 3.11
Crypto
```

**启动前请检查Mongodb运行状态**

详细教程参见[wiki](https://github.com/Darknights-master/Darknights-server/wiki)

## [Todo List](https://github.com/Darknights-master/Darknights-server/wiki/Todo)

## ViewCount

![:darknights](https://count.getloli.com/get/@:darknights)

## Contributors

[![contributors](https://contributors-img.web.app/image?repo=Darknights-master/Darknights-server)](https://github.com/Darknights-master/Darknights-server/graphs/contributors)

## Acknowledgments

[Tao0lu: Server-side Proxy](https://github.com/Tao0Lu/Arknights_Anti-addiction_Cheater)

[guch8017: Gacha System](https://github.com/guch8017/ArknightsGachaMonitor)

[Kengxxiao: Game Data](https://github.com/Kengxxiao/ArknightsGameData)
