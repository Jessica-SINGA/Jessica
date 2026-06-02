# Add alternative final boards without 7-cost minions
import re

with open('酒馆战棋-S13攻略.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The actual whitespace pattern before ], winCondition: is \n   (newline + 3 spaces)
# Not \n\t   (newline + tab + 3 spaces) as originally written

# Define the alternatives: (old string to find, replacement string)
alts = [
  # Demons: remove 萨格拉斯的勇士(7本), replace with 魔焰执行者
  ("c('demons','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077')\n   ], winCondition:'饲料",
   "c('demons','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077')\n   ], finalBoardAlt:[\n     c('demons','饥饿的魔蝠','5本·全体吞食引擎','BG21_005'),\n     c('demons','食力征服者','6本·吞食buff酒馆','BG35_153'),\n     c('demons','狂蝠恐惧卫士','6本·法术吞食联动','BG31_871'),\n     c('demons','提克迪奥斯','5本·受伤+3/+2','BG26_523'),\n     c('demons','魔焰执行者','4本·吞食成长','BG34_500'),\n     c('demons','扭曲的愤怒卫士','6本·出售产饲料','BG35_155'),\n     c('demons','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077')\n   ], winConditionAlt:'无7本版本：魔焰执行者代替萨格拉斯的勇士，吞噬成长节奏更快。魔蝠+食力征服者核心不变，每回合全体数值指数级增长。'\n   ], winCondition:'饲料"),

  # Elementals: remove 石器时代顽石(7本), add 空气亡魂
  ("c('elementals','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077')\n   ], winCondition:'法术",
   "c('elementals','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077')\n   ], finalBoardAlt:[\n     c('elementals','极紫外升腾者','6本·战斗成长引擎','BG31_810'),\n     c('elementals','活化艾泽里特','5本·法术联动','BG28_707'),\n     c('elementals','守护者艾库隆','4本·圣盾核心','BG31_812'),\n     c('elementals','爆焰灯神','4本·刷新+7/+7','BG34_865'),\n     c('elementals','惊喜元素','6本·万能三连','BG26_175'),\n     c('elementals','空气亡魂','5本·乘借东风','BG34_858'),\n     c('elementals','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077')\n   ], winConditionAlt:'无7本版本：空气亡魂的乘借东风替代顽石，每回合花7币触发法术联动。活化艾泽里特+极紫外双引擎驱动，乘借东风法术触发双倍加成。'\n   ], winCondition:'法术"),

  # Nagas: remove 海巫扎尔吉拉(7本), add 宁静的冥想者
  ("c('nagas','海巫扎尔吉拉','7本·复制塑造','BG27_514')\n   ], winCondition:'阿茜萨",
   "c('nagas','海巫扎尔吉拉','7本·复制塑造','BG27_514')\n   ], finalBoardAlt:[\n     c('nagas','潮汐主母阿茜萨','6本·施法全体+1/+1','BG23_013'),\n     c('nagas','护戒纳迦','6本·攻击放戒指','BG34_921'),\n     c('nagas','乘波骑士','4本·纳迦风怒','BG23_007'),\n     c('nagas','热情沙锤手','4本·复制塑造','BG26_505'),\n     c('nagas','大漩涡涌流纳迦','5本·战斗中法术双倍','BG34_922'),\n     c('nagas','无情的女王护卫','6本·战吼亡语进化','BG34_926'),\n     c('nagas','宁静的冥想者','5本·法术buff','BG32_835')\n   ], winConditionAlt:'无7本版本：宁静的冥想者替代海巫。每回合施法驱动阿茜萨全队+1/+1，大漩涡涌流使法术双倍。冥想者使酒馆法术额外+1/+1，与阿茜萨叠加成长。'\n   ], winCondition:'阿茜萨"),

  # Beasts: remove 坚韧的科多兽(7本), add 下水道老鼠头目
  ("c('beasts','香蕉猛猿','4本·召唤攻击翻倍','BG26_802')\n   ], winCondition:'经典鹦鹉",
   "c('beasts','香蕉猛猿','4本·召唤攻击翻倍','BG26_802')\n   ], finalBoardAlt:[\n     c('beasts','巨狼戈德林','6本·亡语+8/+8','BGS_018'),\n     c('beasts','巨大的金刚鹦鹉','4本·触发最左亡语','BGS_078'),\n     c('beasts','提图斯·瑞文戴尔','泛用·亡语翻倍','BG25_354'),\n     c('beasts','狂乱的猎豹','6本·野兽群体成长','BG34_321'),\n     c('beasts','下水道老鼠头目','5本·亡语召老鼠','BG35_604'),\n     c('beasts','炫彩灼天者','5本·受伤群体buff','BG29_806'),\n     c('beasts','香蕉猛猿','4本·召唤攻击翻倍','BG26_802')\n   ], winConditionAlt:'无7本版本：下水道老鼠头目替代科多兽。鹦鹉+瑞文+狼爹核心不变，亡语全队+8/+8(瑞文翻倍=+16/+16)。下水道老鼠头目提供额外亡语频率。'\n   ], winCondition:'经典鹦鹉"),

  # Pirates: remove 杉德尔船长(7本), add 船难海贼
  ("c('pirates','佩吉·斯特迪伯','3本·手牌引擎','BG25_032')\n   ], winCondition:'悬赏令",
   "c('pirates','佩吉·斯特迪伯','3本·手牌引擎','BG25_032')\n   ], finalBoardAlt:[\n     c('pirates','舰长尤朵拉','6本·亡语全队+8/+8','BG33_828'),\n     c('pirates','卑鄙的德鲁斯特','6本·海盗成长引擎','BG32_234'),\n     c('pirates','骄傲的私掠者','5本·悬赏翻倍','BG33_825'),\n     c('pirates','空军上将罗杰斯','6本·悬赏令核心','BG33_823'),\n     c('pirates','船难海贼','5本·战吼亡语悬赏令','BG33_821'),\n     c('pirates','无耻的海盗','5本·左位海盗成长','BG35_701'),\n     c('pirates','佩吉·斯特迪伯','3本·手牌引擎','BG25_032')\n   ], winConditionAlt:'无7本版本：船难海贼替代杉德尔船长的金色功能。悬赏令循环不变(罗杰斯+私掠者+德鲁斯特)，尤朵拉亡语全队+8/+8。船难海贼战吼亡语都产悬赏令，提供额外触发。'\n   ], winCondition:'悬赏令"),

  # Undead: remove 缝合回收者(7本), add 古墓捣蛋鬼
  ("c('undead','骷髅狂射手','5本·复仇成长','BG35_334')\n   ], winCondition:'全局攻击力",
   "c('undead','骷髅狂射手','5本·复仇成长','BG35_334')\n   ], finalBoardAlt:[\n     c('undead','罪奔者布兰契','5本·复生保留加成','BG24_005'),\n     c('undead','永恒召唤者','6本·亡语召永恒骑士','BG25_009'),\n     c('undead','永恒骑士','2本·死亡成长核心','BG25_008'),\n     c('undead','被遗忘者纺织工','6本·法术全局+2攻','BG34_692'),\n     c('undead','致命打击者','6本·亡语召手牌亡灵','BG31_835'),\n     c('undead','骷髅狂射手','5本·复仇成长','BG35_334'),\n     c('undead','古墓捣蛋鬼','5本·放不下buff','BG30_129')\n   ], winConditionAlt:'无7本版本：古墓捣蛋鬼替代缝合回收者。全局攻击力叠加不变，布兰契复生保留。古墓捣蛋鬼在站满时触发全队+2/+2，配合亡灵亡语频率快速触发。'\n   ], winCondition:'全局攻击力"),

  # Mechs: remove 极性B-Box拳手(7本), add 蓄能女沙皇
  ("c('mechs','坠落的飞天魔像','6本·亡语圣盾成长','BG35_342')\n   ], winCondition:'月铁毁灭战舰",
   "c('mechs','坠落的飞天魔像','6本·亡语圣盾成长','BG35_342')\n   ], finalBoardAlt:[\n     c('mechs','月铁毁灭战舰','6本·磁力卫星核心','BG31_171'),\n     c('mechs','蓄能女沙皇','5本·圣盾法术','BG28_741'),\n     c('mechs','废铁枪骑士','6本·磁力全队+5/+5','BG34_175'),\n     c('mechs','P-0UL-TR-0N护巢机','6本·复仇圣盾攻击','BG33_371'),\n     c('mechs','偏折机器人','3本·圣盾核心','BGS_071'),\n     c('mechs','附魔哨卫','4本·磁力法术buff','BG35_341'),\n     c('mechs','坠落的飞天魔像','6本·亡语圣盾成长','BG35_342')\n   ], winConditionAlt:'无7本版本：蓄能女沙皇替代Bbox。月铁每回合产2张6/6磁力卫星，废铁枪每磁力全队+5/+5。女沙皇使圣盾随从获得+4攻击力，配合偏折和P-0UL形成圣盾武库体系。'\n   ], winCondition:'月铁毁灭战舰"),

  # Murlocs: remove 未来鱼人(7本), add 魔鳍真菌学家
  ("c('murlocs','原始鱼人画家','6本·低费成长','BG33_893')\n   ], winCondition:'裁脍鱼人",
   "c('murlocs','原始鱼人画家','6本·低费成长','BG33_893')\n   ], finalBoardAlt:[\n     c('murlocs','合唱鱼人','6本·得手牌属性','BG26_354'),\n     c('murlocs','裁脍鱼人','4本·手牌成长引擎','BG26_137'),\n     c('murlocs','拜戈尔格国王','4本·全体+4/+4','BGS_030'),\n     c('murlocs','鱼人蟊贼','5本·手牌+5/+5','BG30_122'),\n     c('murlocs','魔鳍真菌学家','6本·法术教鱼人','BG33_891'),\n     c('murlocs','怒胆喷毒鱼人','5本·烈毒','BG33_318'),\n     c('murlocs','原始鱼人画家','6本·低费成长','BG33_893')\n   ], winConditionAlt:'无7本版本：魔鳍真菌学家替代未来鱼人。手牌buff体系不变，魔鳍每回合买法术教会一个1/1鱼人，补强经济战力。合唱鱼人复制手牌属性为核心终结手段。'\n   ], winCondition:'裁脍鱼人"),
]

for old, new in alts:
    if old not in content:
        print(f'WARNING: pattern not found for: {old[:60]}...')
    else:
        content = content.replace(old, new, 1)
        print(f'OK: replaced pattern for {old[:60]}...')

with open('酒馆战棋-S13攻略.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
