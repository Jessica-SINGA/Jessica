# Update all tribe ratings, final boards, and overview based on research data
import re

with open('酒馆战棋-S13攻略.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ===== 1. Overview section: update ranking table =====
old_overview = '''<tr><td><span class="tribe-rank rank-t0">T0</span></td><td>恶魔</td><td>版本答案·吞噬饲料体系，数值指数级增长</td></tr>
<tr><td><span class="tribe-rank rank-t1">T1</span></td><td>元素、龙、纳迦</td><td>元素身材恐怖，圣盾龙高攻，女王纳迦成型极快</td></tr>
<tr><td><span class="tribe-rank rank-t2">T2</span></td><td>野猪人、野兽</td><td>野猪人灵活多流派，野兽猿神带队</td></tr>
<tr><td><span class="tribe-rank rank-t3">T3</span></td><td>鱼人、亡灵</td><td>下毒鱼/宰割亡灵，特定对局可用</td></tr>
<tr><td><span class="tribe-rank rank-t4">T4</span></td><td>机械、海盗</td><td>星元自动机/经济挂件，强度垫底</td></tr>'''

new_overview = '''<tr><td><span class="tribe-rank rank-t0">T0</span></td><td>恶魔、元素</td><td>吞噬饲料指数成长；魔网浮灵+活化艾泽里特法术联动</td></tr>
<tr><td><span class="tribe-rank rank-t1">T1</span></td><td>龙、纳迦</td><td>圣盾高攻传功龙；女王护卫成型极快</td></tr>
<tr><td><span class="tribe-rank rank-t2">T2</span></td><td>亡灵、野猪人、野兽</td><td>补丁后亡灵崛起T1级别；野猪人灵活；猿神带队</td></tr>
<tr><td><span class="tribe-rank rank-t3">T3</span></td><td>野兽、鱼人</td><td>特定对局可用，上限有限</td></tr>
<tr><td><span class="tribe-rank rank-t4">T4</span></td><td>机械、海盗</td><td>磁力/经济挂件，强度垫底</td></tr>'''

if old_overview in content:
    content = content.replace(old_overview, new_overview, 1)
    print("1. Overview table: OK")
else:
    print("1. Overview table: NOT FOUND")

# Update the overview description
old_desc = '<div class="tribe-mechanic">S13 灾变降临（35.4.2补丁）：饰品系统回归（第6/9回各选一次，4选1），恶魔新增饲料机制，龙族新增多彩幼龙体系。恶魔版本答案T0独一档，元素/龙/纳迦T1强势。海盗纯经济挂件垫底。数据来源：9700分+高分段大数据。</div>'
new_desc = '<div class="tribe-mechanic">S13 灾变降临（35.4.2补丁）：饰品系统回归（第6/9回各选一次，4选1），恶魔饲料吞噬，元素法术联动，龙传功高攻圣盾，纳迦女王护卫成型最快。补丁后亡灵崛起(堕落屠夫复仇3)。数据来源：网易炉指导9700分+大数据 + 什么值得买高分分析。</div>'

if old_desc in content:
    content = content.replace(old_desc, new_desc, 1)
    print("2. Overview desc: OK")
else:
    print("2. Overview desc: NOT FOUND")

# ===== 2. Elementals: T1 → T0, update final board =====
old_elem = '''  {id:'elementals', icon:'🔥', name:'元素流', rank:'T1', rc:'rank-t1',
   mechanic:'酒馆法术+元素成长，指数级身材膨胀，T1级别强度。投球手+元素刷新体系，配合活化艾泽里特法术联动。',
   phases:[
     {l:'前期',r:'1-4回',cls:'phase-early',
      t:'沙丘土著(1本每局+1/+1)、爆裂飓风(圣盾风怒)过渡。商贩元素(卖=3/3元素)。投球手(火焰/冰雪)出售成长。',
      cards:[c('elementals','沙丘土著','1本·酒馆成长','BG31_815'),c('elementals','爆裂飓风','1本·圣盾风怒','BGS_119'),c('elementals','火焰投球手','2本·出售加攻','BG31_816'),c('elementals','冰雪投球手','2本·出售加命','BG31_818'),c('elementals','商贩元素','2本·卖=3/3元素','BGS_115')]},
     {l:'中期',r:'5-8回',cls:'phase-mid',
      t:'邪能元素(3本酒馆+2/+1)、刷新畸体/酒馆旋风(赚节奏)。守护者艾库隆(4本圣盾核心)。活化艾泽里特(5本法术联动)。',
      cards:[c('elementals','邪能元素','3本·酒馆buff','BG25_041'),c('elementals','幼体水波','3本·亡语刷新成长','BG34_856'),c('elementals','野火元素','3本·过杀溅射','BGS_126'),c('elementals','守护者艾库隆','4本·圣盾核心','BG31_812'),c('elementals','爆焰灯神','4本·刷新+7/+7','BG34_865'),c('elementals','魔网浮灵','4本·奥术吸收','BG35_881'),c('elementals','刷新畸体','4本·免费刷新','BGS_116'),c('elementals','酒馆旋风','4本·随机元素','BGS_123'),c('elementals','活化艾泽里特','5本·法术联动','BG28_707'),c('elementals','空气亡魂','5本·乘借东风','BG34_858'),c('elementals','火焰之地的逸火','5本·获取燃焰','BG35_882')]},
     {l:'后期',r:'9回+',cls:'phase-late',
      t:'惊喜元素(6本万能三连)+极紫外升腾者(战斗开始成长)。石器时代顽石(7本购买翻倍)。需要铜须+达卡莱附魔师。',
      cards:[c('elementals','惊喜元素','6本·万能三连','BG26_175'),c('elementals','极紫外升腾者','6本·战斗开始成长','BG31_810'),c('elementals','石器时代顽石','7本·购买翻倍','BG34_950')]}
   ], slogan:'投球手+沙丘土著开局 → 刷新畸体赚节奏 → 极紫外升腾者终结',
   finalBoard:[
     c('elementals','极紫外升腾者','6本·战斗成长引擎','BG31_810'),
     c('elementals','活化艾泽里特','5本·法术联动','BG28_707'),
     c('elementals','守护者艾库隆','4本·圣盾核心','BG31_812'),
     c('elementals','爆焰灯神','4本·刷新+7/+7','BG34_865'),
     c('elementals','惊喜元素','6本·万能三连','BG26_175'),
     c('elementals','石器时代顽石','7本·购买翻倍','BG34_950'),
     c('elementals','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077')
   ], finalBoardAlt:[
     c('elementals','极紫外升腾者','6本·战斗成长引擎','BG31_810'),
     c('elementals','活化艾泽里特','5本·法术联动','BG28_707'),'''

new_elem = '''  {id:'elementals', icon:'🔥', name:'元素流', rank:'T0', rc:'rank-t0',
   mechanic:'酒馆法术+元素成长，T0级别指数级膨胀。魔网浮灵奥术吸收复制高血量属性，活化艾泽里特法术联动酒馆成长。铜须为版本刚需。',
   phases:[
     {l:'前期',r:'1-4回',cls:'phase-early',
      t:'沙丘土著(1本每局+1/+1)、爆裂飓风(圣盾风怒)过渡。商贩元素(卖=3/3元素)。投球手(火焰/冰雪)出售成长。',
      cards:[c('elementals','沙丘土著','1本·酒馆成长','BG31_815'),c('elementals','爆裂飓风','1本·圣盾风怒','BGS_119'),c('elementals','火焰投球手','2本·出售加攻','BG31_816'),c('elementals','冰雪投球手','2本·出售加命','BG31_818'),c('elementals','商贩元素','2本·卖=3/3元素','BGS_115')]},
     {l:'中期',r:'5-8回',cls:'phase-mid',
      t:'邪能元素(3本酒馆+2/+1)、刷新畸体/酒馆旋风(赚节奏)。守护者艾库隆(4本圣盾核心)。魔网浮灵(4本奥术吸收核心)！活化艾泽里特(5本法术联动酒馆)。',
      cards:[c('elementals','邪能元素','3本·酒馆buff','BG25_041'),c('elementals','幼体水波','3本·亡语刷新成长','BG34_856'),c('elementals','野火元素','3本·过杀溅射','BGS_126'),c('elementals','守护者艾库隆','4本·圣盾核心','BG31_812'),c('elementals','爆焰灯神','4本·刷新+7/+7','BG34_865'),c('elementals','魔网浮灵','4本·奥术吸收核心','BG35_881'),c('elementals','刷新畸体','4本·免费刷新','BGS_116'),c('elementals','酒馆旋风','4本·随机元素','BGS_123'),c('elementals','活化艾泽里特','5本·法术联动','BG28_707'),c('elementals','空气亡魂','5本·乘借东风','BG34_858'),c('elementals','火焰之地的逸火','5本·获取燃焰','BG35_882')]},
     {l:'后期',r:'9回+',cls:'phase-late',
      t:'惊喜元素(6本万能三连)+极紫外升腾者(战斗开始成长)。空气亡魂花7币乘借东风(+8/+8)持续成长。铜须+达卡莱附魔师。',
      cards:[c('elementals','惊喜元素','6本·万能三连','BG26_175'),c('elementals','极紫外升腾者','6本·战斗开始成长','BG31_810'),c('elementals','空气亡魂','5本·花7币乘借东风','BG34_858')]}
   ], slogan:'魔网浮灵奥术吸收 → 活化艾泽里特+铜须 → 指数级膨胀',
   finalBoard:[
     c('elementals','魔网浮灵','4本·奥术吸收核心','BG35_881'),
     c('elementals','极紫外升腾者','6本·战斗成长引擎','BG31_810'),
     c('elementals','活化艾泽里特','5本·法术联动','BG28_707'),
     c('elementals','火焰之地的逸火','5本·获取燃焰','BG35_882'),
     c('elementals','爆焰灯神','4本·刷新+7/+7','BG34_865'),
     c('elementals','空气亡魂','5本·乘借东风','BG34_858'),
     c('elementals','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077')
   ], finalBoardAlt:[
     c('elementals','极紫外升腾者','6本·战斗成长引擎','BG31_810'),
     c('elementals','活化艾泽里特','5本·法术联动','BG28_707'),'''

if old_elem in content:
    content = content.replace(old_elem, new_elem, 1)
    print("3. Elementals data: OK")
else:
    print("3. Elementals data: NOT FOUND")

# Replace elementals finalBoardAlt end part (石器时代顽石 → 空气亡魂)
old_elem_alt_end = '''     c('elementals','爆焰灯神','4本·刷新+7/+7','BG34_865'),
     c('elementals','惊喜元素','6本·万能三连','BG26_175'),
     c('elementals','空气亡魂','5本·乘借东风','BG34_858'),
     c('elementals','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077')
   ], cardsAltDesc:'无7本版本：空气亡魂替代石器时代顽石。每回合花7币触发乘借东风→法术联动活化艾泽里特+极紫外双引擎。',
   winCondition:'法术酒馆永动机：活化艾泽里特使酒馆元素永久成长+爆焰灯神刷新+7/+7+空气亡魂乘借东风。铜须翻倍战吼收益。极紫外升腾者战斗开始成长终结。指数级膨胀。','''

new_elem_alt_end = '''     c('elementals','爆焰灯神','4本·刷新+7/+7','BG34_865'),
     c('elementals','空气亡魂','5本·乘借东风','BG34_858'),
     c('elementals','守护者艾库隆','4本·圣盾核心','BG31_812'),
     c('elementals','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077')
   ], cardsAltDesc:'无7本版本：空气亡魂替代石器时代顽石。每回合花7币触发乘借东风(+8/+8)→法术联动活化艾泽里特+极紫外双引擎，成长稳定持续。',
   winCondition:'T0永动机：魔网浮灵每回合奥术吸收复制酒馆最高生命值一半属性(铜须翻倍两张)→活化艾泽里特每施放法术酒馆元素永久+3/+3→空气亡魂花7币乘借东风+8/+8→爆焰灯神刷新+7/+7。极紫外战斗开始成长终结。指数级膨胀。','''

if old_elem_alt_end in content:
    content = content.replace(old_elem_alt_end, new_elem_alt_end, 1)
    print("4. Elementals alt end: OK")
else:
    print("4. Elementals alt end: NOT FOUND")

# ===== 3. Dragons: remove 珍稀增强幼龙, update final board =====
# Replace 珍稀增强幼龙 with 骨火巨龙夜之魇 in finalBoard
old_dragon_final = '''   finalBoard:[
     c('dragons','奥术守护者卡雷苟斯','5本·战吼成长引擎','BGS_041'),
     c('dragons','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077'),
     c('dragons','火铸唤魔师','6本·法术成长引擎','BG32_822'),
     c('dragons','珍稀增强幼龙','4本·战斗+4/+4','BG21_014'),
     c('dragons','执念诗心龙','4本·圣盾保留','BG29_813'),
     c('dragons','泰蕾苟萨','2本·保留战斗加成','BG21_015'),
     c('dragons','绿色多彩幼龙','龙+2/+4','BG34_636t'),
   ], winCondition:'每触发一次战吼→全体龙永久+2/+2(卡雷苟斯)，铜须翻倍。珍稀增强幼龙战斗开始全体+4/+4，执念诗心龙+泰蕾苟萨保留战斗加成回合间累积。火铸唤魔师配合酒馆法术叠层。核心是铜须+卡雷苟斯双核驱动，每回合buy战吼随从→全体龙无限成长。'},'''

new_dragon_final = '''   finalBoard:[
     c('dragons','奥术守护者卡雷苟斯','5本·战吼成长引擎','BGS_041'),
     c('dragons','布莱恩·铜须','泛用·双倍战吼','BG_LOE_077'),
     c('dragons','火铸唤魔师','6本·法术成长引擎','BG32_822'),
     c('dragons','骨火巨龙夜之魇','6本·亡语传递攻击力','BG29_815'),
     c('dragons','执念诗心龙','4本·圣盾保留','BG29_813'),
     c('dragons','泰蕾苟萨','2本·保留战斗加成','BG21_015'),
     c('dragons','生火专家','6本·拿酒馆法术','BG28_595'),
   ], winCondition:'传功龙路线：卡雷苟斯(战吼→全体+2/+2)+铜须翻倍为成长引擎，火铸唤魔师(法术叠层)配合生火专家产酒馆法术叠层。骨火巨龙夜之魇亡语将高攻传递给其他龙。执念诗心龙+泰蕾苟萨保留战斗加成回合间累积。绿色多彩幼龙/蓝色多彩幼龙为灵活位。注意：大威天龙S13仅T4强度(怕亡灵频率)，走传功龙混法术路线更优。'},'''

if old_dragon_final in content:
    content = content.replace(old_dragon_final, new_dragon_final, 1)
    print("5. Dragons final board: OK")
else:
    print("5. Dragons final board: NOT FOUND")

# Update dragon mechanic
old_dragon_mech = '''   mechanic:'多彩幼龙(5色)+卡雷苟斯战吼体系。S13新增多彩幼龙联动酒馆法术和龙族成长。','''
new_dragon_mech = '''   mechanic:'传功龙路线。卡雷苟斯(5本战吼核心)+火铸唤魔师(法术叠层)。骨火巨龙夜之魇亡语传递高攻。珍稀增强幼龙大数据-0.05影响陷阱卡，不建议放最终阵容。','''

if old_dragon_mech in content:
    content = content.replace(old_dragon_mech, new_dragon_mech, 1)
    print("6. Dragons mechanic: OK")
else:
    print("6. Dragons mechanic: NOT FOUND")

# Update dragon slogan
old_dragon_slogan = "slogan:'前期蓄势主唱 → 多彩龙+卡雷苟斯 → 后期火铸唤魔师',"
new_dragon_slogan = "slogan:'蓄势主唱开局 → 卡雷苟斯+铜须战吼成长 → 骨火巨龙传功 -> 火铸唤魔师叠层',"

if old_dragon_slogan in content:
    content = content.replace(old_dragon_slogan, new_dragon_slogan, 1)
    print("7. Dragons slogan: OK")
else:
    print("7. Dragons slogan: NOT FOUND")

# Update dragon late phase description
old_dragon_late = "t:'生火专家(6本拿法术)、骨火巨龙夜之魇(亡语传递攻击力)。火铸唤魔师(6本战斗成长)。黑曜石掠夺者(7本狂战斧)。',"
new_dragon_late = "t:'生火专家(6本拿法术)、骨火巨龙夜之魇(亡语传递攻击力)。火铸唤魔师(6本法术战斗成长)。珍稀增强幼龙为中期过渡卡后期乏力。',"

if old_dragon_late in content:
    content = content.replace(old_dragon_late, new_dragon_late, 1)
    print("8. Dragons late phase: OK")
else:
    print("8. Dragons late phase: NOT FOUND")

# ===== 4. Undead: T3 → T2 (post-patch崛起), update final board =====
old_undead = '''  {id:'undead', icon:'💀', name:'亡灵流', rank:'T3', rc:'rank-t3',
   mechanic:'亡灵频率·攻击力全局累积体系。疫病行尸(全局+2攻)、被遗忘者纺织工(法术全局+2攻)。缝合回收者(7本套娃)+提图斯·瑞文戴尔。',
   phases:[
     {l:'前期',r:'1-4回',cls:'phase-early',
      t:'复生漫步者(1本复生)、鳄鱼人掠夺者(2本身材成长)。永恒骑士(2本+4/+2超模)。',
      cards:[c('undead','复生漫步者','1本·复生','BG25_001'),c('undead','捕食的跟踪者','1本·亡语成长','BG25_013'),c('undead','鳄鱼人掠夺者','2本·亡语频率','BG28_300'),c('undead','永恒骑士','2本·+4/+2超模','BG25_008')]},'''

new_undead = '''  {id:'undead', icon:'💀', name:'亡灵流', rank:'T2', rc:'rank-t2',
   mechanic:'补丁后亡灵崛起T1~T2级别，堕落屠夫复仇3成为新一代毒瘤。频率亡语+全局攻击累积+骨火巨龙瑞文传攻。',
   phases:[
     {l:'前期',r:'1-4回',cls:'phase-early',
      t:'复生漫步者(1本复生)、永恒骑士(2本+4/+2超模锁血)、灵魂杂耍者。',
      cards:[c('undead','复生漫步者','1本·复生','BG25_001'),c('undead','捕食的跟踪者','1本·亡语成长','BG25_013'),c('undead','鳄鱼人掠夺者','2本·亡语频率','BG28_300'),c('undead','永恒骑士','2本·+4/+2超模','BG25_008')]},'''

if old_undead in content:
    content = content.replace(old_undead, new_undead, 1)
    print("9. Undead header: OK")
else:
    print("9. Undead header: NOT FOUND")

# Update undead mid phase
old_undead_mid = "{l:'中期',r:'5-8回',cls:'phase-mid',\n      t:'遗骸看管者(3本优质三连)、疫病行尸(全局+2攻)。古墓捣蛋鬼(3本放不下buff)配合高频率触发。被遗忘者纺织工(6本法术全局+2攻)。',\n      cards:[c('undead','遗骸看管者','3本·优质三连','BG25_022'),c('undead','古墓捣蛋鬼','3本·放不下buff','BG30_129'),c('undead','疫病行尸','4本·全局+2攻','BG34_690'),c('undead','永恒骑士','2本·死亡成长','BG25_008'),c('undead','永恒召唤者','6本·亡语召永恒','BG25_009'),c('undead','被遗忘者纺织工','6本·法术全局+2攻','BG34_692'),c('undead','提图斯·瑞文戴尔','5本·亡语翻倍','BG25_354')]},"

new_undead_mid = "{l:'中期',r:'5-8回',cls:'phase-mid',\n      t:'遗骸看管者(3本优质三连)、疫病行尸(全局+2攻)。**堕落屠夫(5本复仇3毒瘤!)**配合法强轻松高攻。被遗忘者纺织工(6本法术全局+2攻)。骨火巨龙+瑞文传攻。',\n      cards:[c('undead','遗骸看管者','3本·优质三连','BG25_022'),c('undead','古墓捣蛋鬼','3本·放不下buff','BG30_129'),c('undead','疫病行尸','4本·全局+2攻','BG34_690'),c('undead','堕落屠夫','5本·复仇3毒瘤','BG35_334'),c('undead','永恒召唤者','6本·亡语召永恒','BG25_009'),c('undead','被遗忘者纺织工','6本·法术全局+2攻','BG34_692'),c('undead','提图斯·瑞文戴尔','5本·亡语翻倍','BG25_354')]},"

if old_undead_mid in content:
    content = content.replace(old_undead_mid, new_undead_mid, 1)
    print("10. Undead mid phase: OK")
else:
    print("10. Undead mid phase: NOT FOUND")

# Update undead late phase
old_undead_late = "{l:'后期',r:'9回+',cls:'phase-late',\n      t:'罪奔者布兰契(5本复生保留加成)+致命打击者(亡语召手牌)。缝合回收者(7本套娃)配合碎地者→陆行鸟→瑞文翻倍。刚需瑞文。',\n      cards:[c('undead','罪奔者布兰契','5本·复生保留加成','BG24_005'),c('undead','致命打击者','6本·亡语召手牌','BG31_835'),c('undead','骷髅狂射手','5本·复仇成长','BG35_334'),c('undead','缝合回收者','7本·套娃核心','BG31_999')]}"

new_undead_late = "{l:'后期',r:'9回+',cls:'phase-late',\n      t:'堕落屠夫(复仇3)+骨火巨龙+瑞文传功。缝合回收者(7本套娃)配合碎地者→瑞文翻倍。频率碾压，亡灵当道。',\n      cards:[c('undead','堕落屠夫','5本·复仇3毒瘤','BG35_334'),c('undead','罪奔者布兰契','5本·复生保留加成','BG24_005'),c('undead','骨火巨龙夜之魇','6本·亡语传递攻击','BG29_815'),c('undead','缝合回收者','7本·套娃核心','BG31_999')]}"

if old_undead_late in content:
    content = content.replace(old_undead_late, new_undead_late, 1)
    print("11. Undead late phase: OK")
else:
    print("11. Undead late phase: NOT FOUND")

# Update undead finalBoard and finalBoardAlt
old_undead_final = '''   slogan:'遗骸看管者开局 → 全局攻击叠加 → 缝合回收者套娃终结',
   finalBoard:[
     c('undead','罪奔者布兰契','5本·复生保留加成','BG24_005'),
     c('undead','永恒召唤者','6本·亡语召永恒骑士','BG25_009'),
     c('undead','永恒骑士','2本·死亡成长核心','BG25_008'),
     c('undead','被遗忘者纺织工','6本·法术全局+2攻','BG34_692'),
     c('undead','致命打击者','6本·亡语召手牌','BG31_835'),
     c('undead','骷髅狂射手','5本·复仇成长','BG35_334'),
     c('undead','提图斯·瑞文戴尔','泛用·亡语翻倍','BG25_354'),
   ], finalBoardAlt:[
     c('undead','罪奔者布兰契','5本·复生保留加成','BG24_005'),
     c('undead','永恒召唤者','6本·亡语召永恒骑士','BG25_009'),
     c('undead','永恒骑士','2本·死亡成长核心','BG25_008'),
     c('undead','被遗忘者纺织工','6本·法术全局+2攻','BG34_692'),
     c('undead','致命打击者','6本·亡语召手牌','BG31_835'),
     c('undead','骷髅狂射手','5本·复仇成长','BG35_334'),
     c('undead','古墓捣蛋鬼','5本·放不下buff','BG30_129'),
   ], winConditionAlt:'无7本版本：古墓捣蛋鬼替代缝合回收者。全局攻击力叠加不变，布兰契复生保留。古墓捣蛋鬼在站满时触发全队+2/+2，配合亡灵亡语频率快速触发。',
   winCondition:'全局攻击力累积+缝合回收者套娃。疫病行尸+被遗忘者纺织工每局全局+2攻叠加。缝合回收者吃掉碎地者→亡语召唤复制→瑞文翻倍→产出6只碎地者碾压。','''

new_undead_final = '''   slogan:'永恒骑士开局锁血 → 堕落屠夫频率+法强 → 骨火巨龙瑞文传攻终结',
   finalBoard:[
     c('undead','堕落屠夫','5本·复仇3毒瘤','BG35_334'),
     c('undead','骨火巨龙夜之魇','6本·亡语传递攻击','BG29_815'),
     c('undead','罪奔者布兰契','5本·复生保留加成','BG24_005'),
     c('undead','永恒召唤者','6本·亡语召永恒骑士','BG25_009'),
     c('undead','永恒骑士','2本·死亡成长核心','BG25_008'),
     c('undead','被遗忘者纺织工','6本·法术全局+2攻','BG34_692'),
     c('undead','提图斯·瑞文戴尔','泛用·亡语翻倍','BG25_354'),
   ], finalBoardAlt:[
     c('undead','堕落屠夫','5本·复仇3毒瘤','BG35_334'),
     c('undead','骨火巨龙夜之魇','6本·亡语传递攻击','BG29_815'),
     c('undead','罪奔者布兰契','5本·复生保留加成','BG24_005'),
     c('undead','永恒召唤者','6本·亡语召永恒骑士','BG25_009'),
     c('undead','永恒骑士','2本·死亡成长核心','BG25_008'),
     c('undead','被遗忘者纺织工','6本·法术全局+2攻','BG34_692'),
     c('undead','古墓捣蛋鬼','5本·放不下buff','BG30_129'),
   ], winConditionAlt:'无7本版本：古墓捣蛋鬼替代缝合回收者。堕落屠夫复仇3频率为核心，全局攻击叠加不变。',
   winCondition:'亡灵频率+传功：堕落屠夫复仇3匹配法强成型高攻频率。骨火巨龙+瑞文使攻击力全局传递。被遗忘者纺织工每施放法术全局+2攻。缝合回收者吃掉左边→亡语召唤复制→瑞文翻倍。S13补丁后亡灵强势崛起。','''

if old_undead_final in content:
    content = content.replace(old_undead_final, new_undead_final, 1)
    print("12. Undead final board: OK")
else:
    print("12. Undead final board: NOT FOUND")

# ===== 5. Naga: update final board alt (replace 海巫扎尔吉拉 alt) =====
old_naga_final = '''     c('nagas','海巫扎尔吉拉','7本·复制塑造','BG27_514')
   ], winCondition:'阿茜萨'''

new_naga_final = '''     c('nagas','宁静的冥想者','5本·法术buff','BG32_835')
   ], winConditionAlt:'无7本版本：宁静的冥想者替代海巫扎尔吉拉(大数据+0.01极低)。冥想者使酒馆法术额外+1/+1，配合阿茜萨每回合施法全纳迦成长。',
   winCondition:'阿茜萨'''

if old_naga_final in content:
    content = content.replace(old_naga_final, new_naga_final, 1)
    print("13. Naga final board alt: OK")
else:
    print("13. Naga final board alt: NOT FOUND")

# ===== 6. Murlocs: T3 → T4, update overview =====
old_murloc_header = "  {id:'murlocs', icon:'🐟', name:'鱼人流', rank:'T3', rc:'rank-t3',"
new_murloc_header = "  {id:'murlocs', icon:'🐟', name:'鱼人流', rank:'T4', rc:'rank-t4',"

if old_murloc_header in content:
    content = content.replace(old_murloc_header, new_murloc_header, 1)
    print("14. Murlocs rank: OK")
else:
    print("14. Murlocs rank: NOT FOUND")

# ===== 7. Update overview description for 7-star =====
old_7star = '<div class="tip-box"><h4>7本随从说明</h4>7本随从整体强度与费用不匹配，高分段数据平庸，大部分7本随从为负收益。非天胡不建议强追7本。</div>'
new_7star = '<div class="tip-box"><h4>7本随从说明</h4>7本随从整体强度与费用不匹配，高分段数据平庸：杉德尔船长+0.05、海巫扎尔吉拉+0.01、萨格拉斯的勇士负收益。非天胡不建议强追7本。</div>'

if old_7star in content:
    content = content.replace(old_7star, new_7star, 1)
    print("15. 7-star tip: OK")
else:
    print("15. 7-star tip: NOT FOUND")

# ===== 8. Update elementals in overview row for rank-t0 =====
# The overview has: <span class="tribe-rank rank-t1">T1</span></td><td>元素
# Already handled in the overview table rewrite above.

# ===== 9. Update 元素 mid phase =====
# Remove 1本 cards from mid phase list (they're listed in 前期, not 中期)
# Already corrected in the full replacement above.

with open('酒馆战棋-S13攻略.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done - all updates applied')
