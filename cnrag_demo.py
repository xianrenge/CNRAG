
from cnrag.core.prompts import QusetionPrompt

qp=QusetionPrompt()
print(qp)
print(qp.template)

print(qp(txt='qqq',sum='www'))

# print({'txt':'mmm'} | f'some {txt}' )

from cnrag.core.runner import SimpleRunner

txts=['今天不开心','世界很美好']
model_dir='/models/m3e-large'
runner=SimpleRunner(txts=txts,model_dir=model_dir)
res=runner.select('明天')
print(res)
