# 前端展示

import gradio as gr


def clear_text(text):
    # 这个函数返回一个空字符串，以清空文本框
    return ""

def get_general_chat_his(log,model_name):
    # f_w='history/general_chat_log.txt'
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d_%H_%M_%S")
    f_w='history/chat_log_%s_%s.txt' % (model_name,dt)
    with open(f_w,'w',encoding='utf-8') as f:
        for h in log:
            f.write('用户：'+h[0].strip())
            f.write('\n')
            f.write('AI：'+h[1].strip())
            f.write('\n')
    return f_w



class WebUi:
	def __init__(self,app=None,web_type='base',web_apps=[]):
		'''
		web_fns:产生gr模块的函数及对应网址名称，如[[fn,url_name],]
		'''
		self.app=app
		self.apps=web_apps

	def add_web_fns(self,app_one=[]):
		if len(app_one)!=2:
			raise 'app_one format error!!!'
		self.apps.append(app_one)

	def launch(self,share=False,server_name='0.0.0.0',server_port='8000',debug=False,enable_queue=False,auth=None):
		'''
			share (bool, default=False)：
			如果设置为 True，Gradio 会生成一个可公开访问的共享链接。
			server_name (str, default="0.0.0.0")：
			指定服务器的主机名，通常设置为 "0.0.0.0" 以允许外部访问。
			server_port (int, default=7860)：
			指定应用运行的端口，可以更改为任何未被占用的端口。
			debug (bool, default=False)：
			如果设置为 True，将在调试模式下启动，提供更多的错误信息。
			enable_queue (bool, default=False)：
			当启用时，Gradio 会在多次请求时使用队列，适合处理长时间运行的任务。
			auth (list of tuples, default=None)：
			用于设置基本身份验证，格式为 [(username1, password1), (username2, password2)]。
		'''
		self.app.launch(share,server_name,server_port,debug,enable_queue,auth)

	def launch_url(self):
		for a in self.apps:
			self.app = gr.mount_gradio_app(self.app, a[0], path=a[1])





# 普通的对话前端
class ChatWeb(WebUi):

	def create_ui(self,dd_model_list=[],dis_txts=[]):
	    with gr.Blocks(title='AI助手') as demo:
	    	if dd_model_list:
		        with gr.Row():
		            model_dd = gr.Dropdown(dd_model_list,label='选择模型')
		    else:
		    	model_dd=''
	        with gr.Row():
	            chatbox = gr.Chatbot(placeholder="......")
	        with gr.Row():
	            with gr.Column(scale=2):
	                message_input = gr.Textbox(placeholder="输入你的消息...",lines=6,label='输入')
	                txt_dis = gr.Textbox(value='\n'.join(dis_txts),lines=4,interactive=False,label='常用语')
	            with gr.Column(scale=1):
	                send_button = gr.Button("发送")
	                down_button = gr.Button("汇总对话记录")
	                down_fl=gr.File(label="下载")
	            
	        def update_chat(log, text,modelname):
	            # print(text,modelname)
	            response = send_message_test_v2("psy_v2", text,log,modelname)
	            log.append((text, response))
	            return log
	        

	        send_button.click(update_chat, inputs=[chatbox, message_input,model_dd], outputs=chatbox)
	        send_button.click(fn=clear_text, inputs=message_input, outputs=message_input)
	        down_button.click(fn=get_general_chat_his,inputs=[chatbox,model_dd],outputs=down_fl)

	    self.app = demo
