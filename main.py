import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import pandas as pd
from PIL import Image, ImageTk
from threading import Thread
from playsound import playsound

###
#game_format_list=["積分賽(JACKPOT顯示)","ICM分配錦標賽","自訂義獎品錦標賽"]
game_format_list=["積分賽(JACKPOT顯示)"]
###

excel_name = ""
people = 0              #總人數
remain_people = 0       #剩餘人數
chips = 0               #總買入組數
Level = 0               #數據編號
current_level = 0       #實際目前level
one_buyin_chips = 0     #單組買入籌碼數
avg_chips = "-"         #均碼
is_data_correct = False #資料格式
game_STOP = False       #暫停
s_width, s_height = 1600 ,900
game_format = ""

def main():
    window = tk.Tk()
    window.title('麻飛亞撲克錦標賽計時器')
    window.iconbitmap('./data/logo.ico')
    window.geometry("300x150")
    window.resizable(False,False)

    #獲取賽制excel名稱
    allFileList = os.listdir('./賽制')

    #刪除副檔名
    allFile_List = []
    for i in allFileList:
        d = os.path.splitext(i)[0]
        allFile_List.append(d)
    #print(allFile_List)

    label = tk.Label(window,text='比賽結構(位於"賽制"資料夾)')
    label.place(x=45, y=10)

    def getTextInput():
        global excel_name
        excel_name = combobox.get()
        #print(excel_name)
        succeed = tk.Tk()
        succeed.title('讀取')
        succeed.geometry("200x50+800+300")
        succeed.resizable(False, False)
        try:
            global is_data_correct
            array,em0,em1,em2,em3,em4 = read_excel_func(excel_name)
            if em0 != "":
                text = em0
                is_data_correct = False
            elif em1 !="":
                text = em1
                is_data_correct = False
            elif em2 !="":
                text = em2
                is_data_correct = False
            elif em3 != "":
                text = em3
                is_data_correct = False
            elif em4 != "":
                text = em4
                is_data_correct = False
            else:
                #pd.read_excel(excel_name + str('.xlsx'))
                text = "讀取成功"
                is_data_correct = True
            label = tk.Label(succeed, text=text, fg="blue", font=('Arial', 12), width=15, height=2)
            label.pack()
        except:
            #print('讀取失敗，請重新輸入')
            label = tk.Label(succeed, text="讀取失敗,請重新輸入", fg="blue",font = ('Arial', 12),width=20,height=2)
            label.pack()
        succeed.mainloop()

    #textExample = tk.Entry(window)
    #textExample.insert(0, "8、9月賽季積分賽")
    #textExample.place(x=50, y=40)

    combobox = ttk.Combobox(window, values=allFile_List)
    combobox.place(x=50, y=30)

    label2 = tk.Label(window, text='比賽類別')
    label2.place(x=45, y=55)

    def get_game_format():
        game_format = combobox2.get()
        #print(game_format)
        return game_format

    combobox2 = ttk.Combobox(window, values=game_format_list)
    combobox2.place(x=50, y=75)

    btnRead = tk.Button(window, text="讀取", command=getTextInput)
    btnRead.place(x=220,y=26)

    def game_start():
        game_format = get_game_format()
        open_and_start(game_format)

    strbutton = tk.Button(window, text='開始', command=game_start)
    strbutton.place(x=90,y=110)

    clsbutton = tk.Button(window, text='關閉', command=window.destroy)
    clsbutton.place(x=180,y=110)


    window.mainloop()

def determination_data_is_correct():
    #資料無誤才會進行讀取
    global is_data_correct
    if is_data_correct == True:
        array = read_excel_func(excel_name)[0]
    else:
        pass
    return array

def read_excel_func(excel_name):
    # 讀取資料
    df = pd.read_excel('./賽制/' + excel_name + str('.xlsx'))

    em0, em1, em2, em3, em4 = "","","","",""

    # 找出休息級別
    break_level = df.index[(df['級別'] == "break")].tolist()

    ###判定資料是否有誤###
    # 刪除無級別的值
    df['級別'] = df['級別'].fillna('9999')
    nan_index = df.index[(df['級別'] == '9999')].tolist()
    df = df.drop(nan_index)

    # 結買是否只有一個
    over_buy_in_level = df.index[(df['結買'] == "*")].tolist()
    if len(over_buy_in_level) != 1:
        #print("截止買入只能有一個")
        em0 = "截買只能有一個"

    # 休息時間是否沒有小大盲、前注
    df['小盲'] = df['小盲'].fillna('8888')
    df['大盲'] = df['大盲'].fillna('8888')
    df['前注'] = df['前注'].fillna('8888')
    #print(df)
    array = df.values
    for x in break_level:
        if array[x][2] != '8888':
            #print("休息時間請勿填入小盲")
            em1 = "break小盲勿填"
        if array[x][3] != '8888':
            #print("休息時間請勿填入大盲")
            em2 = "break大盲勿填"
        if array[x][4] != '8888':
            #print("休息時間請勿填入前注")
            em3 = "break前注勿填"
    # 結買是否在休息時間
    if array[over_buy_in_level[0]][1] != 'break':
        em4 = "截買需在休息時間"
    #print(array)

    return array,em0,em1,em2,em3,em4

