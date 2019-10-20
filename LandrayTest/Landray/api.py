import json
from os import path
import requests
from Landray import app

ip = app.config["IP"]
client_id = app.config["CLIENT_ID"]
client_secret = app.config["CLIENT_SECRET"]


class MyRequest(object):
    def __init__(self, prefix_path):
        """
        拼接URL
        :param prefix_path: 不同微服务, 不同的前缀
        """
        self.prefix_url = ip + prefix_path

    def send_get(self, suffix_path, querystring=None, headers=None):
        """
        发送get请求
        :param suffix_path: 请求链接的API
        :param querystring: 请求参数
        :param headers: 请求头
        :return:
        """
        try:
            url = self.prefix_url + suffix_path
            if headers is None:
                headers = {
                    'Content-Type': "application/json",
                    'Cache-Control': "no-cache"
                }
            response = requests.request("GET", url, headers=headers, params=querystring)
            status_code = response.status_code
            if status_code <= 200 or status_code <= 299:
                return response.json()
            app.logger.error(response.json())
            return False
        except requests.exceptions.RequestException:
            app.logger.error('HTTP Request failed')
            return False

    def send_post(self, suffix_path, querystring=None, body=None, headers=None):
        """
        发送POST请求
        :param suffix_path: 请求链接的API
        :param querystring: 请求参数
        :param body: 请求体
        :param headers: 请求头
        :return:
        """
        try:
            url = self.prefix_url + suffix_path
            response = requests.request("POST", url, data=json.dumps(body), headers=headers, params=querystring)
            status_code = response.status_code
            if status_code >= 201 or status_code <= 299:
                return response.json()
            app.logger.error(response.json())
            return False
        except requests.exceptions.RequestException:
            app.logger.error('HTTP Request failed')
            return False

    def send_put(self, suffix_path, headers=None, body=None, querystring=None):
        """
        发送PUT请求
        :param suffix_path: 请求链接的API
        :param headers: 请求头
        :param body: 请求体
        :param querystring: 请求参数
        :return:
        """
        try:
            url = self.prefix_url + suffix_path
            response = requests.request("PUT", url, data=json.dumps(body), headers=headers, querystring=querystring)
            if response.status_code >= 201 or response.status_code <= 299:
                return response.json()
            app.logger.error(response.json())
            return False
        except requests.exceptions.RequestException:
            app.logger.error("HTTP Request failed")
            return False

    def upload_file(self, suffix_path, filepath, headers=None):
        """
        发送上传文件请求
        :param suffix_path: 上传文件的API
        :param filepath: 上传文件的路径
        :param headers: 请求头
        :return:
        """
        properties = {"fileName": path.basename(filepath),
                      "from": "LOCAL"}
        json_properties = json.dumps(properties)
        file_data = {"file": (path.basename(filepath), open(filepath, "rb"))}
        url = self.prefix_url + suffix_path
        try:
            response = requests.post(
                url=url,
                params={
                    "properties": json_properties,
                },
                headers=headers,
                files=file_data,
            )
            status_code = response.status_code
            if status_code >= 201 or status_code <= 299:
                return response.json()
            app.logger.error(response.json())
            return False
        except requests.exceptions.RequestException:
            app.logger.error('HTTP Request failed')
            return False


class Oauth(object):
    """
    Oauth 微服务
    """

    def __init__(self):
        self.obj = MyRequest("oauth/oauth/")

    def get_access_token(self):
        """
        获取access_token
        :return:
        """
        suffix_path = "token"
        querystring = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        response = self.obj.send_get(suffix_path, querystring)
        if response is False:
            return False
        access_token = response.get("access_token")
        return access_token


class Open(object):
    """
    open 微服务
    """

    def __init__(self):
        self.obj = MyRequest("open/")

    def create_enterprise_authentications(self, body):
        """
        创建企业认证流程
        :param body: POST 请求体
        :return: action_url
        """
        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
            'X-Signit-App-Id': client_id
        }
        access_token = Oauth().get_access_token()
        if access_token is False:
            app.logger.error("获取access_token失败")
            return False
        querystring = {
            "access_token": access_token,
        }
        response = self.obj.send_post("enterprise-authentications", querystring, body, headers)
        if response is False:
            app.logger.error("创建企业实名认证流程失败")
            return False
        action_url = response.get("actionUrl")
        if action_url:
            return action_url
        app.logger.error("获取action_url失败{}", response)
        return False
