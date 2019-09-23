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
        print(x1,y1)
        self.mcanvas[x1][y1] = 1
        print(self.mcanvas[x1][y1])
        #self.old_x = e.x
        #self.old_y = e.y
        #x1, y1 = ( e.x - 1 ), ( e.y - 1 )
        #x2, y2 = ( e.x + 1 ), ( e.y + 1 )
        #self.c.create_oval( x1, y1, x2, y2, width=self.penwidth,fill=self.color_fg,)

    def reset(self,e):   
        self.old_x = None
        self.old_y = None
        self.mcanvas  = np.zeros((400,400), dtype=int)      

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
        url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = Image.open(url)
        i = np.array(img)
        it = bk.negative_transform(i)
        newimg = Image.fromarray(it) 
        self.c.image = ImageTk.PhotoImage(newimg)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def efeito_meanfilter(self):
        #url = 'images/'+self.input.get()
        url = self.input
        #img = Image.open('images/einstein.jpeg')
        img = Image.open(url)
        i = np.array(img)
        i = bk.rgb2gray(i)
        it = bk.mean_filter(i,3)
        newimg = Image.fromarray(it) 
        self.c.image = ImageTk.PhotoImage(newimg)
        self.c.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.c.image)
        self.c.pack()

    def loadimg(self):
        #url = 'images/'+self.input.get()
        url = filedialog.askopenfilename()
        self.input = url
        #img = Image.open('images/einstein.jpeg')
        img = Image.open(url)
        self.c.image = ImageTk.PhotoImage(img)
        self.size[0] = img.width
        self.size[1] = img.height
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

        Button(self.controls, text="Carregar imagem",command=self.loadimg).grid(row=1,column=1)
        self.c = Canvas(self.master,width=self.size[0],height=self.size[1],bg=self.color_bg, cursor='circle')
        self.mcanvas = np.zeros(self.size, dtype=int)
        self.c.pack(fill=BOTH,expand=True)

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
        effectmenu.add_command(label='Filtro Média',command=self.efeito_meanfilter)
        menu.add_cascade(label='Opções',menu=optionmenu)
        optionmenu.add_command(label='Salvar Canvas',command=self.save)
        optionmenu.add_command(label='Limpar Canvas',command=self.clear)
        optionmenu.add_command(label='Sair',command=self.master.destroy) 
        
        

if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('Fotocompra')
    root.mainloop()