def find_overbuyin_break(excel_name):
    df = pd.read_excel('./賽制/' + excel_name + str('.xlsx'))

    # 找出截止買入級別
    over_buy_in_level = df.index[(df['級別'] == "break") & (df['結買'] == "*")].tolist()
    len(over_buy_in_level)

    # 找出休息級別
    break_level = df.index[(df['級別'] == "break")].tolist()
    len(break_level)

    return over_buy_in_level,break_level

def calculate_overbuyin_time(array=[], over_buy_in_level=[], Level=int):
    print(array)
    #print(over_buy_in_level, break_level)
    #print(Level)
    # 計算結買時間
    #print(range(Level, over_buy_in_level[0]+1))
    over_buy_in_time = 0
    if Level > over_buy_in_level[0]:
        pass
    else:
        for i in range(Level,over_buy_in_level[0]+1):
            #level_time = int(array[Level][5])
            over_buy_in_time = over_buy_in_time + int(array[i][5])
    #print(over_buy_in_time)

    return over_buy_in_time

def calculate_break_time(array=[], break_level=int, Level=int):
    # 計算休息時間
    de_array = []
    #print(len(break_level))
    for x in break_level:
        if Level < x:
            #print(x,"在此區間")
            de_array.append(x)

    #print(de_array)
    #print(range(Level,de_array[0]))
    next_break_time = 0
    if not de_array:
        pass
    else:
        for i in range(Level,de_array[0]):
            #level_time = int(array[Level][5])
            next_break_time = next_break_time + int(array[i][5])
    #print(next_break_time)
    return next_break_time

