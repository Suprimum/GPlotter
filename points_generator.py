
import numpy as np
from math import *

MAX = 20
MIN = -20
STEP = 0.1

MIN3D = 0
MAX3D = 10
STEP3D = 0.1


class Points():
	def __init__(self,eqtn,eqtn_type):
		self.eqtn = eqtn
		self.eqtn_type = eqtn_type

		self.cart_coord = {
					'x_values':None,
					'y_values':None,
					'error': False
		}
		self.polar_coord = {
				't_values': None,
				'r_values': None,
				'error': False
		}
		self.cart3d_coord = {
					'x_values':None,
					'y_values':None,
					'z_values':None,
					'error': False
		}

	def get_etype(self):
		return self.eqtn_type

	def get_eqtn(self):
		return self.eqtn

	def generate_polar_points(self):
		dep = None
		try:
			dep = self.eqtn[0]
		except:
			self.polar_coord['error']=True
			return self.polar_coord

		if dep == 'r':
			eqt = self.eqtn.replace('t','({t})')
			r = []
			self.t_values = np.arange(0,(4*np.pi),0.1)
			self.r_values = None

			try:
				eqt = eqt[eqt.index('=')+1:]
				for tVal in self.t_values:
					rVal = eval(eqt.format(t=tVal))
					r.append(rVal)

				self.r_values = np.array(r)

				self.polar_coord['r_values']=self.r_values
				self.polar_coord['t_values']=self.t_values
				return self.polar_coord
			except:
				self.polar_coord['error']=True
				return self.polar_coord
		elif dep == 't':
			eqt = self.eqtn.replace('r','({r})')
			t = []
			self.r_values = np.arange(0,10,0.1)
			self.t_values = None

			try:
				eqt = eqt[eqt.index('=')+1:]
				for rVal in self.r_values:
					tVal = eval(eqt.format(r=rVal))
					t.append(tVal)

				self.t_values = np.array(t)

				self.polar_coord['r_values']=self.r_values
				self.polar_coord['t_values']=self.t_values
				return self.polar_coord
			except:
				self.polar_coord['error']=True
				return self.polar_coord

		else:
			self.polar_coord['error']=True
			return self.polar_coord

	def generate_cartessian_points(self):
		dep = None
		try:
			dep = self.eqtn[0]
		except:
			self.cart_coord['error']=True
			return self.cart_coord

		if dep == 'y':
			eqt = self.eqtn.replace('^','**').replace('x','({x})')
			y = []
			self.x_values = np.arange(MIN,MAX,STEP)
			self.y_values = None

			try:
				eqt = eqt[eqt.index('=')+1:]

				for xVal in self.x_values:
					yVal = eval(eqt.format(x=xVal))
					y.append(yVal)

				self.y_values = np.array(y)

				self.cart_coord['y_values']=self.y_values
				self.cart_coord['x_values']=self.x_values
				return self.cart_coord
			except:
				self.cart_coord['error']=True
				return self.cart_coord

		elif dep == 'x':
			eqt = self.eqtn.replace('^','**').replace('y','({y})')
			x = []
			self.y_values = np.arange(MIN,MAX,STEP)
			self.x_values = None

			try:
				eqt = eqt[eqt.index('=')+1:]

				for yVal in self.y_values:
					xVal = eval(eqt.format(y=yVal))
					x.append(xVal)

				self.x_values = np.array(x)

				self.cart_coord['x_values']=self.x_values
				self.cart_coord['y_values']=self.y_values
				return self.cart_coord
			except:
				self.cart_coord['error']=True
				return self.cart_coord
		else:
			self.cart_coord['error']=True
			return self.cart_coord


	def generate_3dsurface_cart_points(self):
		dep = None
		t_values = np.arange(0,10*np.pi,0.1)

		try:
			dep = self.eqtn[0]
		except:
			self.cart3d_coord['error']=True
			return self.cart3d_coord

		if dep == 'y':
			eqt = self.eqtn.replace('^','**').replace('x','({x})').replace('z','({z})').replace('t','({t})')
			y = []
			self.z_values = self.x_values = np.arange(MIN3D,MAX3D,STEP3D)
			self.y_values = None

			try:
				eqt = eqt[eqt.index('=')+1:]

				for xVal,zVal,tVal in zip(self.x_values,self.z_values,t_values):
					yVal = eval(eqt.format(x=xVal,z=zVal,t=tVal))
					y.append(yVal)

				self.y_values = np.array(y)

				self.cart3d_coord['x_values'],self.cart3d_coord['z_values'] = np.meshgrid(self.x_values,self.z_values)
				self.cart3d_coord['x_values'],self.cart3d_coord['y_values'] = np.meshgrid(self.x_values,self.y_values)
				return self.cart3d_coord
			except:
				self.cart3d_coord['error']=True
				return self.cart3d_coord

		elif dep == 'x':
			eqt = self.eqtn.replace('^','**').replace('y','({y})').replace('z','({z})').replace('t','({t})')
			x = []
			self.z_values = self.y_values = np.arange(MIN3D,MAX3D,STEP3D)
			self.x_values = None

			try:
				eqt = eqt[eqt.index('=')+1:]

				for yVal,zVal,tVal in zip(self.y_values,self.z_values,t_values):
					xVal = eval(eqt.format(y=yVal,z=zVal,t=tVal))
					x.append(xVal)

				self.x_values = np.array(x)

				self.cart3d_coord['x_values'],self.cart3d_coord['y_values']=np.meshgrid(self.x_values,self.y_values)
				self.cart3d_coord['z_values'],self.cart3d_coord['y_values']=np.meshgrid(self.z_values,self.y_values)
				return self.cart3d_coord
			except:
				self.cart3d_coord['error']=True
				return self.cart3d_coord

		elif dep == 'z':
			eqt = self.eqtn.replace('^','**').replace('y','({y})').replace('x','({x})').replace('t','({t})')
			z = []
			self.y_values = self.x_values = np.arange(MIN3D,MAX3D,STEP3D)
			self.z_values = None

			try:
				eqt = eqt[eqt.index('=')+1:]

				for xVal,yVal,tVal in zip(self.x_values,self.y_values,t_values):
					zVal = eval(eqt.format(y=yVal,x=xVal,t=tVal))
					z.append(zVal)

				self.z_values = np.array(z)

				self.cart3d_coord['x_values'],self.cart3d_coord['y_values']=np.meshgrid(self.x_values,self.y_values)
				self.cart3d_coord['z_values'],self.cart3d_coord['y_values']=np.meshgrid(self.z_values,self.y_values)
				return self.cart3d_coord
			except:
				self.cart3d_coord['error']=True
				return self.cart3d_coord

		elif dep == 'p':
			t_values,f_values = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
			eqt = self.eqtn.replace('t','({t})').replace('f','({f})')
			x = []
			y = []
			z = []

			try:
				eqt = eqt[eqt.index('=')+1:]
				p=eval(eqt)

				xVals = p*np.sin(f_values)*np.cos(t_values)
				yVals = p*np.sin(f_values)*np.sin(t_values)
				zVals = p*np.cos(f_values)

				self.cart3d_coord['x_values'] = xVals
				self.cart3d_coord['y_values'] = yVals
				self.cart3d_coord['z_values'] = zVals

				return self.cart3d_coord
			except:
				self.cart3d_coord['error']=True
				raise
				return self.cart3d_coord
		elif dep == 'r':
			eqt = self.eqtn.replace('t','({t})').replace('f','({f})')
			x = []
			y = []
			z = []

			try:
				eqt = eqt[eqt.index('=')+1:]

				r=eval(eqt.format(t=2*np.pi))
				t_values,f_values = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
				h = np.arange(0,200,20) # divide the height 1 into 20 parts
				x = np.outer(r*np.sin(t_values), np.ones(len(h))) # x value repeated 20 times
				y = np.outer(r*np.cos(t_values),np.ones(len(h))) # y value repeated 20 times
				z = np.outer(np.ones(len(x)),h) # x,y corresponding height


				self.cart3d_coord['x_values'] = x
				self.cart3d_coord['y_values'] = y
				self.cart3d_coord['z_values'] = z

				return self.cart3d_coord
			except:
				self.cart3d_coord['error']=True
				raise
				return self.cart3d_coord
		else:
			self.cart3d_coord['error']=True
			return self.cart3d_coord
'''
if __name__ == '__main__':
	eqt = input ('eqt: ')

	values = Points(eqt,'linear')
	print (values.generate_linear_points())


		grad_b = self.eqtn.index('=')+1
		grad_e = self.eqtn.index('x')
		grad = self.eqtn[grad_b:grad_e]
		if not grad:
			grad = 1
		elif grad == '-':
			grad = -1

		const_b = grad_e+2
		const = None
		try:
			const = int(self.eqtn[const_b:])
		except:
			const = 0

		opr = None
		compute = None
		try:
			opr = self.eqtn[grad_e+1]
			compute = '{}*{}{}{}'
		except:
			opr = None
			compute = '{}*{}'

		y = []

		if opr == '+':
			for x in x_values:
				value = eval(compute.format(grad,x,'+',const))
				y.append(value)
		if opr == '-':
			for x in self.x_values:
				value = eval(compute.format(grad,x,'-',const))
				y.append(value)
		elif opr == None:
			for x in self.x_values:
				value = eval(compute.format(grad,x))
				y.append(value)

x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color="r")

'''