<div align="center">

[![logo](https://raw.githubusercontent.com/Darknights-master/Darknights-server/main/assets/icon-192x192.png)](https://github.com/arkntools)
# Darknights - Darknights Server
*You know exactly what it is*
</div>

Darknights 服务器，目前只实现中国大陆CN服务器

由于开发者精力(能力)有限，大部分游戏内功能目前*并未实现*。

如果您有好的想法或建议，或者想参与到开发中，欢迎提交[issue](https://github.com/Darknights-master/Darknights-server/issues)或[pull request](https://github.com/Darknights-master/Darknights-server/pulls)

<strike>破解yj服务器 x </strike>

<strike>自己建服务器 √ </strike>

## Deployment

### requirements
```
python 3.x
mongodb
bottle >= 0.13
pymongo >= 3.11
gunicorn
nginx(推荐)
```
开发使用 bottle + gunicorn + nginx 环境，请自签证书并放置于cert目录下

请结合[代理](https://github.com/Darknights-master/Darknights-proxy)使用

**启动前请检查Mongodb运行状态**

Shell下python cytokinesis.py即可

## License

本Project在[Apache-2.0 License](https://github.com/Darknights-master/Darknights-server/blob/main/LICENSE)下开源

⚠**严禁**利用本Project内全部或部分代码作任何形式的商业用途

⚠**Prohibit** any form of commercial use

⚠いかなる形の商業的使用も禁止されています

项目icon系作者手搓, inspired by [Texas](https://www.pixiv.net/artworks/87060370)

本Project与 **上海鹰角网络科技有限公司(HYPERGRYPH)** 及其旗下手游 **明日方舟(Arknights)** 无任何直接或间接的关联

## Contributors

[![contributors](https://contributors-img.web.app/image?repo=Darknights-master/Darknights-server)](https://github.com/Darknights-master/Darknights-server/graphs/contributors)

## Development

View [wiki](https://github.com/Darknights-master/Darknights-server/wiki)

## Todo

<strike>显然远不止这些，毕竟是一个*一年15.578亿流水的大公司*做的</strike>

### GamePlayFunction

- [x] Register (注册)
+ - [x] Basic User Info
+ - [ ] Additional User Info
+ - [x] MinorBypass
+ - [x] Announcement (公告)
- [x] Authentication
+ - [x] Password Login
+ - [x] Auth Login (Remember Me)
- [x] SyncData
+ - [x] Basic User Info
+ - [ ] Additional User Info
- [ ] SyncStatus (Help Needed)
+ - [ ] SyncBuilding (基建)
+ - [ ] SyncNormalGacha
+ - [ ] ...
- [ ] UserStatus (用户信息)
+ - [ ] Level (用户等级)
+ - [x] Change User Name (改名)
+ - [ ] ...
- [x] Gacha (抽卡系统)
+ - [ ] NormalGacha (公开招募)
+ - [x] AdvancedGacha (干员寻访)
+ - [x] TenAdvancedGacha (十连)
+ - [ ] Pool (卡池/概率系统)
- [ ] Checkin (签到)
+ - [ ] Daily (每日)
+ - [ ] Activity (活动)
+ - [ ] OpenServer (开服)
- [x] Mail (邮件)
+ - [x] MailList
+ - [ ] ReceiveMail
- [ ] Activity (活动)
- [ ] Crisis (活动*)
- [ ] Mission/Flag/Story System (活动**)
- [x] Battle 
+ - [x] Save/Get BattleReplay (代理指挥)
+ - [x] Squad (编队)
+ - [ ] AntiCheat (反作弊 不打算实现)
+ - [ ] Count (作战计数)
+ - [ ] **Rewards (奖励系统)**
+ + - [ ] Activity (活动掉落)
+ + - [ ] Basic (关卡随机/固定掉落)
- [ ] CharBuild (角色养成)
+ - [ ] BoostPoetntial (潜能)
+ - [ ] Upgrade (升级)
+ - [ ] Paradox Simulation (悖论模拟)
+ - [ ] ...
- [ ] Inventory (物品)
+ - [ ] Voucher (干员兑换券等)
+ - [ ] Token (干员信物)
+ - [ ] Consumable (消耗品,如理智顶液/改名卡)
- [ ] Infrastructure (基建)
+ - [ ] Room (基建功能)
+ - [ ] Social (社交)
+ - [ ] ...
- [ ] Shop (商店)
+ - [ ] Skin
+ - [ ] Social
+ - [ ] ...
- [x] Payment (不会真的接入支付系统)
+ - [x] Order (订单)
+ + - [x] Create Order (假的)
+ + - [ ] Confirm Order (假的)
+ - [x] Alipay (假的)
+ - [ ] WeChat
+ - [ ] ... 
- [ ] Misc (杂项)
+ - [x] Exchange Diamond Shard (合成玉兑换)
+ - [ ] Exchange Sanity (理智兑换 <strike>磕 源 石</strike>)

### AuxiliaryFunction

- [x] Database Operation (数据库) (Enhancement needed)
- [x] Log System (日志) (Enhancement needed)
- [ ] Ping (用户游玩信息 未作记录)
- [ ] Errors (错误处理)
- [ ] ...

### Document

- [x] ReadMe
- [ ] API Doc
