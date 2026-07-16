"""
电商运营分析系统实训 — Pandas 学生实验手册
第三天下午：淘宝全品类全国数据
完成人：黎一鸣
"""

from pathlib import Path
import pandas as pd

# ============================================================
# 环境准备
# ============================================================
DATA_DIR = Path('data')
CSV_PATH = DATA_DIR / '淘宝全品类全国数据.csv'

print('当前工作目录：', Path.cwd())
print('数据文件存在：', CSV_PATH.exists())

df = pd.read_csv(CSV_PATH)

# ============================================================
# 任务1：读取数据并完成初步观察
# 目标：确认数据是否读入成功，并说清每一行代表什么
# ============================================================
print("\n" + "=" * 60)
print("【任务1：数据初步观察】")
print("=" * 60)

print('数据规模：', df.shape)
print('\n字段名：')
print(df.columns.tolist())
print('\n前5行预览：')
print(df.head(5))
print('\n数据信息：')
print(df.info())

print("\n" + "-" * 40)
print("【任务1 文字答案】")
print("-" * 40)
print("问：本数据的一行代表什么？一共有多少行和多少列？")
print("答：本数据每一行代表一条淘宝商品记录。")
print(f"   共有 {df.shape[0]} 行（条商品记录），{df.shape[1]} 列（个字段）。")

# ============================================================
# 任务2：查看字段类型与缺失值
# 目标：找出哪些字段适合直接数值统计，哪些需要后续处理
# ============================================================
print("\n" + "=" * 60)
print("【任务2：字段类型与缺失值统计】")
print("=" * 60)

print('\n各字段数据类型：')
print(df.dtypes)

print('\n缺失值数量（从高到低排序）：')
missing_count = df.isna().sum().sort_values(ascending=False)
print(missing_count)

print('\n缺失率（百分比）：')
missing_rate = (df.isna().mean() * 100).round(1).sort_values(ascending=False)
print(missing_rate)

print("\n" + "-" * 40)
print("【任务2 文字答案】")
print("-" * 40)
print("可直接数值统计的字段：商品价格")
print("  → 原因：该字段为 float64 数值类型，无缺失值，可直接使用 describe()、mean()、median() 等统计方法。")
print("\n暂不宜直接精确数值统计的字段：商品销量")
print("  → 原因：该字段为 object 文本类型，存储的是 '100+人付款'、'1万+人付款' 等文字分档，")
print("         无法直接求均值或中位数，需要先清洗转换为数值。")
print(f"\n补充：风格、面料、版型、适用季节等字段缺失率较高（如版型缺失 {missing_rate.get('版型', 'N/A')}%），")
print("      这些字段需要在后续课程中进行清洗处理。")

# ============================================================
# 任务3：选择列与选择行
# 目标：掌握 Series、DataFrame、loc 和 iloc 的基本用法
# ============================================================
print("\n" + "=" * 60)
print("【任务3：列选择与行选择】")
print("=" * 60)

# 一列 → Series
print('\n单列选择（Series）：')
price_series = df['商品价格']
print(f"类型：{type(price_series)}")
print(f"前5个值：{price_series.head().tolist()}")

# 多列 → DataFrame
print('\n多列选择（DataFrame）：')
product_view = df[['商品id', '一级品类', '商品价格', '省份', '商品销量']]
print(f"类型：{type(product_view)}")
print(product_view.head())

# loc 按标签选择（0:4 包含索引 4，即前5行）
print('\nloc 按标签选择前5行 [0:4]：')
print(df.loc[0:4, ['一级品类', '商品价格', '省份']])

# iloc 按位置选择（0:5 不包含索引 5，即前5行）
print('\niloc 按位置选择前5行 [0:5]：')
print(df.iloc[0:5, 0:4])

print("\n" + "-" * 40)
print("【任务3 文字答案】")
print("-" * 40)
print("问：df['商品价格'] 与 df[['商品价格']] 的区别是什么？")
print("答：df['商品价格']（单中括号）返回的是 Series（一维数据），")
print("    df[['商品价格']]（双中括号）返回的是 DataFrame（二维表格）。")
print("问：loc 与 iloc 的区别是什么？")
print("答：loc 按索引标签（index label）选择，0:4 包含索引 4，共5行；")
print("    iloc 按整数位置选择，0:5 不包含位置 5，也是5行，但语义不同。")

# ============================================================
# 任务4：条件筛选与排序
# 目标：用业务条件找出目标商品，并按价格排序
# ============================================================
print("\n" + "=" * 60)
print("【任务4：条件筛选与排序】")
print("=" * 60)

# 单条件：省份为"广东"
guangdong = df[df['省份'] == '广东']
print(f"\n广东省商品数：{guangdong.shape[0]} 条")

# 多条件：广东 且 商品价格 >= 1000
condition = (df['省份'] == '广东') & (df['商品价格'] >= 1000)
selected = df.loc[condition, ['商品id', '一级品类', '二级品类', '商品价格', '省份', '商品销量']]
selected = selected.sort_values(by='商品价格', ascending=False)
print(f"\n广东且价格≥1000元的商品数：{selected.shape[0]} 条")
print("\n价格最高的前10条：")
print(selected.head(10))

# 或条件：浙江 或 江苏
zhejiang_or_jiangsu = df[(df['省份'] == '浙江') | (df['省份'] == '江苏')]
print(f"\n浙江或江苏商品数：{zhejiang_or_jiangsu.shape[0]} 条")

