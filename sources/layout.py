#!/usr/bin/python3.8


import gplot
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mimetypes

class View(tk.Tk):
	def __init__(self):
		super().__init__()

		self.frame1 = tk.Frame(self)
		self.list_frame = tk.Frame(self.frame1,borderwidth=2,bg='#fff',width=150,height=400)
		self.canvas = tk.Canvas(self.frame1)
		self.frame2 = tk.Frame(self)

		l = ['Cartessian plots','Polar plots','3D cartessian plots']

		list_objs = []
		for i in range(len(l)):
			list_objs.append(gplot.ListFrame(master=self.list_frame,text=l[i],
					bg='#fff',width=150,height=400,)
				)

		self.input = gplot.InputFrame(self.frame2,list_objs,self.canvas)
		self.logo = tk.Label(self,text="Copyright {} 2020 SuperPosition Inv.".format(chr(61402)))


		menu = tk.Menu(self)
		filemenu = tk.Menu(menu,tearoff=0)
		editmenu = tk.Menu(menu,tearoff=0)
		aboutmenu = tk.Menu(menu,tearoff=0)

		submenu = tk.Menu(editmenu,tearoff=0)
		submenu.add_command(label='cartessian',command=self.new_cart_frame)
		submenu.add_command(label='polar',command=self.new_polar_frame)
		submenu.add_command(label='3d',command=self.new_3d_frame)

		filemenu.add_command(label='save as png',command=self.save_png)
		filemenu.add_separator()
		filemenu.add_command(label='close %s'%chr(62163),command=self.close)

		editmenu.add_cascade(label='coordinate frame',menu=submenu)
		editmenu.add_separator()
		editmenu.add_command(label='clear')
		editmenu.add_checkbutton(label='grid',variable=self.input.grid_var,onvalue=True,offvalue=False,command=self.toggle_grid)

		aboutmenu.add_command(label='Help %s'%chr(61529))
		aboutmenu.add_command(label='About Gplotter %s'%chr(61530))

		menu.add_cascade(label='file',menu=filemenu)
		menu.add_separator()
		menu.add_cascade(label='edit',menu=editmenu)
		menu.add_cascade(label='about',menu=aboutmenu)
		self.config(menu=menu)

		self.input.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
		self.list_frame.pack(side=tk.LEFT,anchor=tk.NW,expand=True,fill=tk.BOTH,padx=10)
		self.canvas.pack(side=tk.LEFT,anchor=tk.NW,expand=True,fill=tk.BOTH,padx=10)
		self.frame2.pack(anchor=tk.N,pady=10,ipady=5)
		self.frame1.pack(anchor=tk.NW)
		self.logo.pack(anchor=tk.S,pady=10)

		self.update_idletasks()

		self.wm_minsize(height=self.winfo_height()+20,width=self.winfo_width()+20)
	def close(self):
		res = mb.askquestion('close window','Are you sure you want to quit program?')
		if res == 'yes':
			self.quit()
		else:
			pass
	def new_cart_frame(self):
		self.input.set_coord('cartessian')
	def new_polar_frame(self):
		self.input.set_coord('polar')
	def new_3d_frame(self):
		self.input.set_coord('3d')

	def save_png(self):
		allftys = tuple(map(lambda t:tuple(reversed(t)),list(mimetypes.types_map.items())))
		imgftys = []
		for item in allftys:
			if 'image' in item[0]:
				imgftys.append(item)

		fname = fd.asksaveasfilename(title='save figure',filetypes=tuple(imgftys[6:]),defaultextension='.png')
		if fname:
			curfig = self.input.get_cur_fig()
			curfig.figure().savefig(fname)

	def toggle_grid(self):
		is_on = not self.input.grid_var.get()
		etype = self.input.get_eqt_type()

		if etype == 'cartessian':
			if is_on:
				self.input.cart_fig.axes().grid(False)
				self.input.cart_fig.figure().canvas.draw()
			else:
				self.input.cart_fig.axes().grid(True)
				self.input.cart_fig.figure().canvas.draw()
		elif etype == 'polar':
			if is_on:
				self.input.polar_fig.axes().grid(False)
				self.input.polar_fig.figure().canvas.draw()
			else:
				self.input.polar_fig.axes().grid(True)
				self.input.polar_fig.figure().canvas.draw()
		elif etype == '3d':
			if is_on:
				self.input.cart3d_fig.axes().grid(False)
				self.input.cart3d_fig.figure().canvas.draw()
			else:
				self.input.cart3d_fig.axes().grid(True)
				self.input.cart3d_fig.figure().canvas.draw()



'''
if __name__ == '__main__':
	app = View()
	app.mainloop()
'''