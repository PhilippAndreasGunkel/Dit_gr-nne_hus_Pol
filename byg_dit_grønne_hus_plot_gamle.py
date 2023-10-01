# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 15:30:48 2023

@author: phgu
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
#print(os.getcwd())
#os.chdir(os.getcwd())

import streamlit as st



passport = "BAU1899"
password = st.text_input("Enter a password", type="password")
#password=passport
cols=['H_ID', 'Category', 'Electricity cost',
       'Electricity production cost from PV', 'Electricity cost from import',
       'Grid tariff cost', 'Tax cost', 'Revenue from electricity export',
       'Tax reimbursment', 'Total cost of electricity', 'PV to HP', 'BT to HP',
       'MP to HP', 'PV to EV', 'BT to EV', 'MP to EV', 'PV to BT', 'PV to MP',
       'BT to MP', 'MP to BT', 'MP to CO', 'BT to CO', 'PV to CO',
       'Capacity of PV', 'Capacity of HST', 'Capacity of BT', 'Capacity of HP',
       'scenario', 'Total electricity import', 'Total transmission GT',
       'Total distribution GT', 'Total cost of electricity import after VAT',
       'Total cost of electricity import before VAT', 'Investment_cost_PV',
       'Investment_cost_HST', 'Investment_cost_BT', 'Investment_cost_HP',
       'Investment_cost_PV_VAT', 'Investment_cost_HST_VAT',
       'Investment_cost_BT_VAT', 'Investment_cost_HP_VAT',
       'Total investment cost before VAT', 'Total investment cost after VAT',
       'Total cost before VAT', 'Total cost after VAT', 'VAT_payments',
       'Occupancy', 'Dwelling size', 'Income', 'PV', 'BT', 'HST', 'HP', 'EV',
       'Distance', 'Yearly heat consumption', 'A_ID', 'Potential HP Capacity',
       'Base electricity consumption']

cols = ['H_ID', 'Category','Capacity of PV','Occupancy', 'Dwelling size', 'Income', 'PV', 'BT', 'HST', 'HP', 'EV',
'Distance', 'Yearly heat consumption', 'A_ID', 'Potential HP Capacity',  'MP to CO', 'BT to CO', 'PV to CO',
'Base electricity consumption','scenario','Self-sufficiency','Total cost of electricity import after VAT','Capacity of BT','Total yearly consumption']

