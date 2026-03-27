import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import psycopg2
import json
import requests


mydb = psycopg2.connect(
                  user = "postgres",
                  host = "localhost",
                  password = "Nixon17",
                  port = "5432",
                  database = "phonepe_db"
)

cursor = mydb.cursor()

## Aggregated_Insurance dataFrame

cursor.execute("select * from aggregated_insurance")


Df1 = cursor.fetchall()

Agg_Insurance = pd.DataFrame(Df1,columns = ('States', 'Year', 'Quarter', 'Transaction_Name', 'Transaction_Count',
       'Transaction_Amount', 'Transaction_Type'))

## Aggregated_Transaction dataFrame


cursor.execute("select * from aggregated_transaction")


Df2 = cursor.fetchall()

Agg_Transaction = pd.DataFrame(Df2,columns = ('States', 'Year', 'Quarter', 'Transaction_Name', 'Transaction_Count',
       'Transaction_Amount', 'Transaction_Type'))

## Aggregated_User dataFrame

cursor.execute("select * from aggregated_user")


Df3 = cursor.fetchall()

Agg_User = pd.DataFrame(Df3,columns = ('States', 'Year', 'Quarter', 'brand', 'Count',
        'percentage'))

## Map_Insurance dataFrame

cursor.execute("select * from map_insurance")



Df4 = cursor.fetchall()

Map_Insurance = pd.DataFrame(Df4,columns = ('States', 'Year', 'Quarter', 'District_Name', 'Transaction_Count',
       'Transaction_Amount', 'Transaction_Type'))


## Map_transaction dataFrame

cursor.execute("select * from map_map")



Df5 = cursor.fetchall()

Map_Transaction = pd.DataFrame(Df5,columns =('States', 'Year', 'Quarter', 'District_Name', 'Transaction_Count',
       'Transaction_Amount', 'Transaction_Type'))

## Map_user dataFrame

cursor.execute("select * from map_user")



Df6 = cursor.fetchall()

Map_User = pd.DataFrame(Df6,columns = ('States', 'Year', 'Quarter', 'District_Name', 'Registered_users',
       'AppOpens'))

## Top_Insurance dataFrame

cursor.execute("select * from top_insurance")



Df7 = cursor.fetchall()
Top_Insurance = pd.DataFrame(Df7,columns = ('States', 'Year', 'Quarter', 'Pin_code', 'Transaction_Amount','Transaction_Type', 'Transaction_Count'
       ))

## Top_Transaction dataFrame

cursor.execute("select * from top_transaction")



Df8 = cursor.fetchall()
Top_Transaction = pd.DataFrame(Df8,columns = ('States', 'Year', 'Quarter', 'Pin_code', 'Transaction_Amount', 
                                              'Transaction_Type', 'Transaction_Count'))

## Top_User dataFrame

cursor.execute("select * from top_user")



Df9 = cursor.fetchall()
Top_User = pd.DataFrame(Df9,columns = ('States', 'Year', 'Quarter', 'Pin_code','RegisteredUsers'))






def Agg_insurance_Year(df, year=None, quarter=None):
    # --- Filter data ---
    if year and quarter:
        Tran = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
        title_prefix = f"{year} Q{quarter}"
    elif year :
        Tran = df[df["Year"] == year]
        title_prefix = f"{year}"
    else:
        st.error("Provide at least a year")
        return

    Tran.reset_index(drop=True, inplace=True)

    # --- Aggregate ---
    Trans = Tran.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()

    # --- Bar charts ---
    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(
            Trans, x="States", y="Transaction_Amount",
            title=f" TRANSACTION AMOUNT {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )
        st.plotly_chart(fig_amount, key = "Agg_Insurance Amount")
    with col2:
        fig_count = px.bar(
            Trans, x="States", y="Transaction_Count",
            title=f" TRANSACTION COUNT {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Bluered_r
        )
        st.plotly_chart(fig_count,key = "Agg_Insurance Count")

    # --- GeoJSON ---
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    # --- Choropleths ---
    col1, col2 = st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Amount",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Amount"].min(), Trans["Transaction_Amount"].max()),
            hover_name="States",
            title=f"TRANSACTION AMOUNT {title_prefix} ",
            fitbounds="locations", width=600, height=600
        )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1,key = "Agg_Insurance Geo Amount")
    with col2:
        fig_india_2 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Count",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Count"].min(), Trans["Transaction_Count"].max()),
            hover_name="States",
            title=f" TRANSACTION COUNT {title_prefix}",
            fitbounds="locations", width=600, height=600
        )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2,key = "Agg_Insurance Geo Count")
    
        

def Agg_user_Year(df,year):
    Trans = df[df["Year"]== year]
    Trans.reset_index(drop = True , inplace = True)
    Tran  = Trans.groupby("brand")[["Count","percentage"]].sum().reset_index()
    
    title_prefix = f"{year}"
    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(Tran,x ="brand",y = "Count",title=f" COUNT {title_prefix}",
                    width=600, height=650,
                    color_discrete_sequence=px.colors.sequential.Blues,hover_name= "brand")
        st.plotly_chart(fig_amount_1)
    with col2:
        fig_amount_2 = px.bar(Tran,x ="brand",y = "percentage",title=f" PERCENTAGE {title_prefix}",
                    width=600, height=650,
                    color_discrete_sequence=px.colors.sequential.Burg,hover_name= "brand")
        st.plotly_chart(fig_amount_2) 



def Agg_user_Year_Quarter(df,year=None,quarter = None):
    if year and quarter:
        Trans = df[(df["Year"]== year) & (df["Quarter"]== quarter)]
        title_prefix = f"{year} and Quarter {quarter}"
    elif year:
        Trans = df[df["Year"]== year]
        title_prefix = f"{year}"
    else:
        st.error("Provide at least a year")
        return
    Trans.reset_index(drop = True , inplace = True)
    Tran  = Trans.groupby("brand")[["Count","percentage"]].sum().reset_index()
    
    
    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(Tran,x ="brand",y = "Count",title=f" COUNT for {title_prefix}",
                    width=600, height=650,
                    color_discrete_sequence=px.colors.sequential.Blues,hover_name= "brand")
        st.plotly_chart(fig_amount_1)
    with col2:
        fig_amount_2 = px.bar(Tran,x ="brand",y = "percentage",title=f" PERCENTAGE for {title_prefix}",
                    width=600, height=650,
                    color_discrete_sequence=px.colors.sequential.Burg,hover_name= "brand")
        st.plotly_chart(fig_amount_2) 
    return Trans


def Agg_user_State(df,State):
    
    Trans = df[df["States"]== State]
    title_prefix = f"{State}"
    
    
    Trans.reset_index(drop = True , inplace = True)
    
    
    
    
    fig_line_1 = px.line(Trans,x ="brand",y = "Count",title=f" COUNT for {title_prefix}",
                    width=600, height=650,
                    color_discrete_sequence=px.colors.sequential.Blues,hover_name= "percentage")
    st.plotly_chart(fig_line_1)
    

def Map_insurance_Year(df, year=None, quarter=None):
    # --- Filter data ---
    if year and quarter:
        Tran = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
        title_prefix = f"{year} Q{quarter}"
    elif year :
        Tran = df[df["Year"] == year]
        title_prefix = f"{year}"
    else:
        st.error("Provide at least a year")
        return

    Tran.reset_index(drop=True, inplace=True)

    # --- Aggregate ---
    Trans = Tran.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()

    # --- Bar charts ---
    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(
            Trans, x="States", y="Transaction_Amount",
            title=f" TRANSACTION AMOUNT {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )
        st.plotly_chart(fig_amount, key = "Map_Insurance Amount")
    with col2:
        fig_count = px.bar(
            Trans, x="States", y="Transaction_Count",
            title=f" TRANSACTION COUNT {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Bluered_r
        )
        st.plotly_chart(fig_count,key = "Map_Insurance Count")

    # --- GeoJSON ---
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    # --- Choropleths ---
    col1, col2 = st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Amount",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Amount"].min(), Trans["Transaction_Amount"].max()),
            hover_name="States",
            title=f"TRANSACTION AMOUNT {title_prefix} ",
            fitbounds="locations", width=600, height=600
        )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1,key = "Map_Insurance Geo Amount")
    with col2:
        fig_india_2 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Count",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Count"].min(), Trans["Transaction_Count"].max()),
            hover_name="States",
            title=f" TRANSACTION COUNT {title_prefix}",
            fitbounds="locations", width=600, height=600
        )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2,key = "Map_Insurance Geo Count")
    return Tran





