import imageio
import back as bk
import colors as cl
from tkinter import *
from tkinter import ttk, colorchooser
from PIL import ImageTk, Image, ImageDraw
import numpy as np


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
        self.c.bind('<B1-Motion>',self.paint) #evento de movimento do mouse
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
        self.c.create_line(x1,y1,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)
        r = float(self.penwidth)
        r = round(r)
        r = int(r)
        self.draw.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=self.color_fg)
        
        #self.old_x = e.x
        #self.old_y = e.y
        #x1, y1 = ( e.x - 1 ), ( e.y - 1 )
        #x2, y2 = ( e.x + 1 ), ( e.y + 1 )
        #self.c.create_oval( x1, y1, x2, y2, width=self.penwidth,fill=self.color_fg,)

    def reset(self,e):   
        self.old_x = None
        self.old_y = None
        #self.mcanvas  = np.zeros((400,400), dtype=int)

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
        quad = self.func.c.create_rectangle((x3 - 10, y3, x3,y3 + 10), fill="green")
        self.coorda = [x3, y3]
        #2/3
        quad = self.func.c.create_rectangle((x4 - 10, y4, x4,y4 + 10), fill="green")
        self.coordb = [x4, y4]

        quad = self.func.c.create_rectangle((x2 - 8, y2-5, x2 + 2, y2 + 5), fill="green")

        self.points = [x1,255-y1,x3,255-y3,x4,255-y4,x2,255-y2]
        #self.points = [x1,255 - y1,x2,255 - y2]
        print(self.points)
        self.getfunc(self.points,20)
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
        print(int(slope*x + intercept))
 
        #P = [0, 0] 
        #Q = [100, 100]
        #a = Q[1] - P[1] 
        #b = P[0] - Q[0]  
        #c = a*(P[0]) + b*(P[1])   
    
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
        self.getfunc(self.points,20)
        #0
        quad = self.func.c.create_oval((0, y1, 10, y1 - 10), fill="green")
        #self.coord = self.func.c.coords(quad)
        #self.func.c.tag_bind(quad, '<B1-Motion>', self.changeCoord)
        #self.func.c.bind('<ButtonRelease-1>',self.reset)
        #1/3
        quad = self.func.c.create_rectangle((x3 - 10, y3, x3,y3 + 10), fill="green")
        self.coorda = [x3, y3]
        #2/3
        quad = self.func.c.create_rectangle((x4 - 10, y4, x4,y4 + 10), fill="green")
        self.coordb = [x4, y4]
        #1
        quad = self.func.c.create_rectangle((x2 - 10, 0, x2, 10), fill="green")
        #func.c.tag_bind(quad, "<B1-Motion>", self.setColor("red"))
        #print(x1, x2, y1, y2)
        
        #middle
        #quad = self.c.create_rectangle((self.img.width/3, self.img.height/3, self.img.width/3 + 10, self.img.height/3 + 10), fill="white")
        #self.c.tag_bind(quad, "<B1-Motion>", lambda x: setColor("red"))
        #quad = self.c.create_rectangle((self.img.width - 10, 0, self.img.width, 10), fill="white")
        #self.c.tag_bind(quad, "<B1-Motion>", lambda x: setColor("red"))


    def changeW(self,e): #mudar raio do pincel
        self.penwidth = e      

    def clear(self):
        self.c.delete(ALL)

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
        #self.colordisplay['bg'] = r,g,b
    
    def changeG(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        cor = '#%02x%02x%02x' % (self.old_red, e, self.old_blue)
        self.colordisplay.itemconfig(self.cordisp, fill=cor)
        self.old_green = e

    def changeB(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        cor = '#%02x%02x%02x' % (self.old_red, self.old_green, e)
        self.colordisplay.itemconfig(self.cordisp, fill=cor)
        self.old_blue = e

    def changeH(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        print("h: ",  e, " s: ", self.old_sat, " v: ",  self.old_val)
        rgb = cl.hsv2rgb(e, self.old_sat, self.old_val)
        print("r: ",  rgb[0], " g: ", rgb[1], " b: ",  rgb[2])
        cor = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
        print(cor)
        self.colorHSV.itemconfig(self.cordisp, fill=cor)
        self.old_hue = e
        #self.colordisplay['bg'] = r,g,b
    
    def changeS(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        print("h: ",  self.old_hue, " s: ", e, " v: ",  self.old_val)
        rgb = cl.hsv2rgb(self.old_hue, e, self.old_val)
        print("h: ", rgb[0], " s: ", rgb[1], " v: ",  rgb[2])
        cor = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
        print(cor)
        self.colorHSV.itemconfig(self.cordisp, fill=cor)
        self.old_sat = e

    def changeV(self,e):  #mudando a cor foreground
        e = int(round(float(e)))
        print("h: ",  self.old_hue, " s: ", self.old_sat, " v: ",  e)
        rgb = cl.hsv2rgb(self.old_hue, self.old_sat, e)
        print("r: ",  rgb[0], " g: ", rgb[1], " b: ",  rgb[2])
        cor = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
        print(cor)
        self.colorHSV.itemconfig(self.cordisp, fill=cor)
        self.old_val = e
    

    def save(self):  #mudando a cor do background
        filename = "canvas.jpg"
        print(np.array(self.input))
        self.input.save(filename)

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
        self.title = Label(self.middledata, text="Filtro da Média", font="roboto 12")
        self.title.pack()
        self.text = Label(self.bottomdata, text="Tamanho do filtro: ")
        self.spin = Spinbox(self.bottomdata, values=(3,5,7,9), width=5)   
        self.submit = Button(self.bottomdata, text="Aplicar",command=self.meanfilter)
        self.text.pack(side=TOP, padx=5, pady=5)
        self.spin.pack(side=TOP, pady=5)
        self.submit.pack(side=TOP, padx=5, pady=5)
        

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
        self.title.pack_forget()
        self.spin.pack_forget()
        self.submit.pack_forget()
        self.text.pack_forget()

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

    def loadimg(self):
        #url = 'images/'+self.input.get()
        url = filedialog.askopenfilename()
        self.input = url
        #img = Image.open('images/einstein.jpeg')
        self.img = Image.open(url)
        self.orimg = self.img
        i = np.array(self.img)
        i = colors.rgb2gray(i)
        self.img = Image.fromarray(i)
        self.old_img = self.img
        self.c.image = ImageTk.PhotoImage(self.img)
        self.size[0] = self.img.width
        self.size[1] = self.img.height
        print(self.size[0],'x',self.size[1])
        resize = '%02dx%02d+100+100' % (600 + self.size[0], 300 + self.size[1]/3)
        print(resize)
        root.geometry(resize)
        self.c.config(width=self.size[0], height=self.size[1])
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def drawWidgets(self):
        #self.master.resizable(width=False, height=False)
        self.controls = Frame(self.master,padx = 5,pady = 5)
        Label(self.controls, text='Raio pincel:',font=('arial 18')).grid(row=0,column=0)
        self.slider = ttk.Scale(self.controls,from_= 200, to = 5,command=self.changeW,orient=VERTICAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=0,column=1)
        #self.input = Entry(self.controls, font=('arial 10'))
        #self.input.focus()
        #self.input.grid(row=1,column=0)
        self.controls.pack(side=LEFT, expand=False)


        self.data = Frame(self.controls)
        self.topdata = Frame(self.master)
        self.middledata = Frame(self.data).grid(row=0)
        self.bottomdata = Frame(self.data).grid(row=1)

        
        tab_control = ttk.Notebook(self.topdata)#1 
        self.abaRGB = ttk.Frame(tab_control)#2
        self.abaHSV = ttk.Frame(tab_control)#2
        tab_control.add(self.abaRGB, text='RGB')#3
        tab_control.add(self.abaHSV, text='HSV')
        tab_control.pack(expand=1, fill='both')

        #SLIDERS RGB
        self.colordisplay = Canvas(self.abaRGB,width=50,height=50,bg=self.color_fg)
        Label(self.abaRGB, text='Cor: ',font=('roboto 12')).grid(row=0,column=0)
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
        self.colorHSV = Canvas(self.abaHSV,width=50,height=50,bg=self.color_fg)
        Label(self.abaHSV, text='Cor: ',font=('roboto 12')).grid(row=0,column=0)
        self.cordisp = self.colorHSV.create_rectangle((0, 0, 50, 50), fill="black")
        self.colorHSV.grid(row=0, column=1)
        self.sliderH = Scale(self.abaHSV,from_= 0, to = 360,width=7,command=self.changeH,orient=HORIZONTAL, fg="red",troughcolor="dark red")
        Label(self.abaHSV, text='H:',font=('roboto 12'), fg="red").grid(row=1,column=0)
        self.sliderH.grid(row=1, column=1)
        self.sliderS = Scale(self.abaHSV,from_= 0, to = 100,width=7,command=self.changeS,orient=HORIZONTAL, fg="green",troughcolor="dark green")
        Label(self.abaHSV, text='S:',font=('roboto 12'), fg="green").grid(row=2,column=0)
        self.sliderS.grid(row=2, column=1)
        self.sliderV = Scale(self.abaHSV,from_= 0, to = 100,width=7,command=self.changeV,orient=HORIZONTAL, fg="blue",troughcolor="dark blue")
        Label(self.abaHSV, text='V:',font=('roboto 12'), fg="blue").grid(row=3,column=0)
        self.sliderV.grid(row=3, column=1)

        Button(self.controls, text="Função",command=self.drawfunc).grid(row=1,column=0)
        Button(self.controls, text="Carregar imagem",command=self.loadimg).grid(row=1,column=1)
        self.c = Canvas(self.master,width=self.size[0],height=self.size[1],bg=self.color_bg, cursor='circle')
        self.mcanvas = np.zeros(self.size, dtype=int)

        self.topdata.pack(side=RIGHT,expand=False)
        self.c.pack(side=BOTTOM,expand=False)
        self.data.grid(row=2, column=0)


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
    root.geometry("600x300+100+100")
    root.title('Fotocompra')
    root.mainloop()