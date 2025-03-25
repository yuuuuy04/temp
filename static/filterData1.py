# filter.py (修改后)
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import re
import numpy as np
INDUSTRY_MAPPING = {
    # 家居类目
    "居家日用": ["Home Supplies", "Household Goods", "Daily Necessities"],
    "厨房用品": ["Kitchenware", "Cooking Utensils", "Kitchen Tools"],
    "家纺布艺": ["Home Textiles", "Bedding", "Curtains", "Fabric Arts", "Textiles & Soft Furnishings"],
    "家电": ["Home Appliances", "Large Appliances", "Small Appliances", "Household Appliances"],
    
    # 服饰类目
    "女装与女士内衣": ["Womenswear & Underwear", "Lingerie", "Women's Fashion"],
    "男装与男士内衣": ["Men's Clothing", "Men's Underwear", "Men's Fashion"],
    "穆斯林时尚": ["Muslim Fashion", "Islamic Clothing", "Hijab Fashion"],
    "鞋靴": ["Footwear", "Shoes", "Boots", "Sneakers"],
    "箱包": ["Bags & Luggage", "Handbags", "Backpacks", "Luggage & Bags"],
    "时尚配件": ["Fashion Accessories", "Jewelry", "Watches", "Belts", "Jewelry Accessories & Derivatives"],
    
    # 美妆个护
    "美妆个护": ["Beauty & Personal Care", "Cosmetics", "Skincare", "Hair Care"],
    
    # 数码电子
    "手机与数码": ["Mobile & Electronics", "Smartphones", "Digital Devices", "Phones & Electronics"],
    "电脑办公": ["Computer & Office", "Laptops", "Computer Accessories", "Computers & Office Equipment"],
    
    # 母婴儿童
    "母婴用品": ["Mother & Baby", "Baby Care", "Maternity", "Nursery", "Baby & Maternity"],
    "儿童时尚": ["Kids Fashion", "Children's Clothing", "Kids Shoes"],
    "玩具和爱好": ["Toys & Hobbies", "Educational Toys", "Collectibles"],
    
    # 运动户外
    "运动与户外": ["Sports & Outdoors", "Fitness", "Camping Gear", "Sports & Outdoor"],
    
    # 家装类目
    "家具": ["Furniture", "Home Furniture", "Office Furniture"],
    "家装建材": ["Home Improvement", "Building Materials", "Hardware"],
    "五金工具": ["Tools & Hardware", "Power Tools", "Hand Tools"],
    
    # 汽配类目
    "汽车与摩托车": ["Auto & Motorcycle", "Car Accessories", "Motorcycle Parts"],
    
    # 特殊类目
    "宠物用品": ["Pet Supplies", "Pet Food", "Pet Grooming"],
    "保健": ["Health Care", "Wellness Products", "Medical Supplies", "Health"],
    "收藏品": ["Collectibles", "Antiques", "Art Collections"],
    "珠宝与衍生品": ["Jewelry", "Luxury Watches", "Fine Jewelry", "Jewelry Accessories & Derivatives"]
}

def convert_percentage_to_decimal(percentage_value):
    """将百分比字符串或数值转换为小数"""
    if isinstance(percentage_value, str):
        # 去掉百分号并转换为小数
        return float(percentage_value.strip('%')) / 100
    elif isinstance(percentage_value, (int, float)):
        # 如果已经是数值类型，则直接返回
        return float(percentage_value)
    else:
        raise ValueError(f"Unsupported type: {type(percentage_value)} for value {percentage_value}")
def preprocess_categories(category_str):
    """使用正则表达式安全解析创作者类别"""
    try:
        # 处理单引号问题并统一格式
        cleaned = re.sub(r"'", '"', str(category_str))
        # 提取所有name字段的值
        names = re.findall(r'"name":\s*"([^"]+)"', cleaned)
        return [{"name": name.strip()} for name in names]
    except Exception as e:
        print(f"解析失败: {category_str}，错误: {str(e)}")
        return []

def calculate_scores(df, model_type='AHP'):
    valid_models = ['AHP', 'Douyin']
    if model_type not in valid_models:
        raise ValueError(f"无效模型类型，可选: {valid_models}")

    weights = {
        '视频GMV（商品交易总额）': 0.35,
        '成交件数': 0.25,
        '粉丝数': 0.2,
        '视频互动率': 0.15,
        '内容生产力': 0.05
    } if model_type == 'AHP' else {}

    # 创建一个用于后续操作的数据副本，保证原始df不变
    df_copy = df.copy()

    # 基础清洗和其他操作保持不变...
    df_copy = df_copy[df_copy['粉丝数'] > 1000]  # 过滤低粉账号
    df_copy['创作者的主要类别'] = df_copy['创作者的主要类别'].apply(preprocess_categories)
    
    # 计算综合GMV
    df_copy['总GMV'] = df_copy['视频GMV（商品交易总额）'].fillna(0) + df_copy['直播间GMV'].fillna(0)

    # 计算互动率
    df_copy['视频互动率'] = df_copy['视频参与度'] / df_copy['视频平均播放次数'].replace(0, np.nan)

    # 生成内容生产力参数
    df_copy['内容生产力'] = (
        np.log1p(df_copy['视频发布次数（最近30天）']) * 0.6 + 
        np.sqrt(df_copy['视频的中位评论数'].fillna(0)) * 0.4
    )

    # 标准化处理
    features = list(weights.keys())
    df_scaled = df_copy.copy()  # 复制一份用于标准化
    df_scaled[features] = MinMaxScaler().fit_transform(df_copy[features])

    # 使用标准化后的数据计算综合得分
    df_scaled['综合得分'] = sum(df_scaled[feat]*weight for feat, weight in weights.items())

    # 返回包含原始数据及新增综合得分列的DataFrame，并根据综合得分排序
    df_with_score = df_copy.copy()
    df_with_score['综合得分'] = df_scaled['综合得分']
    return df_with_score.sort_values('综合得分', ascending=False)

