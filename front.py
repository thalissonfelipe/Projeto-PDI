import imageio
import back as bk
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
        self.func = None
        self.coord = [0,0]
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint) #evento de movimento do mouse
        self.c.bind('<Button-1>',self.paintdot) #evento quando clica com botão do mouse
        self.c.bind('<ButtonRelease-1>',self.reset) #evento quando soltar o botão do mouse

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
        self.mcanvas  = np.zeros((400,400), dtype=int)

    def changeCoord(self,e):   
        self.func.c.delete(ALL)
        print(e.x, e.y) 
        if e.x < self.img.width/2 and 0 < e.y < self.img.height:
            x1, y1 = ( 0 ), ( e.y )
            x2, y2 = ( self.img.width ), ( self.old_x )
            self.old_y = e.y
        elif  0 < e.y < self.img.height:
            x1, y1 = ( 0 ), ( self.old_y )
            x2, y2 = ( self.img.width ), ( e.y )
            self.old_x = e.y
        else:
            x1, y1 = ( 0 ), ( self.old_y )
            x2, y2 = ( self.img.width ), ( self.old_x )
        #self.func.c.coords(self.line, [x1,y1,x2,y2]) OBS: É POSSÍVEL MUDAR AS COORDENADAS DE UM WIDGET
        self.func.c.create_line(x1,y1,x2,y2,width=5,fill='green',capstyle=ROUND,smooth=True)
        quad = self.func.c.create_oval((x1-2, y1+5, 8, y1 - 5), fill="green")
        #self.func.c.tag_bind(quad, '<B1-Motion>', self.changeCoord)
        quad = self.func.c.create_rectangle((x2 - 8, y2-5, x2 + 2, y2 + 5), fill="green")
        #func.c.tag_bind(quad, "<B1-Motion>", self.setColor("red"))
        #self.old_x = e.x
        #self.old_y = e.y
    
    def drawfunc(self):
        self.old_x = 0
        self.old_y = self.img.height
        self.func = Tk()
        self.func.title('Função')
        self.func.bind('<B1-Motion>',self.changeCoord)
        self.func.c = Canvas(self.func,width=self.size[0],height=self.size[1],bg=self.color_bg, cursor='circle')
        self.func.c.pack(expand=False)
        white = (255, 255, 255)
        

        x1, y1 = ( 0 ), ( self.img.height )
        x2, y2 = ( self.img.width ), ( 0 )
        self.func.c.create_line(x1,y1,x2,y2,width=5,fill='green',capstyle=ROUND,smooth=True)
        quad = self.func.c.create_oval((0, self.img.height, 10, self.img.height - 10), fill="green")
        self.coord = self.func.c.coords(quad)
        #self.func.c.tag_bind(quad, '<B1-Motion>', self.changeCoord)
        #self.func.c.bind('<ButtonRelease-1>',self.reset)
        quad = self.func.c.create_rectangle((self.img.width - 10, 0, self.img.width, 10), fill="green")
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

    def change_fg(self):  #mudando a cor foreground
        self.color_fg=colorchooser.askcolor(color=self.color_fg)[1]

    def change_bg(self):  #mudando a cor do background
        self.color_bg=colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg

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
        it = bk.negative_transform(i)
        self.img = Image.fromarray(it) 
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
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_meanfilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img)
        #i = bk.rgb2gray(i)
        it = bk.mean_filter(i,3)
        self.img = Image.fromarray(it) 
        self.c.image = ImageTk.PhotoImage(self.img)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_laplacefilter(self):
        #url = 'images/'+self.input.get()
        #url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = self.img
        i = np.array(img)
        #i = bk.rgb2gray(i)
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
        i = np.array(self.img)
        i = bk.rgb2gray(i)
        self.img = Image.fromarray(i)
        self.c.image = ImageTk.PhotoImage(self.img)
        self.size[0] = self.img.width
        self.size[1] = self.img.height
        self.c.config(width=self.size[0], height=self.size[1])
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def drawWidgets(self):
        self.controls = Frame(self.master,padx = 5,pady = 5)
        Label(self.controls, text='Raio pincel:',font=('arial 18')).grid(row=0,column=0)
        self.slider = ttk.Scale(self.controls,from_= 200, to = 5,command=self.changeW,orient=VERTICAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=0,column=1)
        #self.input = Entry(self.controls, font=('arial 10'))
        #self.input.focus()
        #self.input.grid(row=1,column=0)
        self.controls.pack(side=LEFT)

        Button(self.controls, text="Função",command=self.drawfunc).grid(row=1,column=0)
        Button(self.controls, text="Carregar imagem",command=self.loadimg).grid(row=1,column=1)
        self.c = Canvas(self.master,width=self.size[0],height=self.size[1],bg=self.color_bg, cursor='circle')
        self.mcanvas = np.zeros(self.size, dtype=int)
        self.c.pack(fill=BOTH, expand=False)

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
        effectmenu.add_command(label='Filtro Média',command=self.efeito_meanfilter)
        effectmenu.add_command(label='Filtro Laplaciano',command=self.efeito_laplacefilter)
        menu.add_cascade(label='Opções',menu=optionmenu)
        optionmenu.add_command(label='Salvar Canvas',command=self.save)
        optionmenu.add_command(label='Limpar Canvas',command=self.clear)
        optionmenu.add_command(label='Sair',command=self.master.destroy) 
        
        

if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('Fotocompra')
    root.mainloop()