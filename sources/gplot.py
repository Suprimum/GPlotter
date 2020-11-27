#!/usr/bin/python3.8

import tkinter as tk
import tkinter.ttk as ttk
import re, math
import points_generator as pgen

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import MaxNLocator
#import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from mpl_toolkits import mplot3d #3d module

eqt_type = ['cartessian','polar','3d']

algebraic_pattern = re.compile('^y?x?=?(\w*\(*-?\d*\.?\d*\*?x?\^?\d?[+-]?\d*\.?\d*\*?x?[+-]?\d*\.?\d*\)*)*/?(\w*\(*-?\d*\.?\d*\*?x?\^?\d?[+-]?\d*\.?\d*\*?x?[+-]?\d*\.?\d*\)*)*$')
polar_pattern = re.compile('^r?\^?\d*t?=?(\d*\^?\d*\.?\d*\^?\d*[+-]?\d*\^?\d*\.?\d*\^?\d*\*?\w*/?\(?t?\)?)*\^?\d*[+-]?(\d*\^?\d*\.?\d*\^?\d*[+-]?\d*\^?\d*\.?\d*\^?\d*\*?\w*/?\(?t?\)?)*\^?\d*$')
algebraic3d_pattern = re.compile('^y?\^?\d*\.?\d*x?\^?\d*\.?\d*z?\^?\d*\.?\d*r?p?=?(\w*\(*-?\d*\.?\d*\*?x?\^?\d?/*[+-]?\d*\.?\d*\*?x?[+-]?\d*\.?\d*\)*)*/?(\w*\(*-?\d*\.?\d*\*?x?\^?\d?[+-]?\d*\.?\d*\*?x?[+-]?\d*\.?\d*\)*)*$')

class GraphFig:
	def __init__(self,coord):
		self.fig = Figure(figsize=(10,4),dpi=100)
		self.coord = coord
		#plt.ion() #turn on interactive mode. use it to interactively modify plots

		self.plots = []
		self.cplot_dict = {}
		self.pplot_dict = {}
		self.c3dplot_dict = {}
		self.ax = None
		self.loc = "upper right"
		self.anchor = (1.2,1.1)

	def add_cart_plot(self,xpoints,ypoints,name):
		self.set_cart_axis()
		#plot points
		line = self.ax.plot(xpoints,ypoints)
		self.cplot_dict[name]=line[-1]
		return line

	def set_cart_axis(self):
		self.ax = self.fig.add_subplot(111,projection='rectilinear')

		#modify graph scale
		self.ax.set_xlim(-10,10)
		self.ax.set_ylim(-10,10)

		#centralize axis
		self.ax.spines['left'].set_position('center') #remove left border
		self.ax.spines['bottom'].set_position('center') #remove bottom border
		self.ax.spines['right'].set_color('none')
		self.ax.spines['top'].set_color('none')
		self.ax.xaxis.set_ticks_position('bottom')
		self.ax.yaxis.set_ticks_position('left')
		self.ax.yaxis.set_major_locator(MaxNLocator(prune='lower'))
		self.ax.xaxis.set_major_locator(MaxNLocator(prune='lower'))
		self.ax.grid(True)

	def add_polar_plot(self,theta,r,name):
		self.set_polar_axis()
		curve = self.ax.plot(theta,r)
		self.pplot_dict[name]=curve[-1]
		return curve

	def set_polar_axis(self):
		rticks = list(range(0,11,2))
		self.ax = self.fig.add_subplot(111,projection='polar')
		self.ax.set_rmax(10.0)
		self.ax.set_rticks(rticks)

		self.ax.set_rlim(-10,10)
		self.ax.set_theta_zero_location('E')
		self.ax.set_theta_direction(1)

	def add_3d_surface_plot(self,x,y,z,name):
		self.set_3d_axis()

		wf = self.ax.plot_wireframe(x,y,z)
		surf = self.ax.plot_surface(x,y,z,rstride=1,cstride=1,edgecolor='none',cmap='jet')
		self.c3dplot_dict[name]=(surf,wf)

		return surf

	def add_3d_cart_plot(self,x,y,z,name):
		self.set_3d_axis()

		line3d = self.ax.plot3D(x,y,z)
		self.c3dplot_dict[name] = (line3d,None)

		return line3d

	def set_3d_axis(self):
		self.ax = self.fig.add_subplot(111,projection='3d')
		self.ax.set_xlabel('x')
		self.ax.set_ylabel('y')
		self.ax.set_zlabel('z')

		#self.ax.mouse_init()
		#self.ax.axes.set_xlim3d(left=0,right=10)
		#self.ax.axes.set_ylim3d(left=0,right=10)
		#self.ax.axes.set_zlim3d(left=0,right=10)

	def add_legend(self,name,anchor=None):
		self.plots.append(name)
		self.fig.legends = [] #clear legend list
		self.fig.legend(self.plots,loc=self.loc)

	def pop_legend(self,name):
		index = self.plots.index(name)
		self.plots.pop(index)
		self.fig.legends = [] #clear legend list
		self.fig.legend(self.plots,loc=self.loc) #update the legend

	def figure(self):
		return self.fig

	def axes(self):
		return self.ax

	def get_coord(self):
		return self.coord

