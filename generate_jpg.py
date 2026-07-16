#!/usr/bin/env python3
"""湖南省光电融合产业全景图 — 生成单张高分辨率 JPG（清华风格）"""

from PIL import Image, ImageDraw, ImageFont
import os

# === 画布尺寸 ===
W, H = 2400, 5400
BG_WHITE = (255, 255, 255)
BG_LIGHT = (245, 243, 248)

# === 清华色彩 ===
THU_PURPLE = (102, 0, 153)
THU_PURPLE_DEEP = (75, 46, 115)
THU_PURPLE_PALE = (243, 239, 247)
THU_PURPLE_MIST = (232, 224, 240)
ACCENT_GOLD = (196, 154, 42)
ACCENT_RED = (156, 40, 40)
ACCENT_TEAL = (0, 108, 103)
ACCENT_NAVY = (26, 46, 92)

TEXT_DARK = (44, 44, 44)
TEXT_BODY = (74, 74, 74)
TEXT_SECONDARY = (122, 122, 138)
TEXT_MUTED = (170, 170, 184)
TEXT_WHITE = (255, 255, 255)
LINE_LIGHT = (224, 220, 232)

# === 字体 ===
def load_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

FONT_TITLE = load_font(72, bold=True)
FONT_SUBTITLE = load_font(36, bold=True)
FONT_SECTION = load_font(48, bold=True)
FONT_BODY = load_font(28)
FONT_SMALL = load_font(24)
FONT_TINY = load_font(20)
FONT_BIG_NUM = load_font(90, bold=True)
FONT_BADGE = load_font(22, bold=True)

img = Image.new('RGB', (W, H), BG_WHITE)
draw = ImageDraw.Draw(img)

# === 工具函数 ===
def rect(x, y, w, h, color):
    draw.rectangle([x, y, x+w, y+h], fill=color)

def rrect(x, y, w, h, color, r=8):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=color)

def hline(x, y, w, color=LINE_LIGHT, width=2):
    draw.line([x, y, x+w, y], fill=color, width=width)

def vline(x, y, h, color=LINE_LIGHT, width=2):
    draw.line([x, y, x, y+h], fill=color, width=width)

def text(x, y, s, font, color):
    draw.text((x, y), s, font=font, fill=color)

def text_center(x, y, w, s, font, color):
    bbox = draw.textbbox((0,0), s, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + (w - tw)//2, y), s, font=font, fill=color)

def text_right(x, y, w, s, font, color):
    bbox = draw.textbbox((0,0), s, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + w - tw, y), s, font=font, fill=color)

# === 布局参数 ===
PAD = 80
CW = W - 2 * PAD  # 内容宽度

y = 0

# ========== 1. 封面区 ==========
# 左侧紫色块
rect(0, 0, 900, 700, THU_PURPLE)
# 紫色区内英文
text(120, 280, "HUNAN OPTOELECTRONIC", load_font(28), (208, 184, 232))
text(120, 330, "FUSION INDUSTRY PANORAMA", load_font(28), (208, 184, 232))
rect(120, 500, 240, 4, (255, 255, 255))
text(120, 530, "2026 INDUSTRY REPORT", load_font(24), (184, 154, 216))

# 右侧白色区
text(1040, 200, "产业研究报告", load_font(28), ACCENT_GOLD)
text(1040, 260, "湖南省光电融合", FONT_TITLE, THU_PURPLE)
text(1040, 360, "产业全景图", FONT_TITLE, THU_PURPLE)
rect(1040, 480, 160, 5, THU_PURPLE)
text(1040, 510, "4×4 现代化产业体系  ·  十五五规划关键之年  ·  2026年度产业图谱", load_font(26), TEXT_SECONDARY)

# KPI 行
kpis = [("1,571.74", "亿元", "重点项目总投资"), ("50", "个", "重点项目"),
        ("478.91", "亿元", "预计新增营收"), ("7", "大", "核心集聚城市")]
