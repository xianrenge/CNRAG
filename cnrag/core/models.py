# 各种模型

from sentence_transformers import SentenceTransformer, util


class Embedding:
	def __init__(self,model_dir=None,is_cuda=True):
		self.model = SentenceTransformer(model_dir)
		self.is_cuda=is_cuda

	def txts_vector(self,vs):
		res=self.model.encode(vs, convert_to_tensor=self.is_cuda)
		return res

	# def txt_vector(self,txt):
	# 	res=self.model.encode(txt, convert_to_tensor=self.is_cuda)
	# 	return res

	def cal_cosine(self,q,vs):
		res=util.pytorch_cos_sim(q, vs)
		res = res[0].tolist()
		return res
	def txt_cosine(self,txt,vs):
		emb=self.txts_vector(txt)
		res=self.cal_cosine(emb,vs)
		return res
