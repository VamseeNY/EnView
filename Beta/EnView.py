import flet as ft
import json 
import os
import subprocess
import time

sysdir=os.path.expanduser("~")


def main(page: ft.Page):
    page.padding=50
    page.scroll=ft.ScrollMode.AUTO
    page.title="EnView"
    page.theme_mode='LIGHT'

    elements=[]

    def get_python_environments():
        environments = []
        user_home = os.path.expanduser("~") #home dir

        for root, dirs, files in os.walk(user_home):
            if 'pyvenv.cfg' in files or 'pyvenv.cfg' in dirs:
                environments.append(root)

        #return environments
    
        python_envs = environments
        python_envs=json.dumps(python_envs)
        with open('envpaths.json','w') as e:
            e.write(python_envs)

        return environments
    
    def retrieve(item):
        senddata=[]   
        name=item.split("\\")[-1]
        command=rf'{sysdir}\\{name}\\Scripts\\activate && pip list && deactivate'

        try:
            output = subprocess.check_output(command, shell=True, universal_newlines=True)
            output=output.split("\n")[2:]
            output=[k.replace(" ","\t") for k in output]
            senddata=output
        except subprocess.CalledProcessError as e:
            output="Can't access env"
            senddata.append(e.output)     

        return(senddata)
    
    def items(count):
        for i in range(count):
            temp_path=paths[i]
            mydata=retrieve(temp_path)
            name=paths[i].split('\\')[-1]
            cl=ft.Column(height=250,width=200,scroll=ft.ScrollMode.AUTO,data=i,spacing=2)

            for j in mydata:                
                cl.controls.append(ft.Text(j))

            b = ft.ElevatedButton("Refresh", on_click=myfunc,data=i,color=ft.colors.BLACK)

            elements.append(ft.Column([ft.Text(name,size=18,color=ft.colors.GREEN_800),cl,b],height=350,width=200))

            pb.value=i/count
            page.update

        return elements
    
    def myfunc(e):
        ind=e.control.data
        data=retrieve(paths[ind])
        name=paths[ind].split('\\')[-1]

        cl=ft.Column(height=250,width=200,scroll=ft.ScrollMode.AUTO,data=ind,spacing=2)

        for j in data:                
            cl.controls.append(ft.Text(j))

        b = ft.ElevatedButton("Refresh", on_click=myfunc,data=ind,color=ft.colors.BLACK)

        elements[ind]=ft.Column([ft.Text(name,size=18,color=ft.colors.GREEN_800),cl,b],height=350,width=200)

        print("refreshed")

        page.update() 

    def search(e):

        paths_new=get_python_environments()
        new=[i for i in paths_new if i not in paths]
        for z in new:
            paths.append(z)
        
        #print(new)
        #print(paths)
        for i in new:
            mydata=retrieve(i)
            name=i.split('\\')[-1]
            cl=ft.Column(height=250,width=200,scroll=ft.ScrollMode.AUTO,data=paths.index(i),spacing=2)

            for j in mydata:                
                cl.controls.append(ft.Text(j))

            b = ft.ElevatedButton("Refresh", on_click=myfunc,data=paths.index(i),color=ft.colors.BLACK)

            elements.append(ft.Column([ft.Text(name,size=18,color=ft.colors.GREEN_800),cl,b],height=350,width=200))


        
        row.controls=elements
        page.update()
        print("content refreshed")
 


    while True:
        try:
            with open('envpaths.json','r') as r:
                paths=r.read()
            break
        except IOError:
                message=ft.Text("Scanning for Environments. Trying again in 20 seconds...")
                page.add(message)
                get_python_environments()
                time.sleep(20)
                page.remove(message)



    paths=json.loads(paths)


    pb = ft.ProgressBar(width=400)
    status=ft.Text("Loading Environments...")
    page.add(ft.Text("Welcome to EnView"),status,pb)


    row = ft.Row(controls=items(len(paths)),wrap=True)

    page.remove(status,pb)
    page.add(row)

    
    ref=ft.ElevatedButton(text="Refresh env list", color=ft.colors.BLACK,bgcolor=ft.colors.WHITE,on_click=search)

    page.add(ref)

ft.app(target=main)