def Map_insurance_State(df,state):
    
    Tran = df[df["States"] == state]
    title_prefix = f"States {state}"


    Tran.reset_index(drop=True, inplace=True)

    
    Tran1 = Tran.groupby("District_Name")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()
    
    
    
    
    col1,col2 = st.columns(2)
    with col1:
        
        fig_bar_1 = px.bar(Tran1,x ="Transaction_Amount",y ="District_Name" ,title=f" Amount for {title_prefix}",
                        width=600, height=650, orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_bar_1, title = "Map State amount")
    with col2:
        fig_bar_2 = px.bar(Tran1,x ="Transaction_Count",y = "District_Name",title=f" Count for {title_prefix}",
                        width=600, height=650, orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_bar_2,title = "Map State amount")
 
 
 
def Agg_Transaction_Year(df, year=None, quarter=None):
    # --- Filter data ---
    if year and quarter:
        Tran = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
        title_prefix = f"{year} Quarter {quarter}"
    elif year :
        Tran = df[df["Year"] == year]
        title_prefix = f"{year}"
    else:
        st.error("Provide at least a year")
        return

    Tran.reset_index(drop=True, inplace=True)

    # --- Aggregate ---
    Trans = Tran.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()

    # --- Bar charts ---
    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(
            Trans, x="States", y="Transaction_Amount",
            title=f" TRANSACTION AMOUNT {title_prefix}",
            width=600, height=650,
            color = "States"
        )
        st.plotly_chart(fig_amount, key = "Agg Transaction Amount")
    with col2:
        fig_count = px.bar(
            Trans, x="States", y="Transaction_Count",
            title=f" TRANSACTION COUNT {title_prefix}",
            width=600, height=650,
            color = "States"
        )
        st.plotly_chart(fig_count,key = "Agg Transaction Count")

    # --- GeoJSON ---
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    # --- Choropleths ---
    col1, col2 = st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Amount",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Amount"].min(), Trans["Transaction_Amount"].max()),
            hover_name="States",
            title=f"TRANSACTION AMOUNT {title_prefix} ",
            fitbounds="locations", width=600, height=600
        )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1,key = "Agg Transaction Geo Amount")
    with col2:
        fig_india_2 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Count",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Count"].min(), Trans["Transaction_Count"].max()),
            hover_name="States",
            title=f" TRANSACTION COUNT {title_prefix}",
            fitbounds="locations", width=600, height=600
        )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2,key = "Agg Transaction Geo Count")
    return Tran




def Agg_Transaction_State(df,state):
    
    Tran = df[df["States"] == state]
    title_prefix = f"State {state}"


    Tran.reset_index(drop=True, inplace=True)

    
    Tran1 = Tran.groupby("Transaction_Name")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()
    
    
    
    
    col1,col2 = st.columns(2)
    with col1:
        
        fig_pie_1 = px.pie(Tran1,values ="Transaction_Amount",names ="Transaction_Name" ,title=f" Amount for {title_prefix}",
                        width=600, height=650, hole = 0.5,
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_pie_1, key = "Agg State amount")
    with col2:
        fig_pie_2 = px.pie(Tran1,values ="Transaction_Count",names = "Transaction_Name",title=f" Count for {title_prefix}",
                        width=600, height=650, hole = 0.5,
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_pie_2,key = "Agg Count amount")


def Map_Transaction_Year(df, year=None, quarter=None):
    # --- Filter data ---
    if year and quarter:
        Tran = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
        title_prefix = f"Year {year} Quarter {quarter}"
    elif year :
        Tran = df[df["Year"] == year]
        title_prefix = f"{year}"
    else:
        st.error("Provide at least a year")
        return

    Tran.reset_index(drop=True, inplace=True)

    # --- Aggregate ---
    Trans = Tran.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()

    # --- Bar charts ---
    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(
            Trans, x="States", y="Transaction_Amount",
            title=f" TRANSACTION AMOUNT {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )
        st.plotly_chart(fig_amount, key = "Map_Transaction Amount")
    with col2:
        fig_count = px.bar(
            Trans, x="States", y="Transaction_Count",
            title=f" TRANSACTION COUNT {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Bluered_r
        )
        st.plotly_chart(fig_count,key = "Map_Transaction Count")

    # --- GeoJSON ---
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    # --- Choropleths ---
    col1, col2 = st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Amount",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Amount"].min(), Trans["Transaction_Amount"].max()),
            hover_name="States",
            title=f"TRANSACTION AMOUNT {title_prefix} ",
            fitbounds="locations", width=600, height=600
        )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1,key = "Map_Transaction Geo Amount")
    with col2:
        fig_india_2 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Count",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Count"].min(), Trans["Transaction_Count"].max()),
            hover_name="States",
            title=f" TRANSACTION COUNT {title_prefix}",
            fitbounds="locations", width=600, height=600
        )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2,key = "Map_Transaction Geo Count")
    return Tran

def Map_Transaction_State(df,state):
    
    Tran = df[df["States"] == state]
    title_prefix = f"State {state}"


    Tran.reset_index(drop=True, inplace=True)

    
    Tran1 = Tran.groupby("District_Name")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()
    
    
    
    
    col1,col2 = st.columns(2)
    with col1:
        
        fig_bar_1 = px.bar(Tran1,x ="Transaction_Amount",y ="District_Name" ,title=f" Amount for {title_prefix}",
                        width=600, height=650, orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_bar_1, title = "Map Transaction State amount")
    with col2:
        fig_bar_2 = px.bar(Tran1,x ="Transaction_Count",y = "District_Name",title=f" Count for {title_prefix}",
                        width=600, height=650, orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_bar_2,title = "Map Transaction State amount")



def Map_User_Year(df, year=None, quarter=None):
    # --- Filter data ---
    if year and quarter:
        Tran = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
        title_prefix = f"Year {year} Quarter {quarter}"
    elif year :
        Tran = df[df["Year"] == year]
        title_prefix = f"{year}"
    else:
        st.error("Provide at least a year")
        return

    Tran.reset_index(drop=True, inplace=True)

    # --- Aggregate ---
    Trans = Tran.groupby("States")[["Registered_users", "AppOpens"]].sum().reset_index()

    # --- Bar charts ---
    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(
            Trans, x="States", y="Registered_users",
            title=f" REGISTERED USERS {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )
        st.plotly_chart(fig_amount, key = "Map_User Registered_user")
    with col2:
        fig_count = px.bar(
            Trans, x="States", y="AppOpens",
            title=f" APP OPENS {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Bluered_r
        )
        st.plotly_chart(fig_count,key = "Map_user App Opens")

    # --- GeoJSON ---
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    # --- Choropleths ---
    col1, col2 = st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Registered_users",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Registered_users"].min(), Trans["Registered_users"].max()),
            hover_name="States",
            title=f" REGISTERED USERS {title_prefix} ",
            fitbounds="locations", width=600, height=600
        )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1,key = "Map_user Geo Amount")
    with col2:
        fig_india_2 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="AppOpens",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["AppOpens"].min(), Trans["AppOpens"].max()),
            hover_name="States",
            title=f" APP OPENS {title_prefix}",
            fitbounds="locations", width=600, height=600
        )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2,key = "Map_User Geo Count")
    return Tran


def Map_User_State(df,state):
    
    Tran = df[df["States"] == state]
    title_prefix = f"State {state}"


    Tran.reset_index(drop=True, inplace=True)

    
    Tran1 = Tran.groupby("District_Name")[["Registered_users", "AppOpens"]].sum().reset_index()
    
    
    
    
    col1,col2 = st.columns(2)
    with col1:
        
        fig_bar_1 = px.bar(Tran1,x ="Registered_users",y ="District_Name" ,title=f" Registered Users for {title_prefix}",
                        width=600, height=650, orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_bar_1, title = "Map User Registered User")
    with col2:
        fig_bar_2 = px.bar(Tran1,x ="Registered_users",y = "District_Name",title=f" App Opens {title_prefix}",
                        width=600, height=650, orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_bar_2,title = "Map User App Opens")


