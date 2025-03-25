import time
import tkinter as tk
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import http.cookies

def startSend(mycookies,info,creator_list,shop_id,region):
    """
    mycookies:用户tiktop首页的cookies
    info:发送的信息
    creator_list:达人列表
    shop_id:店铺id
    region:地区
    """
    # root = tk.Tk()
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()
    url=f"https://affiliate.tiktokglobalshop.com/seller/im?shop_id={shop_id}&creator_id={creator_list[0]}&enter_from=affiliate_creator_details&shop_region={region}"
    chrome_options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    # chrome_options.add_argument(f"window-size={screen_width},{screen_height}")
    cookies = http.cookies.SimpleCookie()
    cookies.load(mycookies)
    service = ChromeService(ChromeDriverManager().install())
    # service = ChromeService(executable_path='static/chromedriver')  # 替换为chromedriver路径
    driver = webdriver.Chrome( options=chrome_options,service=service)
    # driver = webdriver.Chrome( options=chrome_options)
    try:
        # 导航到目标网站
        driver.get(url)  
        wait = WebDriverWait(driver, 30)
        # 添加cookies
        for cookie_name in cookies:
            cookie = {
                'name': cookie_name,
                'value': cookies[cookie_name].value,
                'domain': '.tiktokglobalshop.com',  # 确保域正确匹配目标网站
                'path': '/',  # 默认路径为根路径
            }
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"Failed to add cookie {cookie['name']}: {e}")
        # 刷新页面使新cookies生效
        driver.refresh()
        time.sleep(3)
        for creator_id in creator_list:
            url = f"https://affiliate.tiktokglobalshop.com/seller/im?shop_id={shop_id}&creator_id={creator_id}&enter_from=affiliate_creator_details&shop_region={region}"
            driver.get(url=url)
            time.sleep(5)
            textarea = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#im_sdk_chat_input > textarea")))
            textarea.send_keys(info)
            time.sleep(5)
            btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#im_sdk_chat_input  div.index-module__footer--mSGEi .index-module__send--8FbXJ button span")))
            print(btn.text)
            # btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#im_sdk_chat_input > div.index-module__footer--mSGEi > div > button")))
            # 尝试使用JavaScript点击以防直接点击失败
            time.sleep(2)
            # driver.execute_script("arguments[0].click();", btn)
            btn.click()
            time.sleep(2)
    finally:
        # 关闭浏览器
        driver.quit()
