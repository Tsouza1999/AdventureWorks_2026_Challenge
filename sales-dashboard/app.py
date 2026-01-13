import streamlit as st
import pandas as pd
import plotly.express as px
from db import load_sales_data

st.set_page_config(
    page_title="Dashboard de Vendas - AdventureWorks",
    layout="wide"
)

st.title("📊 Dashboard de Vendas - AdventureWorks")
st.caption("Análise interativa de vendas por período, produto e região")

@st.cache_data
def load_data():
    df = load_sales_data("../queries/sales_query.sql")
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    return df

df = load_data()

st.sidebar.header("Filtros")

min_date = df["OrderDate"].min().date()
max_date = df["OrderDate"].max().date()

start_date, end_date = st.sidebar.date_input(
    "Período",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

products = sorted(df["ProductName"].unique())
selected_products = st.sidebar.multiselect(
    "Produtos",
    options=products,
    default=products
)

regions = sorted(df["StateProvince"].unique())
selected_regions = st.sidebar.multiselect(
    "Regiões",
    options=regions,
    default=regions
)

filtered_df = df[
    (df["OrderDate"].dt.date >= start_date) &
    (df["OrderDate"].dt.date <= end_date) &
    (df["ProductName"].isin(selected_products)) &
    (df["StateProvince"].isin(selected_regions))
]

total_sales = filtered_df["LineTotal"].sum()
total_orders = filtered_df["SalesOrderID"].nunique()
avg_ticket = total_sales / total_orders if total_orders > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total de Vendas", f"R$ {total_sales:,.2f}")
col2.metric("📦 Total de Pedidos", f"{total_orders}")
col3.metric("🎯 Ticket Médio", f"R$ {avg_ticket:,.2f}")

st.divider()

sales_by_product = (
    filtered_df
    .groupby("ProductName")["LineTotal"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_bar = px.bar(
    sales_by_product,
    x="ProductName",
    y="LineTotal",
    title="Top 10 Produtos por Vendas",
    labels={
        "LineTotal": "Total de Vendas",
        "ProductName": "Produto"
    }
)

st.plotly_chart(fig_bar, use_container_width=True)

sales_over_time = (
    filtered_df
    .groupby(pd.Grouper(key="OrderDate", freq="M"))["LineTotal"]
    .sum()
    .reset_index()
)

fig_line = px.line(
    sales_over_time,
    x="OrderDate",
    y="LineTotal",
    title="Vendas ao Longo do Tempo",
    markers=True,
    labels={
        "LineTotal": "Total de Vendas",
        "OrderDate": "Data"
    }
)

st.plotly_chart(fig_line, use_container_width=True)