def Top_insurance_Year(df, year=None, quarter=None):
    # --- Filter data ---
    if year and quarter:
        Tran = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
        title_prefix = f"{year} Q{quarter}"
    elif year :
        Tran = df[df["Year"] == year]
        title_prefix = f"{year}"
    else:
        st.error("Provide at least a year")
        return

    Tran.reset_index(drop=True, inplace=True)

    # --- Aggregate ---
    Trans = Tran.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()

    # --- Bar charts ---
    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(
            Trans, x="States", y="Transaction_Amount",
            title=f" TRANSACTION AMOUNT {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )
        st.plotly_chart(fig_amount, key = "Top_Insurance Amount")
    with col2:
        fig_count = px.bar(
            Trans, x="States", y="Transaction_Count",
            title=f" TRANSACTION COUNT {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Bluered_r
        )
        st.plotly_chart(fig_count,key = "Top_Insurance Count")

    # --- GeoJSON ---
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    # --- Choropleths ---
    col1, col2 = st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Amount",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Amount"].min(), Trans["Transaction_Amount"].max()),
            hover_name="States",
            title=f"TRANSACTION AMOUNT {title_prefix} ",
            fitbounds="locations", width=600, height=600
        )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1,key = "Top_Insurance Geo Amount")
    with col2:
        fig_india_2 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Count",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Count"].min(), Trans["Transaction_Count"].max()),
            hover_name="States",
            title=f" TRANSACTION COUNT {title_prefix}",
            fitbounds="locations", width=600, height=600
        )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2,key = "Top_Insurance Geo Count")
    return Tran

def Top_Insurance_State(df,state):
    
    Tran = df[df["States"] == state]
    title_prefix = f"State {state}"


    Tran.reset_index(drop=True, inplace=True)

    
    Tran1 = Tran.groupby("Pin_code")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()
    
    
    
    
    col1,col2 = st.columns(2)
    with col1:
        
        fig_pie_1 = px.pie(Tran1, values="Transaction_Amount",names ="Pin_code" ,title=f" Amount for {title_prefix}",
                        width=600, height=650, hole = 0.5,
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_pie_1, title = "Top Insurance State amount")
    with col2:
        fig_pie_2 = px.pie(Tran1,values ="Transaction_Count",names = "Pin_code",title=f" Count for {title_prefix}",
                        width=600, height=650, hole =0.5,
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_pie_2,title = "Top Insurance State amount")




def Top_Transaction_Year(df, year=None, quarter=None):
    # --- Filter data ---
    if year and quarter:
        Tran = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
        title_prefix = f"{year} Q{quarter}"
    elif year :
        Tran = df[df["Year"] == year]
        title_prefix = f"{year}"
    else:
        st.error("Provide at least a year")
        return

    Tran.reset_index(drop=True, inplace=True)

    # --- Aggregate ---
    Trans = Tran.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()

    # --- Bar charts ---
    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(
            Trans, x="States", y="Transaction_Amount",
            title=f" TRANSACTION AMOUNT {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )
        st.plotly_chart(fig_amount, key = "Top_Transaction Amount")
    with col2:
        fig_count = px.bar(
            Trans, x="States", y="Transaction_Count",
            title=f" TRANSACTION COUNT {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Bluered_r
        )
        st.plotly_chart(fig_count,key = "Top_Transaction Count")

    # --- GeoJSON ---
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    # --- Choropleths ---
    col1, col2 = st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Amount",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Amount"].min(), Trans["Transaction_Amount"].max()),
            hover_name="States",
            title=f"TRANSACTION AMOUNT {title_prefix} ",
            fitbounds="locations", width=600, height=600
        )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1,key = "Top_Transaction Geo Amount")
    with col2:
        fig_india_2 = px.choropleth(
            Trans, geojson=data1, locations="States",
            featureidkey="properties.ST_NM",
            color="Transaction_Count",
            color_continuous_scale="Sunsetdark",
            range_color=(Trans["Transaction_Count"].min(), Trans["Transaction_Count"].max()),
            hover_name="States",
            title=f" TRANSACTION COUNT {title_prefix}",
            fitbounds="locations", width=600, height=600
        )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2,key = "Top_Transaction Geo Count")
    return Tran

def Top_Transaction_State(df,state):
    
    Tran = df[df["States"] == state]
    title_prefix = f"State {state}"


    Tran.reset_index(drop=True, inplace=True)

    
    Tran1 = Tran.groupby("Pin_code")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()
    
    
    
    
    col1,col2 = st.columns(2)
    with col1:
        
        fig_pie_1 = px.pie(Tran1, values="Transaction_Amount",names ="Pin_code" ,title=f" Amount for {title_prefix}",
                        width=600, height=650, hole = 0.5,
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_pie_1, title = "Top Transaction State amount")
    with col2:
        fig_pie_2 = px.pie(Tran1,values ="Transaction_Count",names = "Pin_code",title=f" Count for {title_prefix}",
                        width=600, height=650, hole =0.5,
                        color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_pie_2,title = "Top Transaction State amount")

def Top_User_Year(df, year=None, quarter=None):
    # --- Filter data ---
    if year and quarter:
        Tran = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
        title_prefix = f"{year} Quarter {quarter}"
    elif year :
        Tran = df[df["Year"] == year]
        title_prefix = f"{year}"
    else:
        st.error("Provide at least a year")
        return

    Tran.reset_index(drop=True, inplace=True)

    # --- Aggregate ---
    Trans = Tran.groupby("States")["RegisteredUsers"].sum().reset_index()

    # --- Bar charts ---

    fig_amount = px.bar(
            Trans, x="States", y="RegisteredUsers",
            title=f" REGISTERED USERS {title_prefix}",
            width=600, height=650,
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )
    st.plotly_chart(fig_amount, key = "REGISTER USERS")
    
    return Tran




def Top_User_State(df,state):
    
    Tran = df[df["States"] == state]
    title_prefix = f"State {state}"


    Tran.reset_index(drop=True, inplace=True)

    
    Tran1 = Tran.groupby("Pin_code")["RegisteredUsers"].sum().reset_index()
    
    
    
    

        
    fig_pie_1 = px.pie(Tran1,values ="RegisteredUsers",names ="Pin_code" ,title=f" REGISTER USERS {title_prefix}",
                        width=600, height=650, hole = 0.5,
                        color_discrete_sequence=px.colors.sequential.Blues)
    st.plotly_chart(fig_pie_1, key = "Registered Users amount")
    
def Top_Transactions_State():


    mydb = psycopg2.connect(
            password="Nixon17",
            port="5432",
            host="localhost",
            database="phonepe_db",
            user="postgres"
        )
    cursor = mydb.cursor()

        # Top performing states by transaction amount
    query1 = f'''
            SELECT states, SUM(transaction_amount) AS Trans_Amount
            FROM aggregated_transaction
            GROUP BY states
            ORDER BY Trans_Amount desc
            LIMIT 10;
        '''
    cursor.execute(query1)
    result1 = cursor.fetchall()
    df1 = pd.DataFrame(result1, columns=["States", "Amount"])

        # Least performing states by transaction amount
        
    query2 = f'''
            SELECT states, SUM(transaction_amount) AS Trans_Amount
            FROM aggregated_transaction
            GROUP BY states
            ORDER BY Trans_Amount asc
            LIMIT 10;
        '''
    cursor.execute(query2)
    result2 = cursor.fetchall()
    df2 = pd.DataFrame(result2, columns=["States", "Amount"])  

    # Top performing states by transaction count
    query3 = f'''
            SELECT states, SUM(transaction_count) AS Trans_Count
            FROM aggregated_transaction
            GROUP BY states
            ORDER BY Trans_Count desc
            LIMIT 10;
        '''
    cursor.execute(query3)
    result3 = cursor.fetchall()
    df3 = pd.DataFrame(result3, columns=["States", "Count"])

    query4 = f'''
            SELECT states, SUM(transaction_count) AS Trans_Count
            FROM aggregated_transaction
            GROUP BY states
            ORDER BY Trans_Count asc
            LIMIT 10;
        '''
    cursor.execute(query4)
    result4 = cursor.fetchall()
    df4 = pd.DataFrame(result4, columns=["States", "Count"])
        # Visualizations
        
    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(df1,
                        x="States", y="Amount",
                        title=" Top Performing States - Amount",
                        hover_name="States",
                        color="Amount",
                        color_continuous_scale=px.colors.sequential.Redor)
        st.plotly_chart(fig)
    with col2:
        fig1 = px.bar(df2,
                        x="States", y="Amount",
                        title="Least Performing States - Amount",
                        hover_name="States",
                        color="Amount",
                        color_continuous_scale=px.colors.sequential.Greens)
        st.plotly_chart(fig1)
    col1,col2 = st.columns(2)
    with col1:
        fig2 = px.bar(df3,
                        x="States", y="Count",
                        title=" Top Performing States - Count",
                        hover_name="States",
                        color="Count",
                        color_continuous_scale=px.colors.sequential.Redor)
        st.plotly_chart(fig2)
    with col2:
        fig3 = px.bar(df4,
                        x="States", y="Count",
                        title="Least Performing States - Count",
                        hover_name="States",
                        color="Count",
                        color_continuous_scale=px.colors.sequential.Greens)
        st.plotly_chart(fig3)
    st.header("Insights")
    max_state = df1.loc[df1['Amount'].idxmax(), 'States']
    max_amount = df1['Amount'].max()
    min_state = df2.loc[df2['Amount'].idxmin(), 'States']
    min_amount = df2['Amount'].min()

    # Count-based insights
    max_state_count = df3.loc[df3['Count'].idxmax(), 'States']
    max_count = df3['Count'].max()
    min_state_count = df4.loc[df4['Count'].idxmin(), 'States']
    min_count = df4['Count'].min()

    

    st.write(f"{max_state} leads in Transaction Amount ({max_amount} ↑), while {min_state} has the lowest Transaction Amount ({min_amount} ↓).")
    st.write(f"{max_state_count} leads in Transaction Count ({max_count} ↑), while {min_state_count} has the lowest Transaction Count ({min_count} ↓).")