kpi_colors = [THU_PURPLE, THU_PURPLE_DEEP, ACCENT_GOLD, ACCENT_TEAL]
for i, (val, unit, label) in enumerate(kpis):
    kx = 1040 + i * 320
    text(kx, 560, val, FONT_BIG_NUM, kpi_colors[i])
    bbox = draw.textbbox((0,0), val, font=FONT_BIG_NUM)
    text(kx + bbox[2]-bbox[0] + 10, 600, unit, load_font(24), TEXT_MUTED)
    text(kx, 660, label, load_font(22), TEXT_SECONDARY)

hline(1040, 730, 1200, LINE_LIGHT, 2)
text(1040, 750, "数据来源：湖南省工业和信息化厅 · 湖南省人民政府门户网站 · 湖南日报", load_font(20), TEXT_MUTED)

y = 820

# ========== 2. 目录 ==========
rect(0, y, W, 6, THU_PURPLE)
y += 30
text(PAD, y, "目  录", FONT_SECTION, THU_PURPLE)
y += 80
hline(PAD, y, CW, LINE_LIGHT)
y += 30

contents = [
    ("01", "产业链全景", "光电融合上中下游全链路解析", THU_PURPLE),
    ("02", "区域布局", "七大核心产业集聚区", ACCENT_TEAL),
    ("03", "重点企业", "16家龙头与重点企业", ACCENT_GOLD),
    ("04", "创新平台", "科研平台与高校力量", THU_PURPLE_DEEP),
    ("05", "政策支撑", "8项核心政策体系", ACCENT_RED),
    ("06", "发展趋势", "四大未来方向", ACCENT_NAVY),
]
for i, (num, title, desc, color) in enumerate(contents):
    col = i % 2
    row = i // 2
    cx = PAD + col * 1100
    cy = y + row * 130
    text(cx, cy, num, FONT_BIG_NUM, color)
    vline(cx + 130, cy + 10, 90, LINE_LIGHT, 2)
    text(cx + 160, cy + 10, title, FONT_SUBTITLE, TEXT_DARK)
    text(cx + 160, cy + 60, desc, FONT_SMALL, TEXT_SECONDARY)

y += 420

# ========== 3. 产业链全景 ==========
rect(0, y, W, 6, THU_PURPLE)
y += 30
text(PAD, y, "光电融合产业链全景", FONT_SECTION, THU_PURPLE)
y += 80
hline(PAD, y, CW, LINE_LIGHT)
y += 20

chain_data = [
    ("上游", "材料 · 芯片", THU_PURPLE, [
        ("光电材料", "基板玻璃、光电特种气体、靶材", "邵虹 · 中化蓝天 · 江丰电子"),
        ("光芯片", "DFB/EML激光芯片、硅光芯片", "硅基Micro-LED · 高速EML"),
        ("功率半导体", "IGBT、MOSFET、第三代半导体", "中车时代半导体 · 三一硅能"),
        ("光纤光缆", "单模/多模光纤、MPO连接器", "信维电子 · 艾迪奥"),
        ("光学元器件", "光学镜头、偏光片、滤光片", "山嘉光电 · 谱特光电"),
    ]),
    ("中游", "器件 · 模组", ACCENT_TEAL, [
        ("新型显示面板", "LCD/OLED、Mini-LED背光/直显", "惠科 · 中沛光电 · 蓝思科技"),
        ("光通信器件", "光模块、激光器、光放大器", "光智通信 · 图灵智算"),
        ("光电传感与精密", "激光蚀刻、COG芯片绑定", "阿秒光学 · 弘宇精密"),
        ("半导体封测", "功率器件封装、集成电路制造", "湘潭智造基地 · 明正宏"),
        ("光电功能材料", "碳基材料、3D玻璃、柔性材料", "金博股份 · 麓邦光电"),
    ]),
    ("下游", "应用 · 终端", ACCENT_GOLD, [
        ("智能终端", "智能手机、具身智能机器人", "蓝思机器人 · 中沛手机"),
        ("数据中心与算力", "AI智算中心、高速光互联", "图灵智算"),
        ("5G通信与网络", "5G基站光模块、运营商集采", "光智通信 · 信维电科"),
        ("安防与车载光电", "安防监控、车载激光雷达", "英飞拓"),
        ("新型显示终端", "LED直显、Mini-LED背光电视", "惠科直显 · 明和数艺"),
    ]),
]

