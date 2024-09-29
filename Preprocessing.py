import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st  


def load_data():
    """Load athlete and region data from CSV files."""
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')
    #print("Shape of the Athletes Events Dataframe:", df.shape)
    #print("Shape of the Noc Region Dataframe:", region_df.shape)
    return df, region_df

def filter_summer_olympics(df):
    """Filter the data for summer olympics only."""
    df_filtered = df[df['Season'] == 'Summer']
    return df_filtered

def merge_data(df_filtered, region_df):
    """Merge athlete data with region data."""
    df_merged = pd.merge(df_filtered, region_df, on='NOC', how='left')
    return df_merged

def is_null(df_merged):
    """Check percentage of missing value for each column."""
    return round((df_merged.isnull().sum() / df_merged.shape[0]) * 100, 2).reset_index()

def clean_data(df_merged):
    """Clean data by handling missing regions and mapping countries."""
    df_merged.drop_duplicates(inplace=True)
    df_merged['region'] = df_merged['region'].str.strip().str.title()
    
    country_mapping = {
        'Germany Dr': 'Germany',
        'West Germany': 'Germany',
        'Soviet Union': 'Russia',
        'Slovakia': 'Czech Republic',
        'Boliva': 'Bolivia'
    }
    df_merged['region'] = df_merged['region'].replace(country_mapping)
    
    noc_to_region_mapping = {
        'SGP': 'Singapore',
        'ROT': 'Refugee Olympic Team',
        'TUV': 'Tuvalu',
        'UNK': 'Unknown'
    }
    df_merged['region'] = df_merged['region'].fillna(df_merged['NOC'].map(noc_to_region_mapping))
    return df_merged

def one_hot_encode_medals(df):
    """Perform one-hot encoding for the 'Medal' column."""
    return pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

def plot_distributions(df):
    """Plot the distributions of numerical columns and calculate skewness."""
    columns_to_check = ['Age', 'Height', 'Weight']
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for i, col in enumerate(columns_to_check):
        sns.histplot(df[col], kde=True, ax=axes[i])
        axes[i].set_title(f'Distribution of {col} (Skewness: {df[col].skew():.2f})')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Frequency')
    
    fig.tight_layout()
    fig.show()

def handle_missing_values(df_merged):
    """Impute missing values for age, height, and weight."""
    df_merged['Age'].fillna(df_merged['Age'].median(), inplace=True)
    df_merged['Height'].fillna(df_merged['Height'].mean(), inplace=True)
    df_merged['Weight'].fillna(df_merged['Weight'].median(), inplace=True)
    return df_merged

def preprocess():
    """Main function to run the entire preprocessing pipeline."""
    df, region_df = load_data()
    df_filtered = filter_summer_olympics(df)
    df_merged = merge_data(df_filtered, region_df)
    df_cleaned = clean_data(df_merged)
    df_imputed = handle_missing_values(df_cleaned)
    plot_distributions(df_imputed)
    df = one_hot_encode_medals(df_imputed)  

    return df

if __name__ == "__main__":
    processed_df = preprocess()
    
    
