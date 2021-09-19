from tkinter import *
import random
from pygame import mixer
import math
import time
window = Tk()
mixer.init()

# ------------------ Set window configurations ----------------------
window.title("Lightning Algorithm")

width_of_window = 620
height_of_window = 640
offset_y = 40

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_offset = (screen_width/2) - (width_of_window/2)
y_offset = (screen_height/2) - (height_of_window/2) - offset_y

window.geometry(f"{width_of_window}x{height_of_window}+{int(x_offset)}+{int(y_offset)}")  # width x height + x_offset + y_offset
window.resizable(width=False, height=False)
window.configure(bg="black")

# ------------------------- Label on the top ----------------------------
# label_1 = Label(window, text="⚡Lightning⚡", bg="black", fg="#ffaa00",pady=8, font="Verdana 15 bold")
# label_1.pack()

# -------------------------- Set Config --------------------------------------
canvas = Canvas(window, width=550, height=590, bg="black", bd=0, highlightthickness=0)
canvas.grid(row=0, column=0)
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
grid_pts = []
vis_grid_pts = []

# rows = 30
# columns = 28
# length = 20
rows = 45
columns = 42
length = 13
pp = 42
qp = 35
pad_box = 0.51
fade_time = 15
pow_num = 9
runs = 5

def run_it():
    # ----------------------------- Grid Draw ------------------------------------

    def print_grid():
        global grid_pts
        for i in range(0, ((rows-1)*length)+1, length):
            for j in range(0, ((columns-1)*length)+1, length):
                details = grid_pts[int(i/length)][int(j/length)]
                if(details[1]==1):
                    canvas.create_line(j, i, j+length, i, fill="white", width=1)
                if(details[2]==1):
                    canvas.create_line(j, i, j, i+length, fill="white", width=1)

    def draw_grid():
        global grid_pts
        global vis_grid_pts
        grid_pts = []
        vis_grid_pts = []
        choice_list_p = [1]*pp + [0]*(100-pp)
        choice_list_q = [1]*qp + [0]*(100-qp)
        for i in range(rows):
            grid_pts.append([])
            vis_grid_pts.append([])
            for j in range(columns):
                t_i = 0
                r_i = 0
                b_i = 0
                l_i = 0
                ver = False
                if(i==0):
                    t_i = -1
                if(j==0):
                    l_i = -1
                if(i==rows-1):
                    b_i = -1
                    ver = True
                if(j==columns-1):
                    r_i = -1
                    ver = True
                if(t_i!=-1):
                    t_i=grid_pts[i-1][j][2] 
                if(l_i!=-1):
                    l_i=grid_pts[i][j-1][1] 
                if(r_i!=-1):
                    r_i=random.choice(choice_list_q)
                if(b_i!=-1):
                    b_i=random.choice(choice_list_p)
                grid_pts[i].append([t_i,r_i,b_i,l_i])
                vis_grid_pts[i].append(ver)
        print_grid()
        
    draw_grid()

    # ----------------------------- Solving ------------------------------------
    start_x = ((columns-2)*length)/2
    start_y = 0
    rr = canvas.create_rectangle(start_x+pad_box, start_y+pad_box, start_x+length-pad_box, start_y+length-pad_box, fill="yellow")
    q = []
    q.append([[start_y, start_x, -1]])
    vis_grid_pts[int(start_y/length)][int(start_x/length)] = True
    found = False

    def get_nxt_idx(x, y, idx):
        ans = []
        v = False
        # bottom
        if(grid_pts[x+1][y][1]==0):
            if(x>=rows-2):
                v = True
                # ans.append([(x+1)*20, y*20, idx])
                return ans, v
            elif(vis_grid_pts[x+1][y]==False):
                vis_grid_pts[x+1][y]=True
                ans.append([(x+1)*length, y*length, idx])
        # top
        if(x!=0 and grid_pts[x][y][1]==0 and vis_grid_pts[x-1][y]==False):
            vis_grid_pts[x-1][y]=True
            ans.append([(x-1)*length, y*length, idx])
        # left
        if(y!=0 and grid_pts[x][y][2]==0 and vis_grid_pts[x][y-1]==False):
            vis_grid_pts[x][y-1]=True
            ans.append([x*length, (y-1)*length, idx])
        # right
        if(y!=columns-2 and grid_pts[x][y+1][2]==0 and vis_grid_pts[x][y+1]==False):
            vis_grid_pts[x][y+1]=True
            ans.append([x*length, (y+1)*length, idx])
        return ans, v

    temp = []
    g = 0

    while(len(q[g])!=0 and not found):
        # print("-------------ok-------------")
        for i in range(len(q[g])):
            r = q[g][i]
            # print(r)
            idx_x = int((r[0])/length)
            idx_y = int((r[1])/length)
            poss_idx, found = get_nxt_idx(idx_x, idx_y, i)
            temp += poss_idx
            if(found):
                break
        g+=1
        if(found):
            canvas.update()
            break
        q.append(temp)
        temp = []
        canvas.update()
        

    # ------------------- Lightning effect ----------------------

    def print_rec(l):
        ll = []
        for j in range(len(l)):
            time.sleep(0.0000005)
            t = canvas.create_rectangle(l[j][1]+pad_box, l[j][0]+pad_box, l[j][1]+length-pad_box, l[j][0]+length-pad_box, fill="yellow")
            ll.append(t)
            canvas.update()
        return ll

    def print_rec_again(l):
        ll = []
        for j in range(len(l)):
            t = canvas.create_rectangle(l[j][1]+pad_box, l[j][0]+pad_box, l[j][1]+length-pad_box, l[j][0]+length-pad_box, fill="yellow")
            ll.append(t)
            canvas.update()
        return ll

    def del_rec(l_id):
        for i in l_id:
            canvas.delete(i)
        canvas.update()
        
    def del_rec_fade(l):
        temp_id1 = []
        cc = 255
        while(cc>=0):
            if cc>= 16:
                c = hex(cc)[-2:]
            else:
                c = "0" + hex(cc)[-1:]
            for j in range(len(l)):
                t = canvas.create_rectangle(l[j][1]+pad_box, l[j][0]+pad_box, l[j][1]+length-pad_box, l[j][0]+length-pad_box, fill=f"#{c}{c}00")
                temp_id1.append(t)
                canvas.update()
            cc -= fade_time
        del_rec(temp_id1)
        
    # ------------------- Driver Code if found solution --------------------
    g = 1
    temp1 = []
    temp2 = []
    if(q[-1]==[]):
        q.pop()

    # for i in q:
    #     print(i)

    if(found):
        mixer.music.load("rain.wav")
        mixer.music.play()
        canvas.delete(rr)
        
        while(g!=len(q)):
            time.sleep(0.09)
            poss_idx = q[g][:]
            poss_idx.sort(reverse = True, key=lambda x: x[0])
            for j in range(len(poss_idx)):
                if(poss_idx[0][0]==0):
                    c = 255
                else:
                    c = int((math.pow(poss_idx[j][0]/poss_idx[0][0], pow_num))*255)
                if c<=15:
                    c = "0"+hex(c)[-1:]
                else:
                    c = hex(c)[-2:]
                c = f"#{c}{c}00"
                t = canvas.create_rectangle(poss_idx[j][1]+pad_box, poss_idx[j][0]+pad_box, poss_idx[j][1]+length-pad_box, poss_idx[j][0]+length-pad_box, fill=c)
                temp2.append(t)
            for i in range(len(temp1)):
                canvas.delete(temp1[i])
            temp1 = temp2[:]
            temp2 = []
            g+=1
            canvas.update()
            
        for i in range(1, len(temp1)):
            canvas.delete(temp1[i])
        canvas.update()

        mixer.music.pause()   
        mixer.music.load("thunder.wav")
        mixer.music.play()
        
        temp = []
        temp.append(poss_idx[0])
        gg = poss_idx[0][2]
        g = len(q)-2
        while(g>=0):
            temp.append(q[g][gg])
            gg = q[g][gg][2]
            g-=1
        # print(temp)
        
        canvas.delete(temp1[0])
        temp_id = print_rec(temp)
        time.sleep(0.07)
        del_rec(temp_id)
        time.sleep(0.1)

        temp_id = print_rec_again(temp)
        time.sleep(0.5)
        del_rec(temp_id)
        del_rec_fade(temp)
        
        mixer.music.pause()   
        
    else:
        return
    
while(runs>=1):
    runs -= 1
    canvas.delete("all")
    run_it()
        
mixer.music.stop()

# ----------------------------- Window display Loop ------------------------------------
time.sleep(1.5)
window.destroy()

window.mainloop()