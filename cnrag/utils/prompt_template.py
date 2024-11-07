# 各种prompt

qusetion_prompt={'input_vars':['txt'],
		'template':'''请对下面的文本进行一个简单的总结。直接输出总结不包含其他解释等内容。

>>>>start<<<<
{txt}
>>>>end<<<<''',
		'out_format':r'(.*)',
		'parse_re':r'(.*)'

	}

query_rewrite_prompt={'input_vars':['txt'],
		'template':'''请对下面的文本进行相同意思的改写。直接输出改写后内容不包含其他解释等内容。

>>>>start<<<<
{txt}
>>>>end<<<<''',
		'out_format':r'(.*)',
		'parse_re':r'(.*)'

	}
