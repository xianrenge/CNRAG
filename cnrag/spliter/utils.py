# 文本切分


import re
from nltk.tokenize import sent_tokenize



# 按固定长度分块
def split_by_length(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# 按段落分块(根据换行符)
def split_by_paragraph(text,sep='\n\n'):
    return text.split(sep)

# 按句子分块
def split_by_sentence(text):
    return re.split('[。.!！?？\n]+', text)

# 按语义分块
def split_by_semantic(text):
    return sent_tokenize(text)

# 重叠分块
def split_with_overlap(text, chunk_size=1000, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end > len(text):
            end = len(text)
        chunks.append(text[start:end])
        start = end - overlap
    return chunks



def split_text(text, split_chars=['\n\n', '\n', '。'], block_size=500, overlap=100):
    # 存储最终的分块结果
    chunks = []
    
    # 按优先级最高的分隔符进行初次切分
    initial_splits = text.split(split_chars[0])
    
    current_chunk = ""
    remaining = ""
    
    for i, split in enumerate(initial_splits):
        # 如果当前分块为空,直接赋值
        if not current_chunk:
            current_chunk = split
            continue
            
        # 如果当前分块+新分块小于块大小,则继续拼接
        if len(current_chunk + split_chars[0] + split) <= block_size:
            current_chunk += split_chars[0] + split
            continue
            
        # 如果当前分块大于块大小,需要用低优先级分隔符再次切分
        if len(current_chunk) > block_size:
            sub_chunks = recursive_split(current_chunk, split_chars[1:], block_size)
            # 处理子分块
            for sub in sub_chunks:
                if len(sub) <= block_size:
                    chunks.append(sub)
                
        # 如果当前分块小于块大小,需要从后续文本拼接
        elif len(current_chunk) < block_size:
            # 拼接后续文本直到超过块大小
            j = i
            while j < len(initial_splits) and len(current_chunk) < block_size:
                next_split = initial_splits[j]
                if len(current_chunk + split_chars[0] + next_split) <= block_size:
                    current_chunk += split_chars[0] + next_split
                    j += 1
                else:
                    break
            
            chunks.append(current_chunk)
            
            # 保持overlap的重叠
            if len(current_chunk) >= overlap:
                current_chunk = current_chunk[-overlap:]
            else:
                current_chunk = ""
                
        # 重置当前分块
        current_chunk = split
    
    # 处理最后剩余的文本
    if current_chunk:
        if len(current_chunk) > block_size:
            sub_chunks = recursive_split(current_chunk, split_chars[1:], block_size) 
            chunks.extend(sub_chunks)
        else:
            chunks.append(current_chunk)
            
    return chunks

def recursive_split(text, split_chars, block_size):
    """递归使用低优先级分隔符切分文本"""
    if not split_chars:
        return [text]
        
    splits = text.split(split_chars[0])
    chunks = []
    current = splits[0]
    
    for split in splits[1:]:
        if len(current + split_chars[0] + split) <= block_size:
            current += split_chars[0] + split
        else:
            if len(current) > block_size and len(split_chars) > 1:
                # 继续用更低优先级分隔符切分
                sub_chunks = recursive_split(current, split_chars[1:], block_size)
                chunks.extend(sub_chunks)
            else:
                chunks.append(current)
            current = split
            
    if current:
        if len(current) > block_size and len(split_chars) > 1:
            sub_chunks = recursive_split(current, split_chars[1:], block_size)
            chunks.extend(sub_chunks)
        else:
            chunks.append(current)
            
    return chunks
text = "这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。1\n\n这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。2\n这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。3\n\n\n这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。4\n\n00这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。1\n\n这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。2\n这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。3\n\n\n这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。4\n\n001122这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。1\n\n这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。2\n这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。3\n\n\n这是一个用于测试的文本。它包含多个句子。我们将尝试将其切分成多个块。每个块的大小应控制在一定范围内。4"
split_text(text)
