
                                                #      Game Window Creation     #
from tkinter import*
import random

def center(master):
	master.update_idletasks()
	width = master.winfo_screenwidth()
	height = master.winfo_screenheight()
	size = tuple(int(_) for _ in master.geometry().split('+')[0].split('x'))
	x = width/2 - size[0]/2
	y = height/2 - size[1]/2 - 35
	master.geometry("%dx%d+%d+%d" % (size + (x, y))) 
	
root = Tk()
root.resizable(width = False, height = False)
root.title("Flappy Bird Beta")
root.geometry('550x700')

top = Canvas(root, width = 550, height = 700, background = "#4EC0CA", bd=0, highlightthickness=0)
top.pack()
                                                            



                                         #       List Of Constants Needed for the Program      #

TIMESPAN = 20     # Speed of overall game. Similar to frame speed
SCORE = -1          
PLAYER_POS_Y = 200    # height at which bird is situated initially
OBSTACLE_POS = 550	  # X coordinate of obstacle
PATHWAY = 0           # Position of gaps between obstacles
CHECK_STOP = False	  # variable to store status of bird. Becomes True when bird crashes

HIGH_SCORE = 0        
HIGH_SCORE2=0         #2nd best score
HIGH_SCORE3=0         #3rd best score

Ymax = 0              #Maximum number of consecutive upward jumps
final_obstacle = Game_HighScore = Final_Score = None    # Labels for: i) last obstacle where the bird crashed  ii) Overall Highest Score  iii) Score at the end
Leaderboard_value1=Leaderboard_value2=Leaderboard_value3=None  # Labels for various parts of leader board


                                      #    Player character introduced and score panel made    #




img = PhotoImage(file="bird.gif")
player = top.create_image(100, PLAYER_POS_Y, image=img)

Top_Obs = top.create_rectangle(OBSTACLE_POS, 0, OBSTACLE_POS + 100, PATHWAY, fill="#74BF2E", outline="#74BF2E")  # Obstacle above 
Bottom_Obs = top.create_rectangle(OBSTACLE_POS, PATHWAY + 200, OBSTACLE_POS + 100, 700, fill="#74BF2E", outline="#74BF2E") # obstacle below
score_widget = top.create_text(15, 45, text="0", font='Impact 60', fill='#ffffff', anchor=W)  #score display at the top left corner


                                                            


                                                #  All Functions needed for the game  #


def restart():
	global OBSTACLE_POS
	global PLAYER_POS_Y
	global SCORE
	global CHECK_STOP
	global TIMESPAN

	PLAYER_POS_Y = 200
	OBSTACLE_POS = 550
	SCORE = -1
	TIMESPAN = 20
	CHECK_STOP = False
	top.delete(Final_Score)
	top.delete(Final_obstacle)
	top.delete(Game_HighScore)
	top.delete(Leaderboard_value1)
	top.delete(Leaderboard_value2)
	top.delete(Leaderboard_value3)
	create_Path()
	root.after(TIMESPAN, gravity)
	root.after(TIMESPAN, Game_Play)
	root.after(TIMESPAN, detectCollision)




                                             #  Functions responsible for Player motion #
def gravity():
	global PLAYER_POS_Y
	global CHECK_STOP

	PLAYER_POS_Y += 8       #downward falling movement
	if PLAYER_POS_Y >= 700: 
		PLAYER_POS_Y = 700
	top.coords(player, 100, PLAYER_POS_Y)
	if CHECK_STOP == False: root.after(TIMESPAN,gravity)    #to make objects appear in smooth motion.

def move_player_up(event = None):
    global PLAYER_POS_Y  
    global Ymax
    global CHECK_STOP
        
    if CHECK_STOP == False: 
        PLAYER_POS_Y -= 20          #for upward motion
        if PLAYER_POS_Y <= 0: PLAYER_POS_Y = 0    #when bird touches the window top
        top.coords(player, 100, PLAYER_POS_Y)
        if Ymax < 5:
            Ymax += 1
            root.after(TIMESPAN, move_player_up)                  
        else: 
            Ymax = 0
    else: 
        restart()





                                            #  Functions associated with handling score  #
def score_record():
	global SCORE
	text_file=open("leaderboard.txt", "a")     # File for saving scores 
	text_file.write(str(SCORE))
	text_file.write('\n')
	text_file.close

def displayScore():
	global Final_obstacle
	global Final_Score
	global Game_HighScore
	global Leaderboard_value1
	global Leaderboard_value2
	global Leaderboard_value3
	Final_obstacle = top.create_rectangle(0, 0, 550, 700, fill='#4EC0CA')
	Final_Score = top.create_text(15, 200, text="Your score: " + str(SCORE), font='Impact 50', fill='#ffffff', anchor=W)
	f=open("leaderboard.txt")            
	contents=f.readlines()
	f.close
	p=[]
	for line in contents:
		p.append(int(line.strip()))
	p.sort(reverse=True)
	HIGH_SCORE=p[0]
	HIGH_SCORE2=p[1]
	HIGH_SCORE3=p[2]
	Leaderboard_value1 = top.create_text(15, 280, text="Leaderboard:",font='Impact 50', fill='#ffffff', anchor=W)
	Game_HighScore = top.create_text(15, 360, text= str(HIGH_SCORE), font='Impact 50', fill='#ffffff', anchor=W)
	Leaderboard_value2 = top.create_text(15, 440, text= str(HIGH_SCORE2), font='Impact 50', fill='#ffffff', anchor=W)
	Leaderboard_value3 = top.create_text(15, 520, text=str(HIGH_SCORE3),font='Impact 50',fill='#ffffff', anchor=W)


                                               #  Vital functions for actual gameplay  #

