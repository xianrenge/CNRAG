# CNRAG
RAG的中文实现方案


## 更新日志
2024年11月6日 新增v1.0基础版本


## 说明
### 概述

此库主要目标是方便安装并高效使用，使用尽量少但可能会遇到让人头疼的第三方库
但仍然会支持目前主流的高阶方法

### 数据
送入vector库中的数据，需要标准化，如[{'index':0,'txt':'...'},]，其中index为默认的索引id，txt为默认进行向量化的字段

### rag流程
大致的主要流程如下：
1.先处理好数据
2.数据切分
3.向量化
4.检索
5.结果过滤

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
