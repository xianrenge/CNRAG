# 对文本进行生成问题

from utils.llm import LLM

# 重问类
class ReQuestion:
	def __init__(self,data=[],from_key='txt',llm=None):
		self.data=data
		self.llm=llm
		self.from_keys=[from_key]
		
	def _do_(self):
		# 遍历数据，llm每个重问，记录到xxx_requestion字段中
		for d in self.data:
			for k in from_keys:
				res=self.llm.get_res(d[k])
				d[k+'_requestion']=res