def Top_Insurance_District(year,quarter):


    mydb = psycopg2.connect(
            password="Nixon17",
            port="5432",
            host="localhost",
            database="phonepe_db",
            user="postgres"
        )
    cursor = mydb.cursor()

        # Top performing district by transaction amount
    query1 = f'''
            SELECT district_name,year,quarter, SUM(transaction_amount) AS Trans_Amount
            FROM map_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY district_name,year,quarter
            ORDER BY Trans_Amount desc
            LIMIT 10;
        '''
    cursor.execute(query1)
    result1 = cursor.fetchall()
    df1 = pd.DataFrame(result1, columns=["District","Year","Quarter", "Amount"])

        # Least performing district by transaction amount
        
    query2 = f'''
            SELECT district_name,year,quarter, SUM(transaction_amount) AS Trans_Amount
            FROM map_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY district_name,year,quarter
            ORDER BY Trans_Amount asc
            LIMIT 10;
        '''
    cursor.execute(query2)
    result2 = cursor.fetchall()
    df2 = pd.DataFrame(result2, columns=["District","Year","Quarter", "Amount"])  

    # Top performing states by transaction count
    query3 = f'''
            SELECT district_name,year,quarter, SUM(transaction_count) AS Trans_Count
            FROM map_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY district_name,year,quarter
            ORDER BY Trans_Count desc
            LIMIT 10;
        '''
    cursor.execute(query3)
    result3 = cursor.fetchall()
    df3 = pd.DataFrame(result3, columns=["District","Year","Quarter", "Count"])

    query4 = f'''
            SELECT district_name,year,quarter, SUM(transaction_count) AS Trans_Count
            FROM map_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY district_name,year,quarter
            ORDER BY Trans_Count asc
            LIMIT 10;
        '''
    cursor.execute(query4)
    result4 = cursor.fetchall()
    df4 = pd.DataFrame(result4, columns=["District","Year","Quarter", "Count"])
        # Visualizations
        
    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(df1,
                        x="District", y="Amount",
                        title=" Top Performing District - Amount",
                        hover_name="District",
                        color="District",
                        color_continuous_scale=px.colors.sequential.Redor)
        st.plotly_chart(fig)
    with col2:
        fig1 = px.bar(df2,
                        x="District", y="Amount",
                        title="Least Performing District - Amount",
                        hover_name="District",
                        color="District",
                        color_continuous_scale=px.colors.sequential.Greens)
        st.plotly_chart(fig1)
    col1,col2 = st.columns(2)
    with col1:
        fig2 = px.bar(df3,
                        x="District", y="Count",
                        title=" Top Performing District - Count",
                        hover_name="District",
                        color="District",
                        color_continuous_scale=px.colors.sequential.Redor)
        st.plotly_chart(fig2)
    with col2:
        fig3 = px.bar(df4,
                        x="District", y="Count",
                        title="Least Performing District - Count",
                        hover_name="District",
                        color="District",
                        color_continuous_scale=px.colors.sequential.Greens)
        st.plotly_chart(fig3)
        
    st.header("Insights")
    max_state = df1.loc[df1['Amount'].idxmax(), 'District'].title()
    max_amount = df1['Amount'].max()
    min_state = df2.loc[df2['Amount'].idxmin(), 'District'].title()
    min_amount = df2['Amount'].min()

    # Count-based insights
    max_state_count = df3.loc[df3['Count'].idxmax(), 'District'].title()
    max_count = df3['Count'].max()
    min_state_count = df4.loc[df4['Count'].idxmin(), 'District'].title()
    min_count = df4['Count'].min()

    

    st.write(f"{max_state} leads in Insurance Amount ({max_amount} ↑), while {min_state} has the lowest Insurance Amount ({min_amount} ↓).")
    st.write(f"{max_state_count} leads in Insurance Count ({max_count} ↑), while {min_state_count} has the lowest Insurance Count ({min_count} ↓).")

def Top_Transactions_District():


    mydb = psycopg2.connect(
            password="Nixon17",
            port="5432",
            host="localhost",
            database="phonepe_db",
            user="postgres"
        )
    cursor = mydb.cursor()

        # Top performing district by transaction amount
    query1 = f'''
            SELECT district_name, SUM(transaction_amount) AS Trans_Amount
            FROM map_map
            GROUP BY district_name
            ORDER BY Trans_Amount desc
            LIMIT 10;
        '''
    cursor.execute(query1)
    result1 = cursor.fetchall()
    df1 = pd.DataFrame(result1, columns=["District", "Amount"])

        # Least performing district by transaction amount
        
    query2 = f'''
            SELECT district_name, SUM(transaction_amount) AS Trans_Amount
            FROM map_map
            GROUP BY district_name
            ORDER BY Trans_Amount asc
            LIMIT 10;
        '''
    cursor.execute(query2)
    result2 = cursor.fetchall()
    df2 = pd.DataFrame(result2, columns=["District", "Amount"])  

    # Top performing states by transaction count
    query3 = f'''
            SELECT district_name, SUM(transaction_count) AS Trans_Count
            FROM map_map
            GROUP BY district_name
            ORDER BY Trans_Count desc
            LIMIT 10;
        '''
    cursor.execute(query3)
    result3 = cursor.fetchall()
    df3 = pd.DataFrame(result3, columns=["District", "Count"])

    query4 = f'''
            SELECT district_name, SUM(transaction_count) AS Trans_Count
            FROM map_map
            GROUP BY district_name
            ORDER BY Trans_Count asc
            LIMIT 10;
        '''
    cursor.execute(query4)
    result4 = cursor.fetchall()
    df4 = pd.DataFrame(result4, columns=["District", "Count"])
        # Visualizations
        
    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(df1,
                        x="District", y="Amount",
                        title=" Top Performing District - Amount",
                        hover_name="District",
                        color="Amount",
                        color_continuous_scale=px.colors.sequential.Redor)
        st.plotly_chart(fig)
    with col2:
        fig1 = px.bar(df2,
                        x="District", y="Amount",
                        title="Least Performing District - Amount",
                        hover_name="District",
                        color="Amount",
                        color_continuous_scale=px.colors.sequential.Greens)
        st.plotly_chart(fig1)
    col1,col2 = st.columns(2)
    with col1:
        fig2 = px.bar(df3,
                        x="District", y="Count",
                        title=" Top Performing District - Count",
                        hover_name="District",
                        color="Count",
                        color_continuous_scale=px.colors.sequential.Redor)
        st.plotly_chart(fig2)
    with col2:
        fig3 = px.bar(df4,
                        x="District", y="Count",
                        title="Least Performing District - Count",
                        hover_name="District",
                        color="Count",
                        color_continuous_scale=px.colors.sequential.Greens)
        st.plotly_chart(fig3)
        
    st.header("Insights")
    max_state = df1.loc[df1['Amount'].idxmax(), 'District'].title()
    max_amount = df1['Amount'].max()
    min_state = df2.loc[df2['Amount'].idxmin(), 'District'].title()
    min_amount = df2['Amount'].min()

    # Count-based insights
    max_state_count = df3.loc[df3['Count'].idxmax(), 'District'].title()
    max_count = df3['Count'].max()
    min_state_count = df4.loc[df4['Count'].idxmin(), 'District'].title()
    min_count = df4['Count'].min()

    

    st.write(f"{max_state} leads in Transaction Amount ({max_amount} ↑), while {min_state} has the lowest Transaction Amount ({min_amount} ↓).")
    st.write(f"{max_state_count} leads in Transaction Count ({max_count} ↑), while {min_state_count} has the lowest Transaction Count ({min_count} ↓).")

    cursor.close()
    mydb.close()

