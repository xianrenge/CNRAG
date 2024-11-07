

from openai import OpenAI
import os
import time
import random
import json




# 先只支持openai的api调用
class LLM:
	def __init__(self,base_url,api_key=None,model_name=None):
		self.client = OpenAI(api_key=gpt_api_key,
						  base_url=base_url,
						)
		self.model_name=model_name

	# 只返回文本及文本列表
	def get_res(self,mess,model_name=None,n=1,temperature=0.95,max_tokens=512,extra_body={}):
	    completion = get_res_ex(mess,model_name,n,temperature,max_tokens,extra_body)
	    if n==1:
	    	return completion.choices[0].message.content
		return [v.message.content for v in completion.choices]

	# 返回完整数据
	def get_res_ex(self,mess,model_name=None,n=1,temperature=0.95,max_tokens=512,extra_body={}):
	    completion = self.client.chat.completions.create(
	        model=model_name,
	        messages=mess,
	        max_tokens=max_tokens,
	        temperature=temperature,
	        n=n,
	        extra_body=extra_body
	    )
		return completion
	
	# 只输入文本，自动标准化送入模型接口
	def txt2res(self,txt,system=None,model_name=None,n=1,temperature=0.95,max_tokens=512,extra_body={}):
		mess=[system] if system else []
		mess.append({"role": "user", "content": txt})
		res=self.get_res(mess,model_name,n,temperature,max_tokens,extra_body)
		return res

	# 只输入文本，自动标准化送入模型接口，返回完整数据
	def txt2res_ex(self,txt,system=None,model_name=None,n=1,temperature=0.95,max_tokens=512,extra_body={}):
		mess=[system] if system else []
		mess.append({"role": "user", "content": txt})
		res=self.get_res_ex(mess,model_name,n,temperature,max_tokens,extra_body)
		return res

