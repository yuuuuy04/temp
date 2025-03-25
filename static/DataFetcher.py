import os
import requests
import pandas as pd
import json
import time
import threading
from ast import literal_eval
from concurrent.futures import ThreadPoolExecutor, as_completed
from .resolve import *

class _Verifier:
    def __init__(self):
        self.__is_verifing = False
        self.__condition_for_is_verifing = threading.Condition()
    
    def __check_need_verify(self,arg_creator_oec_id,arg_url,arg_header):
        data = {
            'creator_oec_id': str(arg_creator_oec_id),  # 将达人ID转换为字符串
            'profile_types': [2]  # 可根据需要更改 profile_types 参数
        }
        json_data = json.dumps(data)
        response = requests.post(url=arg_url, headers=arg_header, data=json_data,timeout=30)
        if len(response.content) != 0 and response.json()['code'] == 0:
            return False
        else:
            return True

    def verify_or_wait(self,arg_creator_oec_id,arg_url,arg_header,arg_cookies,arg_region,arg_path_chromedriver):
        print("debug:verify_or_wait")
        with self.__condition_for_is_verifing:
            if self.__is_verifing:
                print(f"debug:__is_verifing = {self.__is_verifing}, wait.")
                self.__condition_for_is_verifing.wait()
                print(f"debug:wait done.")
                need_verifing = False
            else:
                print(f"debug:__is_verifing = {self.__is_verifing}, next check.")
                self.__is_verifing = True
                need_verifing = True
            


        if need_verifing and self.__check_need_verify(
            arg_creator_oec_id=arg_creator_oec_id,
            arg_url=arg_url,
            arg_header=arg_header):
            print(f"debug:need resolve.")
            print('startResolve return',startResolve(mycookies=arg_cookies,region=arg_region,arg_creator_oec_id=arg_creator_oec_id,arg_header=arg_header,arg_url=arg_url,arg_path_chromedriver=arg_path_chromedriver))
            print(f"debug:done resolve.")
            with self.__condition_for_is_verifing:
                print(f"debug:notify_all")
                self.__is_verifing = False
                # time.sleep(10)
                self.__condition_for_is_verifing.notify_all()
                
