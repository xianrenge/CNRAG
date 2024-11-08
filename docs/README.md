
## rag常见问题

跨文档聚合信息需求

询问大文档的某个点

如何决定是否需要检索外部知识

如何判断自身不会的问题或知识



  多跳推理（multi-hop reasoning）  
“_What name was given to the son of the man who defeated the usurper Allectus?_”
  联系不同信息片段全面回答问题  


缺点和问题：  
数据表示局限：现有方法大多依赖扁平数据表示，这种方式难以捕捉实体之间复杂的关系信息。例如，在处理涉及多个相关实体且关系复杂的查询时，无法深入理解实体间的内在联系，从而限制了信息检索的准确性和全面性。  
上下文连贯性差：这些系统往往缺乏足够的上下文感知能力。当面对涉及多个实体及其相互关系的查询时，难以保持回答的连贯性，导致生成的回答可能无法完全满足用户的查询需求，无法提供一个完整、逻辑连贯的解决方案。  
知识更新困难：部分现有方法在知识图的动态更新和扩展方面存在不足。随着新知识的不断产生，系统难以有效地将新信息纳入到已有的知识结构中，导致知识的时效性和完整性受到影响，无法及时为用户提供最新的准确信息。  
检索效率不足：对于大规模查询，一些现有方法采用的检索方式效率较低，例如可能依赖暴力搜索。这种方式在处理大量数据时，会消耗过多的计算资源和时间，导致检索速度慢，无法满足实时性要求较高的应用场景。  


## 技术汇总
GraphRag  

https://github.com/microsoft/graphrag

参考：https://xie.infoq.cn/article/18ca7cd7702fc0f03baa02b01
一种通过整合知识图谱来增强 RAG 技术的创新方法。  
GraphRAG 非常适合处理复杂任务，如多跳推理（multi-hop reasoning）和联系不同信息片段全面回答问题等。  

两个基本过程：索引和查询。  
索引：即知识图谱相关流程，另外，层次聚类、Community 摘要  
查询：  
  全局搜索：通过利用 Community 摘要  
  本地搜索：特定 Entity 的邻居和相关概念  



LightRAG
https://github.com/HKUDS/LightRAG
https://www.jiqizhixin.com/articles/2024-10-14-2
结合了图结构与双层检索机制，显著降低了大模型检索增强的成本，提升了信息检索的准确性和效率。  
（大体上和GraphRag类似）  
首先，通过引入图结构，LightRAG能够更好地捕捉实体之间的复杂依赖关系，实现全面的信息理解。  
其次，其双层检索策略允许系统同时处理具体和抽象的查询，确保用户获得既相关又丰富的响应。  
此外，LightRAG具备快速适应新数据的能力，使其在动态环境中保持高效和准确。  






### 评估

RAGChecker    
链接：https://www.zhihu.com/question/648008556/answer/3600495692  

特点：  
全面评估：RAGChecker提供整体指标，用于评估整个RAG流程。  
诊断指标：用于分析检索组件的诊断检索器指标。用于评估生成组件的诊断生成器指标。这些指标为针对性改进提供了有价值的见解。  
细粒度评估：利用声明级别的蕴含操作进行细粒度评估。  
基准数据集：一个包含4000个问题、涵盖10个领域的全面的RAG基准数据集（即将推出）。  
元评估：一个用于评估RAGChecker结果与人类判断相关性的人工标注偏好数据集。  



