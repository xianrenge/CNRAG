# CNRAG
RAG的中文实现方案  
目标：简洁、高效、易改  


## 更新日志
2024年11月6日 新增v1.0基础版本  


## 说明

### 概述

此库主要目标是方便安装并高效使用，使用尽量少的第三方库，以免遇到让人头疼的bug不易调试  
但仍然会实时跟进并支持目前主流的高阶方法  

### 数据
送入vector库中的数据，需要标准化，如[{'index':0,'txt':'...'},]，其中index为默认的索引id，txt为默认进行向量化的字段  

### rag流程
大致的主要流程如下：  
1.先处理好数据  
2.数据切分+数据增强  
3.向量化+索引  
4.检索  
5.结果过滤+生成模块  


## 示例

### 简短示例
```python
from cnrag.core.runner import SimpleRunner

txts=['今天不开心','世界很美好']
model_dir='/models/m3e-large'
runner=SimpleRunner(txts=txts,model_dir=model_dir)
res=runner.select('明天')
print(res)

```

## 技术收集
相关技术详细情况请参阅docs目录  
GraphRag

## 计划清单TODO
多介质支持（古文、文言文、多语言、图片、语音、方言、视频等）  

图/索引  
语义分块  
微调大模型引擎（is_rag、selfrag、）  
支持前端、api  
第三方数据存储兼容(faiss、)  
具体案例（篮球、足球、财经、、、）

其他：
代理机，sql或元数据筛选，step-back