class CheckB(tk.Checkbutton):
	def __init__(self,master,var,line_obj,canvas,fig):
		super().__init__(master,onvalue=True,offvalue=False,variable=var,bg='#fff')

		self.var = var
		self.line_obj = line_obj
		self.canvas = canvas
		self.fig = fig

		self.bind("<Button-1>",self.on_but1)

	def fig_lines(self,lines):
		self.lines = lines

	def render(self,state):
		#edit plot as required
		self.line_obj.set_visible(state)
		#update the plot
		self.fig.canvas.draw()

	def on_but1(self,event):
		visible = self.var.get()
		if visible:
			self.render(False)
		else:
			self.render(True)

class CloseLabel(tk.Label):
	def __init__(self,eqt,root,inp,canvas,**args):
		super().__init__(**args,bg='#fff')

		self.eqt = eqt
		self.root = root #its master <list frame>
		self.canvas = canvas
		self.input = inp

		self.bind("<Button-1>",self.remove)

	def remove(self,event):
		if (self.input.get_eqt_type() == 'cartessian') and (self.root.fig.get_coord() == 'cartessian'):
			#remove its list item
			check,label,cls = self.root.triple.pop(self.eqt)
			check.grid_forget()
			label.grid_forget()
			cls.grid_forget()
			#remove the drawing
			line = self.root.fig.cplot_dict.pop(self.eqt)
			line.remove()
			self.root.fig.pop_legend(self.eqt)
			self.root.fig.figure().canvas.draw()

		elif (self.input.get_eqt_type() == 'polar') and (self.root.fig.get_coord() == 'polar'):
			#remove its list item
			check,label,cls = self.root.triple.pop(self.eqt)
			check.grid_forget()
			label.grid_forget()
			cls.grid_forget()
			#remove the drawing
			curve = self.root.fig.pplot_dict.pop(self.eqt)
			curve.remove()
			self.root.fig.pop_legend(self.eqt)
			self.root.fig.figure().canvas.draw()

		elif (self.input.get_eqt_type() == '3d') and (self.root.fig.get_coord() == '3d'):
			#remove its list item
			check,label,cls = self.root.triple.pop(self.eqt)
			check.grid_forget()
			label.grid_forget()
			cls.grid_forget()
			#remove the drawing
			surf = self.root.fig.c3dplot_dict.pop(self.eqt)
			for obj in surf:
				obj.remove()
			self.root.fig.pop_legend(self.eqt)
			self.root.fig.figure().canvas.draw()



class ListFrame(tk.LabelFrame):
	def __init__(self,**args):
		super().__init__(**args)
		self.triple = {}
		self.pack()
		self.fig=None

	def set_fig(self,fig):
		self.fig = fig

	def update(self):
		for i, p in enumerate(list(self.triple.values())):
			p[0].grid(row=i,column=0)
			p[1].grid(row=i,column=1)
			p[2].grid(row=i,column=2)

	def add_item(self,data,line_obj=None,canvas=None,fig=None):
		var = tk.BooleanVar()
		var.set(True)
		check = CheckB(self,var,line_obj,canvas,fig)
		label = tk.Label(self,text=data,bg='#fff')
		cls_but = CloseLabel(data,self,self.input,canvas,master=self,text='{}'.format(chr(62163)),fg='#f00')

		label.bind("<Double-Button-1>",(lambda event:self.input.input_var.set(data)))
		self.triple[data]=(check,label,cls_but)
		self.update()

	def get_item(self,index):
		if index in enumerate(self.triple):
			return self.triple[index]
		else:
			return False
	def set_input_source(self,inp):
		self.input = inp

class ComboBox(ttk.Combobox):
	def __init__(self,**args):
		super().__init__(**args)

		self.event_add("<<ComboClicked>>","<Button-1>")
		self.event_add("<<ComboValueChanged>>","<FocusIn>")
		#self.bind("<<ComboClicked>>",self.on_combo_clicked)

