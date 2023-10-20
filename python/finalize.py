#!/usr/bin/python
# -*- coding: UTF-8 -*-

import nbformat as nbf
import nbconvert as nb
import os
import re
from matplotlib import pyplot as plt
import shutil







def main(): 
    jup_path='../'
    html_path='../html/'
    elements_path='../_elements/'
    cp = os.path.split(os.getcwd())[-1]
    if cp == 'notebooks':
        jup_path =  ""
        html_path = "html/"
        elements_path = "_elements/"

    shutil.rmtree(html_path)
    os.mkdir(html_path)
    print("TOC")
    lst=[]
    content_lst=[]
    if jup_path=='':
        f = os.listdir()
    else:
        f = os.listdir(jup_path)
    for file in f:
        fname = os.fsdecode(file)
        if fname.endswith(".ipynb") and (not 'Untitled' in fname): 
            link=fname.replace('.ipynb','.html')
            text=fname
            content_lst.append([text,link])
            if fname.endswith(".ipynb"): 
                lst.append(f"[{fname}]({text})\r")
    lst.sort()
    content_lst.sort(key=lambda x:int(x[0][0:2]))
    for i in lst:
        print(i)
            
            
    print('Parsing ...')
    for file in f:
        fname = os.fsdecode(file)
        if fname.endswith(".ipynb") and (not 'Untitled' in fname):  
            print(f"nummerates {fname}")
            replace_all(jup_path+fname,'"../img/', '"img/')
            recount_and_replace(jup_path+fname,'#### Eksempel')
            recount_and_replace(jup_path+fname,'#### Oppgave')
            html_name=html_path+file.replace('.ipynb','.html')
            html=convert_ipynb_to_html(jup_path+fname)
            html=insert_custom_html(html, content_lst, elements_path)
            write(html_name,html)
            replace_all(html_name, '"img/','"../img/')


def replace_all(fname,what, to):
    f=open(fname,encoding='utf-8')
    s=f.read()
    i=1
    n=0
    while True:
        m=re.search(what,s[n:])
        if m is None:
            break
        s=s[:m.start()+n]+to+s[m.end()+n:]
        n+=m.end()
        i+=1
    f.close()
    if i>1:
        write(fname,s)

def replace(s,start_str,end_str,to,owerwrite=[False,False]):
    m0=re.search(start_str,s)
    if m0 is None:
        raise RuntimeError(f'Failed to find {start_str}')    
    m1=re.search(end_str,s[m0.end():])
    if m1 is None:
        raise RuntimeError(f'Failed to find {end_str}')
    if owerwrite[0]:
        start=m0.start()
    else:
        start=m0.end()
    if owerwrite[1]:
        end=m1.end()+m0.end()
    else:
        end=m1.start()+m0.end()
    
    s=s[:start]+to+s[end:]
    return s
    
    
def recount_and_replace(fname,what):
    if len(what.split(' '))!=2 or not ('#' in what):
        raise RuntimeError(f'what needs to be on the form "#### word", not {what}')
    f=open(fname,encoding='utf-8')
    s=f.read()
    i=1
    n=0
    while True:
        m=re.search(what+' (\d+)',s[n:])
        if m is None:
            break
        old=s[m.start()+n:m.end()+n]
        new=f'{what} {i}'
        s=s[:m.start()+n]+new+s[m.end()+n:]
        s=replace_references(s, old, new)
        n+=m.end()
        i+=1
    f.close()
    if i>1:
        write(fname,s)

        
def replace_references(s,old,new):
    n=0
    old=old[old.find(' ')+1:]
    new=new[new.find(' ')+1:]
    if old==new:
        return s
    while True:
        m=re.search(f"\\w*(?<!#### ){old}",s[n:])
        if m is None:
            break
        s=s[:m.start()+n]+new+s[m.end()+n:]
        n+=m.end()
    return s

def convert_ipynb_to_html(ipynbfile):
    html,res=nb.HTMLExporter(template_name='Classic').from_filename(ipynbfile)
    html=html.replace('.ipynb">','.html">')
    return html
    

def insert_custom_html(html,content_list, elements_path):
    css=read(elements_path+'css.html')
    banner=read(elements_path+'banner.html')
    content=read(elements_path+'left_menu_top.html')
    left_menu=read(elements_path+'left_menu.html')
    html=replace(html, 
                 'require.min.js"></script>\n',
                 '\n<style type="text/css">', 
                 '<link rel="icon" type="image/x-icon" href="../img/favicon.ico">')        
    html=replace(html, ".container {",".row {", css,[True,False])
    html=replace(html, "<body>",'<div tabindex="-1"', banner)

    for text,link in content_list:
        content+=f'\t\t\t<a href="{link}">{text}</a><br>\n'
    content+=left_menu
    html=replace(html, 
                 '<div class="container" id="notebook-container">',
                 '<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">', 
                 content)

    return html
    
    

def write(fname,s):
    f=open(fname,'w',encoding="utf-8")
    f.write(s)
    f.close()    
    
def read(fname):
    f=open(fname,'r',encoding="utf-8")
    r=f.read()
    f.close() 
    return r
    

main()