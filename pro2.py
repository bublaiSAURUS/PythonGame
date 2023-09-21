from tkinter import*
import tkinter
import random
import time

sleep_time=0.01
root=Tk()
root.title("TEST")
canvas = tkinter.Canvas(root, bg='green', height=900, width=600,)
canvas.pack()
def my_score():
    my_shot=random.randint(0,6)
    if my_shot%2==0:
        loadingtext1 = canvas.create_text(450, 75,fill='Blue',)
        canvas.itemconfig(loadingtext1, text='You Scored!',font=("Arial Bold", 10),)
        canvas.after(700, lambda: canvas.delete(loadingtext1))
    else:
        loadingtext1 = canvas.create_text(450, 75,fill='Red',)
        canvas.itemconfig(loadingtext1, text='You MISSED!',font=("Arial Bold", 10),)
        canvas.after(700, lambda: canvas.delete(loadingtext1))


class Roy:
    
    
    x=random.randint(0,1)#decides whether to hit left or right
    xs=random.randint(0,6)#deviation along X-axis
    yspeed=random.randint(5,10)#Actual shot power
    i=0
    
    
    def __init__(self,master):
        self.canvas=master
        self.ball=canvas.create_oval(290,10,330,50,fill='white')
        self.gloves=canvas.create_rectangle(300,450,380,460,fill='brown')
        self.canvas.bind_all('<Right>', self.board_right)
        self.canvas.bind_all('<Left>', self.board_left)
        self.width=self.canvas.winfo_width()
        self.height=self.canvas.winfo_height()
        self.shoot()
        print(Roy.xs)
        print(Roy.yspeed)
        self.t=self.save()
        print(self.t)
    
        

    
    
    def board_right(self,event):
        x1, y1, x2, y2 = canvas.coords(self.gloves)
        dx=0
    # make sure the platform is not moved beyond right wall
        if x2 < 600:
            dx = min(600-x2, 15)
        canvas.move(self.gloves, dx, 0)
    
    def board_left(self,event):
        x1, y1, x2, y2 = canvas.coords(self.gloves)
    # make sure the platform is not moved beyond left wall
        dx=0
        if x1 > 0:
            dx = min(x1, 15)
        canvas.move(self.gloves, -dx, 0)

    
    
    
    
    def save(self):
        x1, y1, x2, y2 = canvas.coords(self.ball)
        a1,b1,a2,b2=canvas.coords(self.gloves)
        if y2 >= b1:
    # calculate center x of the ball
            cx = (x1 + x2) // 2
    # check whether save or not
            px1, _, px2, _ = canvas.coords(self.gloves)
            if px1 <= cx <= px2:
                yspeed = -2
                loadingtext1 = canvas.create_text(320, 75,fill='Blue',)
                canvas.itemconfig(loadingtext1, text='Good Save!',font=("Arial Bold", 10),)
                canvas.after(1500, lambda: canvas.delete(loadingtext1))
                return 'True'
            else:
                
                loadingtext1 = canvas.create_text(320, 75,fill='Red')
                canvas.itemconfig(loadingtext1, text='opponent Scored!',font=("Arial Bold", 10),)
                canvas.after(1500, lambda: canvas.delete(loadingtext1))
                return 'False'
        canvas.move(self.ball, Roy.xs, Roy.yspeed)
        root.update_idletasks()
        root.update()
        time.sleep(sleep_time)
        y=self.save()
        return y
    
    
    def shoot(self):
        print(Roy.x)
        if(Roy.x==1):
            Roy.xs=-Roy.xs




Roy(root)

root.mainloop()