card_w = 380
card_gap = 12
row_h = 280
for row_idx, (label, sub, color, items) in enumerate(chain_data):
    ry = y + row_idx * (row_h + 15)
    # 左侧标签
    rect(PAD, ry, 200, row_h, color)
    text_center(PAD, ry + 80, 200, label, FONT_SUBTITLE, TEXT_WHITE)
    text_center(PAD, ry + 150, 200, sub, FONT_SMALL, (224, 208, 240))
    # 5个卡片
    for i, (title, desc, ent) in enumerate(items):
        cx = PAD + 220 + i * (card_w + card_gap)
        rect(cx, ry, card_w, row_h, BG_LIGHT)
        rect(cx, ry, card_w, 4, color)
        # 边框
        for b in range(1):
            draw.rectangle([cx, ry, cx+card_w, ry+row_h], outline=LINE_LIGHT, width=1)
        text(cx + 15, ry + 20, title, FONT_BODY, color)
        text(cx + 15, ry + 75, desc, FONT_SMALL, TEXT_BODY)
        hline(cx + 15, ry + 180, card_w - 30, LINE_LIGHT, 1)
        text(cx + 15, ry + 195, ent, FONT_TINY, color)

y += 3 * (row_h + 15) + 30

# ========== 4. 七大核心集聚区 ==========
rect(0, y, W, 6, THU_PURPLE)
y += 30
text(PAD, y, "七大核心产业集聚区", FONT_SECTION, THU_PURPLE)
y += 80
hline(PAD, y, CW, LINE_LIGHT)
y += 20

regions = [
    ("长沙", "省会 · 核心引擎", "新型显示龙头 · 智能终端 · 先进计算", "百亿+项目6个", THU_PURPLE,
     "惠科 · 蓝思科技 · 图灵智算 · 麓邦光电 · 明和数艺 · 韶光芯材"),
    ("株洲", "功率半导体国家队", "功率半导体全产业链 · 国家级集群", "220+企业", ACCENT_TEAL,
     "中车时代半导体 · 三一硅能 · 赛德雷特"),
    ("湘潭", "半导体智造基地", "半导体制造 · 智能终端设备", "23.8亿投资", ACCENT_GOLD,
     "半导体湘潭智造基地 · 蓝思智能终端 · 锦智光电 · 金杯电工"),
    ("益阳", "湖南光电谷", "光通信器件 · 长益科创走廊节点", "86项专利 · 12项转化", THU_PURPLE_DEEP,
     "未来光电技术研究院 · 金博股份 · 信维电科 · 光智通信 · 江丰电子"),
    ("郴州", "湘南光电谷", "光电显示完整产业链 · 湾区转移承接", "80亿产值 · 59家企业", ACCENT_RED,
     "宜章经开区 · 山嘉光电 · 谱特光电 · 中沛光电 · 英飞拓 · 阿秒光学"),
    ("邵阳", "基板玻璃基地", "显示基板玻璃 · 上下游配套集聚", "4条热端生产线", ACCENT_NAVY,
     "邵虹基板玻璃 · 致成科技"),
]

rc_w = 700
rc_h = 380
rc_gap = 15
for i, (city, badge, role, data_str, color, enterprises) in enumerate(regions):
    col = i % 3
    row = i // 3
    rx = PAD + col * (rc_w + rc_gap)
    ry = y + row * (rc_h + rc_gap)
    rect(rx, ry, rc_w, rc_h, BG_WHITE)
    draw.rectangle([rx, ry, rx+rc_w, ry+rc_h], outline=LINE_LIGHT, width=1)
    rect(rx, ry, 8, rc_h, color)
    text(rx + 25, ry + 15, badge, FONT_BADGE, color)
    text(rx + 25, ry + 55, city, load_font(52, bold=True), TEXT_DARK)
    text_right(rx + rc_w - 200, ry + 60, 180, data_str, FONT_BODY, color)
    text(rx + 25, ry + 130, role, FONT_SMALL, TEXT_SECONDARY)
    hline(rx + 25, ry + 180, rc_w - 50, LINE_LIGHT, 1)
    text(rx + 25, ry + 195, enterprises, FONT_SMALL, TEXT_BODY)

