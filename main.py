import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

@st.cache_data
def read_data():
    df = pd.read_csv(URL, dtype={'Quarter': str, 
                            'Canada': np.int32,
                            'Newfoundland and Labrador': np.int32,
                            'Prince Edward Island': np.int32,
                            'Nova Scotia': np.int32,
                            'New Brunswick': np.int32,
                            'Quebec': np.int32,
                            'Ontario': np.int32,
                            'Manitoba': np.int32,
                            'Saskatchewan': np.int32,
                            'Alberta': np.int32,
                            'British Columbia': np.int32,
                            'Yukon': np.int32,
                            'Northwest Territories': np.int32,
                            'Nunavut': np.int32})
    return df


@st.cache_data
def format_date(date):
    if date[1] == 2:
        return float(date[2:]) + 0.25
    elif date[1] ==3:
        return float(date[2:]) + 0.50
    elif date[1] ==4:
        return float(date[2:]) + 0.75
    else:
        return float(date[2:])
    
@st.cache_data
def end_before_start(start_date, end_date):
    num_start_date = format_date(start_date)
    num_end_date = format_date(end_date)

    if num_start_date > num_end_date:
        return True
    else:
        return False
    
def display_dashboard(start_date,end_date,location):
    tab1,tab2 = st.tabs(['Population change','Compare'])

    with tab1:
        st.subheader(f'Population change from {start_date} to {end_date} in {location}')
        col1,col2 = st.columns(2)

        with col1:
            #initial = df.loc[df['Quarter'] == start_date,location].item()
            initial = df.loc[df['Quarter'] == start_date,location].item()
            final = df.loc[df['Quarter'] == end_date,location].item()

            percentage_diff = round((final - initial)/initial * 100,2)
            delta = f'{percentage_diff}%'
            st.metric(start_date,value=initial)
            st.metric(end_date,value=final,delta=delta)
        
        with col2:
            start_idx = df.loc[df['Quarter'] == start_date].index.item()
            end_idx = df.loc[df['Quarter'] == end_date].index.item()

            filtered_df = df.iloc[start_idx:end_idx+1]

            fig,ax = plt.subplots()
            ax.plot(filtered_df['Quarter'],filtered_df[location])
            ax.set_xlabel('Time')
            ax.set_ylabel('Population')
            ax.set_xticks([filtered_df['Quarter'].iloc[0],filtered_df['Quarter'].iloc[-1]])
            fig.autofmt_xdate()
            st.pyplot(fig)
    
    with tab2:
        st.subheader('Compare with other locations')
        all_targets = st.multiselect('Choose other locations',options=df.columns[1:],default=[location])
        fig,ax = plt.subplots()
        for each in all_targets:
            ax.plot(filtered_df['Quarter'],filtered_df[each])
        ax.set_xlabel('Time')
        ax.set_ylabel('Population')
        ax.set_xticks([filtered_df['Quarter'].iloc[0],filtered_df['Quarter'].iloc[-1]])
        st.pyplot(fig)

if __name__ == '__main__':
    df = read_data()
    st.title('Population of Canada')
    st.markdown('Source table can be found [here](https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv)')
    with st.expander('See full data table'):
        st.write(df)
    
    with st.form('form_key'):
        col1,col2,col3 = st.columns(3)
        with col1:
            st.write('Choose a starting date')
            start_quarter = st.selectbox('Quarter',options=['Q1','Q2','Q3','Q4'],index=2, key='start_q')
            start_year = st.slider('Year',min_value=1991,max_value=2023,value=1991,step=1,key='start_y')
        
        with col2:
            st.write('Choose an end date')
            end_quarter = st.selectbox('Quarter',options=['Q1','Q2','Q3','Q4'],index=2, key='end_q')
            end_year = st.slider('Year',min_value=1991,max_value=2023,value=2023,step=1,key='end_y')
        
        with col3:
            st.write('Choose a location')
            location = st.selectbox('choose a location',options=df.columns[1:],index=0)
        sbmt_btn = st.form_submit_button('Analyze',type='primary')

    start_date = f'{start_quarter} {start_year}'
    end_date = f'{end_quarter} {end_year}'
    if start_date not in df['Quarter'].to_list() or end_date not in df['Quarter'].to_list():
        st.error('No data available. Check your quarter and year selection')
    elif end_before_start(start_date,end_date):
        st.error('Dates dont work. Start date must come before end date.')
    else:
        display_dashboard(start_date,end_date,location)