class DataFetcher:
    def __init__(self):
        self.__verifier = _Verifier()
        self.__lock_for_scv = threading.Lock()

    def __task_fetch_data_package_1(
            self,
            creator_oec_id,
            existing_ids, 
            creator_ids,
            url,
            header,
            cookies_str,
            region,
            path_file_data,
            arg_path_chromedriver):
        creator_oec_id_str = str(creator_oec_id) 
        if creator_oec_id_str in existing_ids:
            print(f"达人ID {creator_oec_id} 已经存在，跳过该ID")
            return  # 跳过已存在的 ID
        # API 请求数据
        data = {
            'creator_oec_id': str(creator_oec_id),  # 将达人ID转换为字符串
            'profile_types': [2]  # 可根据需要更改 profile_types 参数
        }
        json_data = json.dumps(data)

        # 请求 URL
        # url = f"https://affiliate.tiktokglobalshop.com/api/v1/oec/affiliate/creator/marketplace/find?{query_string}"
        try:
            # 发起POST请求
            response = requests.post(url=url, headers=header, data=json_data,timeout=30)

            if len(response.content) != 0 and response.json()['code'] == 0:
                response_data = response.json()  # 获取 JSON 数据

                creator_profile = response_data['creator_profile']

                # 提取数据
                cid = creator_profile.get('creator_oecuid', {}).get('value', '')
                med_commission_rate = creator_profile.get('med_commission_rate', {}).get('value', '')
                industry_groups = creator_profile.get('industry_groups', {}).get('value', '')
                ec_video_engagement = creator_profile.get('ec_video_engagement', {}).get('value', '')
                ec_live_engagement = creator_profile.get('ec_live_engagement', {}).get('value', '')
                ec_video_gpm = creator_profile.get('ec_video_gpm', {}).get('value', '')
                ec_live_gpm = creator_profile.get('ec_live_gpm', {}).get('value', '')
                product_cnt = creator_profile.get('product_cnt', {}).get('value', '')
                promoted_product_num = creator_profile.get('promoted_product_num', {}).get('value', '')
                selection_region = creator_profile.get('selection_region', {}).get('value', '')
                med_gmv_revenue = creator_profile.get('med_gmv_revenue', {}).get('value', '')
                video_publish_cnt_30d = creator_profile.get('video_publish_cnt_30d', {}).get('value', '')
                live_streaming_cnt_30d = creator_profile.get('live_streaming_cnt_30d', {}).get('value', '')
                units_sold = creator_profile.get('units_sold', {}).get('value', '')

                # 获取新增的字段
                ec_video_med_comment_cnt = creator_profile.get('ec_video_med_comment_cnt', {}).get('value', '')

                # 佣金率处理：除以100并加上百分号
                if med_commission_rate:
                    med_commission_rate = f"{float(med_commission_rate) / 10000:.2%}"

                # 创建要保存的字典
                new_data = {
                    'creator_oecuid': cid,
                    'med_commission_rate': med_commission_rate,
                    'industry_groups': industry_groups,
                    'ec_video_engagement': ec_video_engagement,
                    'ec_live_engagement': ec_live_engagement,
                    'ec_video_gpm': ec_video_gpm,
                    'ec_live_gpm': ec_live_gpm,
                    'promoted_product_num': promoted_product_num,
                    'selection_region': selection_region,
                    'med_gmv_revenue': med_gmv_revenue,
                    'video_publish_cnt_30d': video_publish_cnt_30d,
                    'live_streaming_cnt_30d': live_streaming_cnt_30d,
                    'ec_video_med_comment_cnt': ec_video_med_comment_cnt,
                    'units_sold':units_sold
                }

                # 改为中文列名
                column_names_mapping = {
                    'creator_oecuid': '达人ID',
                    'med_commission_rate': '中位佣金率',
                    'industry_groups': '行业群组',
                    'ec_video_engagement': '视频的互动参与度',
                    'ec_live_engagement': '直播的互动参与度',
                    'ec_video_gpm': '每千次观看的收益',
                    'ec_live_gpm': '直播的每千次观看收益',
                    'promoted_product_num': '推广的产品数量',
                    'selection_region': '选择的地区',
                    'med_gmv_revenue': '中位GMV收入',
                    'video_publish_cnt_30d': '视频发布次数（最近30天）',
                    'live_streaming_cnt_30d': '直播次数（最近30天）',
                    'ec_video_med_comment_cnt': '视频的中位评论数',
                    'units_sold':'成交件数'
                }

                # 使用映射来重命名新数据的键为中文列名
                new_data_chinese = {column_names_mapping.get(k, k): v for k, v in new_data.items()}

                # 将新数据转换为 DataFrame
                df_new = pd.DataFrame([new_data_chinese])
                # 指定要保存的 CSV 文件路径和名称

            # 判断文件是否存在
                file_exists = os.path.isfile(path_file_data)

                # 保存数据到文件
                with self.__lock_for_scv:
                    df_new.to_csv(
                        path_file_data,
                        index=False,
                        encoding='utf-8-sig',
                        mode='a',  # 追加模式
                        header=not file_exists  # 如果文件不存在，写入表头
                    )
                print(f"数据获取成功: {creator_oec_id}")

            else:
                print(f"API 请求失败，状态码: {response.status_code} - {creator_oec_id}")
                # **************** change *******************
                self.__verifier.verify_or_wait(
                    arg_creator_oec_id=creator_oec_id,
                    arg_url=url,
                    arg_header=header,
                    arg_cookies=cookies_str,
                    arg_region=region,
                    arg_path_chromedriver = arg_path_chromedriver
                    )
                # *******************************************
                creator_ids.append(creator_oec_id_str)
        except Exception as e:
            print(f"请求失败，错误: {e} - {creator_oec_id}")
            creator_ids.append(creator_oec_id_str)
            with self.__verifier.__condition_for_is_verifing:
                self.__verifier.__is_verifing =False
                self.__verifier.__condition_for_is_verifing.notify_all()
            time.sleep(0.5)
    
    def __task_fetch_data_package_2(
            self,
            creator_oec_id,
            existing_ids, 
            creator_ids,
            url,
            header,
            cookies_str,
            region,
            path_file_data,
            arg_path_chromedriver):
        creator_oec_id_str = str(creator_oec_id) 
        if creator_oec_id_str in existing_ids:
            print(f"达人ID {creator_oec_id} 已经存在，跳过该ID")
            return  # 跳过已存在的 ID
        # API 请求数据
        data = {
            'creator_oec_id': str(creator_oec_id),  # 将达人ID转换为字符串
            'profile_types': [3]  # 可根据需要更改 profile_types 参数
        }
        json_data = json.dumps(data)

        # 请求 URL
        # url = f"https://affiliate.tiktokglobalshop.com/api/v1/oec/affiliate/creator/marketplace/find?{query_string}"
        try:
            # 发起POST请求
            response = requests.post(url=url, headers=header, data=json_data,timeout=30)

            if len(response.content) != 0 and response.json()['code'] == 0:
                response_data = response.json()  # 获取 JSON 数据
                creator_profile = response_data['creator_profile']
                # 提取数据
                follower_ages_v2 = creator_profile.get('follower_ages_v2', {}).get('value', '')  # 获取粉丝年龄段数据
                follower_genders_v2 = creator_profile.get('follower_genders_v2', {}).get('value', '')  # 获取粉丝性别数据
                follower_state_location = creator_profile.get('follower_state_location', {}).get('value', '')  # 获取粉丝所在州/地区
                has_invited_before_90d = creator_profile.get('has_invited_before_90d', {}).get('is_authorized', '')  # 获取过去90天是否被邀请过
                # 创建要保存的字典
                new_data = {
                    'creator_oec_id': creator_oec_id,
                    'follower_ages_v2': follower_ages_v2,
                    'follower_genders_v2': follower_genders_v2,
                    'follower_state_location': follower_state_location,
                    'has_invited_before_90d': has_invited_before_90d,
                }
                # 改为中文列名
                column_names_mapping = {
                    'creator_oec_id': '达人ID',
                    'follower_ages_v2': '粉丝年龄段数据',
                    'follower_genders_v2': '粉丝性别数据',
                    'follower_state_location': '粉丝所在州/地区',
                    'has_invited_before_90d': '过去90天是否被邀请过',
                }

                # 使用映射来重命名新数据的键为中文列名
                new_data_chinese = {column_names_mapping.get(k, k): v for k, v in new_data.items()}

                # 将新数据转换为 DataFrame
                df_new = pd.DataFrame([new_data_chinese])

            # 判断文件是否存在
                file_exists = os.path.isfile(path_file_data)

                # 保存数据到文件
                df_new.to_csv(
                    path_file_data,
                    index=False,
                    encoding='utf-8-sig',
                    mode='a',  # 追加模式
                    header=not file_exists  # 如果文件不存在，写入表头
                )
                print(f"数据获取成功: {creator_oec_id}")

            else:
                print(f"API 请求失败，状态码: {response.status_code} - {creator_oec_id}")
                # **************** change *******************
                self.__verifier.verify_or_wait(
                    arg_creator_oec_id=creator_oec_id,
                    arg_url=url,
                    arg_header=header,
                    arg_cookies=cookies_str,
                    arg_region=region,
                    arg_path_chromedriver = arg_path_chromedriver
                    )
                # *******************************************
                creator_ids.append(creator_oec_id_str)
        except Exception as e:
            print(f"请求失败，错误: {e} - {creator_oec_id}")
            with self.__verifier.__condition_for_is_verifing:
                self.__verifier.__is_verifing =False
                self.__verifier.__condition_for_is_verifing.notify_all()
            creator_ids.append(creator_oec_id_str)
            time.sleep(0.5)
        
    def fetch_data_package_1(
            self,
            arg_creator_ids,
            arg_url,
            arg_header,
            arg_cookies_str,
            arg_region,
            arg_path_chromedriver,
            arg_path_file_data = 'data/data1.csv',
            arg_max_workers = 5):
        """获取数据包1"""
        # 判断文件是否存在
        file_exists = os.path.isfile(arg_path_file_data)

        # 读取已有CSV文件
        df_existing = pd.read_csv(arg_path_file_data) if file_exists else arg_creator_ids  # 读取现有 CSV 文件，如果文件不存在则返回空的 DataFrame
        existing_ids = df_existing['达人ID'].astype(str).tolist() if file_exists else []  # 获取已保存的达人ID并确保是字符串类型

        # **************** change *********************************************************

        # 使用线程池并发执行任务
        with ThreadPoolExecutor(max_workers=arg_max_workers) as executor:
            futures = []
            for creator_oec_id in arg_creator_ids:
                future = executor.submit(
                    self.__task_fetch_data_package_1,
                    creator_oec_id,
                    existing_ids,
                    arg_creator_ids,
                    arg_url,
                    arg_header,
                    arg_cookies_str,
                    arg_region,
                    arg_path_file_data,
                    arg_path_chromedriver
                )
                futures.append(future)

            # 等待所有任务完成
            for future in as_completed(futures):
                future.result()  # 捕获异常或结果
        # *********************************************************************************
            
        print(f"所有数据已保存")
    

    def fetch_data_package_2(
            self,
            arg_creator_ids,
            arg_url,
            arg_header,
            arg_cookies_str,
            arg_region,
            arg_path_chromedriver,
            arg_path_file_data = 'data/data2.csv',
            arg_max_workers = 5):
        """获取数据包2"""
        # 判断文件是否存在
        file_exists = os.path.isfile(arg_path_file_data)

        # 读取已有CSV文件
        df_existing = pd.read_csv(arg_path_file_data) if file_exists else arg_creator_ids  # 读取现有 CSV 文件，如果文件不存在则返回空的 DataFrame
        existing_ids = df_existing['达人ID'].astype(str).tolist() if file_exists else []  # 获取已保存的达人ID并确保是字符串类型

        # **************** change *********************************************************
        # 使用线程池并发执行任务
        with ThreadPoolExecutor(max_workers=arg_max_workers) as executor:
            futures = []
            for creator_oec_id in arg_creator_ids:
                future = executor.submit(
                    self.__task_fetch_data_package_2,
                    creator_oec_id,
                    existing_ids,
                    arg_creator_ids,
                    arg_url,
                    arg_header,
                    arg_cookies_str,
                    arg_region,
                    arg_path_file_data,
                    arg_path_chromedriver
                )
                futures.append(future)

            # 等待所有任务完成
            for future in as_completed(futures):
                future.result()  # 捕获异常或结果
        # *********************************************************************************
            
        print(f"所有数据已保存")
