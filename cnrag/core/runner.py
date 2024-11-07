# 运行示例

from cnrag.utils.data import files_data,data_format
from cnrag.core.vector import VectorDB


# 简单示例
class SimpleRunner:
    def __init__(self,data_path=None,txts=[],model_dir=None):
    	if data_path:
    		self.data=files_data(data_path)
    	elif txts:
    		self.data=data_format(txts)
    	else:
    		self.data=[]

    	self.vectordb=VectorDB(embedding_model_dir=model_dir)

    	if self.data and self.vectordb:
    		self.insert(self.data)


    def insert(self,txts):
    	# print(txts)
    	self.vectordb.insert(txts)
    	return True

    def select(self,query,**kwarg):
    	res=self.vectordb.select(query,**kwarg)
    	return res

