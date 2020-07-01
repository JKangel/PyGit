#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
# from ihome.libs.yuntongxun.CCPRestSDK import REST
# import ConfigParser
import logging

#���ʺ�
accountSid= '8aaf070872fe32ae0173046227840353';

#���ʺ�Token
accountToken= '605933dce9f147dea7e3e4c53a86095c';

#Ӧ��Id
appId='8aaf070872fe32ae01730462287d035a';

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com';

#����˿� 
serverPort='8883';

#REST�汾��
softVersion='2013-12-26';

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id


class CCP(object):
  """�Լ���װ�ķ��Ͷ��ŵĸ�����"""

  instance = None

  def __new__(cls):
    # �ж�CCP����û���Ѿ������õĶ���,���û��,����һ������,���ұ���
    # �����, �򽫱���Ķ���ֱ�ӷ���
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
      # ��ʾ���ͳɹ�
      return 0
    else:
      # ����ʧ��
      return -1
      



# def sendTemplateSMS(to,datas,tempId):

    
#     #��ʼ��REST SDK
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
    
   
#sendTemplateSMS(�ֻ�����,��������,ģ��Id)

if __name__ == "__main__":
    ccp = CCP()
    res = ccp.send_template_sms("13269505382", ['1234', 5], 1)
    print(res)