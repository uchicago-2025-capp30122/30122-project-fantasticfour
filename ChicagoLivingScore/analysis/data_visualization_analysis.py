from pathlib import Path
import pandas as pd
import altair as alt

# provides us with a heatmap of all the zipcodes and their indicators
def create_heatmap(df):
    heatmap = alt.Chart(df).mark_rect().encode(
        x=alt.X('zipcode:N', title='Zip Code'),
        y=alt.Y('final_score:N', title='Indicator'),
        color=alt.Color('final_score:Q', scale=alt.Scale(scheme='viridis')),  # Color based on score
        tooltip=['zipcode', 'avg_income_score', 'crime_score', 'avg_price_per_sqft','final_score']
    ).transform_fold(
        ['crime_score', 'education_score', 'avg_income_score', 'final_score']
    ).properties(
        title='Comparison of Key Indicators by Zip Code',
        width=600,
        height=400
    )

    return heatmap

def combine_charts(chart_1, chart_2):
    combined_chart = alt.hconcat(chart_1,chart_2).resolve_scale(y='independent')

    return combined_chart

def creat_bar_chats(df):
    
    #top 5 best zipcodes
    top_five = df.nlargest(5, "final_score")
    best_places = top_five[['zipcode', 'final_score']]
    
    #worst 5 zopcodes
    
    top_five_worst = df.nsmallest(5, "final_score")
    worst_places = top_five_worst[['zipcode', 'final_score']]
    
    
    chart_best = alt.Chart(best_places).mark_bar().encode(
        x=alt.X('zipcode:N', sort='-y', title='Zipcode'),
        y=alt.Y('final_score:Q', title='best overall'),
        tooltip=['zipcode', 'final_score']
    ).properties(
        title='Top 5 Zipcodes',
        width=400,
        height=300
    )
    
    chart_worst = alt.Chart(worst_places).mark_bar(color="salmon").encode(
        x=alt.X('zipcode:N', sort='-y', title='Zipcode'),
        y=alt.Y('final_score:Q', title='worst overall'),
        tooltip=['zipcode', 'final_score']
    ).properties(
        title='Worst 5 Zipcodes',
        width=400,
        height=300
    )    

    combined = combine_charts(chart_best,chart_worst)
    return combined


def create_heatmap_html(df):
    chart = create_heatmap(df)
    return chart.to_html()

def create_bar_html(df):
    chart = creat_bar_chats(df)
    return chart.to_html()

file_path = Path(__file__).parent.parent / "data" / "cleaned_data" / "final_living_score.csv"
df = pd.read_csv(file_path)
heatmap = create_heatmap(df)
bar_charts = creat_bar_chats(df)