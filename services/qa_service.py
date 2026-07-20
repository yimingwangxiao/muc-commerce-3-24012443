from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
    normalized = question.replace(" ", "").lower()

    # 1. 总用户数相关
    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"

    # 2. 流失率相关
    if any(word in normalized for word in ["流失率", "流失比例", "流失占比", "流失了多少", "多少流失"]):
        return f"整体用户流失率为{metrics['流失率']:.1%}，共有{int(metrics['流失人数']):,}名用户流失。"

    # 3. 偏好品类相关
    if any(word in normalized for word in ["偏好品类", "品类", "喜欢什么", "偏好什么", "分类"]):
        return (
            "用户偏好品类共5类：Mobile Phone（2,080人，占比最高）、"
            "Laptop & Accessory（2,050人）、Fashion（826人）、"
            "Grocery（410人）、Others（264人）。"
        )

    # 4. 生命周期风险相关
    if any(word in normalized for word in ["生命周期", "阶段", "哪个阶段", "风险", "哪个群体"]):
        highest = segment_df.loc[segment_df["流失率"].idxmax()]
        lowest = segment_df.loc[segment_df["流失率"].idxmin()]
        return (
            f"生命周期共5个阶段。流失风险最高的是「{highest['TenureGroup']}」阶段，"
            f"流失率{highest['流失率']:.1%}（{int(highest['流失人数'])}人流失/{int(highest['用户数'])}人）；"
            f"最稳定的是「{lowest['TenureGroup']}」阶段，"
            f"流失率{lowest['流失率']:.1%}。"
        )

    # 5. 订单相关
    if any(word in normalized for word in ["订单", "订单数", "平均订单", "下单"]):
        return (
            f"用户平均订单数为{metrics['平均订单数']:.2f}单，"
            f"中位数为{int(metrics['订单数中位数'])}单。"
            f"说明大部分用户订单数偏低，少数高订单用户拉高了平均值。"
        )

    return (
        "抱歉，我还不能回答这个问题。目前支持的问题类型："
        "总用户数、流失率、偏好品类、生命周期风险、订单数据。"
        "请换一种问法试试。"
    )
