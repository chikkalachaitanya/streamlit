import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="superstore",page_icon="📊",layout="wide")

st.title("📊 : Sample Superstore EDA")

# os.chdir(r"C:\work\streamlit")
df = pd.read_excel("Sample-Superstore.xlsx")

col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# getting the min and max date
startdate = pd.to_datetime(df["Order Date"]).min()
enddate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("start Date", startdate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", enddate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")
# create for region
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if region:
    df2 = df[df["Region"].isin(region)]
else:
    df2 = df.copy()

# create for state
state = st.sidebar.multiselect("Select your state", df2["State"].unique())
if state:
    df3 = df2[df2["State"].isin(state)]
else:
    df3 = df2.copy()

# create for city
city = st.sidebar.multiselect("Select your city", df3["City"].unique())
if city:
    df4 = df3[df3["City"].isin(city)]
else:
    df4 = df3.copy()

category_df = df4.groupby(by=["Category"], as_index = False)["Sales"].sum()

with col1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x="Category", y="Sales",text=['${:,.2f}'.format(x) for x in category_df["Sales"]])
    st.plotly_chart(fig, width="stretch", height=350)

with col2:
    st.subheader("Region wise Sales")
    fig = px.pie(df4, values="Sales", names="Region", hole=0.5)
    fig.update_traces(text=df4["Region"], textposition="outside")
    st.plotly_chart(fig, width="stretch", height=350)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Category View data"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download data", data=csv, file_name="Category.csv", mime="text/csv",
                           help='Click here to download the data as a csv file')

with cl2:
    with st.expander("Region View data"):
        region = df4.groupby(by="Region",as_index=False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button("Download data", data=csv, file_name="Region.csv", mime="text/csv",
                           help='Click here to download the data as a csv file')

df4["month-year"] = df4["Order Date"].dt.to_period("M")
st.subheader("Time series Analysis")

linechart = pd.DataFrame(df4.groupby(df4["month-year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x="month-year", y="Sales", labels={"Sales" : "Amount"}, height=400, template="gridon")
st.plotly_chart(fig2, width="stretch")

with st.expander("View data of time series"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf=8")
    st.download_button('Download data', data=csv, file_name="Timeseries.csv", mime='text/csv')

# create a tree map based on Region, category, subcategory
st.subheader("Hierarichal view of sales using treemap")
fig3 = px.treemap(df4, path=["Region","Category","Sub-Category"], values="Sales", hover_data=["Sales"],
                  color="Sub-Category")
fig3.update_layout(height=650)
st.plotly_chart(fig3,width="stretch")

chart1,chart2 = st.columns((2))
with chart1:
    st.subheader("Segment wise Sales")
    fig = px.pie(df4, values="Sales", names="Segment", template="plotly_dark")
    fig.update_traces(text=df4["Segment"], textposition="inside")
    st.plotly_chart(fig, width="stretch")

with chart2:
    st.subheader("category wise Sales")
    fig = px.pie(df4, values="Sales", names="Category", template="gridon")
    fig.update_traces(text=df4["Category"], textposition="inside")
    st.plotly_chart(fig, width="stretch")

import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Subcategory Sales Summary")
with st.expander("Summary table"):
    df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig = ff.create_table(df_sample,colorscale="cividis")
    st.plotly_chart(fig, width="stretch")

    st.markdown("Month wise Sub-Category table")
    df4["month"] = df4["Order Date"].dt.month_name()
    sub_category_year = pd.pivot_table(data=df4, values="Sales", index=["Sub-Category"], columns="month")
    st.write(sub_category_year.style.background_gradient(cmap="Blues"))

# create scatter plot
data1 = px.scatter(df4, x="Sales", y="Profit", size="Quantity")
data1.update_layout(title="Relationship between Sales and Profit using scatterplot",
                    title_font = dict(size=20), 
                    xaxis =dict(title="Sales",title_font=dict(size=19)),
                    yaxis = dict(title="Profit",title_font=dict(size=19)))
st.plotly_chart(data1, width = "stretch")

with st.expander("View data"):
    st.write(df4.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# download original dataset
csv = df.to_csv(index=False).encode('utf-8')

st.download_button('Download data', data=csv, file_name='Data.csv', mime='text/csv')

