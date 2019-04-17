from flask import Flask, render_template, request

from login_weibo import WeiboUpdate
from util import response_json

app = Flask(__name__)

weibo = WeiboUpdate()

#  启动微博通知API
@app.route('/service_control', methods=["post"])
def service_control():
    """
    1.实例化WeiboUpdate对象
    2.执行登录，返回验证码链接
    3.
    :return: 
    """
    status = request.form['status']
    print(status)
    if status == 'start':
        weibo.start()
        return response_json(0, '启动成功')
    else:
        weibo.close()
        return response_json(0, '关闭成功')


# 验证码验证API
@app.route('/verify_code', methods=["post"])
def verify_code():
    """
    
    :return: 
    """
    verify = request.form['verify']
    if weibo.real_login(verify):
        return response_json(0, '登陆成功')
    else:
        return response_json(-1, '验证码错误')



# 验证码接收API
@app.route('/get_verify_code', methods=["post"])
def get_verify_code():
    """
    
    :return: url
    """
    url = weibo.get_verify_url()
    return response_json(0, 'success', {'url': url})


# 启动邮件通知
@app.route('/run', methods=["post"])
def run():
    """

    :return: url
    """
    weibo.run(10)
    return response_json(0, 'success')


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9500)
    # app.run(debug=True)