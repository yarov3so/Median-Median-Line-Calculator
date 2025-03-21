import numpy as np
import pandas as pd
import re
import statistics as stat
import streamlit as st

def comprehend(mystring):
    mystring=mystring.replace(" ", "")
    data_list=mystring.split(",")
    data =[]
    for el in data_list:
        try:
            data.append(float(el))
        except: 
            for i in range(int(re.findall(r'\d+', el)[0])):
                data.append(None)
    return data

def try_int(num):
    
    num_int=None
    try:
        num_int=int(num)
    except:
        None
    if num==num_int:
        return num_int
    else:
        return round(float(num),2)
    
datapts=pd.DataFrame(columns=['x', 'y'])
current_entry={0}

st.title("Median-Median Line Calculator")
st.markdown("Produces the equation of the line of best fit in slope-intercept form using the Median-Median method.")

entries={}
i=0
while True:
    
    entries[i]=st.text_input("Enter a pair of coordinates separated by a comma, or write 'done' if you are done: ",key=i)
    if len(entries[i])==0:
        st.stop()
    if "," not in entries[i]:
        break
    try:
        datapts.loc[len(datapts)]=comprehend(entries[i])
    except:
        st.markdown("Cannot parse your entry! Did you make a typo?")
        st.stop()
    i+=1

if len(datapts)==0 or (i==0 and "," not in entries[0]) or (i==0 and entries[0] == ",") :
    st.markdown("You have entered no data points!")
    st.stop()

if len(datapts)<3:
    st.markdown("You need at least three points (ideally many more) to apply the Median-Median line method!")
    st.stop()

datapts=datapts.sort_values(by="x")
n=len(datapts)

st.markdown("You have entered the following coordinates:")
st.dataframe(datapts,hide_index=True)

if len(datapts)/3 - len(datapts)//3 < 0.5:
    n_outer=len(datapts)//3
else:
    n_outer=len(datapts)//3 + 1

st.markdown(f"The first and third (i.e. outer) groups have {n_outer} points, whereas the second (middle) group has {len(datapts)-2*n_outer} points.")

G1=datapts.iloc[:n_outer]
st.markdown(f"Group 1:")
st.dataframe(G1,hide_index=True)

G2=datapts.iloc[n_outer:len(datapts)-n_outer]
st.markdown(f"Group 2:")
st.dataframe(G2,hide_index=True)

G3=datapts.iloc[len(datapts)-n_outer:]
st.markdown(f"Group 3:")
st.dataframe(G3,hide_index=True)

M1=(stat.median(G1["x"]),stat.median(G1["y"]))
M2=(stat.median(G2["x"]),stat.median(G2["y"]))
M3=(stat.median(G3["x"]),stat.median(G3["y"]))

st.markdown("As such, we have:")

st.markdown(f"""$M1 = {(try_int(M1[0]),try_int(M1[1]))}$  
$M2 = {(try_int(M2[0]),try_int(M2[1]))}$  
$M3 = {(try_int(M3[0]),try_int(M3[1]))}$""")

P=((M1[0]+M2[0]+M3[0])/3,(M1[1]+M2[1]+M3[1])/3)

st.markdown(f"Then, $ P = \\left( \\frac{{ M1_x + M2_x + M3_x }}{{ 3 }}) , \\frac{{ M1_y + M2_y + M3_y }}{{ 3 }} \\right) = \\left( \\frac{{ {try_int(M1[0])} + {try_int(M2[0])} + {try_int(M3[0])} }}{{ 3 }} , \\frac{{ {try_int(M1[1])} + {try_int(M2[1])} + {try_int(M3[1])} }}{{ 3 }} \\right) = {(try_int(P[0]),try_int(P[1]))} $")

m=(M3[1]-M1[1])/(M3[0]-M1[0])
b=P[1]-m*P[0]

st.markdown("We use M1 and M3 to find the slope of the line of best fit:")
st.markdown(f"$ \\text{{Slope}} = \\frac{{ M3_y - M1_y }}{{ M3_x - M1_x }} = \\frac{{ {try_int(M3[1])} - {try_int(M1[1])} }}{{ {try_int(M3[0])} - {try_int(M1[0])} }} = {try_int(m)}$")

st.markdown(f"\nWe calculate the y-intercept b by focing the line with slope {try_int(m)} to pass through the point P:")
st.markdown(f"$y = mx + b$")
st.markdown(f"$y = {try_int(m)}(x) + b$")
st.markdown(f"$ {try_int(P[1])} = {try_int(m)} \cdot ( {try_int(P[0])} ) + b $ &nbsp;  $\Leftarrow$  plugging the coordinates of P into the slope-intercept form of the line of best fit.")
st.markdown(f"$ b = {try_int(P[1])} - ({try_int(m)}) \cdot ({try_int(P[0])}) = {b} $")

st.markdown(f"And so, the Median-Median method produces the following line of best fit in slope-intercept form:")
if try_int(b)>0:
    st.markdown(f"$y = {try_int(m)}x + {try_int(b)}$")
if try_int(b)==0:
    st.markdown(f"$y = {try_int(m)}x$")
if try_int(b)<0:
    st.markdown(f"$y = {try_int(m)}x {try_int(b)}$")

st.text("")
st.markdown("""*Crafted by yarov3so*   
<a href="https://www.buymeacoffee.com/yarov3so" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="width: 9em; height: auto; padding-top: 0.7em; padding-bottom: 1em" ></a>  
See my other [Math Help Tools](https://mathh3lptools.streamlit.app)""",unsafe_allow_html=True)
