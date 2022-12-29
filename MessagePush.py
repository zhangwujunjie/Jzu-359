import requests


# PushPlus
def pushMessage(title, content, token):
    # title 是标题
    # content是正文内容
    # token是 token
    url = 'http://www.pushplus.plus/send?token=' + token + '&title=' + title + '&content=' + content + '&template=html'
    resp = requests.post(url)
    if resp.json()["code"] == 200:
        print('推送消息提醒成功！')
    else:
        print('推送消息提醒失败！')
