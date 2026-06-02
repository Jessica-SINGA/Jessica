import re

with open('酒馆战棋-S13攻略.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. mech-murloc: replace 未来鱼人 with 魔鳍真菌学家
old1 = "cards:[c('murlocs','裁脍鱼人','核心·手牌成长','BG26_137'),c('murlocs','合唱鱼人','核心·得手牌属性','BG26_354'),c('murlocs','未来鱼人','手牌继承','BG34_145'),c('murlocs','拜戈尔格国王','全体+4/+4','BGS_030'),c('murlocs','鱼人蟊贼','使用鱼人全队+5/+5','BG30_122'),c('mechs','附魔哨卫','磁力法术buff','BG35_341'),c('mechs','月铁毁灭战舰','磁力卫星6/6','BG31_171'),c('mechs','废铁枪骑士','磁力全队+5/+5','BG34_175')],\n   strategy:"
new1 = "cards:[c('murlocs','裁脍鱼人','核心·手牌成长','BG26_137'),c('murlocs','合唱鱼人','核心·得手牌属性','BG26_354'),c('murlocs','未来鱼人','手牌继承','BG34_145'),c('murlocs','拜戈尔格国王','全体+4/+4','BGS_030'),c('murlocs','鱼人蟊贼','使用鱼人全队+5/+5','BG30_122'),c('mechs','附魔哨卫','磁力法术buff','BG35_341'),c('mechs','月铁毁灭战舰','磁力卫星6/6','BG31_171'),c('mechs','废铁枪骑士','磁力全队+5/+5','BG34_175')],\n\t   cardsAlt:[c('murlocs','裁脍鱼人','核心·手牌成长','BG26_137'),c('murlocs','合唱鱼人','核心·得手牌属性','BG26_354'),c('murlocs','魔鳍真菌学家','6本·法术教鱼人','BG33_891'),c('murlocs','拜戈尔格国王','全体+4/+4','BGS_030'),c('murlocs','鱼人蟊贼','使用鱼人全队+5/+5','BG30_122'),c('mechs','附魔哨卫','磁力法术buff','BG35_341'),c('mechs','月铁毁灭战舰','磁力卫星6/6','BG31_171'),c('mechs','废铁枪骑士','磁力全队+5/+5','BG34_175')],\n\t   cardsAltDesc:'无7本版本：魔鳍真菌学家替代未来鱼人。手牌buff体系不变，魔鳍每回合买法术养一个1/1鱼人补强经济战力。',\n   strategy:"

if old1 in content:
    content = content.replace(old1, new1, 1)
    print("1. mech-murloc: OK")
else:
    print("1. mech-murloc: NOT FOUND")

# 2. demon-pirate: replace 萨格拉斯的勇士 with 魔焰执行者
old2 = "cards:[c('pirates','佩吉·斯特迪伯','核心·手牌引擎','BG25_032'),c('pirates','空军上将罗杰斯','悬赏令核心','BG33_823'),c('pirates','骄傲的私掠者','悬赏翻倍','BG33_825'),c('pirates','无耻的海盗','左位牌数成长','BG35_701'),c('demons','饥饿的魔蝠','5本·全体吞食','BG21_005'),c('demons','食力征服者','吞食buff酒馆','BG35_153'),c('demons','提克迪奥斯','受伤+3/+2','BG26_523'),c('demons','萨格拉斯的勇士','全体+5/+5','BG27_016')],\n   strategy:"
new2 = "cards:[c('pirates','佩吉·斯特迪伯','核心·手牌引擎','BG25_032'),c('pirates','空军上将罗杰斯','悬赏令核心','BG33_823'),c('pirates','骄傲的私掠者','悬赏翻倍','BG33_825'),c('pirates','无耻的海盗','左位牌数成长','BG35_701'),c('demons','饥饿的魔蝠','5本·全体吞食','BG21_005'),c('demons','食力征服者','吞食buff酒馆','BG35_153'),c('demons','提克迪奥斯','受伤+3/+2','BG26_523'),c('demons','萨格拉斯的勇士','全体+5/+5','BG27_016')],\n\t   cardsAlt:[c('pirates','佩吉·斯特迪伯','核心·手牌引擎','BG25_032'),c('pirates','空军上将罗杰斯','悬赏令核心','BG33_823'),c('pirates','骄傲的私掠者','悬赏翻倍','BG33_825'),c('pirates','无耻的海盗','左位牌数成长','BG35_701'),c('demons','饥饿的魔蝠','5本·全体吞食','BG21_005'),c('demons','食力征服者','吞食buff酒馆','BG35_153'),c('demons','提克迪奥斯','受伤+3/+2','BG26_523'),c('demons','魔焰执行者','4本·吞食成长','BG34_500')],\n\t   cardsAltDesc:'无7本版本：魔焰执行者(4本)替代萨格拉斯的勇士(7本)。吞噬成长节奏更快，魔蝠+食力征服者核心不变。',\n   strategy:"

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("2. demon-pirate: OK")
else:
    print("2. demon-pirate: NOT FOUND")

# 3. ele-pirate: replace 石器时代顽石 with 空气亡魂
old3 = "cards:[c('elementals','活化艾泽里特','核心·法术酒馆成长','BG28_707'),c('elementals','极紫外升腾者','核心·战斗成长','BG31_810'),c('elementals','爆焰灯神','刷新+7/+7','BG34_865'),c('elementals','守护者艾库隆','圣盾核心','BG31_812'),c('pirates','空军上将罗杰斯','悬赏令','BG33_823'),c('pirates','骄傲的私掠者','悬赏翻倍','BG33_825'),c('pirates','佩吉·斯特迪伯','手牌引擎','BG25_032'),c('elementals','石器时代顽石','购买翻倍','BG34_950')],\n   strategy:"
new3 = "cards:[c('elementals','活化艾泽里特','核心·法术酒馆成长','BG28_707'),c('elementals','极紫外升腾者','核心·战斗成长','BG31_810'),c('elementals','爆焰灯神','刷新+7/+7','BG34_865'),c('elementals','守护者艾库隆','圣盾核心','BG31_812'),c('pirates','空军上将罗杰斯','悬赏令','BG33_823'),c('pirates','骄傲的私掠者','悬赏翻倍','BG33_825'),c('pirates','佩吉·斯特迪伯','手牌引擎','BG25_032'),c('elementals','石器时代顽石','购买翻倍','BG34_950')],\n\t   cardsAlt:[c('elementals','活化艾泽里特','核心·法术酒馆成长','BG28_707'),c('elementals','极紫外升腾者','核心·战斗成长','BG31_810'),c('elementals','爆焰灯神','刷新+7/+7','BG34_865'),c('elementals','守护者艾库隆','圣盾核心','BG31_812'),c('pirates','空军上将罗杰斯','悬赏令','BG33_823'),c('pirates','骄傲的私掠者','悬赏翻倍','BG33_825'),c('pirates','佩吉·斯特迪伯','手牌引擎','BG25_032'),c('elementals','空气亡魂','5本·乘借东风','BG34_858')],\n\t   cardsAltDesc:'无7本版本：空气亡魂替代石器时代顽石。每回合花7币触发乘借东风→法术联动活化艾泽里特+极紫外双引擎。',\n   strategy:"

if old3 in content:
    content = content.replace(old3, new3, 1)
    print("3. ele-pirate: OK")
else:
    print("3. ele-pirate: NOT FOUND")

# 4. undead-mech: replace 缝合回收者 + 极性B-Box拳手
old4 = "cards:[c('undead','缝合回收者','核心·复制左边随从','BG31_999'),c('undead','疫病行尸','全局+2攻','BG34_690'),c('undead','被遗忘者纺织工','法术全局+2攻','BG34_692'),c('undead','罪奔者布兰契','复生保留加成','BG24_005'),c('mechs','月铁毁灭战舰','磁力卫星6/6','BG31_171'),c('mechs','极性B-Box拳手','连锁磁力','BG26_149'),c('mechs','拔线机','圣盾亡语频率','BG29_611'),c('undead','提图斯·瑞文戴尔','亡语翻倍','BG25_354')],\n   strategy:"
new4 = "cards:[c('undead','缝合回收者','核心·复制左边随从','BG31_999'),c('undead','疫病行尸','全局+2攻','BG34_690'),c('undead','被遗忘者纺织工','法术全局+2攻','BG34_692'),c('undead','罪奔者布兰契','复生保留加成','BG24_005'),c('mechs','月铁毁灭战舰','磁力卫星6/6','BG31_171'),c('mechs','极性B-Box拳手','连锁磁力','BG26_149'),c('mechs','拔线机','圣盾亡语频率','BG29_611'),c('undead','提图斯·瑞文戴尔','亡语翻倍','BG25_354')],\n\t   cardsAlt:[c('undead','古墓捣蛋鬼','5本·放不下buff','BG30_129'),c('undead','疫病行尸','全局+2攻','BG34_690'),c('undead','被遗忘者纺织工','法术全局+2攻','BG34_692'),c('undead','罪奔者布兰契','复生保留加成','BG24_005'),c('mechs','月铁毁灭战舰','磁力卫星6/6','BG31_171'),c('mechs','蓄能女沙皇','5本·圣盾法术','BG28_741'),c('mechs','拔线机','圣盾亡语频率','BG29_611'),c('undead','提图斯·瑞文戴尔','亡语翻倍','BG25_354')],\n\t   cardsAltDesc:'无7本版本：古墓捣蛋鬼替代缝合回收者，蓄能女沙皇替代Bbox。全局攻击叠加+圣盾法术体系。',\n   strategy:"

if old4 in content:
    content = content.replace(old4, new4, 1)
    print("4. undead-mech: OK")
else:
    print("4. undead-mech: NOT FOUND")

with open('酒馆战棋-S13攻略.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