def Top_Transactions_Pincode():


    mydb = psycopg2.connect(
            password="Nixon17",
            port="5432",
            host="localhost",
            database="phonepe_db",
            user="postgres"
        )
    cursor = mydb.cursor()

        # Top performing district by transaction amount
    query1 = f'''
            SELECT pin_code, SUM(transaction_amount) AS Trans_Amount
            FROM top_transaction
            GROUP BY pin_code
            ORDER BY Trans_Amount desc
            LIMIT 10;
        '''
    cursor.execute(query1)
    result1 = cursor.fetchall()
    df1 = pd.DataFrame(result1, columns=["Pincode", "Amount"])

        # Least performing district by transaction amount
        
    query2 = f'''
            SELECT pin_code, SUM(transaction_amount) AS Trans_Amount
            FROM top_transaction
            GROUP BY pin_code
            ORDER BY Trans_Amount asc
            LIMIT 10;
        '''
    cursor.execute(query2)
    result2 = cursor.fetchall()
    df2 = pd.DataFrame(result2, columns=["Pincode", "Amount"])  

    # Top performing states by transaction count
    query3 = f'''
            SELECT pin_code, SUM(transaction_count) AS Trans_Count
            FROM top_transaction
            GROUP BY pin_code
            ORDER BY Trans_Count desc
            LIMIT 10;
        '''
    cursor.execute(query3)
    result3 = cursor.fetchall()
    df3 = pd.DataFrame(result3, columns=["Pincode", "Count"])

    query4 = f'''
            SELECT pin_code, SUM(transaction_count) AS Trans_Count
            FROM top_transaction
            GROUP BY pin_code
            ORDER BY Trans_Count asc
            LIMIT 10;
        '''
    cursor.execute(query4)
    result4 = cursor.fetchall()
    df4 = pd.DataFrame(result4, columns=["Pincode", "Count"])
        # Visualizations
        
    col1,col2 = st.columns(2)
    with col1:
        fig = px.pie(df1,
                        names="Pincode", values="Amount",
                        title=" Top Performing Pincode - Amount",
                        hover_name="Pincode",
                        color="Amount")
        st.plotly_chart(fig)
    with col2:
        fig1 = px.pie(df2,
                        names ="Pincode", values="Amount",
                        title="Least Performing Pincode - Amount",
                        hover_name="Pincode",
                        color="Amount")
        st.plotly_chart(fig1)
    col1,col2 = st.columns(2)
    with col1:
        fig2 = px.pie(df3,
                        names ="Pincode", values ="Count",
                        title=" Top Performing Pincode - Count",
                        hover_name="Pincode",
                        color="Count")
        st.plotly_chart(fig2)
    with col2:
        fig3 = px.pie(df4,
                        names ="Pincode", values="Count",
                        title="Least Performing Pincode - Count",
                        hover_name="Pincode",
                        color="Count"
                        )
        st.plotly_chart(fig3)
    
    st.header("Insights")
    max_state = df1.loc[df1['Amount'].idxmax(), 'Pincode']
    max_amount = df1['Amount'].max()
    min_state = df2.loc[df2['Amount'].idxmin(), 'Pincode']
    min_amount = df2['Amount'].min()

    # Count-based insights
    max_state_count = df3.loc[df3['Count'].idxmax(), 'Pincode']
    max_count = df3['Count'].max()
    min_state_count = df4.loc[df4['Count'].idxmin(), 'Pincode']
    min_count = df4['Count'].min()

    

    st.write(f"{max_state} leads in Transaction Amount ({max_amount} ↑), while {min_state} has the lowest Transaction Amount ({min_amount} ↓).")
    st.write(f"{max_state_count} leads in Transaction Count ({max_count} ↑), while {min_state_count} has the lowest Transaction Count ({min_count} ↓).")

    cursor.close()
    mydb.close()

def Top_Insurance_Pincode1(year,quarter):


    mydb = psycopg2.connect(
            password="Nixon17",
            port="5432",
            host="localhost",
            database="phonepe_db",
            user="postgres"
        )
    cursor = mydb.cursor()

        # Top performing district by transaction amount
    query1 = f'''
            SELECT pin_code,year,quarter, SUM(transaction_amount) AS Trans_Amount
            FROM top_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY pin_code,year,quarter
            ORDER BY Trans_Amount desc
            LIMIT 10;
        '''
    cursor.execute(query1)
    result1 = cursor.fetchall()
    df1 = pd.DataFrame(result1, columns=["Pincode","Year","Quarter", "Amount"])

        # Least performing district by transaction amount
        
    query2 = f'''
            SELECT pin_code,year,quarter, SUM(transaction_amount) AS Trans_Amount
            FROM top_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY pin_code,year,quarter
            ORDER BY Trans_Amount asc
            LIMIT 10;
        '''
    cursor.execute(query2)
    result2 = cursor.fetchall()
    df2 = pd.DataFrame(result2, columns=["Pincode","Year","Quarter", "Amount"])  

    # Top performing states by transaction count
    query3 = f'''
            SELECT pin_code,year,quarter, SUM(transaction_count) AS Trans_Count
            FROM top_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY pin_code,year,quarter
            ORDER BY Trans_Count desc
            LIMIT 10;
        '''
    cursor.execute(query3)
    result3 = cursor.fetchall()
    df3 = pd.DataFrame(result3, columns=["Pincode","Year","Quarter", "Count"])

    query4 = f'''
            SELECT pin_code,year,quarter, SUM(transaction_count) AS Trans_Count
            FROM top_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY pin_code,year,quarter
            ORDER BY Trans_Count asc
            LIMIT 10;
        '''
    cursor.execute(query4)
    result4 = cursor.fetchall()
    df4 = pd.DataFrame(result4, columns=["Pincode","Year","Quarter","Count"])
        # Visualizations
        
    col1,col2 = st.columns(2)
    with col1:
        fig = px.pie(df1,
                        names="Pincode", values="Amount",
                        title=" Top Performing Pincode - Amount",
                        hover_name="Pincode",
                        color="Pincode")
        st.plotly_chart(fig)
    with col2:
        fig1 = px.pie(df2,
                        names ="Pincode", values="Amount",
                        title="Least Performing Pincode - Amount",
                        hover_name="Pincode",
                        color="Pincode")
        st.plotly_chart(fig1)
    col1,col2 = st.columns(2)
    with col1:
        fig2 = px.pie(df3,
                        names ="Pincode", values ="Count",
                        title=" Top Performing Pincode - Count",
                        hover_name="Pincode",
                        color="Pincode")
        st.plotly_chart(fig2)
    with col2:
        fig3 = px.pie(df4,
                        names ="Pincode", values="Count",
                        title="Least Performing Pincode - Count",
                        hover_name="Pincode",
                        color="Pincode"
                        )
        st.plotly_chart(fig3)
    
    

    

    

    
def Transaction_Type():
    mydb = psycopg2.connect(
        password = "Nixon17",
        database = "phonepe_db",
        port = "5432",
        user = "postgres",
        host = "localhost"
        )
    cursor = mydb.cursor()
    
    query1 = f'''SELECT 
        transaction_name,
        SUM(transaction_amount) AS total_amount,
        SUM(transaction_count) AS total_count
    FROM aggregated_transaction
    GROUP BY transaction_name;'''

    cursor.execute(query1)
    result1 = cursor.fetchall()

    df = pd.DataFrame(result1, columns = ["Transaction_Type","Total_Amount","Total_Count"])
    
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Transaction Type - Amount")
        fig1 = px.pie(df, names = 'Transaction_Type', values = 'Total_Amount',
                      hover_name = 'Transaction_Type',
                      color="Total_Amount"
                       )
        
        st.plotly_chart(fig1)
        
    with col2:
        st.subheader("Transaction Type - Count")
        fig2 = px.pie(df, names = 'Transaction_Type', values = 'Total_Count',
                      hover_name = 'Transaction_Type',
                      color="Total_Count"
                        )
        st.plotly_chart(fig2)
    st.header("Insights")

    # Find max/min transaction types by amount
    max_amount_row = df.loc[df["Total_Amount"].idxmax()]
    min_amount_row = df.loc[df["Total_Amount"].idxmin()]

    # Find max/min transaction types by count
    max_count_row = df.loc[df["Total_Count"].idxmax()]
    min_count_row = df.loc[df["Total_Count"].idxmin()]

    st.write(f"{max_amount_row['Transaction_Type']} has the highest transaction amount ({max_amount_row['Total_Amount']} ↑), "
            f"while {min_amount_row['Transaction_Type']} has the lowest ({min_amount_row['Total_Amount']} ↓).")

    st.write(f"{max_count_row['Transaction_Type']} has the highest transaction count ({max_count_row['Total_Count']} ↑), "
            f"while {min_count_row['Transaction_Type']} has the lowest ({min_count_row['Total_Count']} ↓).")
    