#password=passport
if passport == password:
    #@st.cache
    def read_data():
        #df_hus_ = pd.read_csv("data/hushold_data.csv",index_col=0)
        #df_hus_ = pd.read_table(r"https://docs.google.com/spreadsheets/d/1OfwiZa91SPHceolfvtbnltDUqHoUHiuA_VJxnpyxP-Q/edit?usp=sharing")
        #os.chdir("data/")
        df_list = []
        for col in cols:
            col_df = pd.read_csv("data/" + col + ".csv")
            df_list.append(col_df)

        new_df = pd.concat(df_list, axis=1)
        df_hus_ = new_df
        #os.chdir("..")
        return df_hus_
    
    df_hus = read_data()
    
    
    st.title("Dit grønne hus")
    st.header("Before you start")
    st.write("We offer two methods of describing your household in a better way:")
    st.write("1. Enter yearly consumption data")
    st.write("2. Choose among predefined household categories")
    st.write("The categorization leaves more broad results of PV sizes, whereas the definition of consumption can lead to more precise outcomes. Still, provide ranges to make sure that there is enough robustness in the outcomes!")
    
    st.write("")
    
    hus_cat_choices = ['Consumption data','Household categorization']
    hus_cat = st.selectbox("Choose the occupancy range of your household. P1: 1 person, P2: 2 persons, P3: 3-4 persons, P5+: 5 or more persons",
                                    options=hus_cat_choices)
    
    
    if hus_cat == 'Household categorization':
        df_hus=df_hus.rename({"Potential HP Capacity":"Base electricity consumption"})
        df_hus["Base electricity consumption"] = df_hus["BT to CO"] + df_hus["MP to CO"] + df_hus["PV to CO"]
        
        st.header("Categories: Chose the categories that describe your household best")
        
        st.write("In order to give more precise representation of your households we would like you to choose among the following categorizations")
        # Ask user for occupancy range selection
        occupancy_options = df_hus["Occupancy"].unique()
        occupancy_range = st.selectbox("Choose the occupancy range of your household. P1: 1 person, P2: 2 persons, P3: 3-4 persons, P5+: 5 or more persons",
                                        options=occupancy_options)
        
        # Filter df_hus based on occupancy range selection
        df_filtered = df_hus[df_hus["Occupancy"] == occupancy_range]
        #H_P5+_A1_€3
        
        heated_area_options = df_hus["Dwelling size"].unique()
        heated_area_range = st.selectbox("What is the heated area of your home? A1: <110sqm, A2 110-146sqm, A3: >146sqm",
                                        options=heated_area_options)
        
        
        st.write("Sizes of PV dependent on your future technology choice")
        # Filter df_filtered based on PV column where value is 1
        
        # Filter df_hus based on heated area selection
        df_filtered = df_filtered[df_filtered["Dwelling size"] == heated_area_range]
        
        
        
        income_options = df_hus["Income"].unique()
        income_range = st.selectbox("Which income group would you rank your household in? €1: <240.000kr/year, €2: 240.000-449.000kr/year, €3: >449.000kr/year",
                                        options=income_options)
            
        # Filter df_hus based on heated area selection
        df_filtered = df_filtered[df_filtered["Income"] == income_range]
        
        df_pv = df_filtered[df_filtered["PV"] == "Yes"]
        df_pv= df_pv.sort_values(by="scenario",ascending = False)
        
        st.header("Results: Capacity of PV dependent on your future Technology investment plans in [kWp]")
        # Create boxplot using Plotly Express
        fig = px.box(df_pv, x="scenario", y="Capacity of PV",
                     title="HP = Heat pump, EV = electric vehicle, BT = Battery, HighPrice = El prices comparable to 2022 levels")
        
        st.plotly_chart(fig)
        
    
    if hus_cat == 'Consumption data':
        
        st.header("Consumption: provide ranges of yearly consumption")
        
        # Ask user for yearly electricity consumption range
        consumption_min = df_hus["Base electricity consumption"].min()
        consumption_max = df_hus["Base electricity consumption"].max()
        consumption_range = st.slider("Choose a range of yearly electricity consumption of your household in kWh/year",
                                      min_value=consumption_min, max_value=consumption_max, value=(4323.25, 4738.7))
        
        # Filter df_hus based on yearly electricity consumption range selection
        df_filtered_2 = df_hus[(df_hus["Base electricity consumption"] >= consumption_range[0]) & (df_hus["Base electricity consumption"] <= consumption_range[1])]
        
        # Ask user for yearly electricity consumption range
        consumption_min = df_hus["Yearly heat consumption"].min()
        consumption_max = df_hus["Yearly heat consumption"].max()
        st.write("If you only know your yearly gas consumption convert over here:")
        input_value = st.number_input('Enter your yearly gas consumption in m3')
        gas_conv = input_value*0.98*10.55
        st.write('Your yearly gas consumption in kWh is: '+str(gas_conv))
        consumption_range = st.slider("Choose a range of yearly heat consumption of your household in kWh/year",
                                      min_value=consumption_min, max_value=consumption_max, value=(9535.5, 11491.5))
        
        # Filter df_hus based on yearly electricity consumption range selection
        df_filtered_2 = df_filtered_2[(df_filtered_2["Yearly heat consumption"] >= consumption_range[0]) & (df_filtered_2["Yearly heat consumption"] <= consumption_range[1])]
        
        
        # Ask user for yearly electricity consumption range
        consumption_min = df_hus["Distance"].min()
        consumption_max = df_hus["Distance"].max()
        consumption_range = st.slider("Choose a range of yearly driving distance in km/year. Leave full range if you dont own a vehicle.",
                                      min_value=consumption_min, max_value=consumption_max, value=(8955.30, 14874.40))
        
        # Filter df_hus based on yearly electricity consumption range selection
        df_filtered_2 = df_filtered_2[(df_filtered_2["Distance"] >= consumption_range[0]) & (df_filtered_2["Distance"] <= consumption_range[1])]
        
        df_pv_2 = df_filtered_2[df_filtered_2["PV"] == "Yes"]
        df_pv_2= df_pv_2.sort_values(by="scenario",ascending = False)
        
        if df_pv_2.empty:
            st.write("No datapoints for this selection available")
        
        else:
            st.header("Results: Capacity of PV dependent on your future Technology investment plans in [kWp]")
            # Create boxplot using Plotly Express
            fig = px.box(df_pv_2, x="scenario", y="Capacity of PV",
                         title="HP = Heat pump, EV = electric vehicle, BT = Battery, HighPrice = El prices comparable to 2022 levels")
            
            st.plotly_chart(fig)
        
        df_filtered = df_filtered_2

    
    
    st.header("Detailed effects of your choice")

    st.write('Which technology bundle are you looking for?')
    tech_bundles = df_filtered['scenario'].unique()
    choice_tech_bundle = st.selectbox("HP = Heat pump, EV = electric vehicle, BT = Battery, HighPrice = El prices comparable to 2022 levels",
                                    options=tech_bundles)
    df_filtered_tech = df_filtered[df_filtered['scenario']==choice_tech_bundle]
    df_filtered_tech["Consumption per kWp of PV"] = df_filtered_tech['Total yearly consumption']/df_filtered_tech["Capacity of PV"]
    
    
    st.header("Expected yearly electricity bill dependent on PV size. Excl. DSO subsription fees of between 400-800Kr/year dependent on your operator")
    # Create boxplot using Plotly Express
    fig = px.box(df_filtered_tech, x="Capacity of PV", y='Total cost of electricity import after VAT')
    fig.update_yaxes(title="Kr/year")
    fig.update_xaxes(title="kWp")
    st.plotly_chart(fig)


    st.header("Expected self-sufficiency dependent on PV size")
    # Create boxplot using Plotly Express
    df_filtered_tech['Self-sufficiency']=df_filtered_tech['Self-sufficiency']*100
    fig = px.box(df_filtered_tech, x="Capacity of PV", y='Self-sufficiency')
    fig.update_yaxes(title="%")
    fig.update_xaxes(title="kWp")
    st.plotly_chart(fig)

    st.header("PV size dependent on total consumption")
    # Create boxplot using Plotly Express
    fig = px.box(df_filtered_tech, x='Total yearly consumption', y="Capacity of PV")
    fig.update_yaxes(title="kWp")
    fig.update_xaxes(title="kWh")
    st.plotly_chart(fig)
    

    if df_filtered_tech['BT'].unique()[0]=='Yes':
        st.header("PV and battery storage mix - Note: batteries might not be a profitable choice")
        # Create boxplot using Plotly Express
        fig = px.box(df_filtered_tech, x="Capacity of PV", y='Capacity of BT')
        fig.update_yaxes(title="kWh")
        fig.update_xaxes(title="kWp")
        st.plotly_chart(fig)




    #!streamlit run byg_dit_grønne_hus_plot_gamle.py

















