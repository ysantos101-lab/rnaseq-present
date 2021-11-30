#       MUST RUN IN python3
try:
    from tkinter import filedialog
    import tkinter as tk
    import tkinter.tk as ttk
    from condition import *
    from make_table import *
    from PIL import ImageTk, Image
    #from tkinter import *
except:
    print('ERRRRROR! MUST BE RUN WITH python3')
    #exit()
from tkinter import filedialog
import tkinter as tk
from condition import *
from functools import partial
from make_table import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image

global classA;classA=[]
global classB;classB=[]
global img
global p_val;p_val=float(0)
img=''


def browse_button_A():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global classA
    global folder_path
    classA=[]
    filenames = filedialog.askopenfilenames()
    classA=list(filenames)

    classA_box.delete(0,tk.END)
    for val in classA:
        classA_box.insert(tk.END,val.split('/')[-1])

    print('ClassA: ')
    print(classA)
    


def browse_button_B():
    global classB
    global folder_path
    classB=[]
    filenames = filedialog.askopenfilenames()

    #folder_path.set(filename)
    classB=list(filenames)

    classB_box.delete(0,tk.END)
    for val in classB:
        classB_box.insert(tk.END,val.split('/')[-1])

    print('ClassB: ')
    print(classB)




    
def update_display():
    print('yay again')
    global p_val
    try:
        p_val=float(p_val_box.get())
    except:
        p_val=float(0)
    print('P-value: '+str(p_val))
    print('Corr method: '+str(corr_method))

    print('class a:')
    print(classA)
    print('class b:')
    print(classB)
    
    
def run_analysis():

        print('class A IDs: ')
        print(classA)
        print('class B IDs: ')
        print(classB)

        make_my_table(classA,classB,cat.get(),catB.get())
        print('Finished making table')

#        a_cov=tk.PhotoImage(file='./output/classA_cov.png')
#        b_cov=tk.PhotoImage(file='./output/classB_cov.png')
#
#        a_cov.place(x=20,y=400)
#        b_cov.place(x=420,y=400)
#
        global p_val
        try:
            p_val=float(p_val_box.get())   
        except:
            p_val=float(0)

        if p_val==0:
            p_val=.05

        global corr_method
        try:
                corr_method=corr_method_box.get()
        except:
                corr_method="BH"

        run_edgeR(classA,classB,p_val,corr_method)


def run_edgeR(classA,classB,p_val=float(.05),corr_method="BH"):
    print('Running edgeR: ')
    subprocess.call("Rscript ./edgeR_filter.R "+str(len(classA))+" "+str(len(classB))+" "+str(p_val)+" "+corr_method+" > ./_RNA_tmp/list_DEGs.txt",shell=True)

    myFile=open('./_RNA_tmp/list_DEGs.txt','r')
    toss=myFile.readline();toss=myFile.readline()
    up_A=0;up_B=0
    for line in myFile:
        data=line.strip().split()
        if len(data)<3:
            print('line break on: ')
            print(line)
            break

        temp=''
        for val in data[1:]:
            temp+=str(val)
            temp+='\t'

        if float(data[2])>0:
            up_A+=1
        else:
            up_B+=1

        DEG_a_label.config(text="Up in classA: "+str(up_A))
        DEG_b_label.config(text="Up in classB: "+str(up_B))
        DEG_box.insert(parent='',index=tk.END,text=data[1],values=(data[2],data[3],data[4],data[5]))
    
    
    myFile.close()


    subprocess.call("sed -i 's/gene//g' ./_RNA_tmp/raw_table.txt",shell=True)

    subprocess.call("CPMconverter.py -i ./_RNA_tmp/raw_table.txt -o ./_RNA_tmp/all_cpm --log",shell=True)
    subprocess.call("python make_DEG_cpm.py",shell=True)

    subprocess.call("Rscript make_heatmap.R "+str(len(classA)),shell=True)






    #subprocess.run("eog -n ./output/volcano.png",shell=True)
    subprocess.Popen("eog -n ./output/volcano.png",shell=True)






   # img=PhotoImage(file='./_RNA_tmp/volcano.png')
   # canvas.create_Image(600,20,image=img)

    #load=tk.PhotoImage(file="./_RNA_tmp/volcano.jpg")
    #load=tk.Image(file='_RNA_tmp/volcano.png')
    #volcano_label.config(image=load)
    #photo_label=tk.Label(image=load)
    #photo_label.place(x=600,y=800)

    





