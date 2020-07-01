#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
# from ihome.libs.yuntongxun.CCPRestSDK import REST
# import ConfigParser
import logging

#主帐号
accountSid= '8aaf070872fe32ae0173046227840353';

#主帐号Token
accountToken= '605933dce9f147dea7e3e4c53a86095c';

#应用Id
appId='8aaf070872fe32ae01730462287d035a';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id


class CCP(object):
  """自己封装的发送短信的辅助类"""

  instance = None

  def __new__(cls):
    # 判断CCP类有没有已经创建好的对象,如果没有,创建一个对象,并且保存
    # 如果有, 则将保存的对象直接返回
    if cls.instance is None:
      obj = super(CCP, cls).__new__(cls)

      obj.rest = REST(serverIP,serverPort,softVersion)
      obj.rest.setAccount(accountSid,accountToken)
      obj.rest.setAppId(appId)
      
      cls.instance = obj
    return cls.instance

  def send_template_sms(self, to, datas, tempId):
    # result = rest.sendTemplateSMS(to,datas,tempId)
    # for k,v in result.iteritems(): 
        
    #     if k=='templateSMS' :
    #             for k,s in v.iteritems(): 
    #                 print '%s:%s' % (k, s)
    #     else:
    #         print '%s:%s' % (k, v)
    try:
        result = self.rest.sendTemplateSMS(to, datas, tempId)
    except Exception as e:
        logging.error(e)
        raise e
    # print result
    # for k, v in result.iteritems():
    #     if k == 'templateSMS':
    #         for k, s in v.iteritems():
    #             print '%s:%s' % (k, s)
    #     else:
    #         print '%s:%s' % (k, v)
    # success = "<statusCode>000000</statusCode>"
    # if success in result:
    #     return True
    # else:
    #     return False
    status_code = result.get("statusCode")
    if status_code == "000000":
      # 表示发送成功
      return 0
    else:
      # 发送失败
      return -1
      



# def sendTemplateSMS(to,datas,tempId):

    
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
    
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems(): 
        
#         if k=='templateSMS' :
#                 for k,s in v.iteritems(): 
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)
    
   
#sendTemplateSMS(手机号码,内容数据,模板Id)

if __name__ == "__main__":
    ccp = CCP()
    res = ccp.send_template_sms("13269505382", ['1234', 5], 1)
    print(res)