def fetch_detail_page(url,header):
    """获取详细页的信息"""
    repeat_check=[]
    for post_data_index in range(0, 1000):
        data_arr = []
        data = {
            "query": "",
            "pagination": {
                "size": 12,
                "search_key": "Amdf/QXk5V0L9UkiotgfHMNCTh3urjUc78Ld8aP/hi4=",
                "next_item_cursor": post_data_index * 12,
                "page": post_data_index
            },
            "filter_params": {},
            "algorithm": 18
        }

        json_data = json.dumps(data)
        try:
            resp = requests.post(url=url, headers=header, data=json_data,timeout=30)
        except Exception as e:
            print(e)
            time.sleep(5)
            resp = requests.post(url=url, headers=header, data=json_data)

        # print(resp.status_code)
        # print(resp.json())
        text = resp.json()
        if text['next_pagination']['has_more']:
            creator_profile_list = text['creator_profile_list']
            for creator_profile_list_index in range(len(creator_profile_list)):
                creator_oecuid = creator_profile_list[creator_profile_list_index]['creator_oecuid']['value']
                if creator_oecuid in repeat_check:
                    continue
                else:
                    repeat_check.append(creator_oecuid)
                    print(creator_oecuid)
                handle = creator_profile_list[creator_profile_list_index]['handle']['value']
                nickname = creator_profile_list[creator_profile_list_index]['nickname']['value']
                selection_region = creator_profile_list[creator_profile_list_index]['selection_region']['value']
                follower_cnt = creator_profile_list[creator_profile_list_index]['follower_cnt']['value']
                ec_video_gpm = creator_profile_list[creator_profile_list_index]['ec_video_gpm']['value']
                ec_live_avg_uv = creator_profile_list[creator_profile_list_index]['ec_live_avg_uv']['value']
                video_avg_view_cnt = creator_profile_list[creator_profile_list_index]['video_avg_view_cnt']['value']
                video_play_cnt_med = creator_profile_list[creator_profile_list_index]['video_play_cnt_med']['value']
                video_gmv = creator_profile_list[creator_profile_list_index].get('video_gmv', {}).get('value', {}).get('value') or None
                live_gmv = creator_profile_list[creator_profile_list_index].get('live_gmv', {}).get('value', {}).get('value') or None
                category = creator_profile_list[creator_profile_list_index]['category']['value']
                top_follower_age = creator_profile_list[creator_profile_list_index]['top_follower_age']['value'][0]['key']
                top_follower_gender = creator_profile_list[creator_profile_list_index]['top_follower_gender']['value'][0]['key']
                video_engagement = creator_profile_list[creator_profile_list_index]['video_engagement']['value']
                ec_video_engagement = creator_profile_list[creator_profile_list_index]['ec_video_engagement']['value']
                has_collaborated = creator_profile_list[creator_profile_list_index]['has_collaborated']['value']
                creator_permission_tag = creator_profile_list[creator_profile_list_index]['creator_permission_tag']['value']
                top_video_data = []
                try:
                    for video_index in range(len(creator_profile_list[creator_profile_list_index]['top_video_data']['value'])):
                        top_video_data.append(creator_profile_list[creator_profile_list_index]['top_video_data']['value'][video_index]['video']['video_infos'][0]['main_url'])
                except:
                    top_video_data = None
                data_arr.append({
                    'creator_oecuid': creator_oecuid,
                    'handle': handle,
                    'nickname': nickname,
                    'selection_region': selection_region,
                    'follower_cnt': follower_cnt,
                    'ec_video_gpm': ec_video_gpm,
                    'ec_live_avg_uv': ec_live_avg_uv,
                    'video_avg_view_cnt': video_avg_view_cnt,
                    'video_play_cnt_med': video_play_cnt_med,
                    'video_gmv': video_gmv,
                    'live_gmv': live_gmv,
                    'category': category,
                    'top_follower_age': top_follower_age,
                    'top_follower_gender': top_follower_gender,
                    'video_engagement': video_engagement,
                    'ec_video_engagement': ec_video_engagement,
                    'has_collaborated': has_collaborated,
                    'creator_permission_tag': creator_permission_tag,
                    'top_video_data': top_video_data,
                })
        else:
            break

        column_names_mapping = {
            'creator_oecuid': '达人ID',
            'handle': '达人用户名',
            'nickname': '达人昵称',
            'selection_region': '选择的地区',
            'follower_cnt': '粉丝数',
            'ec_video_gpm': '视频每千次播放实际最低/最高收益',
            'ec_live_avg_uv': '直播间的平均独立访客数',
            'video_avg_view_cnt': '视频平均播放次数',
            'video_play_cnt_med': '视频播放次数中位数',
            'video_gmv': '视频GMV（商品交易总额）',
            'live_gmv': '直播间GMV',
            'category': '创作者的主要类别',
            'top_follower_age': '最大粉丝年龄组',
            'top_follower_gender': '最大粉丝性别',
            'video_engagement': '视频参与度',
            'ec_video_engagement': '电商视频参与度',
            'has_collaborated': '是否有过合作',
            'creator_permission_tag': '达人的权限标签',
            'top_video_data': '视频数据',
        }

        # 使用上述映射来重命名 data_arr 中的键为中文列名
        data_arr = [{column_names_mapping.get(k, k): v for k, v in item.items()} for item in data_arr]

        # 将 data_arr_renamed 转换为 DataFrame 并写入 CSV 文件
        df = pd.DataFrame(data_arr)

        # 指定要保存的 CSV 文件路径和名称
        csv_file_path = os.path.join('data', 'detail_page.csv')

        # 判断文件是否存在
        file_exists = os.path.isfile(csv_file_path)

        # 如果文件已存在，则以追加模式打开，否则创建新文件
        df.to_csv(
            csv_file_path,
            index=False,
            encoding='utf-8-sig',
            mode='a',  # 追加模式
            header=not file_exists  # 只有当文件不存在时才写入表头
        )
        print(f"数据{post_data_index}已成功追加到 {csv_file_path}")
