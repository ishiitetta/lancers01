import os 
from selenium.webdriver import Chrome,ChromeOptions
import time
import pandas as pd 
import sys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException




### Chromeを起動する関数
def set_driver(driver_path,headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    #options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome()
def login(driver):
    driver.find_element_by_class_name('css-1d2js8m').click()
    time.sleep(2)
    USER = driver.find_element_by_id('UserEmail')
    PASS = driver.find_element_by_id('UserPassword')

    user_key = input('メールアドレスを入力してください>>')
    pass_key = input('パスワードを入力してください>>')

    USER.send_keys(user_key)
    PASS.send_keys(pass_key)
    driver.find_element_by_id('form_submit').click()
    time.sleep(3)
    # ランサーに切り替える
    try:
        driver.find_element_by_class_name('dashboard-menu__title-switch').click()
    except:
        print('ユーザ名かパスワードが間違っています')
        driver.close()
        sys.exit()


def main():
    #chromeを起動
    driver = set_driver("Chromedriver", False)
    #サイトを立ち上げる
    driver.get("https://www.lancers.jp/")
    # ログイン関数を起動
    login(driver)
    # カテゴリーを入力
    key = input('検索したいカテゴリーを入力してください>>>')
    driver.find_element_by_class_name('css-oh82f3').send_keys(key)
    driver.find_element_by_class_name('css-abf23e').click()
    time.sleep(3)
    # 要素を一つずつ抽出するためのXpath
    title_len = driver.find_elements_by_class_name('c-media__title-inner')

    # データフレーム用のリスト作成
    list_info = []
    


   
  
    next = True
    while next == True:
        try:
            path_front = '/html/body/div[3]/div[2]/main/section/div/div[2]/div[3]/div['
            path_count = 1
            path_end = ']/div[1]/div[2]/a/span'

            while len(title_len) >= path_count:
                path = path_front + str(path_count) + path_end
                title_link = driver.find_elements_by_class_name('c-media__content__right')

                # ポップアップが出てきた場合にクリック出てこなかったら無視
                try:
                    pop_link = driver.find_elements_by_css_selector('.c-modal__close.fas.fa-times')
                    if len(pop_link) >= 1:
                        for k in pop_link:
                            k.click()
                except ElementClickInterceptedException:
                    pass

                for t in title_link:
                    aTag = t.find_element_by_tag_name('a')
                    url = aTag.get_attribute('href')

                for l in driver.find_elements_by_xpath(path):
                    l.click()
                    path_count += 1
                    time.sleep(1)
                  
                  
                    head_list = driver.find_elements_by_css_selector('.c-heading.heading--lv1')
                    price_list = driver.find_elements_by_xpath('//*[@id="workDescriptionLink"]/div/div/div[1]/div[2]/div[1]/div/p/span')
                    time_limit_list = driver.find_elements_by_xpath('//*[@id="workDescriptionLink"]/div/div/div[1]/div[2]/div[2]/div/p[2]')
                    propose_list = driver.find_elements_by_xpath('//*[@id="workDescriptionLink"]/div/div/div[1]/div[2]/div[3]/div/p[2]')

                    # ランクと本人確認があるものは除外
                    lank_info = driver.find_elements_by_class_name('alert__heading')
                    alert_info = driver.find_elements_by_css_selector('.alert__description.c-list.list--linkA01')
                    if len(lank_info) >= 2:
                        driver.back()
                    if len(alert_info) >= 1:
                        driver.back()
                 
                    # 1ページ文の要素を抽出
                    for head, price, time_limit, propose in zip(head_list, price_list, time_limit_list, propose_list):
                        print(head.text)
                        print(price.text)
                        print(time_limit.text)
                        print(propose.text)
                        print(url)
                        # リストに代入
                        list_info += [[head.text, price.text, time_limit.text, propose.text, url]]
                        # csvファイルに書き出し
                        df = pd.DataFrame(data=list_info,columns=['案件名', '価格', '残り時間', '提案数', 'URL'])
                        df.to_csv('lancers01.csv',encoding='utf-8_sig')
                        driver.back()
            
            # 1ページ文の処理が終わったら次へをクリック
            next_button = driver.find_element_by_css_selector('.pager__item.pager__item--next')
            next_button.click()
            time.sleep(2)


        except NoSuchElementException:             
            next == False
            print('処理が終了しました')
            break
        
        

        
### 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main() 


 
    
