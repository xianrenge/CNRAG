# 数据



# 从目录中文件中获取文本列表
def files_txts(data_path,file_extensions=['.txt']):
	txts=[]
	for fn in os.listdir(data_path):
		if not any(fn.endswith(ext) for ext in file_extensions):
			continue
		with open(os.path.join(data_path,fn),'r',encoding='utf-8') as f:
			txts.append(f.read())
	return txts


# 对文本列表统一格式化为标准格式[{'index':0,'txt':'...'},]
def data_format(txts,key='txt',start_id=0):
	res=[]
	for i,t in enumerate(txts):
		res.append({'index':i+start_id,key:t})
	return res


# 从目录中读取文本
# geted:txt todo:
def files_data(data_path,key='txt',start_id=0,file_extensions=['.txt']):
	txts=files_txts(data_path,file_extensions)
	data=data_format(txts,key,start_id)
	return data



# todo
# 对目录进行深层循环遍历


class BaseData:
	def __init__(self):
		self.data=[]


class Files2Data(BaseData):
	def __init__(self,data_path):
		self.data=[]