print("\n" + "-" * 40)
print("【任务4 文字答案】")
print("-" * 40)
print(f"筛选结果：广东省商品共 {guangdong.shape[0]} 条，")
print(f"其中价格≥1000元的有 {selected.shape[0]} 条，")
print(f"浙江或江苏商品共 {zhejiang_or_jiangsu.shape[0]} 条。")

# ============================================================
# 任务5：描述性统计与分组统计
# 目标：对商品价格和一级品类形成一条可解释的结论
# ============================================================
print("\n" + "=" * 60)
print("【任务5：描述性统计与分组统计】")
print("=" * 60)

# 商品价格的描述性统计
print('\n商品价格描述性统计：')
price_stats = df['商品价格'].describe().round(2)
print(price_stats)

# 一级品类商品数
print('\n一级品类商品数分布：')
category_counts = df['一级品类'].value_counts()
print(category_counts)

# 一级品类汇总（按平均价格从高到低）
print('\n一级品类汇总（按平均价格排序）：')
category_summary = (
    df.groupby('一级品类')
      .agg(商品数=('商品id', 'size'),
           平均价格=('商品价格', 'mean'),
           中位价格=('商品价格', 'median'))
      .sort_values('平均价格', ascending=False)
      .round(2)
)
print(category_summary)

print("\n" + "-" * 40)
print("【任务5 文字答案（规范结论）】")
print("-" * 40)
print("在本数据集的 25,000 条商品记录中，使用商品价格字段进行描述性统计分析：")
print(f"商品价格均值为 {price_stats['mean']} 元，中位数为 {price_stats['50%']} 元，")
print(f"标准差为 {price_stats['std']} 元，说明价格分布较为分散。")
print("按一级品类分组聚合后发现，数码家电的平均商品价格高于其他所有品类。")
print("结论边界：该结论基于商品的标价统计，不代表实际成交金额，")
print("也不能外推到全网用户的购买偏好或全平台商品分布。")

# ============================================================
# 挑战任务：做一张"省份—类别"小结表
# 目标：比较两个省份的商品数量、平均价格与最常见一级品类
# ============================================================
print("\n" + "=" * 60)
print("【挑战任务：省份—类别对比分析】")
print("=" * 60)

provinces = ['广东', '江苏']
subset = df[df['省份'].isin(provinces)]

# 省份汇总
province_summary = (
    subset.groupby('省份')
          .agg(商品数=('商品id', 'size'),
               平均价格=('商品价格', 'mean'),
               中位价格=('商品价格', 'median'))
          .round(2)
)
print('\n省份汇总对比：')
print(province_summary)

# 各自最常见一级品类
top_categories = {}
for province in provinces:
    top_category = (subset.loc[subset['省份'] == province, '一级品类']
                         .value_counts()
                         .head(1))
    top_categories[province] = top_category
    print(f'\n{province} 最常见一级品类：')
    print(top_category)

# 挑战任务结论
print("\n" + "-" * 40)
print("【挑战任务 规范结论】")
print("-" * 40)

# 获取数据用于结论
gd_count = province_summary.loc['广东', '商品数']
js_count = province_summary.loc['江苏', '商品数']
gd_avg = province_summary.loc['广东', '平均价格']
js_avg = province_summary.loc['江苏', '平均价格']
gd_median = province_summary.loc['广东', '中位价格']
js_median = province_summary.loc['江苏', '中位价格']

print(f"结论一（描述差异）：")
print(f"在本数据集 25,000 条商品记录中，使用省份字段筛选广东（{int(gd_count)} 条）")
print(f"和江苏（{int(js_count)} 条）两个省份，按省份分组聚合后：广东的商品平均价格")
print(f"为 {gd_avg} 元（中位数 {gd_median} 元），高于江苏的 {js_avg} 元")
print(f"（中位数 {js_median} 元）。广东最常见一级品类为数码家电，")
print(f"江苏最常见一级品类为图书音像，两地商品结构存在差异。")

print(f"\n结论二（说明边界）：")
print(f"该结论仅基于数据集中采集到的商品标价和品类分布，不代表两省实际")
print(f"电商交易全貌。商品销量为文字分档暂未纳入分析，价格均为标价而非")
print(f"实际成交价，且数据集可能存在采样偏差，不能外推为两省真实消费水平")
print(f"或全网商品分布的全貌。")

# ============================================================
# 保存结果到文件
# ============================================================
print("\n" + "=" * 60)
print("【保存结果文件】")
print("=" * 60)

# 创建输出目录
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)

# 保存广东高价商品
selected.head(10).to_csv(output_dir / '广东高价商品Top10.csv', index=False, encoding='utf-8-sig')
print("已保存：output/广东高价商品Top10.csv")

# 保存品类汇总
category_summary.to_csv(output_dir / '一级品类汇总.csv', encoding='utf-8-sig')
print("已保存：output/一级品类汇总.csv")

# 保存省份对比
province_summary.to_csv(output_dir / '省份对比汇总.csv', encoding='utf-8-sig')
print("已保存：output/省份对比汇总.csv")

# 保存浙江或江苏商品（前100条采样）
zhejiang_or_jiangsu.head(100).to_csv(output_dir / '浙江或江苏商品_前100条.csv', index=False, encoding='utf-8-sig')
print("已保存：output/浙江或江苏商品_前100条.csv")

print("\n所有任务完成！")