def start_filter_excel_data(file_path, filter_conditions):
    # 读取数据
    df = pd.read_csv(file_path)
    
    # 将'中位佣金率'列从百分比转换为小数
    if '中位佣金率' in df.columns:
        df['中位佣金率'] = df['中位佣金率'].apply(convert_percentage_to_decimal)

    # 如果selectedCategories不为空，则进行筛选
    if 'selectedCategories' in filter_conditions and filter_conditions['selectedCategories']:
        # 将每行的商品类别字符串转成集合，去除可能存在的多余空格
        df['categories_set'] = df['商品类别'].apply(lambda x: set([item.strip() for item in x.split('、')]))
        # 筛选逻辑：只要行中的任何一个类别出现在selectedCategories中，就保留该行
        selected_set = set(filter_conditions['selectedCategories'])
        df = df[df['categories_set'].apply(lambda x: bool(x.intersection(selected_set)))]
        df = df.drop(columns=['categories_set'])  # 移除临时创建的categories_set列
    
    # 粉丝数范围筛选
    minFans = filter_conditions.get('minFans')
    maxFans = filter_conditions.get('maxFans')
    if not (minFans == 0 and maxFans == "ismax"):
        if minFans is not None:
            df = df[df['粉丝数'] >= minFans]
        if maxFans != "ismax" and maxFans is not None:
            df = df[df['粉丝数'] <= maxFans]

    # 中位佣金率范围筛选
    minCommissionRate = filter_conditions.get('minCommissionRate')
    maxCommissionRate = filter_conditions.get('maxCommissionRate')
    if not (minCommissionRate == 0 and maxCommissionRate == "ismax"):
        if minCommissionRate is not None:
            df = df[df['中位佣金率'] >= minCommissionRate]
        if maxCommissionRate != "ismax" and maxCommissionRate is not None:
            df = df[df['中位佣金率'] <= maxCommissionRate]

    # 视频GMV范围筛选
    minGMV = filter_conditions.get('minGMV')
    maxGMV = filter_conditions.get('maxGMV')
    if not (minGMV == 0 and maxGMV == "ismax"):
        if minGMV is not None:
            df = df[df['视频GMV（商品交易总额）'] >= minGMV]
        if maxGMV != "ismax" and maxGMV is not None:
            df = df[df['视频GMV（商品交易总额）'] <= maxGMV]

    # 推广的产品数量范围筛选
    minPromoteProductNum = filter_conditions.get('minPromoteProductNum')
    maxPromoteProductNum = filter_conditions.get('maxPromoteProductNum')
    if not (minPromoteProductNum == 0 and maxPromoteProductNum == "ismax"):
        if minPromoteProductNum is not None:
            df = df[df['推广的产品数量'] >= minPromoteProductNum]
        if maxPromoteProductNum != "ismax" and maxPromoteProductNum is not None:
            df = df[df['推广的产品数量'] <= maxPromoteProductNum]

    # 平均播放次数范围筛选
    minVideoPlayNum = filter_conditions.get('minVideoPlayNum')
    maxVideoPlayNum = filter_conditions.get('maxVideoPlayNum')
    if not (minVideoPlayNum == 0 and maxVideoPlayNum == "ismax"):
        if minVideoPlayNum is not None:
            df = df[df['视频平均播放次数'] >= minVideoPlayNum]
        if maxVideoPlayNum != "ismax" and maxVideoPlayNum is not None:
            df = df[df['视频平均播放次数'] <= maxVideoPlayNum]

    # 视频发布次数范围筛选
    minVideoPublishNum = filter_conditions.get('minVideoPublishNum')
    maxVideoPublishNum = filter_conditions.get('maxVideoPublishNum')
    if not (minVideoPublishNum == 0 and maxVideoPublishNum == "ismax"):
        if minVideoPublishNum is not None:
            df = df[df['视频发布次数（最近30天）'] >= minVideoPublishNum]
        if maxVideoPublishNum != "ismax" and maxVideoPublishNum is not None:
            df = df[df['视频发布次数（最近30天）'] <= maxVideoPublishNum]

    # 是否邀请过筛选
    if 'isInvite' in filter_conditions and filter_conditions['isInvite'] is not None:
        df = df[df['是否有过合作'] == filter_conditions['isInvite']]
    
    # 原有筛选逻辑保持不变...
    
    # 添加智能排序计算
    if filter_conditions.get('need_smart_rank', False):
        model_type = filter_conditions.get('model_type', 'AHP')
        df = calculate_scores(df, model_type)
    
    return df