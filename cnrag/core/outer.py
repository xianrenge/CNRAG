# 输出解析

import re

def txt_parse(txt :str,txt_re :str) -> list:
	res=re.findall(txt_re,txt,flags=re.DOTALL)
	return res

def out_parse(txt,parse=None):
	if isinstance(parse,str):
		res=txt_parse(txt,parse)
	elif isinstance(parse,list):
		res=[]
		for p in parse:
			res.extend(txt_parse(txt,p))
	elif isinstance(parse,dict):
		res={}
		for k,v in parse.item():
			res[k]=txt_parse(txt,v)
	return res

class BaseOutPaser:
	def __init__(self):
		self.format=''

