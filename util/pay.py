#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse
from alipay.aop.api.util.SignatureUtils import verify_with_rsa, get_sign_content


from django.conf import settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


class AliPay:
    def __init__(self):
        """
        设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
        """
        self.alipay_client_config = AlipayClientConfig()
        # 网关
        self.alipay_client_config.server_url = settings.ZFB_SERVER_URL
        # app_id
        self.alipay_client_config.app_id = settings.ZFB_APPID
        # 商家id
        self.alipay_client_config.seller_id = settings.ZFB_SELLER_ID
        # app私钥
        self.alipay_client_config.app_private_key = settings.ZFB_APP_PRIVATE_KEY
        # 支付宝公钥
        self.alipay_client_config.alipay_public_key = settings.ZFB_PUBLIC_KEY
        # 通知地址
        self.notify_url = settings.ZFB_NOTIFY_URL
        # return url
        self.return_url = settings.ZFB_RETURN_URL
        """
        得到客户端对象。
        注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
        logger参数用于打印日志，不传则不打印，建议传递。
        """
        self.client = DefaultAlipayClient(alipay_client_config=self.alipay_client_config, logger=logger)


    def TradePagePay(self, out_trade_no, total_amount, subject, product_code):

        # 对照接口文档，构造请求对象
        model = AlipayTradePagePayModel()
        # 订单号
        # model.out_trade_no = "pay2805020000228"
        model.out_trade_no = out_trade_no
        # 订单金额
        # model.total_amount = 0.01
        model.total_amount = total_amount
        # 订单标题
        # model.subject = "测试"
        model.subject = subject
        # 与支持包签约的产品码名称
        # model.product_code = "FAST_INSTANT_TRADE_PAY"
        model.product_code = product_code

        request = AlipayTradePagePayRequest(biz_model=model)
        request.return_url = self.return_url
        request.notify_url = self.notify_url
        # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
        response = self.client.page_execute(request, http_method="GET")
        return response

    def get_sign(self, all_params):
        return get_sign_content(all_params)


    def verify_sign(self, unsigned_string, sign):
        return verify_with_rsa(self.alipay_client_config.alipay_public_key, bytes(unsigned_string, encoding='utf-8'), sign)

