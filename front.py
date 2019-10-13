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
        self.func.c = Canvas(self.func,width=255,height=255,bg=self.color_bg, cursor='circle')
        self.func.c.pack(expand=False)
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
        quad = self.func.c.create_rectangle((x3 - 10, y3-5, x3,y3 + 5), fill="green")
        self.coorda = [x3, y3]
        #2/3
        quad = self.func.c.create_rectangle((x4 - 10, y4-5, x4,y4 + 5), fill="green")
        self.coordb = [x4, y4]
        #1
        quad = self.func.c.create_rectangle((x2 - 10, 0, x2, 10), fill="green")
        button = Button(self.func, text="Aplicar",bg='#98ee99',fg='#000000',command=self.applyfunc)
        button.pack(side = LEFT)
        sair = Button(self.func, text="Sair",command=self.func.destroy)
        sair.pack(side = RIGHT)
        cancelar = Button(self.func, text="Cancelar",bg='#FFe0e0',fg='#000000',command=lambda:self.undo(0))
        cancelar.pack(side = RIGHT)
        #func.c.tag_bind(quad, "<B1-Motion>", self.setColor("red"))
        #print(x1, x2, y1, y2)
        
        #middle
        #quad = self.c.create_rectangle((self.img.width/3, self.img.height/3, self.img.width/3 + 10, self.img.height/3 + 10), fill="white")
        #self.c.tag_bind(quad, "<B1-Motion>", lambda x: setColor("red"))
        #quad = self.c.create_rectangle((self.img.width - 10, 0, self.img.width, 10), fill="white")
        #self.c.tag_bind(quad, "<B1-Motion>", lambda x: setColor("red"))

    def efeito_neg(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        it = bk.negative_filter(i) 
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
        hist = bk.histogram(i)
        it = bk.equalize_hist(i, hist)
        self.img = Image.fromarray(it) 
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_meanfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        self.controls.hide(self.abacontrole)
        self.abamean = Frame(self.controls,bg='#102027')
        self.controls.add(self.abamean, text='Ajustes do filtro')
        self.title = Label(self.abamean, text="Filtro da Média", font="roboto 12")
        self.title.grid(row=0,column=0,columnspan=2, sticky=W+E)
        self.text = Label(self.abamean, text="Tamanho do filtro: ")
        self.spin = Spinbox(self.abamean, values=(1,3,5,7,9), width=5)   
        self.submit = Button(self.abamean, text="Aplicar",command=self.meanfilter)
        #self.data.grid(row=0,column=0)
        self.text.grid(row=1,column=0)
        self.spin.grid(row=1,column=1)
        self.submit.grid(row=2,column=0, columnspan=2, sticky=W+E)
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
        self.controls.hide(self.abamean)
        self.controls.add(self.abacontrole)


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
        
        

    def fourierbkp(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img)
        i = cl.rgb2gray(i)
        it = fr.fft2(i)
        ft = fr.fft2shift(it)
        espectro = plt.imshow(abs(ft), cmap='gray')


        plt.savefig('images/ftemp.png', bbox_inches='tight')   # save the figure to file
        #plt.close(fig)
        img = Image.open('images/ftemp.png')
        #self.img = Image.fromarray(ft)
        self.img = img
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def fourier(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img)
        i = cl.rgb2gray(i)
        it = fr.fft2(i)
        ft = fr.fft2shift(it)
        
        fig = plt.figure(figsize=(5,5))
        print(abs(ft))
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
        print(fou.shape)
        fou = fou[40:width, 40:height]
        print(fou.shape)

        #canvas = FigureCanvasTkAgg(fig,self.c)
        #canvas.show()
        #canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        #plt.savefig('images/ftemp.png', bbox_inches='tight')   # save the figure to file
        #plt.close(fig)
        #img = Image.open('images/ftemp.png')
        self.img = Image.fromarray(fou)
        #self.img = img
        self.old_img = img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.size[0] = self.img.width
        self.size[1] = self.img.height
        self.c.config(width=self.img.width, height=self.img.height)
        self.c.create_image(self.img.width/2, self.img.height/2, anchor=CENTER, image=self.c.image)
        self.c.pack()
        white = (255, 255, 255)
        self.input = Image.new("RGB", (self.size), white)
        self.draw = ImageDraw.Draw(self.input)

    

    def loadimg(self):
        #url = 'images/'+self.input.get()
        url = filedialog.askopenfilename()
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
        resize = '%02dx%02d+100+100' % (600 + self.size[0], 300 + self.size[1]/4)
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

        #self.master.resizable(width=False, height=False)
        self.master.minsize(width=600, height=300)
        self.master.configure(background='#102027')
        self.toolbar = Frame(self.master,relief='groove',bg='#37474f',pady=4)

        styleAbas = ttk.Style()
        styleAbas.configure("C.TNotebook", foreground="#37474f", background='#102027')
        self.controls = ttk.Notebook(self.master, height=450, width=200, style="C.TNotebook")
        self.abacontrole = Frame(self.controls,bg='#102027')#2
        self.controls.add(self.abacontrole, text='Ajustes pincel')

        raiotxt = Label(self.abacontrole, text='Raio pincel:',font=('roboto 12'),bg='#102027',fg='#ffffff')
        raiotxt.grid(row=0,column=0)
        style = ttk.Style()
        style.configure("BW.Horizontal.TScale", foreground="black", background="#102027")
        self.slider = ttk.Scale(self.abacontrole,from_= 5, to = 200,command=self.changeW,orient=HORIZONTAL, style="BW.Horizontal.TScale")
        self.slider.set(self.penwidth)
        self.slider.grid(row=1,column=0, columnspan=2, sticky=W+E)
        desfaz = Button(self.toolbar, text="<<",command=lambda:self.undo(0),bg='#62727b',fg='#ffffff')
        desfaz.grid(row=0,column=0)
        self.toolbar.pack(side=TOP,expand=False, fill='x')
        self.controls.pack(side=LEFT, expand=False)

        


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
        Label(self.colorframe, text='Cor: ',bg='#102027',fg='#ffffff',font=('roboto 12')).grid(row=0,column=0)
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
        Button(self.toolbar, text="Carregar imagem",command=self.loadimg,bg='#98ee99',fg='#000000').grid(row=0,column=1,sticky=W+E)
        self.c = Canvas(self.master,width=self.size[0],height=self.size[1],bg=self.color_bg, cursor='circle')
        self.mcanvas = np.zeros(self.size, dtype=int)

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
        optionmenu = Menu(menu)
        menu.add_cascade(label='Cores',menu=colormenu)
        colormenu.add_command(label='Cor do Pincel',command=self.change_fg)
        colormenu.add_command(label='Cor do BG',command=self.change_bg)
        menu.add_cascade(label='Efeitos',menu=effectmenu)
        effectmenu.add_command(label='Aplicar Negativo',command=self.efeito_neg)
        effectmenu.add_command(label='Aplicar Eq. Histograma',command=self.efeito_hist)
        effectmenu.add_command(label='Aplicar Função',command=self.drawfunc)
        effectmenu.add_command(label='Histograma',command=self.histograma)
        effectmenu.add_command(label='Trans. Fourier',command=self.fourier)
        effectmenu.add_separator()
        effectmenu.add_command(label='Filtro Média',command=self.efeito_meanfilter)
        effectmenu.add_command(label='Filtro Laplaciano',command=self.efeito_laplacefilter)
        menu.add_cascade(label='Opções',menu=optionmenu)
        optionmenu.add_command(label='Salvar Canvas',command=self.save)
        optionmenu.add_command(label='Limpar Canvas',command=self.clear)
        optionmenu.add_command(label='Sair',command=self.master.destroy) 
        
        

if __name__ == '__main__':
     
    root = Tk()
    main(root)
    root.geometry("1000x450+100+100")
    root.title('Fotossíntese')
    root.iconbitmap('Fs.ico')
    root.mainloop()