def Top_Transactions_Quarters(quarter):


    mydb = psycopg2.connect(
            password="Nixon17",
            port="5432",
            host="localhost",
            database="phonepe_db",
            user="postgres"
        )
    cursor = mydb.cursor()

        # Top performing district by transaction amount
    query1 = f'''
                        SELECT 
                states, quarter
                ,
                SUM(transaction_amount) AS total_amount
                
            FROM aggregated_transaction
            GROUP BY states, quarter
            having quarter = {quarter}
            order by total_amount desc
            limit 10;
        '''
    cursor.execute(query1)
    result1 = cursor.fetchall()
    df1 = pd.DataFrame(result1, columns=["State","Quarter", "Amount"])

        # Least performing district by transaction amount
        
    query2 = f'''
                        SELECT 
                states, quarter
                ,
                SUM(transaction_amount) AS total_amount
                
            FROM aggregated_transaction
            GROUP BY states, quarter
            having quarter = {quarter}
            order by total_amount asc
            limit 10;
        '''
    cursor.execute(query2)
    result2 = cursor.fetchall()
    df2 = pd.DataFrame(result2, columns=["State","Quarter", "Amount"])  

    # Top performing states by transaction count
    query3 = f'''
                        SELECT 
                states, quarter
                ,
                SUM(transaction_count) AS total_count
                
            FROM aggregated_transaction
            GROUP BY states, quarter
            having quarter = {quarter}
            order by total_count desc
            limit 10;
        '''
    cursor.execute(query3)
    result3 = cursor.fetchall()
    df3 = pd.DataFrame(result3, columns=["State","Quarter", "Count"])

    query4 = f'''
                        SELECT 
                states, quarter
                ,
                SUM(transaction_count) AS total_count
                
            FROM aggregated_transaction
            GROUP BY states, quarter
            having quarter = {quarter}
            order by total_count asc
            limit 10;
        '''
    cursor.execute(query4)
    result4 = cursor.fetchall()
    df4 = pd.DataFrame(result4, columns=["State","Quarter", "Count"])
        # Visualizations
        
    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(df1,
                        x ="State", y ="Amount",
                        title=f" Top Performing States Quarter {quarter} - Amount",
                        hover_name="State",
                        color="Amount")
        st.plotly_chart(fig)
    with col2:
        fig1 = px.bar(df2,
                        x ="State", y ="Amount",
                        title=f"Least Performing States Quarter {quarter} - Amount",
                        hover_name="State",
                        color="Amount")
        st.plotly_chart(fig1)
    col1,col2 = st.columns(2)
    with col1:
        fig2 = px.bar(df3,
                        x ="State", y ="Count",
                        title=f"Top Performing States Quarter {quarter} - Count",
                        hover_name="State",
                        color="Count")
        st.plotly_chart(fig2)
    with col2:
        fig3 = px.bar(df4,
                       x ="State", y="Count",
                        title=f"Least Performing States Quarter {quarter} - Count",
                        hover_name="State",
                        color="Count"
                        )
        st.plotly_chart(fig3)
        
    

    cursor.close()
    mydb.close()
   
def Top_Insurance_State(year,quarter):


    mydb = psycopg2.connect(
            password="Nixon17",
            port="5432",
            host="localhost",
            database="phonepe_db",
            user="postgres"
        )
    cursor = mydb.cursor()

        # Top performing states by transaction amount
    query1 = f'''
            SELECT states,year,quarter, SUM(transaction_amount) AS Trans_Amount
            FROM aggregated_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY states,year,quarter
            ORDER BY Trans_Amount desc
            LIMIT 10;
        '''
    cursor.execute(query1)
    result1 = cursor.fetchall()
    df1 = pd.DataFrame(result1, columns=["States", "Year","Quarter","Amount"])

        # Least performing states by transaction amount
        
    query2 = f'''
            SELECT states,year,quarter, SUM(transaction_amount) AS Trans_Amount
            FROM aggregated_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY states,year,quarter
            ORDER BY Trans_Amount asc
            LIMIT 10;
        '''
    cursor.execute(query2)
    result2 = cursor.fetchall()
    df2 = pd.DataFrame(result2, columns=["States", "Year","Quarter", "Amount"])  

    # Top performing states by transaction count
    query3 = f'''
            SELECT states,year,quarter, SUM(transaction_count) AS Trans_Count
            FROM aggregated_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY states,year,quarter
            ORDER BY Trans_Count desc
            LIMIT 10;
        '''
    cursor.execute(query3)
    result3 = cursor.fetchall()
    df3 = pd.DataFrame(result3, columns=["States", "Year","Quarter", "Count"])

    query4 = f'''
            SELECT states,year,quarter, SUM(transaction_count) AS Trans_Count
            FROM aggregated_insurance
            where year = {year} and quarter = {quarter}
            GROUP BY states,year,quarter
            ORDER BY Trans_Count asc
            LIMIT 10;
        '''
    cursor.execute(query4)
    result4 = cursor.fetchall()
    df4 = pd.DataFrame(result4, columns=["States", "Year","Quarter", "Count"])
        # Visualizations
        
    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(df1,
                        x="States", y="Amount",
                        title=" Top Performing States - Amount",
                        hover_name="States",
                        color="Amount",
                        color_continuous_scale=px.colors.sequential.Redor)
        st.plotly_chart(fig)
    with col2:
        fig1 = px.bar(df2,
                        x="States", y="Amount",
                        title="Least Performing States - Amount",
                        hover_name="States",
                        color="Amount",
                        color_continuous_scale=px.colors.sequential.Greens)
        st.plotly_chart(fig1)
    col1,col2 = st.columns(2)
    with col1:
        fig2 = px.bar(df3,
                        x="States", y="Count",
                        title=" Top Performing States - Count",
                        hover_name="States",
                        color="Count",
                        color_continuous_scale=px.colors.sequential.Redor)
        st.plotly_chart(fig2)
    with col2:
        fig3 = px.bar(df4,
                        x="States", y="Count",
                        title="Least Performing States - Count",
                        hover_name="States",
                        color="Count",
                        color_continuous_scale=px.colors.sequential.Greens)
        st.plotly_chart(fig3)
    st.header("Insights")
    max_state = df1.loc[df1['Amount'].idxmax(), 'States']
    max_amount = df1['Amount'].max()
    min_state = df2.loc[df2['Amount'].idxmin(), 'States']
    min_amount = df2['Amount'].min()

    # Count-based insights
    max_state_count = df3.loc[df3['Count'].idxmax(), 'States']
    max_count = df3['Count'].max()
    min_state_count = df4.loc[df4['Count'].idxmin(), 'States']
    min_count = df4['Count'].min()

    

    st.write(f"{max_state} leads in Insurance Amount ({max_amount} ↑), while {min_state} has the lowest Insurance Amount ({min_amount} ↓).")
    st.write(f"{max_state_count} leads in Insurance  Count ({max_count} ↑), while {min_state_count} has the lowest Insurance Count ({min_count} ↓).")
    

def connect_sql(query):

    mydb = psycopg2.connect(
                password="Nixon17",
                port="5432",
                host="localhost",
                database="phonepe_db",
                user="postgres"
            )
    cursor = mydb.cursor()   
    cursor.execute(query)
    result = cursor.fetchall()
    return result   
    
def Transaction_Growth():
    query =''' with state_year as
(select states,year,sum(transaction_amount) as total
from aggregated_transaction 
group by states,year)
select states,year,total,
lag(total) over (partition by states order by year) as prev_amount,
case when lag(total) over (partition by states order by year) is null
then null
else Round(
(total -  (lag(total)  over (partition by states order by year)))*100/
(lag(total)  over (partition by states order by year)),2)
end as Growth_rate
from state_year
order by states,year
;'''  
    result1 = connect_sql(query)
    df = pd.DataFrame(result1, columns = ["States","Year", "Total_Amount", "prev_amount", "Growth_rate"])
    
    state = sorted(df["States"].unique())
    

    selected_state = st.selectbox("Select State", state)
    

    df_filtered = df[(df["States"] == selected_state)]

    
    fig1 = px.line(df_filtered, x ="Year", y  ="Growth_rate", markers=True,
                            title="Yearly Transaction Amount by State")
    st.plotly_chart(fig1)
    ##st.dataframe(df_filtered[["States", "Year", "Total_Amount", "prev_amount", "Growth_rate"]])
    st.subheader("🧠 Insights")
    for _, row in df_filtered.iterrows():
        if row["Growth_rate"] is not None:
            if row["Growth_rate"] > 0:
                st.write(f"⚡ In {row['Year']}, {selected_state} grew by {row['Growth_rate']}% compared to the previous year.")
            elif row["Growth_rate"] < 0:
                st.write(f"🔻 In {row['Year']}, {selected_state} declined by {abs(row['Growth_rate'])}% compared to the previous year.")
            else:
                st.write(f"⏸️ In {row['Year']}, {selected_state} remained flat with no growth.")

