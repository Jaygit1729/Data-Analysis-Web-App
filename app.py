import pandas as pd
import streamlit as st
import Preprocessing
import helper
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go

st.sidebar.title("Summer Olympic Analysis (1896-2016)")

st.sidebar.image("https://logos-world.net/wp-content/uploads/2021/09/Olympics-Logo-700x394.png")


# Custom CSS to increase the width of the sidebar

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 350px;  /* Set your desired width */
    }
    </style>
    """,
    unsafe_allow_html=True)


df = Preprocessing.preprocess()

user_menu = st.sidebar.radio(
                            'Select an option', 
                            ['🥇 Medal Tally', 
                            '📊 Overall Analysis', 
                            '🌍 Country-Wise Analysis', 
                            '🏃 Athlete-Wise Analysis'] 
                            )


if user_menu == '🥇 Medal Tally':
    st.sidebar.header("🥇 Medal Tally")  

    year, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",year)
    selected_country = st.sidebar.selectbox("Select Country",country)
    
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country=='Overall':
        st.title('Overall Medal Tally')
    elif selected_year == 'Overall' and selected_country !='Overall':
        st.title('Year Wise Medal Tally for {}'.format(selected_country))
    elif selected_year != 'Overall' and selected_country =='Overall':
        st.title('Total Medal Tally for the year {}.'.format(selected_year))
    else:
        st.title('Medal tally for {} in {}'.format(selected_country,selected_year))

    st.table(medal_tally)

    st.title("Medal Tally Trend")

    # Create traces for Gold, Silver, Bronze, and Total medals
    fig11 = go.Figure()

    # Line for Gold medals
    fig11.add_trace(go.Scatter(x=medal_tally['Year'] if 'Year' in medal_tally.columns else medal_tally['region'],
                             y=medal_tally['Gold'], mode='lines+markers', name='Gold',
                             line=dict(color='gold', width=4)))

    # Line for Silver medals
    fig11.add_trace(go.Scatter(x=medal_tally['Year'] if 'Year' in medal_tally.columns else medal_tally['region'],
                             y=medal_tally['Silver'], mode='lines+markers', name='Silver',
                             line=dict(color='silver', width=2)))

    # Line for Bronze medals
    fig11.add_trace(go.Scatter(x=medal_tally['Year'] if 'Year' in medal_tally.columns else medal_tally['region'],
                             y=medal_tally['Bronze'], mode='lines+markers', name='Bronze',
                             line=dict(color='#cd7f32', width=2)))

    # Line for Total medals
    fig11.add_trace(go.Scatter(x=medal_tally['Year'] if 'Year' in medal_tally.columns else medal_tally['region'],
                             y=medal_tally['Total'], mode='lines+markers', name='Total',
                             line=dict(color='black', width=2)))
    
    helper.customize_plotly_chart(fig11,'Country','Number of Medals',f"Medal Tally for {selected_country} in {selected_year}",width= 800,height=600)

    st.plotly_chart(fig11)

elif user_menu == '📊 Overall Analysis':

    # Displaying the KPI of Olympic Games as a tile

    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    events = df['Event'].nunique()
    sports = df['Sport'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title('🎯Top Statistics for the Olympic 🎯')

    col1, col2, col3 = st.columns(3)                                                # Create a grid using st.columns
    col4, col5, col6 = st.columns(3)


    with col1:                                                                      # First Row of KPIs with dynamic values and formatting
        st.metric(label=" 📅 Editions", value=f"{editions:,}")

    with col2:
        st.metric(label="🏙️ Cities", value=f"{cities:,}")

    with col3:
        st.metric(label="🎽 Sports", value=f"{sports:,}")

    with col4:                                                                      # Second Row of KPIs with dynamic values and formatting
        st.metric(label="🏆 Events", value=f"{events:,}")

    with col5:
        st.metric(label="🏋️‍♂️ Athletes", value=f"{athletes:,}")

    with col6:
        st.metric(label="🌍 Nations", value=f"{nations:,}")


    # Plotting Nations Participation in the Olympics Over time

    nations_over_time = helper.participating_nations_over_time(df)


    fig1 = px.line(
                    data_frame=nations_over_time, 
                    x='Editions', 
                    y='Count of Participating Countries', 
                    markers=True,                                                               
                    line_shape='spline',                                                        
                    color_discrete_sequence=['#636EFA']                                         
                    )
    
    helper.customize_plotly_chart(fig1,'Olympic Editions','Number of Participating Countries','Year-on-Year Trend for Participating Nations in Summer Olympics',width= 700,height=400)

    st.plotly_chart(fig1)


    # Plotting Events Trend in the Olympics Over time

    events_over_time = helper.events_over_time(df)

    fig2 = px.line(
                    data_frame= events_over_time,
                    x='Year',
                    y='Event',
                    markers= True,
                    line_shape='spline',
                    color_discrete_sequence=['#636EFA']  
                    )
    helper.customize_plotly_chart(fig2, 'Olympic Editions' , 'Number of Events','Year-on-Year Trend for Events in Summer Olympics')
    
    st.plotly_chart(fig2)

    # Plotting Participation of Athletes in the Olympics Over time

    athelets_over_time = helper.athelets_over_time(df)

    fig3 = px.line(
                    data_frame=athelets_over_time,
                    x='Year',
                    y='Name',
                    markers=True,
                    line_shape='spline',
                    color_discrete_sequence=['#636EFA'] 
        )
    helper.customize_plotly_chart(fig3, 'Olympic Editions','Number of Atheletes','Year on Year Trend for Athletes Participation in Olympic')

    
    st.plotly_chart(fig3)

    # Events Over time for every Sports in the Olympic

    st.title("Events over time (Every Sport)")
    event_over_time_every_sports = helper.event_over_time_every_sports(df) 

    # Ploting Events Over time for every Sports

    fig4, ax = plt.subplots(figsize=(30, 30))
    ax = sns.heatmap(event_over_time_every_sports, annot=True, cmap='crest', linewidths=.5)
    helper.customize_heatmap(ax)
    st.pyplot(fig4)

    # Most successful Athletes over time

    st.title('Most Successful Athletes')

    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sports_list)
    most_succeessful_athletes = helper.most_successful_athletes(df,selected_sport)
    st.table(most_succeessful_athletes)

# Country-Wise Analysis

elif user_menu == '🌍 Country-Wise Analysis':

    st.sidebar.title('Country-Wise Analysis')
    countries = df['region'].unique().tolist()
    countries.sort()
    default_index = countries.index('Usa') if 'Usa' in countries else 0

    # Use the index to set 'USA' as the default value

    selected_country = st.sidebar.selectbox('Select a Country', countries, index=default_index)

    # Plotting countrywise medal tally

    st.title("{} Medal Trend over the years".format(selected_country))

    filtered_df  = helper.Countrywise_Medal_Tally(df,selected_country)
    fig5 = px.line(
                    data_frame=filtered_df,
                    x= 'Year',
                    y='Medal',
                    markers= True,
                    line_shape ='spline',
                    color_discrete_sequence=['#636EFA'] 
                    )
    
    helper.customize_plotly_chart(fig5,'Olympic Editions','Medal', "Medal Trend over the years")
    st.plotly_chart(fig5)

    # Country excel in selected sports

    st.title("{} Excels in Below Sports".format(selected_country))

    # Plotting the heatmap

    pivot_df  = helper.Countrywise_Sport_Perf(df,selected_country)
    fig6, ax = plt.subplots(figsize=(30, 30))
    ax = sns.heatmap(pivot_df, annot=True, cmap='crest', linewidths=.5)
    helper.customize_heatmap(ax)
    st.pyplot(fig6)

    # Top 20 Successful Athletes for selected country

    st.title("Top 20 Successfull  Athletes for {} in the Olympic".format(selected_country))
    temp_df = helper.most_succeessful_athletes_countrywise(df,selected_country)
    st.table(temp_df)

# Athlete Wise Analysis

else:

    st.title("Athlete-Wise Analysis")
    df_cleaned = df.drop_duplicates(subset=['Name', 'Event', 'Year'])
    df_cleaned = df_cleaned.dropna(subset=['Age', 'Medal'])
    medal_winners_df = df_cleaned[df_cleaned['Medal'].notna()]
    overall_age = medal_winners_df['Age']
    gold_medal_age = medal_winners_df[medal_winners_df['Medal'] =='Gold']['Age']
    silver_medal_age = medal_winners_df[medal_winners_df['Medal'] =='Silver']['Age']
    bronze_medal_age = medal_winners_df[medal_winners_df['Medal'] =='Bronze']['Age']

    # Create the distribution plot using Plotly's figure factory - pdf of different medal aged group athletes

    fig7 = ff.create_distplot(
                                [overall_age,gold_medal_age,silver_medal_age,bronze_medal_age],       
                                ['overall_age','gold_medal_age','silver_medal_age','bronze_medal_age'],   
                                show_hist=False,                                                        
                                curve_type='kde',                                                       
                                   
                             )

    helper.customize_plotly_chart(fig7,'Age','Density','PDF of Age for Medal-Winning Athletes')
    st.plotly_chart(fig7)

    # PDF of Age for Gold Medal-Winning Athletes

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    
    for sport in famous_sports:
        temp_df = df.drop_duplicates(['Name','Age','Sport'])
        temp_df = temp_df[temp_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig8 = ff.create_distplot(  x,
                                name,
                                show_hist=False,  
                                show_rug=False,
                                curve_type='kde'  
                                )
    helper.customize_plotly_chart(
                                fig8,
                                'Age' ,
                                'Density','PDF of Age for Gold Medal-Winning Athletes'
                                )
    st.plotly_chart(fig8)

    # Height vs Weight analysis with respect to different sports

    

    
    st.title("Height vs Weight Analysis w.r.t. Different Sports")

    # Dropdown to select sport
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sports_list)

    
    temp_df = helper.weight_vs_height(df, selected_sport)

   

    color_map = {
    'Gold': 'gold',
    'Silver': 'silver',
    'Bronze': '#cd7f32',  
    'No Medal': 'gray'    
}

   
    fig8 = px.scatter(
        data_frame=temp_df,
        x='Weight',
        y='Height',
        color='Medal',
        symbol='Sex',
        size_max=200,
        color_discrete_map= color_map,
        labels={'Weight': 'Weight (kg)', 'Height': 'Height (cm)'}
    )

    helper.customize_plotly_chart(fig8, 'Weight','Height',f'Height vs Weight Analysis - {selected_sport}')
    st.plotly_chart(fig8)


    # Male vs Female Participation

    st.title("Male vs Female Participation in the Olympics Over the Years")

    malevsfemale = helper.MalevsFemale(df)

    fig9 = px.line(
                data_frame = malevsfemale,
                x ='Year',
                y = ['Male','Female'],
                 markers= True,
                line_shape='spline',
                color_discrete_sequence=['#636EFA','#EF553B']
              )
    helper.customize_plotly_chart(fig9, 'Year','Male vs Female','Participation of Male VS Female in Olympic')    
    st.plotly_chart(fig9)

