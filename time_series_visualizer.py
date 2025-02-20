import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Clean data
lower_percentile = df['value'].quantile(0.025)
upper_percentile = df['value'].quantile(0.975)

df = df[(df['value'] >= lower_percentile) & (df['value'] <= upper_percentile)]

print(f"Data count after cleaning: {df.shape[0]}")

def draw_line_plot():
    # Draw line plot
    # Create a copy of the cleaned data frame
    df_line = df.copy()

    print("Data sample before plotting:")
    print(df_line.head())
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the data: x-axis is 'date', y-axis is 'value' (page views)
    ax.plot(df_line.index, df_line['value'], color='blue')
    
    # Set the title and labels
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Create a new column 'month' to extract the month from the 'date' column
    df_bar['month'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year

    # Aggregate data by year and month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    df_bar.columns = df_bar.columns.map({
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    })

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a bar plot where each bar represents the average page views per month per year
    df_bar.plot(kind='bar', ax=ax)

    # Set the title and labels
    ax.set_title("Average Page Views Per Month (5/2016-12/2019)")
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)


    # Ensure the 'value' column is of type float
    df_box['value'] = df_box['value'].astype(float)

    # Create a figure with two subplots (one for year and one for month)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Create a box plot for page views grouped by year on ax1
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    # Create a box plot for page views grouped by month on ax2
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
