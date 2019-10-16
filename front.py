import imageio
import back as bk
import colors as cl
import fourier as fr
from tkinter import *
from tkinter import ttk, colorchooser
from PIL import ImageTk, Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg") 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os


class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.penwidth = 5
        self.mcanvas = [0]
        self.input = 0
        self.draw = 0
        self.size = [400,400]
        self.img = [0]
        self.orimg = [0]
        self.old_img = [0]
        self.func = None
        self.points = [0,0,0,0,0,0,0,0]
        self.pfuncao = [0,0,0,0]
        self.coorda = [0,0]
        self.coordb = [0,0]
        self.old_red = 0
        self.old_green = 0
        self.old_blue = 0
        self.old_hue = 0
        self.old_sat = 0
        self.old_val = 0
        self.drawWidgets()
        #self.c.bind('<B1-Motion>',self.paint) #evento de movimento do mouse
        self.c.bind('<Button-1>',self.paintdot) #evento quando clica com botão do mouse
        self.c.bind('<ButtonRelease-1>',self.reset) #evento quando soltar o botão do mouse
        self.master.bind('<Control-Key-z>', self.undo) #Control+Z

    def paint(self,e):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)

        self.old_x = e.x
        self.old_y = e.y

    def paintdot(self,e):
        x1, y1 = ( e.x ), ( e.y )
        r = float(self.penwidth)
        r = round(r)
        r = int(r)
        #self.c.create_line(x1,y1,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)
        self.c.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, width=1,fill=self.color_fg,)
        
        self.draw.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=self.color_fg)
        filename = "canvas.jpg"
        self.input.save(filename)

        xx, yy = np.mgrid[:self.size[0], :self.size[1]]
        xcenter = e.x
        ycenter = e.y
        # circles contains the squared distance to the (100, 100) point
        # we are just using the circle equation learnt at school
        circle = (xx - xcenter) ** 2 + (yy - ycenter) ** 2
        # donuts contains 1's and 0's organized in a donut shape
        # you apply 2 thresholds on circle to define the shape
        #mc = np.logical_and(1, circle < (r*100))
        #print(mc)
        for k in range(self.mcanvas.shape[0]):
            for l in range(self.mcanvas.shape[1]):
                if circle[k,l] < (r*100):
                    self.mcanvas[k,l] = cl.rgb2gray_avg(self.old_red,self.old_green,self.old_blue)/255
        print(self.mcanvas)
        #self.mcanvas = np.logical_and(mc, self.mcanvas)
        #print(self.mcanvas)
        #print(self.mcanvas.shape)
        #self.old_x = e.x
        #self.old_y = e.y
        #x1, y1 = ( e.x - 1 ), ( e.y - 1 )
        #x2, y2 = ( e.x + 1 ), ( e.y + 1 )
        #self.c.create_oval( x1, y1, x2, y2, width=self.penwidth,fill=self.color_fg,)

    def reset(self,e):   
        self.old_x = None
        self.old_y = None
        #self.mcanvas  = np.zeros((400,400), dtype=int)

    def save(self):  #salvando
        filename = "canvas.jpg"
        print(np.array(self.input))
        self.input.save(filename)

    def changeW(self,e): #mudar raio do pincel
        self.penwidth = e      

    def clear(self):
        self.c.delete(ALL)
        white = (255, 255, 255)
        self.input = Image.new("RGB", (self.size), white)
        filename = "canvas.jpg"
        self.input.save(filename)
        self.mcanvas = np.ones(self.size)
        print(self.mcanvas)
        print(self.mcanvas.shape)

    def undo(self,e):
        self.c.image = ImageTk.PhotoImage(self.old_img)
        self.size[0] = self.old_img.width
        self.size[1] = self.old_img.height
        self.c.config(width=self.size[0], height=self.size[1])
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        img = self.old_img
        self.old_img = self.img
        self.img = img

    def change_fg(self):  #mudando a cor foreground
        self.color_fg=colorchooser.askcolor(color=self.color_fg)[1]

    def change_bg(self):  #mudando a cor do background
        self.color_bg=colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg

    def changeR(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        cor = '#%02x%02x%02x' % (e, self.old_green, self.old_blue)
        self.colordisplay.itemconfig(self.cordisp, fill=cor)
        self.color_fg = cor
        self.old_red = e
        (h,s,v) = cl.rgb2hsv(e, self.old_green, self.old_blue)
        print(h,s,v)
        self.sliderH.set(h)
        self.old_hue = h
        self.sliderS.set(s)
        self.old_sat = s
        self.sliderV.set(v)
        self.old_val = v
        #self.colordisplay['bg'] = r,g,b
    
    def changeG(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        cor = '#%02x%02x%02x' % (self.old_red, e, self.old_blue)
        self.colordisplay.itemconfig(self.cordisp, fill=cor)
        self.color_fg = cor
        self.old_green = e
        (h,s,v) = cl.rgb2hsv(self.old_red, e, self.old_blue)
        print(h,s,v)
        self.sliderH.set(h)
        self.old_hue = h
        self.sliderS.set(s)
        self.old_sat = s
        self.sliderV.set(v)
        self.old_val = v

    def changeB(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        cor = '#%02x%02x%02x' % (self.old_red, self.old_green, e)
        self.colordisplay.itemconfig(self.cordisp, fill=cor)
        self.color_fg = cor
        self.old_blue = e
        (h,s,v) = cl.rgb2hsv(self.old_red, self.old_green, e)
        print(h,s,v)
        self.sliderH.set(h)
        self.old_hue = h
        self.sliderS.set(s)
        self.old_sat = s
        self.sliderV.set(v)
        self.old_val = v

    def changeH(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        rgb = cl.hsv2rgb(e, self.old_sat/100, self.old_val/100)
        cor = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
        self.color_fg = cor
        self.colordisplay.itemconfig(self.cordisp, fill=cor)
        self.old_hue = e
        self.sliderR.set(rgb[0])
        self.old_red = rgb[0]
        self.sliderG.set(rgb[1])
        self.old_green = rgb[1]
        self.sliderB.set(rgb[2])
        self.old_blue = rgb[2]
        #self.colordisplay['bg'] = r,g,b
    
    def changeS(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        rgb = cl.hsv2rgb(self.old_hue, e/100, self.old_val/100)
        cor = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
        self.color_fg = cor
        self.colordisplay.itemconfig(self.cordisp, fill=cor)
        self.old_sat = e
        self.sliderR.set(rgb[0])
        self.old_red = rgb[0]
        self.sliderG.set(rgb[1])
        self.old_green = rgb[1]
        self.sliderB.set(rgb[2])
        self.old_blue = rgb[2]

    def changeV(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        rgb = cl.hsv2rgb(self.old_hue, self.old_sat/100, e/100)
        cor = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
        self.color_fg = cor
        self.colordisplay.itemconfig(self.cordisp, fill=cor)
        self.old_val = e
        self.sliderR.set(rgb[0])
        self.old_red = rgb[0]
        self.sliderG.set(rgb[1])
        self.old_green = rgb[1]
        self.sliderB.set(rgb[2])
        self.old_blue = rgb[2]

    def changeCoord(self,e):
        height = 255
        width = 255
        self.func.c.delete(ALL)
        #print(e.x, e.y) 
        if e.x < 20 and 0 <= e.y <= height:
            x1, y1 = ( 0 ), ( e.y )
            x2, y2 = ( width ), ( self.old_x )
            x3, y3 = self.coorda
            x4, y4 = self.coordb
            self.old_y = e.y
        elif e.x > width - 20 and 0 <= e.y <= height:
            x1, y1 = ( 0 ), ( self.old_y )
            x2, y2 = ( width ), ( e.y )
            x3, y3 = self.coorda
            x4, y4 = self.coordb
            self.old_x = e.y
        elif e.x < width/2 and 0 <= e.y <= height:
            x1, y1 = ( 0 ), ( self.old_y )
            x2, y2 = ( width ), ( self.old_x )
            self.coorda = [e.x, e.y]
            x3, y3 = self.coorda
            x4, y4 = self.coordb
        elif e.x > width/2 and 0 <= e.y <= height:
            x1, y1 = ( 0 ), ( self.old_y )
            x2, y2 = ( width ), ( self.old_x )
            self.coordb = [e.x, e.y]
            x3, y3 = self.coorda
            x4, y4 = self.coordb
        else:
            x1, y1 = ( 0 ), ( self.old_y )
            x2, y2 = ( width ), ( self.old_x )
            x3, y3 = self.coorda
            x4, y4 = self.coordb

        #self.func.c.coords(self.line, [x1,y1,x2,y2]) OBS: É POSSÍVEL MUDAR AS COORDENADAS DE UM WIDGET
        #self.func.c.create_line(x1,y1,x2,y2,width=5,fill='green',capstyle=ROUND,smooth=True)
        self.func.c.create_line(x1,y1,x3,y3,width=5,fill='green',capstyle=ROUND,smooth=True)
        self.func.c.create_line(x3,y3,x4,y4,width=5,fill='red',capstyle=ROUND,smooth=True)
        self.func.c.create_line(x4,y4,x2,y2,width=5,fill='black',capstyle=ROUND,smooth=True)
        
        quad = self.func.c.create_oval((x1-2, y1+5, 8, y1 - 5), fill="green")
        #self.func.c.tag_bind(quad, '<B1-Motion>', self.changeCoord)
        quad = self.func.c.create_rectangle((x3 - 10, y3-5, x3,y3 + 5), fill="green")
        self.coorda = [x3, y3]
        #2/3
        quad = self.func.c.create_rectangle((x4 - 10, y4-5, x4,y4 + 5), fill="green")
        self.coordb = [x4, y4]

        quad = self.func.c.create_rectangle((x2 - 8, y2-5, x2 + 2, y2 + 5), fill="green")

        self.points = [x1,255-y1,x3,255-y3,x4,255-y4,x2,255-y2]
        #self.points = [x1,255 - y1,x2,255 - y2]
        #print(self.points)
        #self.getfunc(self.points,200)
        #func.c.tag_bind(quad, "<B1-Motion>", self.setColor("red"))
        #self.old_x = e.x
        #self.old_y = e.y
    
    #def funcao(self, Q):

    def getfunc(self, P, x):
        (x1,y1,x3,y3,x4,y4,x2,y2) = P

        if x1 < x < x3:
            if (x3-x1) != 0:
                slope = (float(y3) - y1)/(float(x3) - x1)
            else: 
                slope = 0
            intercept = y1 - slope*x1

        elif x3 < x < x4:
            if (x4-x3) != 0:
                slope = (float(y4) - y3)/(float(x4) - x3)
            else: 
                slope = 0
            intercept = y3 - slope*x3
        else:
            if (x2-x4) != 0:
                slope = (float(y2) - y4)/(float(x2) - x4)
            else: 
                slope = 0
            intercept = y4 - slope*x4
        return int(slope*x + intercept)
 
        #P = [0, 0] 
        #Q = [100, 100]
        #a = Q[1] - P[1] 
        #b = P[0] - Q[0]  
        #c = a*(P[0]) + b*(P[1]) 

    def applyfunc(self):
        img = self.img
        i = np.array(img)
        it = i
        if len(i.shape) == 2:
            for row in range(i.shape[0]):
                for col in range(i.shape[1]):
                    it[row,col] = self.getfunc(self.points, i[row,col])
        else:
            for row in range(i.shape[0]):
                for col in range(i.shape[1]):
                    it[row,col,0] = self.getfunc(self.points, i[row,col,0])
                    it[row,col,1] = self.getfunc(self.points, i[row,col,1])
                    it[row,col,2] = self.getfunc(self.points, i[row,col,2])
        self.img = Image.fromarray(it)
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
    
    def drawfunc(self):
        self.old_x = 0
        self.old_y = 255
        self.func = Tk()
        self.func.title('Função')
        self.func.bind('<B1-Motion>',self.changeCoord)
        self.func.configure(background='#102027')
        self.func.resizable(width=False, height=False)
        titlelbl = Label(self.func,text="Desenhe a Função",bg='#102027',fg='#ffffff',font=('roboto 18'))
        titlelbl.grid(row=0, column=1, columnspan=10,sticky=N+S+W+E)
        self.func.c = Canvas(self.func,width=255,height=255,bg=self.color_bg, cursor='circle')
        self.func.c.grid(row=1, column=1, rowspan=10,columnspan=10)
        white = (255, 255, 255)
        height = 255
        width = 255
        

        x1, y1 = ( 0 ), (height )
        x2, y2 = ( width ), ( 0 )
        x3, y3 = ( 0.33*width ), ( 0.66*height )
        x4, y4 = ( 0.66*width ), ( 0.33*height )
        self.func.c.create_line(x1,y1,x3,y3,width=5,fill='green',capstyle=ROUND,smooth=True)
        self.func.c.create_line(x3,y3,x4,y4,width=5,fill='red',capstyle=ROUND,smooth=True)
        self.func.c.create_line(x4,y4,x2,y2,width=5,fill='black',capstyle=ROUND,smooth=True)

        self.points = [x1,255-y1,x3,255-y3,x4,255-y4,x2,255-y2]
        #self.getfunc(self.points,200)
        #0
        quad = self.func.c.create_oval((0, y1, 10, y1 - 10), fill="green")
        #self.coord = self.func.c.coords(quad)
        #self.func.c.tag_bind(quad, '<B1-Motion>', self.changeCoord)
        #self.func.c.bind('<ButtonRelease-1>',self.reset)
        #1/3
        quad = self.func.c.create_rectangle((x3 - 5, y3-5, x3+5,y3 + 5), fill="green")
        self.coorda = [x3, y3]
        #2/3
        quad = self.func.c.create_rectangle((x4 - 5, y4-5, x4+5,y4 + 5), fill="green")
        self.coordb = [x4, y4]
        #1
        quad = self.func.c.create_rectangle((x2 - 10, 0, x2, 10), fill="green")

        labeltick1 = Label(self.func,text="",bg='#62727b',fg='#ffffff',font=('roboto 10'))
        labeltick1.grid(row=1, column=0, rowspan=10,sticky=N+S+W+E)
        labeltick1 = Label(self.func,text="250",bg='#62727b',fg='#ffffff',font=('roboto 10'))
        labeltick1.grid(row=1, column=0, sticky=W+E)
        labeltick1 = Label(self.func,text="0",bg='#62727b',fg='#ffffff',font=('roboto 10'))
        labeltick1.grid(row=11, column=0, sticky=W+E)

        labeltick2 = Label(self.func,text="",bg='#62727b',fg='#ffffff',font=('roboto 10'))
        labeltick2.grid(row=11, column=1, columnspan=10, sticky=W+E)
        labeltick2 = Label(self.func,text="250",bg='#62727b',fg='#ffffff',font=('roboto 10'))
        labeltick2.grid(row=11, column=10, sticky=W+E)
        #labelticks = Label(self.func,text="0",bg='#62727b',fg='#ffffff',font=('roboto 10'))
        #labelticks.grid(row=10, column=1, sticky=W+E)
        #framebtn = Frame(self.func)
        button = Button(self.func, text="Aplicar",bg='#98ee99',fg='#000000',command=self.applyfunc)
        button.grid(row=13, column=0, columnspan=5, sticky=W+E)
        sair = Button(self.func, text="Sair",command=self.func.destroy)
        sair.grid(row=13, column=10,columnspan=2, sticky=W+E)
        cancelar = Button(self.func, text="Cancelar",bg='#FFe0e0',fg='#000000',command=lambda:self.undo(0))
        cancelar.grid(row=13, column=7,columnspan=3, sticky=W+E)

        #cancelar.pack(side = RIGHT)
        #framebtn.grid(row=2,column=0)
        #func.c.tag_bind(quad, "<B1-Motion>", self.setColor("red"))
        #print(x1, x2, y1, y2)
        
        #middle
        #quad = self.c.create_rectangle((self.img.width/3, self.img.height/3, self.img.width/3 + 10, self.img.height/3 + 10), fill="white")
        #self.c.tag_bind(quad, "<B1-Motion>", lambda x: setColor("red"))
        #quad = self.c.create_rectangle((self.img.width - 10, 0, self.img.width, 10), fill="white")
        #self.c.tag_bind(quad, "<B1-Motion>", lambda x: setColor("red"))


    ## EFEITOS DIRETOS

    def efeito_neg(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img) 
        it = bk.negative_filter(i) 
        self.img = Image.fromarray(it)
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_log(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img) 
        it = bk.logarithm_filter(i) 
        self.img = Image.fromarray(it)
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_hist(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img)
        if len(i.shape) == 2:
            hist = bk.histogram(i)
        else:
            imghsv = cl.imgrgb2hsv(i)
            hist = bk.histogram_hsv(imghsv)
        it = bk.equalize_hist(i, hist)
        self.img = Image.fromarray(it) 
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_laplacefilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        self.old_img = img
        i = np.array(img)
        #i = colors.rgb2gray(i)
        it = bk.laplacian_filter(i)
        self.img = Image.fromarray(it) 
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_sharpen(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        self.old_img = img
        i = np.array(img)
        #i = colors.rgb2gray(i)
        it = bk.sharpen_filter(i)
        self.img = Image.fromarray(it) 
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_sobel(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        self.old_img = img
        i = np.array(img)
        #i = colors.rgb2gray(i)
        it = bk.sobel_filter(i)
        self.img = Image.fromarray(it) 
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_sepia(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        self.old_img = img
        i = np.array(img)
        #i = colors.rgb2gray(i)
        it = bk.sepia_filter(i)
        self.img = Image.fromarray(it) 
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()


  
    ## EFEITOS COM CONTROLADORES 

    def passa_alta(self, radius):
        xx, yy = np.mgrid[:self.size[0], :self.size[1]]
        xcenter = self.size[0]//2
        ycenter = self.size[1]//2 
        # circles contains the squared distance to the (100, 100) point
        # we are just using the circle equation learnt at school
        circle = (xx - xcenter) ** 2 + (yy - ycenter) ** 2
        # donuts contains 1's and 0's organized in a donut shape
        # you apply 2 thresholds on circle to define the shape
        filtro = np.logical_and(True, circle > (radius*100))
        #self.img = Image.fromarray(donut) 
        #self.old_img = img
        #self.c.image = ImageTk.PhotoImage(self.img)
        #self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        #self.c.pack()
        espectro = self.fouriert
        for m in range(espectro.shape[0]):
            for n in range(espectro.shape[1]):
                if filtro[m,n] == 0:
                    espectro[m,n] = 0
        f = fr.ifft2shift(espectro)
        f = fr.ifft2(f)
        self.img = Image.fromarray(f)
        #self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def passa_faixa(self, minr, maxr):
        xx, yy = np.mgrid[:self.size[0], :self.size[1]]
        xcenter = self.size[0]//2
        ycenter = self.size[1]//2 
        # circles contains the squared distance to the (100, 100) point
        # we are just using the circle equation learnt at school
        circle = (xx - xcenter) ** 2 + (yy - ycenter) ** 2
        # donuts contains 1's and 0's organized in a donut shape
        # you apply 2 thresholds on circle to define the shape
        filtro = np.logical_and(circle < (maxr*100), circle > (minr*100))
        #self.img = Image.fromarray(donut) 
        #self.old_img = img
        #self.c.image = ImageTk.PhotoImage(self.img)
        #self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        #self.c.pack()
        espectro = self.fouriert
        for m in range(espectro.shape[0]):
            for n in range(espectro.shape[1]):
                if filtro[m,n] == 0:
                    espectro[m,n] = 0
        f = fr.ifft2shift(espectro)
        f = fr.ifft2(f)
        self.img = Image.fromarray(f)
        #self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def passa_baixa(self, radius):
        xx, yy = np.mgrid[:self.size[0], :self.size[1]]
        xcenter = self.size[0]//2
        ycenter = self.size[1]//2 
        # circles contains the squared distance to the (100, 100) point
        # we are just using the circle equation learnt at school
        circle = (xx - xcenter) ** 2 + (yy - ycenter) ** 2
        # donuts contains 1's and 0's organized in a donut shape
        # you apply 2 thresholds on circle to define the shape
        filtro = np.logical_and(circle < (radius*100), True)
        #self.img = Image.fromarray(donut) 
        #self.old_img = img
        #self.c.image = ImageTk.PhotoImage(self.img)
        #self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        #self.c.pack()
        espectro = self.fouriert
        for m in range(espectro.shape[0]):
            for n in range(espectro.shape[1]):
                if filtro[m,n] == 0:
                    espectro[m,n] = 0
        f = fr.ifft2shift(espectro)
        f = fr.ifft2(f)
        self.img = Image.fromarray(f)
        #self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()


    def efeito_highboost(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        aba = Frame(self.controls,bg='#102027')
        self.controls.add(aba, text='Ajustes do efeito')
        self.title = Label(aba, text="Efeito Highboost", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.text = Label(aba, text="Tamanho do filtro: ", bg='#102027', fg='#FFFFFF')
        self.spin = Spinbox(aba, values=(3,5,7,9), width=5)
        self.text2 = Label(aba, text="Quantidade c:", bg='#102027', fg='#FFFFFF')
        self.slider = Scale(aba,from_= -20, to = 20, width=10, orient=HORIZONTAL, bg='#102027',highlightbackground='#102027',highlightcolor='#102027', fg="#98ee99",troughcolor="#FFFFFF")
        self.slider.set(1)
        self.submit = Button(aba, text="Aplicar",bg='#98ee99',command=self.highboost, padx=3)
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0, columnspan=3, sticky=W+E)
        self.spin.grid(row=2,column=0, columnspan=3, sticky=W+E)
        self.text2.grid(row=3,column=0, columnspan=3, sticky=W+E)
        self.slider.grid(row=4,column=0, columnspan=3, sticky=W+E)
        self.submit.grid(row=5,column=0, columnspan=3, sticky=W+E)
        self.controls.pack()

    def highboost(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img)
        f = int(self.spin.get())
        c = int(self.slider.get())
        it = bk.highboost(i,c,f) 
        self.img = Image.fromarray(it)
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_threshold(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        aba = Frame(self.controls,bg='#102027')
        self.controls.add(aba, text='Ajustes do efeito')
        self.title = Label(aba, text="Efeito Threshold", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.text = Label(aba, text="Flag: ", bg='#102027', fg='#FFFFFF')
        self.spin = Spinbox(aba, values=(1,2,3), width=5)
        self.text2 = Label(aba, text="threshold:", bg='#102027', fg='#FFFFFF')
        self.slider = Scale(aba,from_= 0, to = 255, width=10, orient=HORIZONTAL, bg='#102027',highlightbackground='#102027',highlightcolor='#102027', fg="#98ee99",troughcolor="#FFFFFF")
        self.slider.set(1)
        self.submit = Button(aba, text="Aplicar",bg='#98ee99',command=self.threshold, padx=3)
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0, columnspan=3, sticky=W+E)
        self.spin.grid(row=2,column=0, columnspan=3, sticky=W+E)
        self.text2.grid(row=3,column=0, columnspan=3, sticky=W+E)
        self.slider.grid(row=4,column=0, columnspan=3, sticky=W+E)
        self.submit.grid(row=5,column=0, columnspan=3, sticky=W+E)
        self.controls.pack()

    def threshold(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img)
        f = int(self.spin.get())
        t = int(self.slider.get())
        it = bk.thresholding(i,t,f) 
        self.img = Image.fromarray(it)
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_gaussian(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        aba = Frame(self.controls,bg='#102027')
        self.controls.add(aba, text='Ajustes do efeito')
        self.title = Label(aba, text="Desfoque Gaussiano", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.text = Label(aba, text="Tamanho do filtro: ", bg='#102027', fg='#FFFFFF')
        self.spin = Spinbox(aba, values=(3,5,7,9), width=5)
        self.text2 = Label(aba, text="Sigma:", bg='#102027', fg='#FFFFFF')
        self.slider = Scale(aba,from_= 0, to = 100, width=10, orient=HORIZONTAL, bg='#102027',highlightbackground='#102027',highlightcolor='#102027', fg="#98ee99",troughcolor="#FFFFFF")
        self.slider.set(1)
        self.submit = Button(aba, text="Aplicar",bg='#98ee99',command=self.gauss, padx=3)
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0, columnspan=3, sticky=W+E)
        self.spin.grid(row=2,column=0, columnspan=3, sticky=W+E)
        self.text2.grid(row=3,column=0, columnspan=3, sticky=W+E)
        self.slider.grid(row=4,column=0, columnspan=3, sticky=W+E)
        self.submit.grid(row=5,column=0, columnspan=3, sticky=W+E)
        self.controls.pack()

    def gauss(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img)
        f = int(self.spin.get())
        print(f)
        c = float(self.slider.get())
        c = c/100
        print(c)
        it = bk.gaussian_filter(i, f, c) 
        self.img = Image.fromarray(it)
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_contraharmonic_meanfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        aba = Frame(self.controls,bg='#102027')
        self.controls.add(aba, text='Ajustes do efeito')
        self.title = Label(aba, text="Média Contra-harmônica", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.text = Label(aba, text="Tamanho do filtro: ", bg='#102027', fg='#FFFFFF')
        self.spin = Spinbox(aba, values=(3,5,7,9), width=5)
        self.text2 = Label(aba, text="Ordem do filtro:", bg='#102027', fg='#FFFFFF')
        self.slider = Scale(aba,from_= -10, to = 10, width=10, orient=HORIZONTAL, bg='#102027',highlightbackground='#102027',highlightcolor='#102027', fg="#98ee99",troughcolor="#FFFFFF")
        self.slider.set(0)
        self.submit = Button(aba, text="Aplicar",bg='#98ee99',command=self.contraharmonic_meanfilter, padx=3)
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0, columnspan=3, sticky=W+E)
        self.spin.grid(row=2,column=0, columnspan=3, sticky=W+E)
        self.text2.grid(row=3,column=0, columnspan=3, sticky=W+E)
        self.slider.grid(row=4,column=0, columnspan=3, sticky=W+E)
        self.submit.grid(row=5,column=0, columnspan=3, sticky=W+E)
        self.controls.pack()

    def contraharmonic_meanfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img)
        f = int(self.spin.get())
        q = float(self.slider.get())
        q = q/100
        if len(i.shape) == 2:
            it = bk.contraharmonic_mean_filter(i, f, q)
        else:
            it = bk.contraharmonic_mean_filter_rgb(i,f,q)    
        self.img = Image.fromarray(it)
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_gamma(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        aba = Frame(self.controls,bg='#102027')
        self.controls.add(aba, text='Ajustes do efeito')
        self.title = Label(aba, text="Efeito Gamma", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.text = Label(aba, text="Gamma: ", bg='#102027', fg='#FFFFFF')
        self.slider = Scale(aba,from_= 1, to = 20, width=10, orient=HORIZONTAL, bg='#102027',highlightbackground='#102027',highlightcolor='#102027', fg="#98ee99",troughcolor="#FFFFFF")
        self.slider.set(1)
        self.submit = Button(aba, text="Aplicar",bg='#98ee99',command=self.gamma, padx=3)
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0, columnspan=3, sticky=W+E)
        self.slider.grid(row=2,column=0, columnspan=3, sticky=W+E)
        self.submit.grid(row=3,column=0, columnspan=3, sticky=W+E)
        self.controls.pack()

    def gamma(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img) 
        gamma = int(self.slider.get())
        it = bk.gamma_filter(i,gamma) 
        self.img = Image.fromarray(it)
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_meanfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        self.abamean = Frame(self.controls,bg='#102027')
        self.controls.add(self.abamean, text='Ajustes do filtro')
        self.title = Label(self.abamean, text="Filtro da Média", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.text = Label(self.abamean, text="Tamanho do filtro: ", bg='#102027', fg='#FFFFFF')
        self.spin = Spinbox(self.abamean, values=(3,5,7,9), width=5)   
        self.submit = Button(self.abamean, text="Aplicar",bg='#98ee99',command=self.meanfilter, padx=3)
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0)
        self.spin.grid(row=1,column=2)
        self.submit.grid(row=2,column=0, columnspan=3, sticky=W+E)
        self.controls.pack()
    

    def meanfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        f = int(self.spin.get())
        img = self.img
        i = np.array(img)
        #i = colors.rgb2gray(i)
        it = bk.mean_filter(i,f)
        self.img = Image.fromarray(it) 
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        self.controls.add(self.abacontrole)
        self.controls.hide(self.abamean)
        self.abacontrole.focus()

    def efeito_medianfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        self.abamean = Frame(self.controls,bg='#102027')
        self.controls.add(self.abamean, text='Ajustes do filtro')
        self.title = Label(self.abamean, text="Filtro da Mediana", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.text = Label(self.abamean, text="Tamanho do filtro: ", bg='#102027', fg='#FFFFFF')
        self.spin = Spinbox(self.abamean, values=(3,5,7,9), width=5)   
        self.submit = Button(self.abamean, text="Aplicar",bg='#98ee99',command=self.medianfilter, padx=3)
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0)
        self.spin.grid(row=1,column=2)
        self.submit.grid(row=2,column=0, columnspan=3, sticky=W+E)
        self.controls.pack()
    

    def medianfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        f = int(self.spin.get())
        img = self.img
        i = np.array(img)
        #i = colors.rgb2gray(i)
        if len(i.shape) == 2:
            it = bk.median_filter(i,f)
        else:
            it = bk.median_filter_rgb(i,f)
        self.img = Image.fromarray(it) 
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        self.controls.add(self.abacontrole)
        self.controls.hide(self.abamean)
        self.abacontrole.focus()

    def efeito_geometricmeanfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        self.abamean = Frame(self.controls,bg='#102027')
        self.controls.add(self.abamean, text='Ajustes do filtro')
        self.title = Label(self.abamean, text="Filtro da Média Geométrica", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.text = Label(self.abamean, text="Tamanho do filtro: ", bg='#102027', fg='#FFFFFF')
        self.spin = Spinbox(self.abamean, values=(3,5,7,9), width=5)   
        self.submit = Button(self.abamean, text="Aplicar",bg='#98ee99',command=self.geometric_meanfilter, padx=3)
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0)
        self.spin.grid(row=1,column=2)
        self.submit.grid(row=2,column=0, columnspan=3, sticky=W+E)
        self.controls.pack()
    

    def geometric_meanfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        f = int(self.spin.get())
        img = self.img
        i = np.array(img)
        #i = colors.rgb2gray(i)
        if len(i.shape) == 2:
            it = bk.geometric_mean_filter(i,f)
        else:
            it = bk.geometric_mean_filter_rgb(i,f)
        self.img = Image.fromarray(it) 
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        self.controls.add(self.abacontrole)
        self.controls.hide(self.abamean)
        self.abacontrole.focus()

    def efeito_harmonic_meanfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        self.abamean = Frame(self.controls,bg='#102027')
        self.controls.add(self.abamean, text='Ajustes do filtro')
        self.title = Label(self.abamean, text="Filtro da Média Harmônica", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.text = Label(self.abamean, text="Tamanho do filtro: ", bg='#102027', fg='#FFFFFF')
        self.spin = Spinbox(self.abamean, values=(3,5,7,9), width=5)   
        self.submit = Button(self.abamean, text="Aplicar",bg='#98ee99',command=self.harmonic_meanfilter, padx=3)
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0)
        self.spin.grid(row=1,column=2)
        self.submit.grid(row=2,column=0, columnspan=3, sticky=W+E)
        self.controls.pack()
    

    def harmonic_meanfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        f = int(self.spin.get())
        img = self.img
        i = np.array(img)
        #i = colors.rgb2gray(i)
        if len(i.shape) == 2:
            it = bk.harmonic_mean_filter(i,f)
        else:
            it = bk.harmonic_mean_filter_rgb(i,f)
        self.img = Image.fromarray(it) 
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        self.controls.add(self.abacontrole)
        self.controls.hide(self.abamean)
        self.abacontrole.focus()

    def control_convmatriz(self):
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        aba = Frame(self.controls,bg='#102027')
        self.controls.add(aba, text='Ajustes do efeito')
        self.title = Label(aba, text="Matriz Genérica", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3,sticky=W+E)
        self.text = Label(aba, text="Tamanho da matriz: ", bg='#102027', fg='#FFFFFF')
        self.spin = Spinbox(aba, values=(3,5,7,9), width=5)
        self.text2 = Label(aba, text="Os valores da matriz: (x,y,z,...)", bg='#102027', fg='#FFFFFF')
        #style.configure("BW.Horizontal.TScale", foreground="black", background="#102027",padx=2)
        self.entrada = Entry(aba)
        self.text3 = Label(aba, text="Os valores da matriz: (x,y,z,...)", bg='#102027', fg='#102027')
        self.submit = Button(aba, text="Aplicar",command=self.efeito_convmatriz, bg='#98ee99')
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0, columnspan=3,sticky=W+E)
        self.spin.grid(row=2, column=0, columnspan=3)
        self.text2.grid(row=3,column=0, columnspan=3,sticky=W+E)
        self.entrada.grid(row=4,column=0, columnspan=3,sticky=W+E)
        self.text3.grid(row=5,column=0, columnspan=3,sticky=W+E)
        self.submit.grid(row=6,column=0, columnspan=3,sticky=W+E)
        self.controls.add(aba)
        aba.focus()

    def efeito_convmatriz(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = np.array(self.img)
        #i = colors.rgb2gray(i)
        size = int(self.spin.get())
        string = self.entrada.get()
        lista = string.split (",")
        kernel = []
        for i in lista:
            kernel.append(int(i))
        if len(kernel) != size**2:
            messagebox.showerror("ERRO!","O número de elementos está errado!")
        kernel = np.array(kernel)
        shape = (size,size)
        kernel.shape = shape
        it = bk.conv_filter(img,kernel)
        self.img = Image.fromarray(it)
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        self.sizelbl['text'] = "Tamanho da imagem: %02dx%02d" %(self.img.width,self.img.height)
        resize = '%02dx%02d+100+100' % (400 + self.img.width, 100 + self.img.height)
        root.geometry(resize)

    def control_chromakey(self):
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        self.imgfundo = np.array(self.img)
        url = filedialog.askopenfilename(title="Selecione a imagem que ficará a frente")
        #self.input = url
        #img = Image.open('images/einstein.jpeg')
        self.img = Image.open(url)
        self.old_img = self.imgfundo
        aba = Frame(self.controls,bg='#102027')
        self.controls.add(aba, text='Ajustes do efeito')
        self.title = Label(aba, text="Chroma Key", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.textcor = Label(aba, text="Ajuste a cor nos slider da direita → →", bg='#102027', fg='#FFFFFF')
        self.textslider = Label(aba, text="Faixa: ", bg='#102027', fg='#FFFFFF')
        #style.configure("BW.Horizontal.TScale", foreground="black", background="#102027",padx=2)
        self.slider = Scale(aba,from_= 0, to = 255, width=10, orient=HORIZONTAL, bg='#102027',highlightbackground='#102027',highlightcolor='#102027', fg="#98ee99",troughcolor="#FFFFFF")
        self.slider.set(100)
        self.submit = Button(aba, text="Aplicar",command=self.efeito_chromakey, bg='#98ee99')
        #self.data.grid(row=0,column=0)
        self.textcor.grid(row=1,column=0,columnspan=3,sticky=W+E)
        self.textslider.grid(row=2,column=0, columnspan=3,sticky=W+E)
        self.slider.grid(row=3,column=0, columnspan=3,sticky=W+E)
        self.submit.grid(row=4,column=0, columnspan=3, sticky=W+E)
        self.controls.add(aba)
        aba.focus()

    def efeito_chromakey(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = np.array(self.img)
        print("Imagem: ",img)
        #i = colors.rgb2gray(i)
        faixa = int(self.slider.get())
        it = cl.chroma_key(img, self.imgfundo, self.old_red, self.old_green, self.old_blue, faixa)
        print(it)
        self.img = Image.fromarray(it)
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        self.sizelbl['text'] = "Tamanho da imagem: %02dx%02d" %(self.img.width,self.img.height)
        resize = '%02dx%02d+100+100' % (400 + self.img.width, 100 + self.img.height)
        root.geometry(resize)

    def control_aumentarHSV(self):
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        aba = Frame(self.controls,bg='#102027')
        self.controls.add(aba, text='Ajustes do efeito')
        self.title = Label(aba, text="Hue/Sat/Value", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.texth = Label(aba, text="Matiz: ", bg='#102027', fg='#FFFFFF')
        self.texts = Label(aba, text="Saturação: ", bg='#102027', fg='#FFFFFF')
        self.textv = Label(aba, text="Iluminação: ", bg='#102027', fg='#FFFFFF')
        #style.configure("BW.Horizontal.TScale", foreground="black", background="#102027",padx=2)
        self.sliderh = Scale(aba,from_= 0, to = 200, width=10, orient=HORIZONTAL, bg='#102027',highlightbackground='#102027',highlightcolor='#102027', fg="#98ee99",troughcolor="#FFFFFF")
        self.sliderh.set(100)
        self.sliders = Scale(aba,from_= 0, to = 200, width=10, orient=HORIZONTAL, bg='#102027',highlightbackground='#102027',highlightcolor='#102027', fg="#98ee99",troughcolor="#FFFFFF")
        self.sliders.set(100)
        self.sliderv = Scale(aba,from_= 0, to = 200, width=10, orient=HORIZONTAL, bg='#102027',highlightbackground='#102027',highlightcolor='#102027', fg="#98ee99",troughcolor="#FFFFFF")
        self.sliderv.set(100)
        self.submit = Button(aba, text="Aplicar",command=self.efeito_aumentarHSV, bg='#98ee99')
        #self.data.grid(row=0,column=0)
        self.texth.grid(row=1,column=0,columnspan=3,sticky=W+E)
        self.sliderh.grid(row=2,column=0, columnspan=3,sticky=W+E)
        self.texts.grid(row=3,column=0,columnspan=3,sticky=W+E)
        self.sliders.grid(row=4,column=0, columnspan=3,sticky=W+E)
        self.textv.grid(row=5,column=0,columnspan=3,sticky=W+E)
        self.sliderv.grid(row=6,column=0, columnspan=3,sticky=W+E)
        self.submit.grid(row=7,column=0, columnspan=3, sticky=W+E)
        self.controls.add(aba)
        aba.focus()

    def efeito_aumentarHSV(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = np.array(self.img)
        #self.input = url
        #img = Image.open('images/einstein.jpeg')
        print("Imagem: ",img)
        #i = colors.rgb2gray(i)
        amounth = int(self.sliderh.get())
        amounts = int(self.sliders.get())
        amountv = int(self.sliderv.get())
        it = cl.HueSatVal_adjust(img, amounth,amounts,amountv)
        print(it)
        self.img = Image.fromarray(it)
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
    
    def control_aumentarbrilho(self):
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        ababrilho = Frame(self.controls,bg='#102027')
        self.controls.add(ababrilho, text='Ajustes do efeito')
        self.title = Label(ababrilho, text="Brilho", bg='#102027', fg='#FFFFFF',font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        self.text = Label(ababrilho, text="Quantidade de brilho: ", bg='#102027', fg='#FFFFFF')
        #style.configure("BW.Horizontal.TScale", foreground="black", background="#102027",padx=2)
        self.slider = Scale(ababrilho,from_= 0, to = 200, width=10, orient=HORIZONTAL, bg='#102027',highlightbackground='#102027',highlightcolor='#102027', fg="#98ee99",troughcolor="#FFFFFF")
        self.slider.set(100)
        self.submit = Button(ababrilho, text="Aplicar",command=self.efeito_aumentarbrilho, bg='#98ee99')
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0,columnspan=3,sticky=W+E)
        self.slider.grid(row=2,column=0, columnspan=3,sticky=W+E)
        self.submit.grid(row=3,column=0, columnspan=3, sticky=W+E)
        self.controls.add(ababrilho)
        ababrilho.focus()

    def efeito_aumentarbrilho(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = np.array(self.img)
        #self.input = url
        #img = Image.open('images/einstein.jpeg')
        print("Imagem: ",img)
        #i = colors.rgb2gray(i)
        amount = int(self.slider.get())
        it = cl.aumentarbrilho(img, amount)
        print(it)
        self.img = Image.fromarray(it)
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def histograma(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        self.func = Tk()
        self.func.title('Histograma')
        tab_hist = ttk.Notebook(self.func)#1 
        self.aba = Frame(tab_hist)#2
        self.abaR = Frame(tab_hist)
        self.abaG = Frame(tab_hist)
        self.abaB = Frame(tab_hist)#2
        
        i = np.array(self.img)
        print(i.shape)
        gray = Figure(figsize=(5,5), dpi=100)
        red = Figure(figsize=(5,5), dpi=100)
        green = Figure(figsize=(5,5), dpi=100)
        blue = Figure(figsize=(5,5), dpi=100)
        pltgray = gray.add_subplot(111)
        pltred = red.add_subplot(111)
        pltgreen = green.add_subplot(111)
        pltblue = blue.add_subplot(111)

        x = list(range(256))
        if len(i.shape) == 2:
            tab_hist.add(self.aba, text='Escala de cinza')
            i = cl.rgb2gray(i)
            hist = bk.histogram(i)
            pltgray.bar(x,hist, width=0.6, color='gray')
            canvas = FigureCanvasTkAgg(gray, self.aba)
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        else:
            tab_hist.add(self.abaR, text='Vermelho')
            tab_hist.add(self.abaG, text='Verde')
            tab_hist.add(self.abaB, text='Azul')

            r,g,b = bk.histogram(i)
            #x = [1,2,3,4,5,6,7,8]
            #y = [5,4,3,1,0,2,8,9]
            pltred.bar(x,r, width=0.6, color='red')
            canvas = FigureCanvasTkAgg(red, self.abaR)
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
            pltgreen.bar(x,g, width=0.6, color='green')
            canvas = FigureCanvasTkAgg(green, self.abaG)
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
            pltblue.bar(x,b, width=0.6, color='blue')
            canvas = FigureCanvasTkAgg(blue, self.abaB)
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        tab_hist.pack(side=BOTTOM,expand=1, fill='both')
        
        

    def inversaFourierbkp(self):
        img = Image.open('canvas.jpg')
        filtro = np.array(img)
        filtro = cl.rgb2gray(filtro)
        #espectro = np.array(self.img)
        espectro = self.fouriert
        diffwidth, diffheight = ( filtro.shape[0] - espectro.shape[0] ), ( filtro.shape[1] - espectro.shape[1] )
        print("Diff: ",diffwidth,", ", diffheight)
        initw = int(round(diffwidth/2))
        finalw = diffwidth - initw
        inith = int(round(diffheight/2))
        finalh = diffheight - inith
        print("Dimensões: ", initw, ", ", finalw, ", ", inith, ", ",finalh)
        print("ESPECTRO: ",espectro.shape)
        print("FILTRO: ",filtro.shape)
        width = filtro.shape[0] - finalw
        height = filtro.shape[1] - finalh
        filtro = filtro[initw:width, inith:height]
        print(filtro.shape)
        for m in range(espectro.shape[0]):
            for n in range(espectro.shape[1]):
                if filtro[m,n] == 0:
                    espectro[m,n] = 0
                elif filtro[m,n] == 1:
                    espectro[m,n] = 1

                #invimg[m,n] = espectro[m,n] * filtro[m,n]

        f = fr.ifft2shift(espectro)
        f = fr.ifft2(f)
        self.img = Image.fromarray(f)
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        resize = '%02dx%02d+100+100' % (400 + self.img.width, 100 + self.img.height)
        root.geometry(resize)

    def inversaFourier(self):
        #img = Image.open('canvas.jpg')
        filtro = self.mcanvas
        #filtro = cl.rgb2gray(filtro)
        #espectro = np.array(self.img)
        espectro = self.fouriert
        #diffwidth, diffheight = ( filtro.shape[0] - espectro.shape[0] ), ( filtro.shape[1] - espectro.shape[1] )
        #print("Diff: ",diffwidth,", ", diffheight)
        #initw = int(round(diffwidth/2))
        #finalw = diffwidth - initw
        #inith = int(round(diffheight/2))
        #finalh = diffheight - inith
        #print("Dimensões: ", initw, ", ", finalw, ", ", inith, ", ",finalh)
        print("ESPECTRO: ",espectro)
        print("FILTRO: ",filtro)
        #width = filtro.shape[0] - finalw
        #height = filtro.shape[1] - finalh
        #filtro = filtro[initw:width, inith:height]
        
        for m in range(espectro.shape[0]):
            for n in range(espectro.shape[1]):
                espectro[m,n] = espectro[m,n]*filtro[m,n]
                #invimg[m,n] = espectro[m,n] * filtro[m,n]
        print("ESPECTRO * FILTRO: ",espectro)
        f = fr.ifft2shift(espectro)
        f = fr.ifft2(f)
        self.img = Image.fromarray(f)
        #self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        resize = '%02dx%02d+100+100' % (400 + self.img.width, 100 + self.img.height)
        root.geometry(resize)

    def inversaGaussFourier(self):
        print("OPA!")
        img = Image.open('canvas.jpg')
        filtro = np.array(img)
        filtro = bk.gaussian_filter(filtro,5,0.5)
        filtro = cl.rgb2gray(filtro)
        #espectro = np.array(self.img)
        espectro = self.fouriert
        diffwidth, diffheight = ( filtro.shape[0] - espectro.shape[0] ), ( filtro.shape[1] - espectro.shape[1] )
        print("Diff: ",diffwidth,", ", diffheight)
        initw = int(round(diffwidth/2))
        finalw = diffwidth - initw
        inith = int(round(diffheight/2))
        finalh = diffheight - inith
        print("Dimensões: ", initw, ", ", finalw, ", ", inith, ", ",finalh)
        print("ESPECTRO: ",espectro.shape)
        print("FILTRO: ",filtro.shape)
        width = filtro.shape[0] - finalw
        height = filtro.shape[1] - finalh
        filtro = filtro[initw:width, inith:height]
        print(filtro.shape)
        for m in range(espectro.shape[0]):
            for n in range(espectro.shape[1]):
                if filtro[m,n] == 0:
                    espectro[m,n] = 0
                elif filtro[m,n] == 1:
                    espectro[m,n] = 1
                #invimg[m,n] = espectro[m,n] * filtro[m,n]
        f = fr.ifft2shift(espectro)
        f = fr.ifft2(f)
        self.img = Image.fromarray(f)
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        resize = '%02dx%02d+100+100' % (400 + self.img.width, 100 + self.img.height)
        root.geometry(resize)
        root.geometry(resize)

    def controllerPincelFourier(self):
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        self.controls.add(self.abacontrole)
        self.abacontrole.focus()

        s = self.pincelFourier
        print(s)
        if s == "Pincel Disco":
            self.inversaFourier()
        elif s == "Pincel Gaussiano":
            self.inversaGaussFourier()
    
    def controllerFiltroFourier(self):
        tabs = self.controls.tabs()
        self.controls.add(self.abacontrole)
        self.abacontrole.focus()
        for t in tabs:
            self.controls.hide(t)

        s = self.filtroFourier
        
        if s == "Passa Baixa":
            radius = int(self.slider2.get())
            self.passa_baixa(radius)
        elif s == "Passa Alta":
            radius = int(self.slider2.get())
            self.passa_alta(radius)
        elif s == "Passa Faixa":
            radius = int(self.slider2.get())
            radius2 = int(self.slider3.get())
            self.passa_faixa(radius, radius2)

    def fourier(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        #self.submitDraw["state"]="active"
        img = self.img
        self.old_img = img
        i = np.array(img)
        i = cl.rgb2gray(i)
        it = fr.fft2(i)
        ft = fr.fft2shift(it)
        self.fouriert = ft
        #print(self.ft.shape)
        fig = plt.figure(figsize=(5,5))
        #print(abs(ft))
        espectro = plt.imshow(abs(ft), cmap='gray')
        ax = plt.gca()
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        plt.savefig('images/ftemp.png', bbox_inches='tight')   # save the figure to file
        #plt.close(fig)
        img = Image.open('images/ftemp.png')
        fou = np.array(img)
        width = fou.shape[0] - 40
        height = fou.shape[1] - 40
        #print(fou.shape)
        fou = fou[40:width, 40:height]
        #print(fou.shape)
        #canvas = FigureCanvasTkAgg(fig,self.c)
        #canvas.show()
        #canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        #plt.savefig('images/ftemp.png', bbox_inches='tight')   # save the figure to file
        #plt.close(fig)
        #img = Image.open('images/ftemp.png')
        self.img = Image.fromarray(fou)
        #self.img = img
        
        self.c.image = ImageTk.PhotoImage(self.img)
        self.size[0] = self.img.width
        self.size[1] = self.img.height
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        resize = '%02dx%02d+100+100' % (400 + self.size[0], 100 + self.size[1])
        root.geometry(resize)
        white = (255, 255, 255)
        print('Tamanho: ',self.size)
        self.input = Image.new("RGB", (self.size), white)
        self.draw = ImageDraw.Draw(self.input)
        tabs = self.controls.tabs()
        for t in tabs:
            self.controls.hide(t)
        
        abapincel = Frame(self.controls,bg='#102027')
        abafiltros = Frame(self.controls,bg='#102027')
        title = Label(abapincel, text="Pincel", bg='#102027', fg='#FFFFFF',font="roboto 12")
        title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        pinceis = [
            "Pincel Disco",
            "Pincel Gaussiano",
        ]
        choose = StringVar()
        choose.set(pinceis[0])
        self.pincelFourier = pinceis[0]
        def add_pincel(e):
            print(e)
            self.pincelFourier = e
        pintxt = Label(abapincel, text='Tipos:',font=('roboto 12'),bg='#102027',fg='#ffffff',padx=2)
        pintxt.grid(row=1,column=0, columnspan=3, sticky=W+E)
        drop = OptionMenu(abapincel, choose, *pinceis,command=add_pincel)
        drop.grid(row=2,column=0, columnspan=3, sticky=W+E)
        raiotxt = Label(abapincel, text='Raio pincel:',font=('roboto 12'),bg='#102027',fg='#ffffff',padx=2)
        raiotxt.grid(row=3,column=0, columnspan=3, sticky=W+E)
        style = ttk.Style()
        style.configure("BW.Horizontal.TScale", foreground="black", background="#102027",padx=2)
        self.slider = ttk.Scale(abapincel,from_= 5, to = 200,command=self.changeW,orient=HORIZONTAL, style="BW.Horizontal.TScale")
        self.mcanvas = np.ones(self.size)
        self.slider.set(self.penwidth)
        self.slider.grid(row=4,column=0, columnspan=3, sticky=W+E)
        self.submitDraw = Button(abapincel, text="Aplicar Filtro",command=self.controllerPincelFourier,bg='#98ee99',fg='#000000',padx=2)
        self.submitDraw.grid(row=5,column=0, columnspan=3, sticky=W+E)

        title = Label(abafiltros, text="Filtros", bg='#102027', fg='#FFFFFF',font="roboto 12")
        title.grid(row=0,column=0,columnspan=3, sticky=W+E)
        filtros = [
            "Passa Baixa",
            "Passa Alta",
            "Passa Faixa"
        ]
        choose2 = StringVar()
        choose2.set(filtros[0])
        self.filtroFourier = filtros[0]
        filtxt = Label(abafiltros, text='Tipos:',font=('roboto 12'),bg='#102027',fg='#ffffff',padx=2)
        filtxt.grid(row=1,column=0, columnspan=3, sticky=W+E)
        
        def add_slider(e):
            print(e)
            self.filtroFourier = e
            if e == "Passa Faixa":
                num = int(self.slider2.get())
                self.slider3 = Scale(abafiltros,from_= 1, to = 190,orient=HORIZONTAL)
                self.slider3.set(1)
                self.slider3.grid(row=3,column=0, columnspan=3, sticky=W+E)
            else:
                self.slider3.grid_forget()
        self.slider2 = Scale(abafiltros,from_= 10, to = 200,orient=HORIZONTAL)
        self.slider2.set(10)
        self.slider2.grid(row=4,column=0, columnspan=3, sticky=W+E)
        self.slider3 = Scale(abafiltros,from_= 1, to = 190,orient=HORIZONTAL)
        self.slider3.set(1)
        self.submitFilter = Button(abafiltros, text="Aplicar Filtro",command=self.controllerFiltroFourier,bg='#98ee99',fg='#000000',padx=2)
        self.submitFilter.grid(row=5,column=0, columnspan=3, sticky=W+E)
        drop2 = OptionMenu(abafiltros, choose2, *filtros, command=add_slider)
        drop2.grid(row=2,column=0, columnspan=3, sticky=W+E)
        self.controls.add(abapincel, text='Pincel')
        self.controls.add(abafiltros, text='Filtros no espectro')
        abapincel.focus()
        

    

    def loadimg(self):
        #url = 'images/'+self.input.get()
        url = filedialog.askopenfilename()
        #filetypes=(("png files","*.png"),("jpg files","*.jpg"),("jpeg files","*.jpeg"),("gif files","*.gif"),("tiff files","*.tiff"),("bitmap files","*.tiff"))
        #self.input = url
        #img = Image.open('images/einstein.jpeg')
        self.img = Image.open(url)
        self.orimg = self.img
        if cl.is_grey_scale(self.img):
            i = np.array(self.img)
            i = cl.rgb2gray(i)
            self.img = Image.fromarray(i)
        self.old_img = self.img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.size[0] = self.img.width
        self.size[1] = self.img.height
        print(self.size[0],'x',self.size[1])
        resize = '%02dx%02d+100+100' % (400 + self.size[0], 100 + self.size[1])
        print(resize)
        root.geometry(resize)
        self.c.config(width=self.size[0], height=self.size[1])
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        white = (255, 255, 255)
        self.input = Image.new("RGB", (self.size), white)
        self.draw = ImageDraw.Draw(self.input)
        self.sizelbl['text'] = "Tamanho da imagem: %02dx%02d" %(self.size[0],self.size[1])

        

    def drawWidgets(self):

        self.master.resizable(width=False, height=False)
        self.master.minsize(width=600, height=300)
        self.master.configure(background='#102027')
        self.toolbar = Frame(self.master,relief='groove',bg='#37474f',pady=4)
        self.footer = Frame(self.master,relief='groove',bg='#37474f',pady=4)

        styleAbas = ttk.Style()
        styleAbas.configure("C.TNotebook", foreground="#FFFFFF", background='#FFFFFF', sticky=N+S+W+E)
        self.controls = ttk.Notebook(self.master, height=450, width=200, style="C.TNotebook")
        self.abacontrole = Frame(self.controls,bg='#102027')#2
        #iphoto = ImageTk.PhotoImage(Image.open('leaf.jpg'))
        #ilbl = Label(self.abacontrole, image=iphoto, padx=4)
        #ilbl.image = iphoto
        #ilbl.grid(row=0,column=0)
        self.controls.add(self.abacontrole, text='Início')

        desfaz = Button(self.toolbar, text="<<",command=lambda:self.undo(0),bg='#62727b',fg='#ffffff')
        desfaz.grid(row=0,column=0)
        img = ImageTk.PhotoImage(Image.open('Fs.png').resize((20,20)))
        #photo = PhotoImage(file="lapis.gif")
        imglbl = Label(self.footer, image=img, padx=4)
        imglbl.image = img # keep a reference!
        imglbl.grid(row=0,column=0,sticky=W+E)
        marklbl = Label(self.footer, text="Fotossíntese®", bg='#37474f',fg='#FFFFFF')
        marklbl.grid(row=0,column=1,sticky=W+E)
        infolbl = Label(self.footer, text="Ícaro de Lima | Thalisson Felipe", bg='#37474f',fg='#FFFFFF')
        infolbl.grid(row=0,column=2, columnspan=2,sticky=W+E)
        ufclbl = Label(self.footer, text="UFC", bg='#37474f',fg='#FFFFFF')
        ufclbl.grid(row=0,column=5,sticky=W+E)
        self.toolbar.pack(side=TOP,expand=False, fill='x')
        self.footer.pack(side=BOTTOM,expand=False, fill='x')
        self.controls.pack(side=LEFT, expand=False, fill=BOTH)
        

        self.data = Frame(self.master)
        self.topdata = Frame(self.master,bg='#102027')
        self.middledata = Frame(self.data).grid(row=0)
        self.bottomdata = Frame(self.data).grid(row=1)

        self.colorframe = Frame(self.topdata,bg='#102027')
        self.colorframe.pack(side=TOP)
        self.properties = Frame(self.topdata,bg='#102027')
        self.properties.pack(side=BOTTOM)
        strsize = "0x0"
        self.sizelbl = Label(self.properties, text=strsize,bg='#62727b',fg='#ffffff',font=('roboto 10'))
        self.sizelbl.grid(row=0,column=0)
        tab_control = ttk.Notebook(self.topdata)#1 
        self.abaRGB = Frame(tab_control)#2
        self.abaHSV = Frame(tab_control)#2
        tab_control.add(self.abaRGB, text='RGB')#3
        tab_control.add(self.abaHSV, text='HSV')
        tab_control.pack(side=BOTTOM,expand=1, fill='both')

        #SLIDERS RGB
        self.colordisplay = Canvas(self.colorframe,width=50,height=50,bg=self.color_fg)
        Label(self.colorframe, text='Cor: ',bg='#102027',fg='#ffffff',font=('roboto 12'),pady=20).grid(row=0,column=0)
        self.cordisp = self.colordisplay.create_rectangle((0, 0, 50, 50), fill="black")
        self.colordisplay.grid(row=0, column=1)
        self.sliderR = Scale(self.abaRGB,from_= 0, to = 255,width=7,command=self.changeR,orient=HORIZONTAL, fg="red",troughcolor="dark red")
        Label(self.abaRGB, text='R:',font=('roboto 12'), fg="red").grid(row=1,column=0)
        self.sliderR.grid(row=1, column=1)
        self.sliderG = Scale(self.abaRGB,from_= 0, to = 255,width=7,command=self.changeG,orient=HORIZONTAL, fg="green",troughcolor="dark green")
        Label(self.abaRGB, text='G:',font=('roboto 12'), fg="green").grid(row=2,column=0)
        self.sliderG.grid(row=2, column=1)
        self.sliderB = Scale(self.abaRGB,from_= 0, to = 255,width=7,command=self.changeB,orient=HORIZONTAL, fg="blue",troughcolor="dark blue")
        Label(self.abaRGB, text='B:',font=('roboto 12'), fg="blue").grid(row=3,column=0)
        self.sliderB.grid(row=3, column=1)

        #SLIDERS HSV
        #self.colorHSV = Canvas(self.abaHSV,width=50,height=50,bg=self.color_fg)
        #self.cordisp = self.colordisplay.create_rectangle((0, 0, 50, 50), fill="black")
        #self.colorHSV.grid(row=0, column=1)
        self.sliderH = Scale(self.abaHSV,from_= 0, to = 360,width=7,command=self.changeH,orient=HORIZONTAL, fg="red",troughcolor="dark red")
        Label(self.abaHSV, text='H(°):',font=('roboto 12'), fg="red").grid(row=1,column=0)
        self.sliderH.grid(row=1, column=1)
        self.sliderS = Scale(self.abaHSV,from_= 0, to = 100,width=7,command=self.changeS,orient=HORIZONTAL, fg="green",troughcolor="dark green")
        Label(self.abaHSV, text='S(%):',font=('roboto 12'), fg="green").grid(row=2,column=0)
        self.sliderS.grid(row=2, column=1)
        self.sliderV = Scale(self.abaHSV,from_= 0, to = 100,width=7,command=self.changeV,orient=HORIZONTAL, fg="blue",troughcolor="dark blue")
        Label(self.abaHSV, text='V(%):',font=('roboto 12'), fg="blue").grid(row=3,column=0)
        self.sliderV.grid(row=3, column=1)

        #Button(self.controls, text="Função",command=self.drawfunc).grid(row=1,column=0)
        #iconl = ImageTk.PhotoImage(file = 'icone-lapis.png')
        #iconl = iconl.subsample(5, 5) 
        loadButton = Button(self.toolbar, text="Carregar imagem",command=self.loadimg,bg='#98ee99',fg='#000000')
        loadButton.grid(row=0,column=1,sticky=W+E)
        #photo = PhotoImage(file="lapis.gif")
        #loadButton.config(image=photo, compound=LEFT)
        #pincelimg = ImageTk.PhotoImage(Image.open('icone-lapis.png').resize((40,40)))
        #photo = PhotoImage(file="lapis.gif")  
        #pincelButton = Button(self.toolbar, image = pincelimg,bg='#98ee99',fg='#000000')
        #pincelButton.image = pincelimg
        #pincelButton.grid(row=0,column=2,sticky=W+E)
        #print(os.getcwd())
        #print(os.listdir())
        self.c = Canvas(self.master,width=self.size[0],height=self.size[1],bg=self.color_bg, cursor='circle')
        self.mcanvas = np.ones(self.size)

        self.topdata.pack(side=RIGHT,expand=False)
        self.c.pack(side=TOP,expand=False)
        

        #self.data.grid(row=2, column=0)


        white = (255, 255, 255)
        self.input = Image.new("RGB", (self.size), white)
        self.draw = ImageDraw.Draw(self.input)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        filemenu = Menu(menu)
        colormenu = Menu(menu)
        effectmenu = Menu(menu)
        filtermenu = Menu(menu)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Cores',menu=colormenu)
        colormenu.add_command(label='Cor do Pincel',command=self.change_fg)
        colormenu.add_command(label='Cor do BG',command=self.change_bg)
        menu.add_cascade(label='Efeitos',menu=effectmenu)
        effectmenu.add_command(label='Aplicar Negativo',command=self.efeito_neg)
        effectmenu.add_command(label='Aplicar Logaritmo',command=self.efeito_log)
        effectmenu.add_command(label='Aplicar Gamma',command=self.efeito_gamma)
        effectmenu.add_command(label='Aplicar Sépia',command=self.efeito_sepia)
        effectmenu.add_command(label='Aplicar Threshold',command=self.efeito_threshold)
        effectmenu.add_command(label='Aplicar Eq. Histograma',command=self.efeito_hist)
        effectmenu.add_command(label='Aplicar Função',command=self.drawfunc)
        effectmenu.add_command(label='Chroma Key',command=self.control_chromakey)
        effectmenu.add_command(label='Ajuste Brilho',command=self.control_aumentarbrilho)
        effectmenu.add_command(label='Ajuste Matiz/Saturação',command=self.control_aumentarHSV)
        effectmenu.add_command(label='Histograma',command=self.histograma)
        effectmenu.add_command(label='Trans. Fourier',command=self.fourier)
        effectmenu.add_command(label='Convolução matriz',command=self.control_convmatriz)
        effectmenu.add_separator()
        menu.add_cascade(label='Filtros',menu=filtermenu)
        filtermenu.add_command(label='Filtro Média',command=self.efeito_meanfilter)
        filtermenu.add_command(label='Filtro Mediana',command=self.efeito_medianfilter)
        filtermenu.add_command(label='Filtro Média Geométrica',command=self.efeito_geometricmeanfilter)
        filtermenu.add_command(label='Filtro Média Harmônica',command=self.efeito_harmonic_meanfilter)
        filtermenu.add_command(label='Filtro Média Contra-Harmônica',command=self.efeito_contraharmonic_meanfilter)
        filtermenu.add_command(label='Filtro Gaussiano',command=self.efeito_gaussian)
        filtermenu.add_command(label='Filtro Laplaciano',command=self.efeito_laplacefilter)
        filtermenu.add_command(label='Filtro Highboost',command=self.efeito_highboost)
        #filtermenu.add_command(label='Filtro Passa Baixa',command=lambda:self.passa_baixa(100))
        #filtermenu.add_command(label='Filtro Passa Alta',command=lambda:self.passa_alta(100))
        #filtermenu.add_command(label='Filtro Passa Faixa',command=lambda:self.passa_faixa(100,400))
        #filtermenu.add_command(label='Inversa Gaussiana',command=self.inversaGaussFourier)
        filtermenu.add_command(label='Filtro Sharpen',command=self.efeito_sharpen)
        filtermenu.add_command(label='Filtro Sobel',command=self.efeito_sobel)
        menu.add_cascade(label='Opções',menu=optionmenu)
        optionmenu.add_command(label='Salvar Canvas',command=self.save)
        optionmenu.add_command(label='Limpar Canvas',command=self.clear)
        optionmenu.add_command(label='Sair',command=self.master.destroy) 
        
        

if __name__ == '__main__':
     
    root = Tk()
    main(root)
    root.geometry("1000x520+100+100")
    root.title('Fotossíntese')
    root.iconbitmap('Fs.ico')
    root.mainloop()