y += 2 * (rc_h + rc_gap) + 30

# ========== 5. 重点企业 ==========
rect(0, y, W, 6, THU_PURPLE)
y += 30
text(PAD, y, "龙头与重点企业", FONT_SECTION, THU_PURPLE)
y += 80
hline(PAD, y, CW, LINE_LIGHT)
y += 20

enterprises = [
    ("蓝思科技", "长沙·浏阳", "智能装备基地，年产1万台设备+50万台机器人", "十大产业项目", ACCENT_RED),
    ("惠科", "长沙·浏阳", "Mini-LED背光/直显模组及整机，百亿级", "十大产业项目", ACCENT_RED),
    ("中车时代半导体", "株洲", "中低压功率器件通线，国家级集群链主", "十大产业项目", ACCENT_RED),
    ("邵虹", "邵阳", "基板玻璃，3条热端+2条冷端生产线", "十大产业项目", ACCENT_RED),
    ("金博股份", "益阳", "光电材料龙头，创新联合体", "创新联合体", ACCENT_GOLD),
    ("信维电科", "益阳", "电子元器件、5G配套核心企业", "", ACCENT_TEAL),
    ("光智通信", "益阳", "光通信器件，长益常科创走廊关键", "", ACCENT_TEAL),
    ("江丰电子", "益阳", "全球靶材龙头，年产值超7.5亿", "", ACCENT_TEAL),
    ("山嘉光电", "郴州·宜章", "大尺寸偏光片，服务惠科/华星/京东方", "", THU_PURPLE),
    ("谱特光电", "郴州·宜章", "打破偏光片日韩垄断，省首套件", "首套件", ACCENT_GOLD),
    ("中沛光电", "郴州·北湖", "链主企业，5秒/台手机整机", "", THU_PURPLE),
    ("英飞拓", "郴州·北湖", "全国安防5强，年产值突破3亿", "", THU_PURPLE),
    ("图灵智算", "长沙", "宽谱域高端光电，量子+光电融合", "", ACCENT_NAVY),
    ("麓邦光电", "长沙", "显示屏项目，光电功能材料", "", ACCENT_NAVY),
    ("明正宏电子", "益阳", "线路板扩建，年产能150万m²", "", ACCENT_TEAL),
    ("阿秒光学", "郴州·北湖", "激光蚀刻设备，良品率98.6%", "上市后备", ACCENT_GOLD),
]

ec_w = 520
ec_h = 200
ec_gap = 12
for i, (name, loc, desc, badge, badge_color) in enumerate(enterprises):
    col = i % 4
    row = i // 4
    ex = PAD + col * (ec_w + ec_gap)
    ey = y + row * (ec_h + ec_gap)
    rect(ex, ey, ec_w, ec_h, BG_WHITE)
    draw.rectangle([ex, ey, ex+ec_w, ey+ec_h], outline=LINE_LIGHT, width=1)
    rect(ex, ey, 5, ec_h, badge_color if badge else LINE_LIGHT)
    text(ex + 20, ey + 10, name, FONT_BODY, TEXT_DARK)
    text(ex + 20, ey + 50, loc, FONT_TINY, TEXT_MUTED)
    text(ex + 20, ey + 80, desc, FONT_SMALL, TEXT_BODY)
    if badge:
        text(ex + 20, ey + 150, badge, FONT_BADGE, badge_color)

y += 4 * (ec_h + ec_gap) + 30

# ========== 6. 创新平台 ==========
rect(0, y, W, 6, THU_PURPLE)
y += 30
text(PAD, y, "创新平台与科研支撑", FONT_SECTION, THU_PURPLE)
y += 80
hline(PAD, y, CW, LINE_LIGHT)
y += 20