class InputFrame(tk.Frame):
	def __init__(self,master,list_objs=None,canvas=None):
		super().__init__(master)

		self.points_dict = None
		self.error = tk.Label(self)

		self.cart_list_obj, self.polar_list_obj, self.cart3d_list_obj = list_objs

		self.canvas = canvas
		#create a figure for unique coordinate systems
		self.cart_fig = GraphFig('cartessian')
		self.polar_fig = GraphFig('polar')
		self.cart3d_fig = GraphFig('3d')

		self.cart_list_obj.set_fig(self.cart_fig)
		self.polar_list_obj.set_fig(self.polar_fig)
		self.cart3d_list_obj.set_fig(self.cart3d_fig)

		self.cart_list_obj.set_input_source(self)
		self.polar_list_obj.set_input_source(self)
		self.cart3d_list_obj.set_input_source(self)

		#set default coordinate axis
		tkplot = self.draw_plot(self.canvas,self.cart_fig)
		self.cart_fig.set_cart_axis()
		tkplot.pack()

		self.input_var = tk.StringVar()
		#self.input_var.set('')
		self.vcmd = (self.register(self.validate_input),"%P")
		self.combo_var = tk.StringVar()
		#self.combo = ComboBox(master=self,textvariable=self.combo_var,values=eqt_type)
		self.cur_var = None
		#self.combo.set('cartessian')
		#self.combo.bind("<<ComboClicked>>",self.on_combo_clicked)

		self.input = tk.Entry(self,validate='key',textvariable=self.input_var,vcmd=self.vcmd)
		self.input.focus_set()

		self.label = tk.Label(self,text='Enter equation:')
		self.eframe = tk.Label(self,text='cartessian')

		self.grid_var = tk.BooleanVar()
		self.grid_var.set(True)

		self.label.pack(side=tk.LEFT)
		self.input.pack(side=tk.LEFT)
		#self.combo.pack(side=tk.LEFT)
		self.error.pack(side=tk.LEFT)
		#self.grid.pack(side=tk.LEFT,padx=20)
		self.eframe.pack(side=tk.RIGHT,padx=60)
		self.cart_list_obj.pack(side=tk.LEFT,anchor=tk.NW,expand=True,fill=tk.BOTH,padx=10)
		self.polar_list_obj.pack_forget()
		self.cart3d_list_obj.pack_forget()

		self.input.bind("<Key-Return>",self.on_return)
		#self.grid.bind("<Button-1>",self.toggle_grid)

	def on_combo_clicked(self,event):
		self.cur_val = self.combo.get()
		self.combo.bind("<<ComboValueChanged>>",self.on_combo_value_changed)

	def on_combo_value_changed(self,event):
		new_val = self.combo.get()
		if self.cur_val == new_val:
			pass
		elif self.cur_val != new_val:
			self.set_coord(new_val)

	def set_coord(self,val):
		self.clear_canvas()
		if val == 'polar':
			tkplot = self.draw_plot(self.canvas,self.polar_fig)
			self.polar_fig.set_polar_axis()
			tkplot.pack()
			self.polar_list_obj.pack(side=tk.LEFT,anchor=tk.NW,expand=True,fill=tk.BOTH,padx=10)
			self.cart_list_obj.pack_forget()
			self.cart3d_list_obj.pack_forget()
			self.eframe.config(text='polar')
		elif val == 'cartessian':
			tkplot = self.draw_plot(self.canvas,self.cart_fig)
			self.cart_fig.set_cart_axis()
			tkplot.pack()
			self.cart_list_obj.pack(side=tk.LEFT,anchor=tk.NW,expand=True,fill=tk.BOTH,padx=10)
			self.polar_list_obj.pack_forget()
			self.cart3d_list_obj.pack_forget()
			self.eframe.config(text='cartessian')
		elif val == '3d':
			tkplot = self.draw_plot(self.canvas,self.cart3d_fig)
			self.cart3d_fig.set_3d_axis()
			tkplot.pack()
			self.cart3d_list_obj.pack(side=tk.LEFT,anchor=tk.NW,expand=True,fill=tk.BOTH,padx=10)
			self.polar_list_obj.pack_forget()
			self.cart_list_obj.pack_forget()
			self.eframe.config(text='3d')


	def toggle_grid(self,event):
		is_on = self.grid_var.get()
		if self.get_eqt_type() == 'cartessian':
			if is_on:
				self.cart_fig.axes().grid(False)
				self.cart_fig.figure().canvas.draw()
			else:
				self.cart_fig.axes().grid(True)
				self.cart_fig.figure().canvas.draw()
		elif self.get_eqt_type() == 'polar':
			if is_on:
				self.polar_fig.axes().grid(False)
				self.polar_fig.figure().canvas.draw()
			else:
				self.polar_fig.axes().grid(True)
				self.polar_fig.figure().canvas.draw()
		elif self.get_eqt_type() == '3d':
			if is_on:
				self.cart3d_fig.axes().grid(False)
				self.cart3d_fig.figure().canvas.draw()
			else:
				self.cart3d_fig.axes().grid(True)
				self.cart3d_fig.figure().canvas.draw()


	def get_eqt_type(self):
		return self.eframe.cget('text')

	def validate_input(self,data):

		if not data:
			self.error.config(text='')
			return True

		result = None

		if self.get_eqt_type() == 'cartessian':
			result = algebraic_pattern.match(data)
		elif self.get_eqt_type() == 'polar':
			result = polar_pattern.match(data)
		if self.get_eqt_type() == '3d':
			result = algebraic3d_pattern.match(data)

		if result:
			self.error.config(text='')
			return True
		else:
			self.error.config(text='invalid linear equation')
			return False

	def draw_plot(self,root,fig):
		#draw the figure on the canvas
		canvas_plot = FigureCanvasTkAgg(fig.figure(),master=root)
		canvas_plot.draw()

		nav_bar = NavigationToolbar2Tk(canvas_plot,root)
		nav_bar.update()

		return canvas_plot.get_tk_widget()

	def clear_canvas(self):
		children = list(self.canvas.children.values())
		for child in children:
			child.destroy()

	def get_canvas(self):
		return self.canvas

	def get_cur_fig(self):
		if self.get_eqt_type() == 'cartessian':
			return self.cart_fig
		elif self.get_eqt_type() == 'polar':
			return self.polar_fig
		if self.get_eqt_type() == '3d':
			return self.cart3d_fig


	def compute_plot(self,points_dict,input):
		coord = self.get_eqt_type()
		if coord == 'cartessian':
			tkplot = self.draw_plot(self.canvas,self.cart_fig)
			lines = self.cart_fig.add_cart_plot(points_dict['x_values'],points_dict['y_values'],input)
			self.cart_list_obj.add_item(input,lines[-1],self.canvas,self.cart_fig.figure())
			self.cart_fig.add_legend(input)
			tkplot.pack()
		elif coord == 'polar':
			tkplot = self.draw_plot(self.canvas,self.polar_fig)
			curves = self.polar_fig.add_polar_plot(points_dict['t_values'],points_dict['r_values'],input)
			self.polar_list_obj.add_item(input,curves[-1],self.canvas,self.polar_fig.figure())
			self.polar_fig.add_legend(input,(1.1,1.0))
			tkplot.pack()
		elif coord == '3d':
			tkplot = self.draw_plot(self.canvas,self.cart3d_fig)
			surf = self.cart3d_fig.add_3d_surface_plot(points_dict['x_values'],points_dict['y_values'],points_dict['z_values'],input)
			self.cart3d_list_obj.add_item(input,surf,self.canvas,self.cart3d_fig.figure())
			self.cart3d_fig.add_legend(input,(1.1,1.0))
			tkplot.pack()


	def input_error(self,p,coord):
		if p['error']:
			#an error occured
			if coord == "cartessian":
				self.error.config(text='invalid input syntax',fg='#f00')
				self.draw_plot(self.canvas,self.cart_fig).pack()
				return True
			elif coord == "polar":
				self.error.config(text='invalid input syntax',fg='#f00')
				self.draw_plot(self.canvas,self.polar_fig).pack()
				return True
			elif coord == "3d":
				self.error.config(text='invalid 3d input syntax',fg='#f00')
				self.draw_plot(self.canvas,self.cart3d_fig).pack()
				return True
		else:
			self.error.config(text='',fg='#000')
			return False

	def on_return(self,event):
		#get equation string
		input = self.input_var.get()
		#initialize points generator
		points = pgen.Points(input,self.get_eqt_type())
		#clear the old drawing
		self.clear_canvas()

		#draw the new graph on the same axis

		if points.get_etype() == 'cartessian':
			points_dict = points.generate_cartessian_points()
			if self.input_error(points_dict,'cartessian'):
				return
			self.compute_plot(points_dict,input)

		elif points.get_etype() == 'polar':
			points_dict = points.generate_polar_points()
			if self.input_error(points_dict,'polar'):
				return
			self.compute_plot(points_dict,input)

		elif points.get_etype() == '3d':
			points_dict = points.generate_3dsurface_cart_points()
			if self.input_error(points_dict,'3d'):
				return
			self.compute_plot(points_dict,input)



		self.input.delete(0,tk.END)