root = tk.Tk()
#folder_path = StringVar()
#lbl1 = Label(master=root,textvariable=folder_path)
#lbl1.grid(row=0, column=1)
#button2 = Button(text="Browse", command=browse_button)
#button2.grid(row=0, column=3)

canvas = tk.Canvas(root)

greeting=tk.Label(text="Welcome to RNAseq-present!")
greeting.config(font=("Courier",44))
greeting.pack()
root.geometry("1200x1200")



classA_button = tk.Button(text="Class A samples",width=20,height=2,command=browse_button_A)
classB_button = tk.Button(text="Class B samples",width=20,height=2,command=browse_button_B)
classA_button.place(x=60,y=60)
classB_button.place(x=60,y=200)

classA_box=tk.Listbox(width=100)
tk.Scrollbar(classA_box,orient="vertical")
classA_box.place(x=280,y=60)
classB_box=tk.Listbox(width=100)
tk.Scrollbar(classB_box,orient="vertical")
classB_box.place(x=280,y=200)


#DEG_box=tk.Listbox(width=130,height=35)
DEG_box=ttk.Treeview(root,columns=("logFC","logCPM","FDR","P-value"))
DEG_box.heading("logFC",text="logFC");DEG_box.heading("logCPM",text="logCPM")
DEG_box.heading("FDR",text="FDR");DEG_box.heading("P-value",text="p-value")
tk.Scrollbar(DEG_box,orient="vertical")
DEG_box.place(x=60,y=600)

DEG_label=tk.Label(text="DEGs found:")
DEG_label.config(font=("Courier",14))
DEG_label.place(x=60,y=560)

DEG_a_label=tk.Label(text="Up in classA: 0")
DEG_a_label.config(font=("Courier",14))
DEG_a_label.place(x=200,y=560)
DEG_b_label=tk.Label(text="Up in classB: 0")
DEG_b_label.config(font=("Courier",14))
DEG_b_label.place(x=400,y=560)


temp=tk.Label(text="Correction Method:")
temp.config(font=("Courier",12))
temp.place(x=60,y=480)
tempF=tk.Label(text=' ( "none","BH","bonferroni" )')
tempF.config(font=("Courier",12))
tempF.place(x=20,y=500)
#global corr_method
corr_method=''
corr_values={"Bonferroni" : "1","BH" : "2","None" : "3"}
i=0;basey=430
#for (text,val) in corr_values.items():
#        temp=tk.Radiobutton(text=text,variable=corr_method,value=val)
#        temp.place(x=60,y=basey+i*30)
        #i+=1

temp=tk.Label(text="P-Value Cutoff:")
temp.config(font=("Courier",12))
temp.place(x=60,y=400)
global p_val
p_val=''
p_val_box=tk.Entry()
p_val_box.place(x=220,y=400)

global corr_method
corr_method=''
corr_method_box=tk.Entry()
corr_method_box.place(x=220,y=480)

cat_label=tk.Label(text="Class A Name: ")
cat_label.config(font=("Courier",12))
cat_label.place(x=60,y=100)
cat=tk.Entry()
cat.place(x=60,y=130)

catB_label=tk.Label(text="class B Name: ")
catB_label.config(font=("Courier",12))
catB_label.place(x=60,y=240)
catB=tk.Entry()
catB.place(x=60,y=270)

run_button=tk.Button(text="Run Analysis!!!",width=25,height=5,command=run_analysis)
run_button.place(x=420,y=430)

update_button=tk.Button(text="Update Display",width=25,height=5,command=update_display)
update_button.place(x=620,y=430)

#a_cov=tk.PhotoImage(file='./output/classA_cov.png')
#b_cov=tk.PhotoImage(file='./output/classB_cov.png')


#cov_box=tk.Label(image=a_cov)
#b_cov_box=tk.Label(image=b_cov)
#cov_box.place(x=20,y=400)
#b_cov_box.place(x=420,y=400)

try:
    img = ImageTk.PhotoImage(Image.open("./_RNA_tmp/volcano.png"))
    canvas.create_image(20,20,anchor=tk.NW,image=img)
except:
    print('couldnt find volcano, continuig:')

canvas.create_image(20,20,anchor=tk.NW,image=img)

tk.mainloop()