platforms = [
    ("湖南未来光电技术研究院", "突破硅基Micro-LED，申报专利86项，成果转化12项", THU_PURPLE),
    ("5G+电容器科技孵化器", "科技型企业孵化器，聚焦光电产业创新孵化", ACCENT_TEAL),
    ("新型电子元器件中试基地", "科技成果转化中试基地，支撑光电元器件产业化", ACCENT_GOLD),
    ("高校科研力量", "国防科大 · 湖南大学 · 中南大学 · 湖南师大", THU_PURPLE_DEEP),
    ("金博股份创新联合体", "光电材料领域产学研协同攻关", ACCENT_RED),
    ("国家新型显示产业联盟", "宜章经开区光电产业协会加入", ACCENT_NAVY),
    ("新型显示研发中心", "投资390万元，4名国家级专家顾问", ACCENT_TEAL),
    ("郴江实验室", "帮助企业解决技术痛点、研发难点", THU_PURPLE),
    ("飞地园区·科创飞地", "益阳-湘江新区飞地园区，光电技术创新中心", THU_PURPLE_DEEP),
]

pc_w = 700
pc_h = 200
pc_gap = 15
for i, (title, desc, color) in enumerate(platforms):
    col = i % 3
    row = i // 3
    px = PAD + col * (pc_w + pc_gap)
    py = y + row * (pc_h + pc_gap)
    rect(px, py, pc_w, pc_h, BG_LIGHT)
    draw.rectangle([px, py, px+pc_w, py+pc_h], outline=LINE_LIGHT, width=1)
    # 编号圆
    draw.ellipse([px+20, py+20, px+70, py+70], fill=color)
    text_center(px+20, py+25, 50, str(i+1), FONT_BODY, TEXT_WHITE)
    text(px + 90, py + 25, title, FONT_BODY, TEXT_DARK)
    text(px + 20, py + 90, desc, FONT_SMALL, TEXT_BODY)

y += 3 * (pc_h + pc_gap) + 30

# ========== 7. 政策支撑 ==========
rect(0, y, W, 6, THU_PURPLE)
y += 30
text(PAD, y, "政策支撑体系", FONT_SECTION, THU_PURPLE)
y += 80
hline(PAD, y, CW, LINE_LIGHT)
y += 20

policies = [
    ("顶层规划", "湖南省\"十五五\"未来产业发展规划", "谋划光电产业布局，光电信息列入重点方向", THU_PURPLE),
    ("产业体系", "\"4×4\"现代化产业体系", "功率半导体纳入重点培育，聚焦新型显示、AI", ACCENT_TEAL),
    ("区域协同", "\"长益\"光电技术科创与产业走廊", "长沙-益阳科创走廊，规划衔接、产业联动", ACCENT_GOLD),
    ("专项支持", "支持益阳高端电子元器件产业", "发展激光器、光传感器、硅光芯片，打造光电谷", THU_PURPLE_DEEP),
    ("成果转化", "\"先用后付\"推广实施方案", "首批推广537项科技成果，加速共性技术转化", ACCENT_RED),
    ("飞地机制", "飞地园区发展若干措施", "支持GDP核算、税收分成、能耗指标分配", ACCENT_NAVY),
    ("知识产权", "知识产权服务集聚试点", "益阳高新区纳入试点，一站式综合服务", THU_PURPLE),
    ("区域规划", "益阳\"十五五\"新型工业化规划", "光电产业为战略性主导，明确光电谷定位", THU_PURPLE_DEEP),
]

plc_w = 1100
plc_h = 170
plc_gap = 10
for i, (tag, title, desc, color) in enumerate(policies):
    col = i % 2
    row = i // 2
    px = PAD + col * (plc_w + 40)
    py = y + row * (plc_h + plc_gap)
    rect(px, py, plc_w, plc_h, BG_WHITE)
    draw.rectangle([px, py, px+plc_w, py+plc_h], outline=LINE_LIGHT, width=1)
    rect(px, py, 8, plc_h, color)
    text(px + 25, py + 15, tag, FONT_BADGE, color)
    text(px + 200, py + 12, title, FONT_BODY, TEXT_DARK)
    text(px + 25, py + 75, desc, FONT_SMALL, TEXT_BODY)

y += 4 * (plc_h + plc_gap) + 30

# ========== 8. 发展趋势 ==========
rect(0, y, W, 6, THU_PURPLE)
y += 30
text(PAD, y, "发展趋势与未来方向", FONT_SECTION, THU_PURPLE)
y += 80
hline(PAD, y, CW, LINE_LIGHT)
y += 20

