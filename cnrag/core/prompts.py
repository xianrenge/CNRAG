# prompt相关

from cnrag.utils.prompt_template import *
from cnrag.core.outer import out_parse

class BasePrompt:
	def __init__(self,template=''):
		self.template=template
		self.parse=None

	def __call__(self,**kwarg):
		res=self.template.format(**kwarg)
		res=self._parse(res)
		return res

	def _parse(self,txt):
		txt=out_parse(txt,self.parse)
		return txt


# 重问
class QusetionPrompt(BasePrompt):
	def __init__(self,template='qusetion_prompt'):
		qusetion_prompt=globals()[template]
		self.template=qusetion_prompt['template']
		self.kwarg=qusetion_prompt['input_vars']
		self.parse=qusetion_prompt['parse_re']



# todo:
# 重问
# query改写
# 摘要
# 提取关键词
# 大模型切分
# llm排序
# 汇总生成