def extract_categories(categories_str):
    """
    使用safe eval解析字符串形式的列表，并返回相应的类别描述，用顿号连接。
    """
    # 加载 JSON 文件中的类别映射
    with open('static/wares.json', 'r', encoding='utf-8') as file:
        category_mapping = json.load(file)
    # JSON结构是{"message": {"magellan_600154": "家纺布艺", ...}}
    category_mapping = category_mapping.get("message", {})
    try:
        # 使用literal_eval来避免json.loads的限制
        categories_list = literal_eval(categories_str)
        names = []
        for item in categories_list:
            starling_key = item.get('starling_key')
            if starling_key and starling_key in category_mapping:
                names.append(category_mapping[starling_key])
        return '、'.join(names)
    except (ValueError, TypeError) as e:
        print(f"无法解析的创作者的主要类别: {categories_str}, 错误: {e}")
        return ''
def merge_csv_files():
    """将四个CSV文件根据达人ID进行整合到一个CSV文件中"""
    # 读取四个CSV文件
    df1 = pd.read_csv('data/data1.csv')
    df2 = pd.read_csv('data/data2.csv')
    df_detail = pd.read_csv('data/detail_page.csv')
    # 将四个DataFrame根据达人ID进行合并
    df_merged = pd.merge(df_detail, df1, on='达人ID', how='left')
    df_merged = pd.merge(df_merged, df2, on='达人ID', how='left')
    # 保存合并后的DataFrame到新的CSV文件
    df_merged['商品类别'] = df_merged['创作者的主要类别'].apply(extract_categories)
    df_merged['达人ID'] = df_merged['达人ID'].astype(str)
    df_merged.to_csv('data/merged_data.csv', index=False, encoding='utf-8-sig')
    print("四个CSV文件已成功合并到 merged_data.csv")