def Transaction_Pincode():
    query =f'''select states,pin_code,sum(transaction_amount) as Amount , sum(transaction_count) as Count
            from top_insurance
            group by states,pin_code
            order by Amount;'''
    result1 = connect_sql(query)
    df = pd.DataFrame(result1, columns = ["States","Pin Code", "Amount","Count"])
    df["Pin Code"] = df["Pin Code"].astype(str)
    
    state = sorted(df["States"].unique())
    

    selected_state = st.selectbox("Select State", state)
    df_filtered = df[(df["States"] == selected_state)]
    
    col1,col2  = st.columns(2)
    with col1:
        fig1 = px.bar(df_filtered, x ="Pin Code", y ="Amount", hover_name = "States")
        st.plotly_chart(fig1) 
    with col2:
        fig2 = px.bar(df_filtered, x ="Pin Code", y  ="Count", hover_name = "States")
        st.plotly_chart(fig2)
    
def Insurance_Growth():
    query =''' with state_year as
(select states,year,sum(transaction_amount) as total
from aggregated_insurance 
group by states,year)
select states,year,total,
lag(total) over (partition by states order by year) as prev_amount,
case when lag(total) over (partition by states order by year) is null
then null
else Round(
(total -  (lag(total)  over (partition by states order by year)))*100/
(lag(total)  over (partition by states order by year)),2)
end as Growth_rate
from state_year
order by states,year
;'''  
    result1 = connect_sql(query)
    df = pd.DataFrame(result1, columns = ["States","Year", "Total_Amount", "prev_amount", "Growth_rate"])
    
    state = sorted(df["States"].unique())
    

    selected_state = st.selectbox("Select State", state)
    

    df_filtered = df[(df["States"] == selected_state)]

    
    fig1 = px.line(df_filtered, x ="Year", y  ="Growth_rate", markers=True,
                            title="Yearly Transaction Amount by State")
    st.plotly_chart(fig1)
    ##st.dataframe(df_filtered[["States", "Year", "Total_Amount", "prev_amount", "Growth_rate"]])
    st.subheader("🧠 Insights")
    for _, row in df_filtered.iterrows():
        if row["Growth_rate"] is not None:
            if row["Growth_rate"] > 0:
                st.write(f"⚡ In {row['Year']}, Insurance taken in {selected_state} grew by {row['Growth_rate']}% compared to the previous year.")
            elif row["Growth_rate"] < 0:
                st.write(f"🔻 In {row['Year']}, Insurance taken in {selected_state} declined by {abs(row['Growth_rate'])}% compared to the previous year.")
            else:
                st.write(f"⏸️ In {row['Year']}, Insurance taken in {selected_state} remained flat with no growth.")        


                
                   
## Streamlit
st.set_page_config(layout = "wide")
st.title("PHONEPE INSIGHTS")


selected = option_menu(
        "Main Menu",
        ["Home", "DATA VISUALIZATION", "Business Case Study"],
        icons=["house", "bookmarks", "award"],
        menu_icon="cast",
        default_index=0,
        orientation= "horizontal"
    )

    # Display content based on selection
if selected == "Home":
    st.title("Welcome to the Phone_Pe")
    st.write("Best Payments App.")
    st.write("Your Daily Companion")
    
    


        
        
        