trends = [
    ("01", "AI + 光电融合", THU_PURPLE,
     "AI算力需求驱动光电技术战略地位提升，光互联替代电互联成为算力网络核心支撑，硅光CPO技术加速落地"),
    ("02", "国产替代加速", ACCENT_TEAL,
     "高端光芯片国产化率不足10%，湖南在功率半导体、靶材、偏光片领域实现突破，\"从0到1\"持续涌现"),
    ("03", "长益科创走廊", ACCENT_GOLD,
     "长沙研发+益阳转化模式深化，飞地园区机制打通区域壁垒，长益常科创走廊光电产业带加速成型"),
    ("04", "湾区产业承接", ACCENT_RED,
     "湖南\"一带一部\"区位优势凸显，50个重点项目中24%承接粤港澳大湾区产业转移，郴州成为核心承接地"),
]

tc_w = 520
tc_h = 500
tc_gap = 20
for i, (num, title_str, color, text_str) in enumerate(trends):
    tx = PAD + i * (tc_w + tc_gap)
    rect(tx, y, tc_w, tc_h, BG_LIGHT)
    draw.rectangle([tx, y, tx+tc_w, y+tc_h], outline=LINE_LIGHT, width=1)
    rect(tx, y, tc_w, 6, color)
    text(tx + 20, y + 25, num, load_font(80, bold=True), THU_PURPLE_MIST)
    rect(tx + 20, y + 130, 80, 4, color)
    text(tx + 20, y + 155, title_str, FONT_SUBTITLE, color)
    # 自动换行
    words = text_str
    max_chars = 22
    lines = []
    cur = ""
    for ch in words:
        cur += ch
        if len(cur) >= max_chars and ch in "，。、 ":
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    for li, line in enumerate(lines):
        text(tx + 20, y + 230 + li * 40, line, FONT_SMALL, TEXT_BODY)

y += tc_h + 30

# ========== 9. 总结 ==========
rect(0, y, W, 6, THU_PURPLE)
y += 30
text(PAD, y, "总结与展望", FONT_SECTION, THU_PURPLE)
y += 80
hline(PAD, y, CW, LINE_LIGHT)
y += 20

text_center(PAD, y, CW, "湖南光电融合产业 — 迈向新质生产力高地", FONT_SUBTITLE, TEXT_DARK)
y += 70

summary_items = [
    ("产业规模", "1,571.74亿元重点项目总投资，50个重点项目，6个百亿级项目", THU_PURPLE),
    ("区域格局", "长沙-株洲-湘潭-益阳-郴州-邵阳-衡阳，七大集聚区协同发展", ACCENT_TEAL),
    ("创新突破", "硅基Micro-LED、功率半导体、偏光片国产替代，\"从0到1\"持续涌现", ACCENT_GOLD),
    ("政策护航", "\"十五五\"规划引领、长益科创走廊、飞地园区、先用后付成果转化", ACCENT_RED),
    ("未来方向", "AI+光电融合、国产替代加速、湾区产业承接、长益常科创走廊成型", ACCENT_NAVY),
]

for i, (title, desc, color) in enumerate(summary_items):
    sy = y + i * 90
    rect(PAD, sy, CW, 70, BG_LIGHT)
    draw.rectangle([PAD, sy, PAD+CW, sy+70], outline=LINE_LIGHT, width=1)
    rect(PAD, sy, 8, 70, color)
    text(PAD + 25, sy + 15, title, FONT_BODY, color)
    text(PAD + 300, sy + 15, desc, FONT_SMALL, TEXT_BODY)

y += 5 * 90 + 30

# 底部
hline(PAD, y, CW, LINE_LIGHT, 1)
y += 10
text_center(PAD, y, CW, "湖南省光电融合产业全景图  |  2026年度  |  基于公开信息整理", FONT_TINY, TEXT_MUTED)
y += 40

# 裁剪空白区域
final_h = y + 40
img = img.crop((0, 0, W, final_h))

# 保存
output_path = "/Users/mrlin/Desktop/qingruan/湖南省光电融合产业全景图.jpg"
img.save(output_path, "JPEG", quality=95)
print(f"JPG 已保存至: {output_path}")
print(f"尺寸: {img.size[0]} x {img.size[1]} px")
