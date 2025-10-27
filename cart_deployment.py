
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt
df = pd.read_csv('cleaned_ds.csv',index_col=0)
st.set_page_config(layout='wide',page_title='Shopping Cart EDA')
st.markdown("<h1 style='text-align: center; color: white;'>Shopping Cart Exploratory Data Analysis</h1>", unsafe_allow_html=True)
st.image('1_IviHioB4RphuX6WEw_hONg.jpg', use_container_width =True)
page  = st.sidebar.radio('Pages',['Homepage','KPI\'s Dashboard','Marketing Report'])

if page == 'Homepage':
    st.subheader('Data Overview')
    st.dataframe(df.head())

    st.subheader('Data Column Description')
    st.markdown("""
| **Column Name**        | **Description** |
|--------------------------|-----------------|
| `Unnamed: 0`            | Index column automatically generated during data saving; not meaningful for analysis. |
| `order_id`              | Unique identifier for each order placed by a customer. |
| `order_date`            | Date on which the customer placed the order. |
| `delivery_date`         | Date on which the order was delivered to the customer. |
| `customer_name`         | Name of the customer who placed the order. |
| `gender`                | Gender identity of the customer. |
| `age`                   | Age of the customer in years. |
| `city`                  | City where the customer resides. |
| `state`                 | State or region where the customer resides. |
| `price_per_unit`        | Price of one unit of the purchased product. |
| `quantity`              | Number of product units purchased in the order. |
| `total_price`           | Total cost of the purchase (`price_per_unit × quantity`). |
| `product_type`          | Category or type of product purchased (e.g., Shirt, Jacket, Trousers). |
| `product_name`          | Specific name or style of the product. |
| `size`                  | Size of the product (e.g., S, M, L, XL). |
| `colour`                | Color of the product. |
| `stock`                 | Available quantity of the product in inventory. |
| `delivery_duration`     | Number of days between order and delivery (`delivery_date - order_date`). |
""")

    st.file_uploader('Upload file')

elif page == 'KPI\'s Dashboard':
    # Basic KPIs
    total_orders = df['order_id'].nunique()
    total_revenue = df['total_price'].sum()
    total_customers = df['customer_name'].nunique()

    avg_order_value = total_revenue / total_orders
    avg_customer_spend = total_revenue / total_customers
    avg_items_per_order = df.groupby('order_id')['product_name'].count().mean()
    col1, col2, col3 = st.columns(3)
    col1.metric("🛒 Total Orders", f"{total_orders:,}")
    col2.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    col3.metric("👥 Total Customers", f"{total_customers:,}")

    col4, col5, col6 = st.columns(3)
    col4.metric("📦 Avg Items per Order", f"{avg_items_per_order:.2f}")
    col5.metric("🏷️ Avg Order Value", f"${avg_order_value:,.2f}")
    col6.metric("💳 Avg Customer Spend", f"${avg_customer_spend:,.2f}")

    st.write("---")

    st.subheader("📈 Revenue Over Time")
    df_sorted = df.sort_values(by= 'order_date')
    revenue_trend = df_sorted.groupby('order_date')['total_price'].sum().reset_index()
    st.plotly_chart(px.line(data_frame= revenue_trend, x= 'order_date', y= 'total_price',
    labels = {'order_date' : 'Order Date', 'total_price' : 'Revenue'}))

    # Top states by revenue
    st.subheader("🏙️ Top States by Revenue")
    state_rev = df.groupby('state')['total_price'].sum().sort_values(ascending=False).head(10).reset_index()
    st.plotly_chart(px.bar(state_rev, x='state', y='total_price', title='Top 10 States by Revenue', text_auto= True))

    # Top products by revenue
    st.subheader("🔥 Top Products by Revenue")
    product_rev = df.groupby('product_name')['total_price'].sum().sort_values(ascending=False).head(10).reset_index()
    st.plotly_chart(px.bar(product_rev, x='product_name', y='total_price', title='Top 10 Products by Revenue',text_auto= True))

elif page == 'Marketing Report':

    start_date = st.sidebar.date_input('Start Date', min_value = df.order_date.min(), max_value = df.order_date.max(), value = df.order_date.min())

    end_date = st.sidebar.date_input('End Date', min_value = df.order_date.min(), max_value = df.order_date.max(), value = df.order_date.max())

    df_filtered = df[(df.order_date >= str(start_date)) & (df.order_date <= str(end_date))]

    # What are the top products in each state ?

    All_states = df_filtered.state.unique().tolist() + ['All States']

    State = st.sidebar.selectbox('State', All_states)

    if State != 'All States':

        df_filtered = df_filtered[df_filtered.state == State]

    st.dataframe(df_filtered)

    st.subheader("🔥 Top Products by State")
    
    top_n = st.sidebar.slider('Top N', min_value = 1, max_value = 30, value = 5)
    products_count = df_filtered.product_name.value_counts().reset_index().head(top_n)
    st.plotly_chart(px.bar(data_frame= products_count, x= 'product_name', y= 'count'))
