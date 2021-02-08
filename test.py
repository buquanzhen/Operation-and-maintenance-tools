from tkinter import *
def cut(editor, event=None):
    editor.event_generate("<<Cut>>")
def copy(editor, event=None):
    editor.event_generate("<<Copy>>")
def paste(editor, event=None):
    editor.event_generate('<<Paste>>')
def rightKey(event, editor):
    menubar.delete(0,END)
    menubar.add_command(label='剪切',command=lambda:cut(editor))
    menubar.add_command(label='复制',command=lambda:copy(editor))
    menubar.add_command(label='粘贴',command=lambda:paste(editor))
    menubar.post(event.x_root,event.y_root)

if __name__=='__main__':
    root=Tk()
    menubar = Menu(root,tearoff=False)#创建一个菜单
	#以Entry为例，Text对象完全一样。
    ent=Text(root)
    ent.pack()
    ent.bind("<Button-3>", lambda x: rightKey(x, ent))#绑定右键鼠标事件
    root.mainloop()