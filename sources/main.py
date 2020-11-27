#!/usr/binpython3.8


if __name__ == '__main__':
	from  layout import View
	import tkinter as tk
	import os


	app = View()
	app.title('GPlotter')
	if os.name == 'posix':
		icon = tk.PhotoImage(file='gplotter.png')
		app.iconphoto(False,icon)
	else:
		app.iconbitmap('gloptter.ico')
	app.mainloop()



