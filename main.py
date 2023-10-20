
# This program does some preprocessing on data from excel such as making pivot tables using pandas and finally tells trend of macd and emacd two important parameters in stock market.
import pandas as pd
import time
list_of_files=["DIFF","MACD","EMACD"]
iterlist=["WEEK","TIMESTAMP","MONTH"]
for g in iterlist:
    for p in list_of_files:
        dfraw=pd.read_csv(fr"C:\Users\Rishit Sharma\PycharmProjects\pythonProject\raw{g}.csv")
        dfraw[g] = pd.to_datetime(dfraw[g], format='%d-%m-%Y')
        sorted_df = dfraw.sort_values(by=g)
        pivot_table = sorted_df.pivot_table(index=g, columns='SYMBOL', values=p, aggfunc='sum')
        mod=pivot_table.fillna("none")
        unique_names = dfraw['SYMBOL'].unique().tolist()
        df_list=pd.DataFrame({"Names":unique_names})
        df_list.to_csv(fr"D:\python_input\list_{g}.csv")
        mod.to_csv(fr"D:\python_input\{p}_{g}.csv")
time.sleep(5)





for iteration in iterlist:
        path1=fr"D:\python_input\list_{iteration}.csv" # List of stocks
        path2=fr"D:\python_input\DIFF_{iteration}.csv" # Difference input file
        path3=fr"D:\python_input\MACD_{iteration}.csv"  # macd file
        path4=fr"D:\python_input\EMACD_{iteration}.csv"  # emacd file
        macd=[]
        emacd=[]
        trend=[]
        defaulter=[]
        min=[]
        max=[]
        value=[]

        df=pd.read_csv(path1)


        names=list(df.Names)



        for j in names:


             df=pd.read_csv(path2)
             list1=list(df[j])
             x = "none" in list1
             y= 0 in list1
             if x==False and y==False:
                 if list1[len(list1) - 1] < list1[len(list1) - 2] and list1[len(list1) - 2] < list1[len(list1) - 3]:
                     trend.append("Decreasing")
                     for i in range(1, len(list1)+1):
                         if list1[len(list1) - i] > list1[len(list1) - i - 1]:
                             max.append( i - 1)
                             min.append("none")
                             value.append(list1[len(list1)-i])
                             break
                         elif i==len(list1):
                             max.append("max NIR")
                             max.append("none")
                             value.append("out of range")

                 elif list1[len(list1) - 1] > list1[len(list1) - 2] and list1[len(list1) - 2] > list1[len(list1) - 3]:
                     trend.append("increasing")
                     for i in range(1, len(list1)+1):
                         if list1[len(list1) - i] < list1[len(list1) - i - 1]:
                             min.append(i - 1)
                             max.append("none")
                             value.append(list1[len(list1)-i])
                             break
                         elif i==len(list1):
                             min.append("min NIR")
                             max.append("none")
                             value.append("out of range")

                 elif list1[len(list1) - 1] > list1[len(list1) - 2] and list1[len(list1) - 2] < list1[len(list1) - 3]:
                     trend.append("MIN was yesterday")
                     min.append("1")
                     max.append("none")
                     value.append(list1[len(list1)-2])
                 else:
                     trend.append("max was yesterday")
                     max.append("1")
                     min.append("none")
                     value.append(list1[len(list1) - 2])

             else:
                 defaulter.append(j)
                 continue

        for w in defaulter:
            names.__delitem__(names.index(w))

        for m,k in zip(names,value):

            dff = pd.read_csv(path2)
            list1 = list(dff[m])

            df1=pd.read_csv(path3)
            list2=list(df1[m])
            macd.append(list2[list1.index(k)])

        for m,k in zip(names,value):

            dff = pd.read_csv(path2)
            list1 = list(dff[m])

            df1=pd.read_csv(path4)
            list3=list(df1[m])
            emacd.append(list3[list1.index(k)])


        df9 = pd.DataFrame(
                {"Name": names, "trend": trend, "min": min, "max": max, "value_diff": value,"macd_value":macd,"emacd_value":emacd})
        df9.to_csv(fr"D:\python_input\OUTPUT_{iteration}.csv")