def open_and_start(game_format):
    global excel_name
    array = determination_data_is_correct()

    def to_the_next_stage():
        global Level , current_level
        Level += 1
        if Level >= len(array)-1:
            Level = len(array)-1
        current_level,small_blind,big_blind,stard,level_time,next_small_blind,next_big_blind,next_stard = update_global_variable(Level)

        print(Level, current_level)
        print("下一階段")
        countdown_alltime_stop()
        countdown_maintime(min2sec(level_time))
        if current_level == 'break':
            label_level['text'] = "休息"
            control_level_label['text'] = "break"
        else:
            label_level['text'] = "Level "+str(current_level)
            control_level_label['text'] = "Level "+str(current_level)
        if small_blind == 8888:
            pass
        else:
            currentlevel_blind['text'] = str(small_blind) + "/" + str(big_blind) + "/" + str(stard)
            control_current_level['text'] = str(small_blind) + "/" + str(big_blind) + "/" + str(stard)
        if next_small_blind == 8888:
            nextlevel_blind['text'] = "休息"
            control_next_level['text'] = "休息"
        else:
            nextlevel_blind['text'] = str(next_small_blind) + "/" + str(next_big_blind) + "/" + str(next_stard)
            control_next_level['text'] = str(next_small_blind) + "/" + str(next_big_blind) + "/" + str(next_stard)

        over_buy_in_time = calculate_overbuyin_time(array, over_buy_in_level, Level)
        if over_buy_in_time == 0:
            overbuytime['text'] = "已截止買入"
        else:
            countdown_over_buy_in_time(min2sec(over_buy_in_time))

        next_break_time = calculate_break_time(array, break_level, Level)
        if next_break_time == 0:
            breaktime['text'] = "-"
        else:
            countdown_next_break_time(min2sec(next_break_time))
        if next_small_blind == 0 and next_big_blind == 0 and next_stard == 0:
            nextlevel_blind['text'] = "-"
            control_next_level['text'] = "-"

    def to_the_previous_stage():
        global Level , current_level
        Level -= 1
        if Level < 0:
            Level = 0
        current_level,small_blind,big_blind,stard,level_time,next_small_blind,next_big_blind,next_stard = update_global_variable(Level)

        print(Level, current_level)
        print("上一階段")
        countdown_alltime_stop()
        countdown_maintime(min2sec(level_time))
        if current_level == 'break':
            label_level['text'] = "休息"
            control_level_label['text'] = "break"
        else:
            label_level['text'] = "Level " + str(current_level)
            control_level_label['text'] = "Level " + str(current_level)
        if small_blind == 8888:
            Level -= 1
            current_level, small_blind, big_blind, stard, level_time, next_small_blind, next_big_blind, next_stard = update_global_variable(Level)
            currentlevel_blind['text'] = str(small_blind) + "/" + str(big_blind) + "/" + str(stard)
            control_current_level['text'] = str(small_blind) + "/" + str(big_blind) + "/" + str(stard)
            Level += 1
            current_level, small_blind, big_blind, stard, level_time, next_small_blind, next_big_blind, next_stard = update_global_variable(Level)
        else:
            currentlevel_blind['text'] = str(small_blind) + "/" + str(big_blind) + "/" + str(stard)
            control_current_level['text'] = str(small_blind) + "/" + str(big_blind) + "/" + str(stard)
        if next_small_blind == 8888:
            nextlevel_blind['text'] = "休息"
            control_next_level['text'] = "休息"
        else:
            nextlevel_blind['text'] = str(next_small_blind) + "/" + str(next_big_blind) + "/" + str(next_stard)
            control_next_level['text'] = str(next_small_blind) + "/" + str(next_big_blind) + "/" + str(next_stard)

        over_buy_in_time = calculate_overbuyin_time(array, over_buy_in_level, Level)
        if over_buy_in_time == 0:
            overbuytime['text'] = "已截止買入"
        else:
            countdown_over_buy_in_time(min2sec(over_buy_in_time))

        next_break_time = calculate_break_time(array, break_level, Level)
        if next_break_time == 0:
            breaktime['text'] = "-"
        else:
            countdown_next_break_time(min2sec(next_break_time))

    def calculate_and_replace_avgchips(): #計算及更新均碼
        global one_buyin_chips, avg_chips, remain_people, chips
        try:
            chips * one_buyin_chips / remain_people
        except:
            pass
        else:
            avg_chips = (format(int(chips * one_buyin_chips / remain_people), ',d'))
            #print(avg_chips)
            #print(type(avg_chips))
            if avg_chips == "0":
                avg_chips = "-"
                avgchip['text'] = avg_chips
                control_avg_chip['text'] = avg_chips
            else:
                avgchip['text'] = avg_chips
                control_avg_chip['text'] = avg_chips

    def close(): #關閉兩個視窗
        control.destroy()
        game.destroy()

    #更新變數
    def update_global_variable(Level):
        global current_level
        current_level = array[Level][1]
        small_blind = int(array[Level][2])
        big_blind = int(array[Level][3])
        stard = int(array[Level][4])
        if Level == len(array)-1:
            next_small_blind = 0
            next_big_blind = 0
            next_stard = 0
        else:
            next_small_blind = int(array[Level + 1][2])
            next_big_blind = int(array[Level + 1][3])
            next_stard = int(array[Level + 1][4])
        level_time = int(array[Level][5])
        #print(current_level, small_blind, big_blind, stard, level_time)
        return current_level,small_blind,big_blind,stard,level_time ,next_small_blind,next_big_blind,next_stard

    global Level
    Level = 0
    current_level, small_blind, big_blind, stard, level_time, next_small_blind, next_big_blind, next_stard = update_global_variable(Level)

    over_buy_in_level, break_level = find_overbuyin_break(excel_name)
    over_buy_in_time = calculate_overbuyin_time(array, over_buy_in_level, Level)
    next_break_time = calculate_break_time(array, break_level, Level)

    #control = tk.Tk()
    control = tk.Toplevel()
    control.title('Control ── '+ excel_name)
    control.iconbitmap('./data/logo.ico')
    control.geometry('600x285')
    control.resizable(False, False)

    #判定比賽類別是否為空
    if game_format == "":
        control.destroy()
        messagebox.showwarning('警告', '請選擇類別!')
        #print("關閉")

    # 控制台參賽人數
    label = tk.Label(control, text='參賽人數')
    label.place(x=0, y=0)
    text0 = tk.Label(control, text=people)
    text0.place(x=100, y=0)
    def minus_people():
        global people
        people -= 1
        if people < 0:
            people = 0
        text0['text'] = people
        players['text'] = "%d/%d" % (remain_people,people)
        calculate_and_replace_avgchips()
    def plus_people():
        global people
        people += 1
        text0['text'] = people
        players['text'] = "%d/%d" % (remain_people,people)
        calculate_and_replace_avgchips()
    buttom_minus = tk.Button(control, text="-", command=minus_people)
    buttom_minus.place(x=200,y=0)
    buttom_plus = tk.Button(control, text="+", command=plus_people)
    buttom_plus.place(x=220, y=0)

    # 控制台剩餘人數
    label0 = tk.Label(control, text='剩餘人數')
    label0.place(x=0, y=40)
    text1 = tk.Label(control, text=remain_people)
    text1.place(x=100, y=40)
    def minus_remainpeople():
        global remain_people
        remain_people -= 1
        if remain_people < 0:
            remain_people = 0
        text1['text'] = remain_people
        players['text'] = "%d/%d" % (remain_people,people)
        calculate_and_replace_avgchips()
    def plus_remainpeople():
        global remain_people
        remain_people += 1
        text1['text'] = remain_people
        players['text'] = "%d/%d" % (remain_people,people)
        calculate_and_replace_avgchips()
    buttom_minus = tk.Button(control, text="-", command=minus_remainpeople)
    buttom_minus.place(x=200, y=40)
    buttom_plus = tk.Button(control, text="+", command=plus_remainpeople)
    buttom_plus.place(x=220, y=40)

    # 控制台組數
    label1 = tk.Label(control, text='組數')
    label1.place(x=0, y=80)
    text2 = tk.Label(control, text=chips)
    text2.place(x=100, y=80)
    def minus_chips():
        global chips
        chips -= 1
        if chips < 0:
            chips = 0
        text2['text'] = chips
        allchips['text'] = chips
        calculate_and_replace_avgchips()
    def plus_chips():
        global chips
        chips += 1
        text2['text'] = chips
        allchips['text'] = chips
        calculate_and_replace_avgchips()
    buttom_minus = tk.Button(control, text="-", command=minus_chips)
    buttom_minus.place(x=200, y=80)
    buttom_plus = tk.Button(control, text="+", command=plus_chips)
    buttom_plus.place(x=220, y=80)

    # 控制台單組籌碼
    def com():
        #驗證輸入值是否為數字
        try:
            int(entry0.get())  # 獲取entry0的值，轉為int，如果不能轉捕獲異常
            global one_buyin_chips
            label3.config(text=format(int(entry0.get()), ',d'))
            one_buyin_chips = int(entry0.get())
            calculate_and_replace_avgchips()
        except:
            messagebox.showwarning('警告', '請輸入數字')
    label2 = tk.Label(control, text='單組碼量')
    label2.place(x=350, y=0)

    label3 = tk.Label(control, text='-')
    label3.place(x=450, y=0)

    label4= tk.Label(control, text='輸入單組碼量')
    label4.place(x=350, y=40)

    entry0 = tk.Entry(control)
    entry0.place(x=450, y=40, width=70)
    OK = tk.Button(control, text="確定",command=com)
    OK.place(x=530, y=40)

    # 控制台上一階段
    buttom_next = tk.Button(control, text="上一階段", command=to_the_previous_stage)
    buttom_next.place(x=20, y=120)
    
    # 控制台下一階段
    buttom_pevious = tk.Button(control, text="下一階段", command=to_the_next_stage)
    buttom_pevious.place(x=100, y=120)

    # 控制台暫停
    def game_stop():
        global game_STOP
        game_STOP = True
        print("暫停")
        stop_red_line(game_STOP)
        buttom_continue['bg']="Green"
        buttom_continue['fg']="White"
        buttom_stop['bg']="White"
        buttom_stop['fg']="Black"
        control_time['fg']="Red"
    buttom_stop = tk.Button(control, text="暫停", command=game_stop,bg='Red',fg='White')
    buttom_stop.place(x=400, y=120)

    # 控制台繼續
    def game_continue():
        global game_STOP
        game_STOP = False
        print("繼續")
        stop_red_line(game_STOP)
        buttom_continue['bg'] = "White"
        buttom_continue['fg'] = "Black"
        buttom_stop['bg'] = "Red"
        buttom_stop['fg'] = "White"
        control_time['fg'] = "Black"
    buttom_continue = tk.Button(control, text="繼續", command=game_continue)
    buttom_continue.place(x=450, y=120)

    # 控制台均碼
    control_avg_chip_label = tk.Label(control, text='均碼')
    control_avg_chip_label.place(x=0, y=240)
    control_avg_chip = tk.Label(control, text='(請填入單組籌碼並按確定)')
    control_avg_chip.place(x=100, y=240)

    # 控制台主要時間
    control_time_label = tk.Label(control, text="時間")
    control_time_label.place(x=350, y=80)
    control_time = tk.Label(control, text='',font=('Rockwell Condensed', 26))
    control_time.place(x=400,y=70)

    # 控制台截買時間
    control_overrebuy_label = tk.Label(control, text='截買時間')
    control_overrebuy_label.place(x=350, y=160)
    control_overrebuy = tk.Label(control, text='')
    control_overrebuy.place(x=450, y=160)

    # 控制台休息時間
    control_next_break_label = tk.Label(control, text='下次休息時間')
    control_next_break_label.place(x=350, y=200)
    control_next_break = tk.Label(control,text='')
    control_next_break.place(x=450, y=200)

    # 控制台目前級別
    control_level_label = tk.Label(control, text="Level " + str(current_level), font=('Rockwell Condensed', 26),
                           fg='Fuchsia')
    control_level_label.place(x=250, y=110)

    # 控制台目前盲注
    control_current_level_label = tk.Label(control, text='目前盲注')
    control_current_level_label.place(x=0, y=160)
    control_current_level = tk.Label(control, text=str(small_blind)+"/"+str(big_blind)+"/"+str(stard))
    control_current_level.place(x=100, y=160)

    # 控制台下階盲注
    control_next_level_label = tk.Label(control, text='下階盲注')
    control_next_level_label.place(x=0, y=200)
    control_next_level = tk.Label(control, text=str(next_small_blind)+"/"+str(next_big_blind)+"/"+str(next_stard))
    control_next_level.place(x=100, y=200)

    # mafia logo
    mafia_label = tk.Label(control, text='Mafia Poker Bar', font=('Rockwell Condensed',12),fg='Gray')
    mafia_label.place(x=506, y=265)

    # 獲取全螢幕大小
    def get_max_xy():
        # s_width = game.winfo_screenwidth()
        # s_height = game.winfo_screenheight()
        #s_width = 1920
        #s_height = 1080
        #s_width = 4096
        #s_height = 2160
        s_width = 1366
        s_height = 768
        #print(s_width,s_height)
        return s_width,s_height

    # 更新元件位置
    def update_game_component(s_width,s_height):
        s_height = s_height
        s_width = s_width
        label_players.place(x=0, y=s_height * 1 / 10, height=s_height * 1.34 / 10 / 3, width=s_width / 4 / 3)
        players.place(x=0, y=s_height * 1.446 / 10, height=s_height * 1.34 / 10 / 3 * 2, width=s_width / 4)
        label_allchips.place(x=0, y=s_height * 2.34 / 10, height=s_height * 1.32 / 10 / 3, width=s_width / 4 / 3)
        allchips.place(x=0, y=s_height * 2.78 / 10, height=s_height * 1.34 / 10 / 3 * 2, width=s_width / 4)
        label_avgchip.place(x=0, y=s_height * 3.67 / 10, height=s_height * 1.35 / 10 / 3, width=s_width / 4 / 2.2)
        avgchip.place(x=0, y=s_height * 4.11 / 10, height=s_height * 1.34 / 10 / 3 * 2, width=s_width / 4)
        label_name.place(x=0, y=0, height=int(s_height / 10), width=int(s_width))
        label_level.place(x=s_width / 4, y=s_height / 10, height=s_height * 0.7 / 10, width=s_width / 2)
        label_time.place(x=s_width / 4, y=s_height * 1.7 / 10, height=s_height * 2.8 / 10, width=s_width / 2)
        label_overbuytime.place(x=s_width * 3 / 4, y=s_height * 1 / 10, height=s_height * 2 / 10 / 3,
                                width=s_width / 4 / 2)
        overbuytime.place(x=s_width * 3 / 4, y=s_height * 1.666 / 10, height=s_height * 2 / 10 / 3 * 2,
                          width=s_width / 4)
        label_breaktime.place(x=s_width * 3 / 4, y=s_height * 3 / 10, height=s_height * 2 / 10 / 3,
                              width=s_width / 4 / 2.5)
        breaktime.place(x=s_width * 3 / 4, y=s_height * 3.666 / 10, height=s_height * 2 / 10 / 3 * 2, width=s_width / 4)
        label_currentlevel.place(x=0, y=s_height * 5 / 10, height=s_height * 1.7 / 10 / 3, width=s_width / 5)
        currentlevel_blind.place(x=0, y=s_height * 5 / 10 + s_height * 1.7 / 10 / 3, height=s_height * 1.7 / 10 / 3 * 2,
                                 width=s_width)
        label_nextlevel.place(x=0, y=s_height * 6.7 / 10, height=s_height * 1.3 / 10 / 3, width=s_width / 5)
        nextlevel_blind.place(x=0, y=s_height * 6.7 / 10 + s_height * 1.3 / 10 / 3, height=s_height * 1.3 / 10 / 3 * 2,
                              width=s_width)
        logo.place(x=s_width / 4, y=s_height * 4.5 / 10, height=s_height / 20, width=s_width / 2)

        line_w = 4

        l1.place(x=0, y=s_height / 10, height=line_w, width=s_width)
        l2.place(x=0, y=s_height * 2.34 / 10, height=line_w, width=s_width / 4)
        l3.place(x=0, y=s_height * 3.66 / 10, height=line_w, width=s_width / 4)
        l4.place(x=s_width * 3 / 4, y=s_height * 3 / 10, height=line_w, width=s_width / 4)
        l5.place(x=0, y=s_height * 5 / 10, height=line_w, width=s_width)
        l6.place(x=s_width / 4, y=s_height / 10, height=s_height * 4 / 10, width=line_w)
        l7.place(x=s_width * 3 / 4, y=s_height / 10, height=s_height * 4 / 10, width=line_w)
        l8.place(x=0, y=s_height * 6.66 / 10, height=line_w, width=s_width)
        l9.place(x=0, y=s_height * 8 / 10, height=line_w, width=s_width)

        last_lebal.place(x=0, y=s_height * 8 / 10, height=s_height * 2 / 10 , width=s_width)

        if game_STOP==True:
            line_color = 'Red'
        else:
            line_color = 'White'
        sl1['bg'] = line_color
        sl1.place(x=s_width / 4, y=s_height / 10, height=line_w, width=s_width / 2)
        sl2['bg'] = line_color
        sl2.place(x=s_width / 4, y=s_height * 5 / 10, height=line_w, width=s_width / 2 + 4)
        sl3['bg'] = line_color
        sl3.place(x=s_width / 4, y=s_height / 10, height=s_height * 4 / 10, width=line_w)
        sl4['bg'] = line_color
        sl4.place(x=s_width * 3 / 4, y=s_height / 10, height=s_height * 4 / 10, width=line_w)

        resize = 0.8
        # 判定比賽類別
        if game_format == "積分賽(JACKPOT顯示)":
            jcakpot.place(x=s_width/10, y=s_height * 8.3 / 10, height=int(155*resize), width=int(606*resize+100))
            jackpot_number.place(x=s_width / 2+30+3, y=s_height * 8.3 / 10, height=int(155*resize), width=int(606*resize-5))

            l01.place(x=s_width / 2+30, y=s_height * 8.3 / 10, height=int(8*resize), width=int(606*resize))
            l02.place(x=s_width / 2+30, y=s_height * 8.3 / 10, height=int(155*resize), width=int(8*resize))
            l03.place(x=s_width / 2+30, y=s_height * 8.3 / 10+155-8-20-5, height=int(8*resize), width=int(606*resize))
            l04.place(x=s_width / 2+606-97-31+30, y=s_height * 8.3 / 10, height=int(155*resize), width=int(8*resize))

        elif game_format == "ICM分配錦標賽":
            # 帶入買入人數、組數，計算總獎金


            # 顯示名次獎金


            pass
        elif game_format == "自訂義獎品錦標賽":
            # 帶入excel表單


            # 顯示名次獎金、獎品


            pass

    # 控制台全螢幕功能
    def all_sceen():
        global s_width, s_height
        s_width, s_height = get_max_xy()
        game.attributes('-fullscreen', True)
        update_game_component(s_width, s_height)
        buttom_allsceen['text'] = "取消全螢幕"
        buttom_allsceen['command'] = cancel_all_sceen

    def cancel_all_sceen():
        global s_width, s_height
        s_width, s_height = 1600,900
        game.attributes('-fullscreen', False)
        update_game_component(s_width, s_height)
        buttom_allsceen['text'] = "全螢幕"
        buttom_allsceen['command'] = all_sceen

    buttom_allsceen = tk.Button(control, text="全螢幕", command=all_sceen)
    buttom_allsceen.place(x=500, y=120)

    ############ 主頁面 ############
    game = tk.Toplevel()
    #game = tk.Tk()
    game.title('Mafia Poker Bar ── '+ excel_name)

    resize_z = 0.71 * 0.85

    s_width = 1600
    s_height = 900
    #print(s_width, s_height)
    game.configure(bg='DarkCyan')
    game.resizable(False, False)
    game.iconbitmap('./data/logo.ico')

    game.geometry('{}x{}'.format(s_width,s_height))

    # 玩家
    label_players = tk.Label(game, text="Players", font=('Rockwell Condensed', int(30*resize_z*0.85)), bg="DarkCyan", fg="White")
    #label_players.place(x=0, y=s_height*1/10, height=s_height*1.34/10/3, width= s_width/4/3)

    players = tk.Label(game, text="0/0", font=('Rockwell Condensed', 52, 'bold'), bg="DarkCyan", fg="White")
    #players.place(x=0, y=s_height*1.446/10, height=s_height*1.34/10/3*2, width= s_width/4)

    # 總組數
    label_allchips = tk.Label(game, text="Rebuy", font=('Rockwell Condensed', int(30*resize_z*0.85)),bg="DarkCyan", fg="White")
    #label_allchips.place(x=0, y=s_height*2.34/10, height=s_height*1.32/10/3, width= s_width/4/3)

    allchips = tk.Label(game, text="0", font=('Rockwell Condensed', 52, 'bold'),bg="DarkCyan", fg="White")
    #allchips.place(x=0, y=s_height*2.78/10, height=s_height*1.34/10/3*2, width= s_width/4)

    # 均碼
    label_avgchip = tk.Label(game, text="Avg Stack", font=('Rockwell Condensed', int(30*resize_z*0.85)),bg='DarkCyan', fg="White")
    #label_avgchip.place(x=0, y=s_height*3.67/10, height=s_height*1.35/10/3, width= s_width/4/3)

    avgchip = tk.Label(game, text=avg_chips, font=('Rockwell Condensed', 52, 'bold'),bg='DarkCyan', fg="White")
    #avgchip.place(x=0, y=s_height*4.11/10, height=s_height*1.34/10/3*2, width= s_width/4)

    # 比賽名稱
    label_name = tk.Label(game, text=excel_name, font=('Helvetica', 52, 'bold'),bg="Black",fg="Fuchsia")
    #label_name.place(x=0,y=0, height=int(s_height/10) , width=int(s_width))

    ###比賽時間###

    #鈴鐺音效
    def play_sound_1():
        playsound('./data/ling1.mp3')
    def play_sound_2():
        playsound('./data/ling2.mp3')
    def play_sound_3():
        playsound('./data/ling3.mp3')

    #音效平行處理
    def play_thread(n):
        #n:鈴鐺響聲數量<=3
        global player_thread
        n=n
        if n == 1:
            player_thread = Thread(target=play_sound_1)
            player_thread.start()
        elif n == 2:
            player_thread = Thread(target=play_sound_2)
            player_thread.start()
        elif n == 3:
            player_thread = Thread(target=play_sound_3)
            player_thread.start()
        else:
            pass

    #倒數計時
    def countdown_maintime(count):
        global x
        # change text in label
        if count>3600:
            m, s = divmod(count, 60)
            h, m = divmod(m, 60)
            #print("%02d:%02d:%02d" % (h, m, s))
            label_time['text'] = "%01d:%02d:%02d" % (h, m, s)
            control_time['text'] = "%01d:%02d:%02d" % (h, m, s)
        else:
            m, s = divmod(count, 60)
            label_time['text'] = "%02d:%02d" % (m, s)
            control_time['text'] = "%02d:%02d" % (m, s)
            if count == 300:
                play_thread(1)
            if count == 60:
                play_thread(2)
            if count == 0:
                play_thread(3)
        #print(count)
        #print("%02d:%02d" % (m, s))

        if count > 0:
            # call countdown again after 1000ms (1s)
            if game_STOP == False:
                x = game.after(1000, countdown_maintime, count - 1)
            elif game_STOP == True:
                x = game.after(1000, countdown_maintime, count)
        else:
            #進入下一階段
            to_the_next_stage()

    def countdown_over_buy_in_time(count):
        global y
        if count > 3600:
            m, s = divmod(count, 60)
            h, m = divmod(m, 60)
            # print("%02d:%02d:%02d" % (h, m, s))
            overbuytime['text'] = "%01d:%02d:%02d" % (h, m, s)
            control_overrebuy['text'] = "%01d:%02d:%02d" % (h, m, s)
        else:
            m, s = divmod(count, 60)
            overbuytime['text'] = "%02d:%02d" % (m, s)
            control_overrebuy['text'] = "%02d:%02d" % (m, s)
        # print(count)
        # print("%02d:%02d" % (m, s))
        if count > 0:
            # call countdown again after 1000ms (1s)
            if game_STOP == False:
                y = game.after(1000, countdown_over_buy_in_time, count - 1)
            elif game_STOP == True:
                y = game.after(1000, countdown_over_buy_in_time, count)
        else:
            # 進入下一階段
            to_the_next_stage()

    def countdown_next_break_time(count):
        global z
        if count > 3600:
            m, s = divmod(count, 60)
            h, m = divmod(m, 60)
            # print("%02d:%02d:%02d" % (h, m, s))
            breaktime['text'] = "%01d:%02d:%02d" % (h, m, s)
            control_next_break['text'] = "%01d:%02d:%02d" % (h, m, s)
        else:
            m, s = divmod(count, 60)
            breaktime['text'] = "%02d:%02d" % (m, s)
            control_next_break['text'] = "%02d:%02d" % (m, s)
        # print(count)
        # print("%02d:%02d" % (m, s))
        if count > 0:
            # call countdown again after 1000ms (1s)
            if game_STOP == False:
                z = game.after(1000, countdown_next_break_time, count - 1)
            elif game_STOP == True:
                z = game.after(1000, countdown_next_break_time, count)
        else:
            # 進入下一階段
            to_the_next_stage()

    def countdown_alltime_stop():
        game.after_cancel(x)
        game.after_cancel(y)
        game.after_cancel(z)

    def min2sec(min):
        return int(min) * 60



    # level
    label_level = tk.Label(game, text="Level "+str(current_level), font=('Rockwell Condensed', int(45*resize_z), 'bold'),bg ='DarkSlateGray',fg='Yellow')
    #label_level.place(x=s_width/4,y=s_height/10, height=s_height*0.7/10 , width=s_width/2)

    # 主要時間 倒數計時
    label_time = tk.Label(game, text="", font=('Rockwell Condensed', int(220*resize_z), 'bold'),bg='DarkSlateGray',fg='Yellow')
    #label_time.place(x=s_width/4,y=s_height*1.7/10, height=s_height*2.8/10 , width=s_width/2)
    countdown_maintime(min2sec(level_time))
    #測試
    #countdown_maintime(10)

    # 截止買入時間 倒數計時
    label_overbuytime = tk.Label(game, text="Rebuy Deadline", font=('Rockwell Condensed', int(30*resize_z)),bg='DarkCyan', fg="White")
    #label_overbuytime.place(x=s_width*3/4, y=s_height*1/10, height=s_height*2/10/3, width= s_width/4/3)

    overbuytime = tk.Label(game, text="", font=('Rockwell Condensed', int(70*resize_z), 'bold'),bg='DarkCyan', fg="White")
    #overbuytime.place(x=s_width*3/4, y=s_height*1.666/10, height=s_height*2/10/3*2, width= s_width/4)
    countdown_over_buy_in_time(min2sec(over_buy_in_time))

    # 下次休息時間 倒數計時
    label_breaktime = tk.Label(game, text="Next Break", font=('Rockwell Condensed', int(30*resize_z)),bg='DarkCyan', fg="White")
    #label_breaktime.place(x=s_width*3/4, y=s_height*3/10, height=s_height*2/10/3, width= s_width/4/3)
    breaktime = tk.Label(game, text="", font=('Rockwell Condensed', int(70*resize_z), 'bold'),bg='DarkCyan', fg="White")
    #breaktime.place(x=s_width*3/4, y=s_height*3.666/10, height=s_height*2/10/3*2, width= s_width/4)
    countdown_next_break_time(min2sec(next_break_time))

    # 目前盲注級別
    label_currentlevel = tk.Label(game, text="Blind/Blind/Ante:", font=('Rockwell Condensed', int(36*resize_z)),bg = "DarkCyan",fg="Yellow")
    #label_currentlevel.place(x=0, y=s_height*5/10, height=s_height*1.7/10/3, width= s_width/5)
    currentlevel_blind = tk.Label(game, text=str(small_blind)+"/"+str(big_blind)+"/"+str(stard), font=('Rockwell Condensed', int(108*0.71), 'bold'),bg = "DarkCyan",fg='Yellow')
    #currentlevel_blind.place(x=0, y=s_height*5/10+s_height*1.7/10/3, height=s_height*1.7/10/3*2, width= s_width)

    # 下一級盲注級別
    label_nextlevel = tk.Label(game, text="Next Blinds (Ante):", font=('Rockwell Condensed', int(36*resize_z)),bg ="DarkCyan",fg="Yellow")
    #label_nextlevel.place(x=0, y=s_height*6.7/10, height=s_height*1.3/10/3, width= s_width/5)
    nextlevel_blind = tk.Label(game, text=str(next_small_blind)+"/"+str(next_big_blind)+"/"+str(next_stard), font=('Rockwell Condensed', int(65*0.71), 'bold'),bg ="DarkCyan",fg='Yellow')
    #nextlevel_blind.place(x=0, y=s_height*6.7/10+s_height*1.3/10/3, height=s_height*1.3/10/3*2, width= s_width)

    # logo
    mafia_logo = Image.open('./data/mafia_logo.png')
    tk_mafia_logo = ImageTk.PhotoImage(mafia_logo)
    logo = tk.Label(game, image=tk_mafia_logo, bg='DarkSlateGray')
    #logo.place(x=s_width / 4, y=s_height * 4.5 / 10, height=s_height / 20, width=s_width / 2)

    # 最下面色塊
    last_lebal = tk.Label(game,text='',bg ="Turquoise")

    # 判定比賽類別
    if game_format == "積分賽(JACKPOT顯示)":
        print(game_format)
        # 顯示JACKPOT logo
        jcakpot = Image.open('./data/jackpot.jpg')
        jcakpot = jcakpot.resize((606, 155))
        tk_jcakpot = ImageTk.PhotoImage(jcakpot)
        jcakpot = tk.Label(game, image=tk_jcakpot, bg='Turquoise')
        #jcakpot.place(x=s_width / 8, y=s_height * 8.1 / 10, height=155, width=606)

        # JACKPOT 金額 label
        jackpot_number = tk.Label(game, text="000,000,000", font=('Bahnschrift SemiBold SemiConden', int(96*0.8)), bg="DarkSlateGray",fg="OrangeRed")
        #jackpot_number_nuber.place(x=s_width / 4, y=s_height * 8.3 / 10, height=155, width=606)

        # 畫線
        l01 = tk.Frame(game, bg='LemonChiffon')
        l02 = tk.Frame(game, bg='LemonChiffon')
        l03 = tk.Frame(game, bg='LemonChiffon')
        l04 = tk.Frame(game, bg='LemonChiffon')

        #control新增的jackpot控制器
        label_jockpot = tk.Label(control, text='輸入JACKPOT')
        label_jockpot.place(x=350, y=240)

        def com_jackpot():
            # 驗證輸入值是否為數字
            try:
                jackpot_n = int(entry_jockpot.get())  # 獲取entry_jockpot的值，轉為int，如果不能轉捕獲異常
                jackpot_n = str(jackpot_n).zfill(9)
                jackpot_n = list(jackpot_n)
                jackpot_n.insert(3, ',')
                jackpot_n.insert(7, ',')
                jackpot_n = "".join(jackpot_n)
                jackpot_number['text'] = jackpot_n
            except:
                messagebox.showwarning('警告', '請輸入數字')

        entry_jockpot = tk.Entry(control)
        entry_jockpot.place(x=450, y=240, width=70)
        OK_jockpot = tk.Button(control, text="確定", command=com_jackpot)
        OK_jockpot.place(x=530, y=240)

    elif game_format == "ICM分配錦標賽":
        # 帶入買入人數、組數，計算總獎金


        # 顯示名次獎金


        pass
    elif game_format == "自訂義獎品錦標賽":
        # 帶入excel表單


        # 顯示名次獎金、獎品


        pass

    #畫線
    line_color = 'Snow'
    l1 = tk.Frame(game, bg=line_color)
    l2 = tk.Frame(game, bg=line_color)
    l3 = tk.Frame(game, bg=line_color)
    l4 = tk.Frame(game, bg=line_color)
    l5 = tk.Frame(game, bg=line_color)
    l6 = tk.Frame(game, bg=line_color)
    l7 = tk.Frame(game, bg=line_color)
    l8 = tk.Frame(game, bg=line_color)
    l9 = tk.Frame(game, bg=line_color)

    sl1 = tk.Frame(game)
    sl2 = tk.Frame(game)
    sl3 = tk.Frame(game)
    sl4 = tk.Frame(game)

    update_game_component(s_width, s_height)


    # 暫停特效
    def stop_red_line(game_STOP):
        global s_width, s_height
        line_w = 4
        if game_STOP==True:
            line_color = 'Red'
        else:
            line_color = 'White'
        sl1['bg'] = line_color
        sl1.place(x=s_width / 4, y=s_height / 10, height=line_w, width=s_width / 2)
        sl2['bg'] = line_color
        sl2.place(x=s_width / 4, y=s_height*5 / 10, height=line_w, width=s_width / 2+4)
        sl3['bg'] = line_color
        sl3.place(x=s_width / 4, y=s_height / 10, height=s_height * 4 / 10, width=line_w)
        sl4['bg'] = line_color
        sl4.place(x=s_width * 3 / 4, y=s_height / 10, height=s_height * 4 / 10, width=line_w)

    # 只要其中一個視窗關閉,就同時關閉兩個視窗
    control.protocol("WM_DELETE_WINDOW", close)
    game.protocol("WM_DELETE_WINDOW", close)

    tk.mainloop()


if __name__ == '__main__':
    main()

