
def country_year_list(df):

    # List of all Unique Years
    years = df['Year'].unique().tolist()
    years.sort()
    # Adding Overall at the top of years list
    years.insert(0,'Overall')

    countries = df['region'].unique().tolist()
    countries.sort()
    countries.insert(0,'Overall')

    return years, countries

def fetch_medal_tally(df, year, country):
    # First, drop duplicates where multiple athletes have the same medal in the same event

    df_unique_medals = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    flag = 0

    # If both year and country are 'Overall', show all data
    if year == 'Overall' and country == 'Overall':
        temp_df = df_unique_medals
        

    # If year is 'Overall' but a specific country is selected, filter by country
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = df_unique_medals[df_unique_medals['region'] == country]

    # If a specific year is selected but country is 'Overall', filter by year
    elif year != 'Overall' and country == 'Overall':
        temp_df = df_unique_medals[df_unique_medals['Year'] == year]

    # If both specific year and country are selected, filter by both year and country
    else:
        temp_df = df_unique_medals[(df_unique_medals['Year'] == year) & (df_unique_medals['region'] == country)]

    
    if flag == 1:
        # Group by year and sum up the medal counts
        temp_df = temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()

    else:
            
        # Group by region and sum up the medal counts
        temp_df = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    # Calculate the total medals
    temp_df['Total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    temp_df.index = temp_df.index + 1
    return temp_df


def customize_plotly_chart(fig, xaxis_title, yaxis_title,title= None,width= None,height=None):
    fig.update_layout(
                        title_font_size=24,
                        xaxis_title=xaxis_title,
                        yaxis_title=yaxis_title,
                        title = title,
                        width = width,
                        height= height,
                        font=dict(size=20),
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(showgrid=False, tickfont=dict(size=18, color='RebeccaPurple', family='Arial')),
                        yaxis=dict(showgrid=True, gridcolor='lightgrey', tickfont=dict(size=18, color='RebeccaPurple', family='Arial')),
                        hovermode="x"
                    )

def participating_nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year','region']).groupby('Year').count()['region'].reset_index().sort_values('Year').rename(columns={'Year':'Editions','region':'Count of Participating Countries'})
    
    return nations_over_time


def events_over_time(df):
     events_over_time = df.drop_duplicates(['Year','Event']).groupby('Year').count()['Event'].reset_index()

     return events_over_time

def athelets_over_time(df):
    athletes_over_time = df.drop_duplicates(['Name','Year']).groupby('Year').count()['Name'].reset_index()

    return athletes_over_time

def event_over_time_every_sports(df):
    filtered_df = df.drop_duplicates(['Event', 'Year', 'Sport'])
    pivot_df = filtered_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')

    return pivot_df

def customize_heatmap(ax):

    # Increase the font size of the x and y axis labels
    ax.set_xlabel("Year", fontsize=25)
    ax.set_ylabel("Sport", fontsize=20)

    ax.tick_params(axis='x', labelsize=20, labelcolor='RebeccaPurple', labelrotation=45, width=2, colors='lightgrey',)  # Customize x ticks
    ax.tick_params(axis='y', labelsize=20, labelcolor='RebeccaPurple', width=2, colors='lightgrey')  # Customize y ticks


def most_successful_athletes(df, sport):
    temp_df = df.dropna(subset=['Medal'])  # Remove rows with missing 'Medal'

    # If the selected sport is 'Overall', find the top 20 athletes overall
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport']== sport]

    # Drop duplicates and reset the index starting from 1
    temp_df =  temp_df['Name'].value_counts().reset_index().head(20).merge(df, left_on='index', right_on='Name', how='left').rename(columns={'index': 'Athletes Name', 'Name_x': 'No. of Medal'})[['Athletes Name', 'No. of Medal', 'Sport', 'region']]
    temp_df = temp_df.drop_duplicates('Athletes Name').reset_index(drop=True)
    temp_df.index = temp_df.index + 1  # Set the index to start from 1

    return temp_df

def Countrywise_Medal_Tally(df, country):
    temp_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    temp_df.dropna(subset=['Medal'],inplace= True)
    filtered_df = temp_df[temp_df['region'] == country].groupby('Year').count()['Medal'].reset_index().sort_values('Year')

    return filtered_df


def Countrywise_Sport_Perf(df,country):
    temp_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    temp_df.dropna(subset=['Medal'],inplace= True)
    filtered_df = temp_df[temp_df['region'] == country]

    # Create a Pivot Table

    pivot_df = filtered_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    return pivot_df

def most_succeessful_athletes_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])  # Remove rows with missing 'Medal'


    # Drop duplicates and reset the index starting from 1
    temp_df =  temp_df[temp_df['region'] == country]['Name'].value_counts().reset_index().head(20).merge(df, left_on='index', right_on='Name', how='left').rename(columns={'index': 'Athletes Name', 'Name_x': 'No. of Medal'})[['Athletes Name', 'No. of Medal', 'Sport']]
    temp_df = temp_df.drop_duplicates('Athletes Name').reset_index(drop=True)
    temp_df.index = temp_df.index + 1  # Set the index to start from 1

    return temp_df

def weight_vs_height(df,sport):
    df_cleaned = df.drop_duplicates(subset=['Name', 'Event', 'Year'])
    df_cleaned['Medal'].fillna('No Medal', inplace= True)
    
    if sport !='Overall':
        temp_df = df_cleaned[df_cleaned['Sport']==sport]
        return temp_df
    else:
        return df_cleaned
    
def MalevsFemale(df):
    df_cleaned = df.drop_duplicates(subset=['Name', 'Event', 'Year'])
    men = df_cleaned[df_cleaned['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = df_cleaned[df_cleaned['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women,on='Year',how='left').fillna(0).astype('int')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'}, inplace= True)

    return final
  
