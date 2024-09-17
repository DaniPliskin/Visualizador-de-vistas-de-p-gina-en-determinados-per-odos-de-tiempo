import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col=["date"])

# Clean data
lower_value = df["value"].quantile(0.025)
top_value = df["value"].quantile(0.975)
df = df[(df["value"] >= lower_value) & (df["value"] <= top_value)]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(df.index, df["value"], color="red", linewidth=1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df.index.year
    df_bar["month"] = df.index.month

    df_bar = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 8))
    df_bar.plot(kind= "bar", ax=ax, stacked=False)

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    plt.legend(title="Months", loc="upper left", labels=[
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ])

    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box["value"] = df_box["value"].astype("float64")

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    colors_month = sns.color_palette("Set3", 12)
    colors = sns.color_palette("Set3", 4)

    flierprops = dict(marker="o", markersize=3, linestyle="none", markerfacecolor="r")

    fig, ax = plt.subplots(1, 2, figsize=(20, 6))

    sns.boxplot(x="year", y="value", data=df_box, ax=ax[0], hue="year", palette=colors, flierprops=flierprops, legend=False)
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")

    sns.boxplot(x="month", y="value", data=df_box, ax=ax[1],  hue="month", palette=colors_month, flierprops=flierprops, order=month_order)
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

