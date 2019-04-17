import json
import time
import re
from selenium import webdriver
from lxml import etree
from util import send_email
from config import receivers


class WeiboUpdate(object):
    def start(self, username='xxxxxxxxx', password='xxxxxxxxx'):
        self.driver = self._get_driver()
        self._login(username, password)

    def close(self):
        self.driver.close()

    def _get_driver(self):
        browser = webdriver.Chrome(executable_path='./chromedriver')
        browser.maximize_window()
        return browser

    def _login(self, username, password):
        """
        获取登录状态
        :param username: 
        :param password: 
        :return: 
        """
        self.driver.get('https://weibo.com/')
        time.sleep(8)
        input_username = self.driver.find_element_by_id('loginname')
        input_username.send_keys(username)
        input_password = self.driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
        input_password.send_keys(password)
        time.sleep(2)

    def real_login(self, verify_code, t=600):
        """
        返回登录状态
        :param verify_code: 
        :return: bool
        """
        input_verify_code = self.driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input')
        input_verify_code.send_keys(verify_code)
        button = self.driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')
        button.click()

        time.sleep(3)

        if '我的首页' in self.driver.title:
            # 执行定时任务解析
            # self.run(t)
            return True
        return False

    def get_verify_url(self):
        # 拿到验证码
        return self.driver.find_element_by_xpath('//img[@node-type="verifycode_image"]').get_attribute('src')

    def parse(self):
        """
        解析微博内容
        :return: 
        """
        html = re.compile('({"ns":"pl.content.homefeed.index".*?)\)</script>').findall(self.driver.page_source)[0]
        new_html = json.loads(html)['html'].replace('&gt;', '>').replace('&lt;', '<')
        selector = etree.HTML(new_html)
        infoes = selector.xpath('//div[@class="WB_feed_detail clearfix"]')
        r = []
        for info in infoes:
            r.append({
                'weibo_author': info.xpath('./div/div[@class="WB_info"]/a/@nick-name')[0],
                'weibo_content': info.xpath('./div/div[@class="WB_text W_f14"]')[0].xpath('string(.)').strip(),
                'weibo_time': info.xpath('./div/div[@class="WB_from S_txt2"]/a/text()')
            })

        return r

    def alert(self, infos):
        """
        判断消息并通知
        :return: 
        """
        message = []
        for info in infos:
            if info['weibo_time']:
                weibo_time = info['weibo_time'][0]
                min = re.compile('([0-9]+)').findall(weibo_time)
                if len(min) and int(min[0]) < 20 and ':' not in weibo_time:
                    message.append('{} {} 发布了新消息'.format(weibo_time, info['weibo_author']))
        message = '\n'.join(message)
        for receiver in receivers:
            if not send_email(message, 'monitor', receiver):
                print('%s： 邮件通知发送失败' % receiver)


    def run(self, T):
        """
        入口方法
        :return:
        """
        self.alert(
            self.parse()
        )
        print('over')
        #  等待
        time.sleep(T)
        self.driver.refresh()



if __name__ == '__main__':
    WeiboUpdate().run(60)