def startLoadData(url,headers,cookies_str,region,details_url):
    if os.path.isfile('data/merged_data.csv'):
        files_to_remove = ['data/merged_data.csv', 'data/data1.csv', 'data/data2.csv','data/detail_page.csv']
        for file in files_to_remove:
            try:
                os.remove(file)
                print(f"成功删除文件: {file}")
            except Exception as e:
                print(f"删除文件 {file} 失败: {e}")
    if not os.path.isfile('data/data1.csv'):
    # 获取详细页信息
        print("无data/data1.csv")
        fetch_detail_page(url=url,header=headers)
    # 读取详细页信息
    df = pd.read_csv("data/detail_page.csv")  # 读取详细页 CSV 文件
    creator_ids = df['达人ID'].tolist()  # 获取达人 ID 列表
    dataFetcher = DataFetcher()
    # 获取数据包1
    dataFetcher.fetch_data_package_1(
        arg_cookies_str=cookies_str,
        arg_creator_ids=creator_ids,
        arg_header=headers,
        arg_max_workers=5,
        arg_region=region,
        arg_url=details_url,
        arg_path_chromedriver=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # 传参测试
    dataFetcher.fetch_data_package_2(
        arg_cookies_str=cookies_str,
        arg_creator_ids=creator_ids,
        arg_header=headers,
        arg_max_workers=5,
        arg_region=region,
        arg_url=details_url,
        arg_path_chromedriver=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # 传参测试
    merge_csv_files()
if __name__ == '__main__':
    cookies_str='_m4b_theme_=new; i18next=zh-CN; s_v_web_id=verify_m7lfabd3_Jl8J2iPR_y0L8_4PMk_Ap2n_JnCRU5Zr1Bmr; passport_csrf_token=0f6e52fed51e4a3c35e80623888646f0; passport_csrf_token_default=0f6e52fed51e4a3c35e80623888646f0; d_ticket=a43e0c2efa8c25a61db8b25e75ef2d56e64a0; msToken=r1H9zW_qhwaTEn8643Pa3BpHjaxgOOxVP09Fuaam7uhSUJkkgDvZ8TZg7DRFK-RGoSgW-6Han2LT960cCDwy6DL-djy5TdDWvgrSNjjFF6nM; uid_tt=975b57e3bd259cb08dacb79f08d041a7eb28b859550287c1ec0eab0b5648eea2; uid_tt_ss=975b57e3bd259cb08dacb79f08d041a7eb28b859550287c1ec0eab0b5648eea2; sid_tt=e1cf181f85ecbd62cd8160a9c9bf1c55; sessionid=e1cf181f85ecbd62cd8160a9c9bf1c55; sessionid_ss=e1cf181f85ecbd62cd8160a9c9bf1c55; msToken=txPiQ0QirmErpftWIkSaJqSEr6QBNCbXuzbZX_aGy3Gx5sm3_UmKqOIHMMKYYPJjdjQ_q04QPk8pFb3elTu6anhoco_nftfUGSUuIQndmLB2; ttwid=1%7CM2-5BOIM_DRiSUPmadgptgUfqntT-cBGso-4J7ylYko%7C1740544642%7C96f4f8c36572c20a72a9449d6145d9d8da0973c927390a753e16ec33770e4455; sid_guard=e1cf181f85ecbd62cd8160a9c9bf1c55%7C1740544643%7C863992%7CSat%2C+08-Mar-2025+04%3A37%3A15+GMT; sid_ucp_v1=1.0.0-KDM3MTgwYjVjOTgzMjI5N2Y0YTIxZTEzOWJkZWJiZGI2ZjA1YWM3NDkKGAiRiJbund7gsGcQg7X6vQYYnDM4AUDrBxADGgJteSIgZTFjZjE4MWY4NWVjYmQ2MmNkODE2MGE5YzliZjFjNTU; ssid_ucp_v1=1.0.0-KDM3MTgwYjVjOTgzMjI5N2Y0YTIxZTEzOWJkZWJiZGI2ZjA1YWM3NDkKGAiRiJbund7gsGcQg7X6vQYYnDM4AUDrBxADGgJteSIgZTFjZjE4MWY4NWVjYmQ2MmNkODE2MGE5YzliZjFjNTU; lang_type=zh-CN; passport_fe_beating_status=false'
    headers = {
    'path': '/api/v1/oec/affiliate/creator/marketplace/find?user_language=zh-CN&aid=6556&app_name=i18n_ecom_alliance&device_id=0&fp=verify_m5z3kj3u_5IrLVhnI_rbyW_4PzT_AW9a_WyqHSuXALryM&device_platform=web&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F131.0.0.0+Safari%2F537.36&browser_online=true&timezone_name=Asia%2FShanghai&oec_seller_id=7495839077177002076&shop_region=MY&msToken=mncDPr3yLt3R-gcrA8RiLp-_O7HxcWEhQMUaEeHB1Qlrkv3THOLRZSma-LokVxumueiLq7AQkWYdCmd0DGRIthC4y2ugtmSOWeAvSGQr0_ODs1lxvDW-_dDsPAz1e2MhJwqMgxil&X-Bogus=DFSzswVYbt-0OEactpj1hcTQh4tl&_signature=_02B4Z6wo00001t6geJQAAIDDAfuL2vnCxqLeoHwAANAt42',
    'content-type': 'application/json',
    'cookie': cookies_str,
    'referer': 'https://affiliate.tiktokglobalshop.com/connection/creator?shop_region=MY',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 Edg/132.0.0.0'
}
    region='MY'
    shop_id="7495839077177002076"
    details_url=f"https://affiliate.tiktokglobalshop.com/api/v1/oec/affiliate/creator/marketplace/profile?user_language=zh-CN&aid=6556&app_name=i18n_ecom_alliance&device_id=0&fp=verify_m7g9hi5s_6ovVNPzE_w6yB_4u9G_9FOF_EEWcpRs7BnaX&device_platform=web&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F133.0.0.0+Safari%2F537.36&browser_online=true&timezone_name=Asia%2FShanghai&oec_seller_id={shop_id}&shop_region={region}&msToken=A8_Dkys1oqImNwD0QD4I4M1g_UxMsEtv1sZpeE1RhZbt2scejKNCcqOxYCwxlvpjB6B6R-zPPopH5rqmM3wWm_GHcROKJbz6V3RLo6hJ3rimBAnt9p5VIraxTw7N-2Q1GrQji9Lq&X-Bogus=DFSzswVuw9zCkQ4ktDy3vcTQh4CI&_signature=_02B4Z6wo00001TKqungAAIDA7fFJNl0tIy0yqr7AACsW47"
    df = pd.read_csv("data/detail_page.csv")  # 读取详细页 CSV 文件
    creator_ids = df['达人ID'].tolist()  # 获取达人 ID 列表
    dataFetcher = DataFetcher()
    dataFetcher.fetch_data_package_1(
        arg_cookies_str=cookies_str,
        arg_creator_ids=creator_ids,
        arg_header=headers,
        arg_max_workers=5,
        arg_region=region,
        arg_url=details_url,
        arg_path_chromedriver=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # 传参测试