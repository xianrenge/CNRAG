# 数据保持

import os
import torch
import time
from datetime import datetime

def save_vector(d,data_dir='./data_save',file_name='vector.pth'):
	if instance(d,dict):
		torch.save(d, os.path.join(data_dir,file_name) )


# 加载数据
def load_vector(d,data_dir='./data_save',file_name='vector.pth'):
	d = torch.load(os.path.join(data_dir,file_name))
	return d


# 小文件记录
def vectordb_log(file='_do',do='heart_jump',data_dir='./vectordb'):
	with open(os.path.join(data_dir,file),'a+',encoding='utf-8') as f:
		dt = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
		f.write(f'--dt:{dt}--{do}--\n')

# 向量持久本地化
def vectordb_persist(db,data_dir='./vectordb'):
	d={'vectors':db.vectors,
		'txt_ids':db.txt_ids,
		'txt_ls_ids':db.txt_ls_ids,
		'txt_ls_vectors':db.txt_ls_vectors,
		'txt_ls_keys':db.txt_ls_keys,
		'txts':db.txts,
		# 'indexs':db.indexs,
		# 'infos':db.infos,
		# 'infos_vectors':db.infos_vectors,
	}
	save_vector(d,data_dir,file_name='db_info.pth') 
	vectordb_log(file='_do',do='db_save',data_dir=data_dir)
	return True