if __name__ == '__main__':
    # cookies_str="_m4b_theme_=new; passport_csrf_token=5ce3b76c8297f59d8bd0be87a10a30a2; passport_csrf_token_default=5ce3b76c8297f59d8bd0be87a10a30a2; d_ticket=84956a23caa1565d890f43d484f40b626d07a; msToken=TUo38ibsW5yrfpnkp5T9FXz45SVDNQ7T9v1J1jsFwoOExGcAiWg2rNYmx9u8XRwzLbx24-c_yeVByjlaO0RC_tq15DtENgIhP-936ngRRIzrSjPhYEkl9gKIRStWSlnHT5ZMFys=; odin_tt=baafa3abe02607c7c2651a87401aaaa735146b0187ca4eec7c278e0a6133a3b4da52f057b312f8efa8997e03b128bc7aa725f28494870efdf0e267d5d61fd45a; i18next=zh-CN; gf_part_2494901=95; gf_part_2508734=72; gf_part_2506134=11; gf_part_2528808=15; gf_part_2532058=10; gf_part_2531717=54; gf_part_2531756=35; gf_part_2531806=72; gf_part_2531816=58; gf_part_2537864=88; gf_part_2537926=72; uid_tt=59d84ce0db82a0bb8a1946e13f566d899a0db8b91d063e973f747d74ffd145e2; uid_tt_ss=59d84ce0db82a0bb8a1946e13f566d899a0db8b91d063e973f747d74ffd145e2; sid_tt=ea79d04d21360083cd5f95f629bb6173; sessionid=ea79d04d21360083cd5f95f629bb6173; sessionid_ss=ea79d04d21360083cd5f95f629bb6173; msToken=Q2WjkJsLnpRYsQ04OK6nxQRehNHOwFMpaeXV8GcQSsVddB1kwm4OruOkke2PbI7LbdrzCSl4YtTDt4IyzRyCUiyAcNYmVWghKnKYVaOh-hYAb2ZjX2WnlqwC-PxEbTQ2_R3fJKc=; sid_guard=ea79d04d21360083cd5f95f629bb6173%7C1739541396%7C863998%7CMon%2C+24-Feb-2025+13%3A56%3A34+GMT; sid_ucp_v1=1.0.0-KGNiZGI1OGRkMDA4ZTY0ZDZkYzNjMjA0MDA5NTE5MWQ4Y2IwYmJjNjEKGAiRiJbund7gsGcQlJe9vQYYnDM4AUDqBxADGgNteTIiIGVhNzlkMDRkMjEzNjAwODNjZDVmOTVmNjI5YmI2MTcz; ssid_ucp_v1=1.0.0-KGNiZGI1OGRkMDA4ZTY0ZDZkYzNjMjA0MDA5NTE5MWQ4Y2IwYmJjNjEKGAiRiJbund7gsGcQlJe9vQYYnDM4AUDqBxADGgNteTIiIGVhNzlkMDRkMjEzNjAwODNjZDVmOTVmNjI5YmI2MTcz; s_v_web_id=verify_m75yai0i_emaz1khl_V1OF_4R1b_AnU2_rsI0R1hfN02k; ttwid=1%7CtbTiHqQMeR2P7_nPdTnRnxy4DLiPRVre1XG6axJLULk%7C1739609016%7C3cac1e84fafc91906eb385e1d502b0f7d06cb1f9dde6d4ebf118932b23e453fb; lang_type=zh-CN; passport_fe_beating_status=false"
    cookies_str="_m4b_theme_=new; i18next=zh-CN; s_v_web_id=verify_m7xeq51y_phI3wCJq_RZhz_4rux_8Sg6_SlqcNyv0oXDu; gf_part_2624033=78; gf_part_2589100=39; passport_csrf_token=c198196053352daceb927592484381d4; passport_csrf_token_default=c198196053352daceb927592484381d4; d_ticket=81afa0a5ee8720fc2191e33a3f84eb93c3d33; msToken=74jEmVpw4SLOJ818QrjMUf2wdKRPk_Bxv8deY05QE2kZpX909YZm-W1HMKs2-nzV89LovTY7Zq-ZK-fg12kS52VxhRogm7IyeZGf0A-dRC6k; uid_tt=daa04d27901cbb323a1a0d8deacd7636f5477f864fbe708859af978b86551dd9; uid_tt_ss=daa04d27901cbb323a1a0d8deacd7636f5477f864fbe708859af978b86551dd9; sid_tt=21c844bd8abf2d494e4c50520d3d85d2; sessionid=21c844bd8abf2d494e4c50520d3d85d2; sessionid_ss=21c844bd8abf2d494e4c50520d3d85d2; msToken=FOEpfqUkjc803rX0ikvMeZ5lL0nJwmkgm8Y6lYdjIbCXLypYUgrLNL0Xj8iwlNCDC9OktQtVTO7z7AsdDrrrIfUsnzaLRUjY38XasX7mWdP4; ttwid=1%7CxmkYpEFCyKRrjJNXvUaYTjLTgFdEXQ_0TV3qS_lR0NQ%7C1741269337%7C5ffad25da183db221f9f408dff4fa836fa9665ced52622b5958cfb2662b20602; sid_guard=21c844bd8abf2d494e4c50520d3d85d2%7C1741269337%7C863983%7CSun%2C+16-Mar-2025+13%3A55%3A20+GMT; sid_ucp_v1=1.0.0-KDRkYzFhYjhhZjc5ZGJhZDNlM2IyNjRhYjYyMGZkMzQxNmJlZjA4ZjcKGAiRiJbund7gsGcQ2dKmvgYYnDM4AUDrBxADGgNzZzEiIDIxYzg0NGJkOGFiZjJkNDk0ZTRjNTA1MjBkM2Q4NWQy; ssid_ucp_v1=1.0.0-KDRkYzFhYjhhZjc5ZGJhZDNlM2IyNjRhYjYyMGZkMzQxNmJlZjA4ZjcKGAiRiJbund7gsGcQ2dKmvgYYnDM4AUDrBxADGgNzZzEiIDIxYzg0NGJkOGFiZjJkNDk0ZTRjNTA1MjBkM2Q4NWQy; lang_type=zh-CN; passport_fe_beating_status=false"
    shop_id="7495839077177002076"
    creator_id_list=["7494015885857097026","7494005977059919561"]
    creator_id_list=["7494015885857097026"]
    info="hello,this is a test"
    region='MY'
    startSend(mycookies=cookies_str,shop_id=shop_id,creator_list=creator_id_list,info=info,region=region)