def create_Path():
	global PATHWAY   
	global SCORE	 
	global TIMESPAN		
	SCORE += 1 			
	top.itemconfig(score_widget, text=str(SCORE))	#picks a random height where the path would appear	
	PATHWAY = random.randint(50, 500)				
	if SCORE % 5 == 0 and SCORE != 0: 			 # speeds the game up each time the score becomes divisible by 5
		TIMESPAN-=1
	

create_Path()


def Game_Play():
	global OBSTACLE_POS
	global PATHWAY
	global CHECK_STOP

	OBSTACLE_POS -= 5     #Adding and moving the obstacles here
	top.coords(Top_Obs, OBSTACLE_POS, 0, OBSTACLE_POS + 100, PATHWAY)
	top.coords(Bottom_Obs, OBSTACLE_POS, PATHWAY + 200, OBSTACLE_POS + 100, 700)
	
	if OBSTACLE_POS < -100: 
		OBSTACLE_POS = 550
		create_Path()
	# if the bird has not crashed then calls itself and runs the game again
	if CHECK_STOP == False: root.after(TIMESPAN, Game_Play) 


def detectCollision():
	global CHECK_STOP                   #falls below                    #crashes above
	if (OBSTACLE_POS < 150 and (PLAYER_POS_Y < PATHWAY + 45 or PLAYER_POS_Y > PATHWAY + 175)):
	#if wall has reached bird or not    
    #NOTICE: The bird itself is stationary. This checks if obstacle reaches the bird, if yes then checks whether the jump of the bird falls in the allocated gap among the obstacles. 
		CHECK_STOP = True
		score_record()
		displayScore()
	if CHECK_STOP == False: 
		root.after(TIMESPAN, detectCollision)



                                           #  Additional Functions associated with gameplay  #




#pausing the game

def pause(event):
	global CHECK_STOP
	if CHECK_STOP==False:
		CHECK_STOP=True



#saving game data

def halt_save_data(event):
	global OBSTACLE_POS
	global PLAYER_POS_Y
	global SCORE
	global CHECK_STOP
	global TIMESPAN
	global PATHWAY
	lines=[OBSTACLE_POS,PLAYER_POS_Y,SCORE,CHECK_STOP,TIMESPAN,PATHWAY]
	if CHECK_STOP==False:
		CHECK_STOP=True
	displayScore()
	with open("save.txt",'w')as f:          # File for saving game details
		for line in lines:
			f.write(str(line))          
			f.write('\n')



#both the following functions are for reloading saved game
def reload_game2():	
	global OBSTACLE_POS
	global PLAYER_POS_Y
	global SCORE
	global CHECK_STOP
	global TIMESPAN
	global PATHWAY
	f=open("save.txt")   
	contents=f.readlines()
	f.close()
	p=[]
	for line in contents:
		p.append(line.strip())
	OBSTACLE_POS=int(p[0])
	PLAYER_POS_Y=int(p[1])
	SCORE=int(p[2])
	if(p[3]=="False"):
		CHECK_STOP=False
	else:
		CHECK_STOP=True
	TIMESPAN=int(p[4])
	PATHWAY=int(p[5])

	top.delete(Final_Score)
	top.delete(Final_obstacle)
	top.delete(Game_HighScore)
	top.delete(Leaderboard_value1)
	top.delete(Leaderboard_value2)
	top.delete(Leaderboard_value3)
	top.itemconfig(score_widget, text=str(SCORE))
	root.after(TIMESPAN, gravity)
	root.after(TIMESPAN, Game_Play)
	root.after(TIMESPAN, detectCollision)


def reload_game1(event):
	reload_game2()


                                              # Special Features for the rule-breakers ;) #
#cheat button
def cheat_button(event):
	global SCORE
	SCORE=SCORE+10000000000
	top.itemconfig(score_widget, text=str(SCORE))

#boss_key
def boss_key(event):
	global CHECK_STOP
	if CHECK_STOP==False:
		CHECK_STOP=True
	root2 = Tk()
	root2.resizable(width = False, height = False)
	root2.title("Notepad")
	root2.geometry('1300x650')
	root2.mainloop()


                                              # Control center of the entire game #

def caller(event):
	global CHECK_STOP
	CHECK_STOP=False
	root.after(TIMESPAN, gravity)
	root.after(TIMESPAN, Game_Play)
	root.after(TIMESPAN, detectCollision)



                                        #   List of all bound keys needed for gameplay  #

root.bind("<Up>", move_player_up)          # For upward motion
root.bind("p",pause)                       # For pausing
root.bind("u",caller)                      # For unpause
root.bind("s",halt_save_data)              # For saving game data
root.bind("r",reload_game1)                # For reloading saved game
root.bind("c",cheat_button)                # For implementing Cheat Code
root.bind("b",boss_key)                    # For implementing boss key
caller(root)
root.mainloop()