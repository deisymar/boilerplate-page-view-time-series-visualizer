import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates =['date'], index_col="date")
#print(df.head())

# Clean data
#df = df.drop(df[(df['value']<df['value'].quantile(0.025)) | (df['value']>df['value'].quantile(0.975))].index)
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]
#print(df)


def draw_line_plot():
    # Draw line plot
     
    fig = df.plot.line(figsize=(15,8), color='red', linewidth=0.9, legend=False);
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.xticks(rotation = 0)
    plt.ylabel('Page Views')    
    #plt.show()
    fig = fig.figure
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy(deep=True)
    #print(df_bar.index)
    df_bar['year'] = df.index.year
    df_bar['month'] = df.index.month_name()  
    #print(df_bar['month'])
    
    df_bar_group = df_bar.groupby(['year', 'month'])['value'].mean() 
    #having a new level of column labels whose inner-most level consists of the pivoted index labels
    #level=-1 month is columns    
    df_bar_group = df_bar_group.unstack(level='month')
    #print(df_bar_group)      

    # Draw bar plot    
    fig = df_bar_group.plot.bar(legend = True, figsize = (10,7)).figure
    
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    month_names=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    plt.legend(title= 'Months', labels= month_names, fontsize=8)
    plt.xticks(fontsize= 10)
    plt.yticks(fontsize= 10)
    
    #plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    #print(df_box)
    df_box.reset_index(inplace=True)   
    df_box['year'] = [d.year  for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date] 
    #print(df_box['year'])
    
    # Draw box plots (using Seaborn)    
    #fig, axes = plt.subplots(nrows =1,ncols=2,figsize=(10,5))
    fig, (ax1, ax2) = plt.subplots(1,2)
    fig.set_figheight(10)
    fig.set_figwidth(30)
    
    sns.boxplot(ax = ax1, x = "year", y = "value", data = df_box)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    
    month_name=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(ax = ax2, x = "month", y = "value", order = month_name, data = df_box)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')  
    
    #plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