#df_hus_2 = df_hus[df_hus["scenario"].isin(['BT_EV_HP_PV','BT_HP','BT_HP_PV', 'BT_PV',  'EV', 'EV_HP', 'EV_HP_PV','EV_PV', 'HP', 'HP_PV', 'noTech', 'PV'])]
#df_hus_2 = df_hus[df_hus["scenario"].isin(['BT_EV_HP_PV','BT_PV','noTech','BT_EV_HP_PV_HighPrice_noTax', 'BT_EV_HP_PV_noTax', 'BT_EV_HP_PV_HighPrice','BT_PV_HighPrice','noTech_HighPrice'])]



#os.chdir("/Users/philippandreasgunkel/Desktop/Python/Dit-gr-nne-hus-main_standard/data_pol")

#for col in df_hus_2.columns:
#    df_hus_2[col].to_csv(str(col)+".csv",index=False)


# # set the directory containing the CSV files
# dir_path = "data/"

# # initialize an empty list to store the dataframes
# dfs = []

# # loop over each file in the directory
# for filename in os.listdir(dir_path):
#     if filename.endswith('.csv'):
#         # construct the full filepath for the CSV file
#         filepath = os.path.join(dir_path, filename)
#         # read the CSV file into a dataframe and append it to the list
#         df = pd.read_csv(filepath)
#         dfs.append(df)

# # concatenate all of the dataframes into a single dataframe
# merged_df = pd.concat(dfs)
# merged_df=merged_df.drop(columns=['sub_string', 'Capacity of heat','Investment cost heat before VAT','Total grid tariff heat','Total heat tax','Total heat CO2 tax','Total heat environmental tax','Total heat cost','Total cost of heating before VAT','Investment cost heat after VAT','Total cost of heating after VAT','Total transport tax','Total transport CO2 tax','Total transport environmental tax','Total transport cost','Total cost of transport before VAT','Total cost of transport after VAT'])
# # print the first few rows of the merged dataframe
# print(merged_df.head())



# merged_df.to_csv("hushold_data.csv")
# df = pd.read_csv(filepath)

#    df_hus['Self-sufficiency'] =  1-df_hus['Total electricity import']/(df_hus[['PV to HP','PV to EV','PV to BT','PV to CO']].sum(axis=1)+df_hus['Total electricity import'])
#    df_hus['Total yearly consumption'] =  (df_hus[['PV to HP','BT to HP','MP to HP','PV to EV','BT to EV','MP to EV','PV to CO','BT to CO','MP to CO']].sum(axis=1))