elif selected == "DATA VISUALIZATION":
    Tab1,Tab2,Tab3 = st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    with Tab1:
        method1 = st.selectbox("Select the Method",["Aggregated Insurance","Aggregated Transaction","Aggregated User"])
        if method1 == "Aggregated Insurance":
            years = st.selectbox(
                "Select the year",
                sorted(Agg_Insurance["Year"].unique()),
                index=len(sorted(Agg_Insurance["Year"].unique()))-1
            )
            quarters = sorted(Agg_Insurance["Quarter"].unique())
            quarter = st.selectbox("Select the quarter (optional)", ["All"] + quarters)

            # Call unified function
            if quarter == "All":
                Agg_insurance_Year(Agg_Insurance, year=years)
            else:
                Agg_insurance_Year(Agg_Insurance, year=years, quarter=quarter)


            
            
            
            
        elif method1 =="Aggregated Transaction":
            years = st.selectbox(
                "Select the year for Aggregated Transaction",
                sorted(Agg_Transaction["Year"].unique()),
                index=len(sorted(Agg_Transaction["Year"].unique()))-1
                )
            quarters = sorted(Agg_Transaction["Quarter"].unique())
            quarter = st.selectbox("Select the quarter (optional) Aggregated Transaction", ["All"] + quarters)
            States = sorted(Agg_Transaction["States"].unique())
            state = st.selectbox("select the State Aggregated Transaction", ["All"] + States)
            
            # Call unified function
            if quarter == "All" and state == "All":
                Agg_Transaction_Year(Agg_Transaction, year=years)
            elif quarter == "All"  and state != "All":
                Variable = Agg_Transaction_Year(Agg_Transaction, year=years)
                Agg_Transaction_State(Variable,state)
            elif quarter != "All" and state == "All":
                
                Agg_Transaction_Year(Agg_Transaction,year = years,quarter=quarter)
            elif quarter == quarter and state == state:
                vars = Agg_Transaction_Year(Agg_Transaction,year = years,quarter=quarter)
                Agg_Transaction_State(vars,state)


           
                  
        elif method1 == "Aggregated User":
            years = st.selectbox(
                "Select the year",
                sorted(Agg_User["Year"].unique()),
                index=len(sorted(Agg_User["Year"].unique()))-1
            )
            quarters = sorted(Agg_User["Quarter"].unique())
            quarter = st.selectbox("Select the quarter (optional)", ["All"] + quarters)
            States = sorted(Agg_User["States"].unique())
            state = st.selectbox("select the State", ["All"] + States)
            # Call unified function
            if quarter == "All" and state == "All":
                Agg_user_Year_Quarter(Agg_User, year=years)
                
            elif quarter == "All" and state == state:
                Variable = Agg_user_Year_Quarter(Agg_User, year=years)
                Agg_user_State(Variable,state)
            elif quarter == quarter and state == "All":
                
                Agg_user_Year_Quarter(Agg_User,year = years,quarter=quarter)
                
            elif quarter == quarter and state == state:
                vars = Agg_user_Year_Quarter(Agg_User,year = years,quarter=quarter)
                Agg_user_State(vars,state)
                
                
                
        with Tab2:
            method2 = st.selectbox("Select the Method",["Map Insurance","Map Transaction","Map User"])
            
            if method2 == "Map Insurance":
                years = st.selectbox(
                "Select the year Map_Insurance",
                sorted(Map_Insurance["Year"].unique()),
                index=len(sorted(Map_Insurance["Year"].unique()))-1,
                key = "Map_Year"
                )
                quarters = sorted(Map_Insurance["Quarter"].unique())
                quarter = st.selectbox("Select the quarter (optional) Map_Insurance", ["All"] + quarters)
                States = sorted(Map_Insurance["States"].unique())
                state = st.selectbox("select the State Map_Insurance", ["All"] + States)
                
                # Call unified function
                if quarter == "All" and state == "All":
                    Map_insurance_Year(Map_Insurance, year=years)
                elif quarter == "All"  and state != "All":
                    Variable = Map_insurance_Year(Map_Insurance, year=years)
                    Map_insurance_State(Variable,state)
                elif quarter != "All" and state == "All":
                    
                    Map_insurance_Year(Map_Insurance,year = years,quarter=quarter)
                elif quarter != "All" and state != "All":
                    vars = Map_insurance_Year(Map_Insurance,year = years,quarter=quarter)
                    Map_insurance_State(vars,state)
                
                
            elif method2 =="Map Transaction":
                years = st.selectbox(
                "Select the year Map_Transaction",
                sorted(Map_Transaction["Year"].unique()),
                index=len(sorted(Map_Transaction["Year"].unique()))-1
                
                )
                quarters = sorted(Map_Transaction["Quarter"].unique())
                quarter = st.selectbox("Select the quarter Map_Transaction", ["All"] + quarters)
                States = sorted(Map_Transaction["States"].unique())
                state = st.selectbox("select the State Map_Transaction", ["All"] + States)
                
                # Call unified function
                if quarter == "All" and state == "All":
                    Map_Transaction_Year(Map_Transaction, year=years)
                elif quarter == "All"  and state != "All":
                    Variable = Map_Transaction_Year(Map_Transaction, year=years)
                    Map_Transaction_State(Variable,state)
                elif quarter != "All" and state == "All":
                    
                    Map_Transaction_Year(Map_Transaction,year = years,quarter=quarter)
                elif quarter != "All" and state != "All":
                    vars = Map_Transaction_Year(Map_Transaction,year = years,quarter=quarter)
                    Map_Transaction_State(vars,state)
                
                
            elif method2 == "Map User":
                years = st.selectbox(
                "Select the year Map_User",
                sorted(Map_User["Year"].unique()),
                index=len(sorted(Map_User["Year"].unique()))-1
                
                )
                quarters = sorted(Map_User["Quarter"].unique())
                quarter = st.selectbox("Select the quarter Map_User", ["All"] + quarters)
                States = sorted(Map_User["States"].unique())
                state = st.selectbox("select the State Map_User", ["All"] + States)
                
                # Call unified function
                if quarter == "All" and state == "All":
                    Map_User_Year(Map_User, year=years)
                elif quarter == "All"  and state != "All":
                    Variable = Map_User_Year(Map_User, year=years)
                    Map_User_State(Variable,state)
                elif quarter != "All" and state == "All":
                    
                    Map_User_Year(Map_User,year = years,quarter=quarter)
                elif quarter != "All" and state != "All":
                    vars = Map_User_Year(Map_User,year = years,quarter=quarter)
                    Map_User_State(vars,state)
        with Tab3:
            method3 = st.selectbox("Select the Method",["Top Insurance","Top Transaction","Top User"])
            if method3 == "Top Insurance":
                years = st.selectbox(
                "Select the year Top_Insurance",
                sorted(Top_Insurance["Year"].unique()),
                index=len(sorted(Top_Insurance["Year"].unique()))-1
                
                )
                quarters = sorted(Top_Insurance["Quarter"].unique())
                quarter = st.selectbox("Select the quarter Top_Insurance", ["All"] + quarters)
                States = sorted(Top_Insurance["States"].unique())
                state = st.selectbox("select the State Top_Insurance", ["All"] + States)
                
                # Call unified function
                if quarter == "All" and state == "All":
                    Top_insurance_Year(Top_Insurance, year=years)
                elif quarter == "All"  and state != "All":
                    Variable = Top_insurance_Year(Top_Insurance, year=years)
                    Top_Insurance_State(Variable,state)
                elif quarter != "All" and state == "All":
                    
                    Top_insurance_Year(Top_Insurance,year = years,quarter=quarter)
                elif quarter != "All" and state != "All":
                    vars = Top_insurance_Year(Top_Insurance,year = years,quarter=quarter)
                    Top_Insurance_State(vars,state)
                    
                    
            elif method3 =="Top Transaction":
                years = st.selectbox(
                "Select the year Top_Transaction",
                sorted(Top_Transaction["Year"].unique()),
                index=len(sorted(Top_Transaction["Year"].unique()))-1
                
                )
                quarters = sorted(Top_Transaction["Quarter"].unique())
                quarter = st.selectbox("Select the quarter Top_Transaction", ["All"] + quarters)
                States = sorted(Top_Transaction["States"].unique())
                state = st.selectbox("select the State Top_Transaction", ["All"] + States)
                
                # Call unified function
                if quarter == "All" and state == "All":
                    Top_Transaction_Year(Top_Transaction, year=years)
                elif quarter == "All"  and state != "All":
                    Variable = Top_Transaction_Year(Top_Transaction, year=years)
                    Top_Transaction_State(Variable,state)
                elif quarter != "All" and state == "All":
                    
                    Top_Transaction_Year(Top_Transaction,year = years,quarter=quarter)
                elif quarter != "All" and state != "All":
                    vars = Top_Transaction_Year(Top_Transaction,year = years,quarter=quarter)
                    Top_Transaction_State(vars,state)
                    
            elif method3 == "Top User":
                years = st.selectbox(
                "Select the year Top_User",
                sorted(Top_User["Year"].unique()),
                index=len(sorted(Top_User["Year"].unique()))-1
                
                )
                quarters = sorted(Top_User["Quarter"].unique())
                quarter = st.selectbox("Select the quarter Top_User", ["All"] + quarters)
                States = sorted(Top_User["States"].unique())
                state = st.selectbox("select the State Top_User", ["All"] + States)
                
                # Call unified function
                if quarter == "All" and state == "All":
                    Top_User_Year(Top_User, year=years)
                elif quarter == "All"  and state != "All":
                    Variable = Top_User_Year(Top_User, year=years)
                    Top_User_State(Variable,state)
                elif quarter != "All" and state == "All":
                    
                    Top_User_Year(Top_User,year = years,quarter=quarter)
                elif quarter != "All" and state != "All":
                    vars = Top_User_Year(Top_User,year = years,quarter=quarter)
                    Top_User_State(vars,state)
                    
                    
elif selected == "Business Case Study":
    st.title("Business Case Study")
    questions = st.selectbox("Select the question",["1. Decoding Transaction Dynamics on PhonePe",
                                                    "2. Device Dominance and User Engagement Analysis",
                                                    "3. Insurance Penetration and Growth Potential Analysis",
                                                    "4. Transaction Analysis for Market Expansion",
                                                    "5. User Engagement and Growth Strategy",
                                                    "6. Insurance Engagement Analysis",
                                                    "7. Transaction Analysis Across States and Districts",
                                                    "8. User Registration Analysis",
                                                    "9. Insurance Transactions Analysis"] )
    
    if questions == "7. Transaction Analysis Across States and Districts":
        Transaction_analysis = st.selectbox("Select ",["States","District","Pincode","User_Engagement"])
        if Transaction_analysis == "States":
            Top_Transactions_State()
        elif Transaction_analysis == "District":    
            Top_Transactions_District()
        elif Transaction_analysis == "Pincode":
            Top_Transactions_Pincode()
        elif Transaction_analysis == "User_Engagement":
            Transaction_Type()
    elif questions == "1. Decoding Transaction Dynamics on PhonePe":
        Transaction_analysis = st.selectbox("Select ",["States","Quarter","Transaction_Type","Growth rate Yearly"])
        if Transaction_analysis == "States":
            Top_Transactions_State()
        elif Transaction_analysis == "Quarter": 
            quarter = st.selectbox("Select the Quarter",[1,2,3,4])   
            Top_Transactions_Quarters(quarter = quarter)
        elif Transaction_analysis == "Transaction_Type":
            Transaction_Type()
        elif Transaction_analysis == "Growth rate Yearly":   
            Transaction_Growth()
            
    elif questions == "4. Transaction Analysis for Market Expansion":
        Transaction_analysis = st.selectbox("Select ",["States","Growth rate"])
        if Transaction_analysis == "States":
            Top_Transactions_State()
        elif Transaction_analysis == "Growth rate":   
            Transaction_Growth()
    elif questions =="9. Insurance Transactions Analysis":
        Transaction_analysis = st.selectbox("Select ",["States","District","Pincode"])
        if Transaction_analysis == "States":
            year = st.selectbox("Select the year",[2020,2021,2022,2023,2024])
            quarter = st.selectbox("Select the quarter",[1,2,3,4])
            Top_Insurance_State(year,quarter)
        elif Transaction_analysis == "District":    
            year = st.selectbox("Select the year",[2020,2021,2022,2023,2024])
            quarter = st.selectbox("Select the quarter",[1,2,3,4])
            Top_Insurance_District(year,quarter)
        elif Transaction_analysis == "Pincode":
            year = st.selectbox("Select the year",[2020,2021,2022,2023,2024])
            quarter = st.selectbox("Select the quarter",[1,2,3,4])
            Top_Insurance_Pincode1(year,quarter)
        
    elif questions == "3. Insurance Penetration and Growth Potential Analysis":
        Insurance_analysis = st.selectbox("Select ",["States","Growth rate"])
        if Insurance_analysis == "Growth rate":
            Insurance_Growth()
        if Insurance_analysis == "States":
            year = st.selectbox("Select the year",[2020,2021,2022,2023,2024])
            quarter = st.selectbox("Select the quarter",[1,2,3,4])
            Top_Insurance_State(year,quarter)
        
        
