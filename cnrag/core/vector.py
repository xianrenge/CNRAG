# 向量类

from cnrag.core.models import Embedding
from cnrag.utils.utils import (
    group_and_max_by_order,
)
from cnrag.utils.save import vectordb_persist

from sentence_transformers import SentenceTransformer,util


# self.vectors改为字典的，txt+其他额外字段的在一起√
# 增加合并方式，倒数融合，分数加权，位置加权
# 增加切分方式
# 多查询、
# 不同相似度方法
# 增加单个数据中有文本列表的向量化支持√
class VectorDB:
    def __init__(self,embedding=None,embedding_model_dir=None,embedding_cuda=True,local_dir=None):
        if embedding:
            self.embedding=embedding
        elif embedding_model_dir:
            self.embedding=SentenceTransformer(embedding_model_dir)
            # self.embedding=Embedding(embedding_model_dir,embedding_cuda)
        else:
            raise '>>> no embedding!'

        if not local_dir: # 无本地已有数据
            self.vectors={}
            self.txt_ids=[]
            self.txt_ls_ids={} # 针对单个txt有多个文本需要向量的情况
            self.txt_ls_vectors={}
            self.txt_ls_keys=[] # 数据字段为列表格式的字段
            self.txts=[]
            self.local_dir=local_dir
            # self.indexs=[]
            # self.infos={}
            # self.infos_vectors={}
        else:
            # 加载相关数据
            pass

    # 插入数据，不能命名的字段有summary,boobm_querys,select_key_txt,from_keys,all_keys
    def insert(self,txts,txts_vector_keys=['txt']):
        if not txts or type(txts[0])!=dict:
            raise '>>> txts[0] type error!'
        self.txts=txts
        # 额外字典参与embedding
        if txts_vector_keys:
            # 文本字典中参与向量计算的文本收集+ids顺序列表
            self.info_ids =[]
            infos_txts={k:[] for k in txts_vector_keys }
            infos_ls_txts={}
            for t in txts:

                self.txt_ids.append(t['index'])
                for i,tik in enumerate(txts_vector_keys):
                    if type(t[tik])==str: # 字段内容为文本，直接整体添加到self.info_ids中
                        infos_txts[tik].append(t[tik])
                    elif type(t[tik])==list: # 字段内容为列表格式，需单独处理
                        if tik not in self.txt_ls_ids:
                            self.txt_ls_ids[tik]=[]
                        self.txt_ls_ids[tik]+=[t['index']]*len(t[tik])
                        if tik not in infos_ls_txts:
                            infos_ls_txts[tik]=[]
                        infos_ls_txts[tik]+=t[tik]
            self.txt_ls_keys=list(infos_ls_txts.keys())

            # 计算embedding
            self.vectors={k:self.embedding.encode(vs, convert_to_tensor=True) for k,vs in infos_txts.items()}
            self.txt_ls_vectors={k:self.embedding.encode(vs, convert_to_tensor=True) for k,vs in infos_ls_txts.items()}
            # self.vectors={k:self.embedding.txts_vector(vs) for k,vs in infos_txts.items()}
            # self.txt_ls_vectors={k:self.embedding.txts_vector(vs) for k,vs in infos_ls_txts.items()}
            print('vectors:',self.vectors)
            print('txt_ls_vectors:',self.txt_ls_vectors)
            if self.local_dir:
                vectordb_persist(self,data_dir=self.local_dir)
        else:
            raise '>>> no data to vector!'

    # 融合方式，and交集，or并集,or_best混合一起且按分数大小排序,or_weight加权混合
    # 返回数据方式：(1)不去重返回undeduplicate：按查找字段返回文本 or 返回指定字段，(2)去重返回deduplicate：指定字段返回（附带命中查找字段说明extra字段）
    # select_keys中遇到数据为列表的字段，目前统计时按分数最大的来
    def select(self,txt,select_keys=['txt'],combine_type='or_best',combine_weight=[],do_type='cosine',
            topk=5,score_thr=0.0,out_score=False,return_keys=['select_key_txt'],return_combine='deduplicate'
            ):
        if return_keys:
            # 有字段不在self.vectors中
            if len([v for v in return_keys if v!='select_key_txt' and v not in self.vectors])>0:
                raise '>>> vector db has not the type data!'
        if not combine_weight:
            combine_weight=[1/len(select_keys)]*len(select_keys)
        else:
            assert  (len(combine_weight) == len(select_keys)), ">>> 权重和查询字段长度不一致！"


        query_embedding = self.embedding.encode(txt, convert_to_tensor=True)
        # query_embedding = self.embedding.txts_vector(txt)
        # print('query_embedding:',query_embedding)

        # 预设分数变量
        if combine_type=='or_weight':
            scores=[0]*len(self.txt_ids)
        elif combine_type=='or_best':
            scores=[0]*len(self.txt_ids)*len(select_keys)
        else:
            raise f'>>> unknown combine_type:{combine_type}'

        # 计算相似度
        scores_ls=[]
        # scores_list_ls=[] # 数据列表字段的分数
        for k in select_keys:
            if k in self.txt_ls_vectors:
                vecs=self.txt_ls_vectors[k]
            else:
                vecs=self.vectors[k]

            cosine_scores = util.pytorch_cos_sim(query_embedding, vecs)
            scores_tmp = cosine_scores[0].tolist()
            if k in self.txt_ls_keys:
                scores_tmp=group_and_max_by_order(self.txt_ls_ids[k],scores_tmp,self.txt_ids) # 按id内最大分数算
                scores_ls.append(scores_tmp)
            else:
                scores_ls.append(scores_tmp)
        print('scores_ls:',len(scores_ls))

        # 统计分数
        if combine_type=='or_weight':
            # 分数-加权融合
            for i,s in enumerate(scores):
                scores[i]=sum([scores_ls[j][i]*w for j,w in enumerate(combine_weight)])
            scores_ids=self.txt_ids
        elif combine_type=='or_best':
            # 混合在一起
            scores=[v for vl in scores_ls for v in vl]
            scores_ids=[[i,k] for k in select_keys for i in self.txt_ids]

        # 排序
        id_score_pairs = list(zip(scores_ids, scores))
        id_score_pairs.sort(key=lambda x: x[1], reverse=True)

        # 分数阈值过滤
        id_score_pairs=[v for v in id_score_pairs if v[1]>=score_thr]

        # 返回数据收集处理
        if return_combine=='deduplicate':
            return_keys=[v for v in return_keys if v!='select_key_txt'] # 此模式排除此字段
            return_pairs=[]
            v_k=0
            ids_geted={}
            for i,d in enumerate(id_score_pairs):
                if v_k>=topk:
                    break
                if len(d[0])==1:# 已去重
                    return_pairs.append(dict(zip(['txt','score']+return_keys,[self.txts[d[0]]['txt'],d[1]]+[self.txts[d[0]][k] for k in return_keys])))
                elif len(d[0])==2:

                    j=ids_geted.get(d[0][0],-1)
                    if j<0: # 还未选中
                        ids_geted[d[0][0]]=v_k # 记录选中位置
                        v_k+=1
                        return_pairs.append(dict(zip(['txt','score']+return_keys+['from_keys'],[self.txts[d[0][0]]['txt'],d[1]]+[self.txts[d[0][0]][k] for k in return_keys]+[[d[0][1]]])))
                    else:# 只添加对应的key
                        return_pairs[j]['from_keys'].append(d[0][1])
        elif return_combine=='undeduplicate': # 不去重返回
            # 
            if combine_type=='or_best':
                return_pairs=[dict(zip(['select_key_txt','score']+return_keys+['from_keys'],[ self.txts[v[0][0]][v[0][1]] ,v[1]]+[self.txts[v[0][0]][k] for k in return_keys]+[[v[0][1]]])) 
                    for v in id_score_pairs[:topk]]
            if combine_type=='or_weight': # 此模式下，默认返回txt
                return_pairs=[dict(zip(['txt','score']+return_keys+['from_keys'],[self.txts[v[0]]['txt'],v[1]]+[self.txts[v[0]][k] for k in return_keys]+[['all_keys']])) 
                    for v in id_score_pairs[:topk]]

        return return_pairs



