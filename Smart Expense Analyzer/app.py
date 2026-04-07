import  streamlit as st
import pandas as pd
import plotly.express as px
from dask.array import append
from rich.jupyter import display
from streamlit import dataframe, bar_chart

from config import CATEGORIES, TAG_MAP, CHART_LAYOUT



st.set_page_config(
    page_title= 'Smart Expense Analyzer',
    page_icon= '💰',
    layout= 'wide'
)


with open('style.css') as css_file:
    st.markdown(f'<style>{css_file.read()}</style>',
                unsafe_allow_html= True)



# Through Prompt

st.markdown("""
<h1 style="font-family:'Syne',sans-serif;font-size:2.3rem;font-weight:800;letter-spacing:-1px;margin-bottom:4px;">
<span style="font-size:2rem;">💰</span>
<span style="color:#b45309;"> Smart Expense Analyzer</span>
</h1>
<p style="color:rgba(28,18,9,.45);font-size:.85rem;margin-top:0;margin-bottom:1rem;">
    Real-time expense & financial analytics
</p>
""", unsafe_allow_html=True)


def find_column(all_columns, keywords):

    for column_name in all_columns:
        for keyword in keywords:
            if keyword in column_name.lower():
                return column_name

    return None



def clean_amount(raw_value):

    cleaned = str(raw_value)
    cleaned = cleaned.replace(',','')
    cleaned = cleaned.replace('₹','')
    cleaned = cleaned.strip()
    return pd.to_numeric(cleaned, errors= 'coerce')


def extract_merchant_name(description):
    description_lower = str(description).lower()

    if description_lower.startswith('paid to'):
        name = description[7:]

    elif description_lower.startswith('money sent to'):
        name = description[13:]

    else:
        name = description


    name = str(name).split('@')[0]
    return name.strip().title()


def get_category(description, tag=''):

    cleaned_tag = str(tag).strip().lstrip('#').lower()
    if cleaned_tag in TAG_MAP:
        return TAG_MAP[cleaned_tag]

    description_lower = str(description).lower()

    for category_name, keyword_list in CATEGORIES.items():
        for keyword in keyword_list:
            if keyword in description_lower:
                if category_name == 'Transfer' and not description_lower.startswith('paid to'):
                    continue
                return category_name


    if description_lower.startswith('paid to'):
        return 'Transfer'


    return 'Other'


def load_bank_statement(uploaded_file):

    try:

        file_name = uploaded_file.name
        if file_name.endswith('.xlsx') or file_name.endswith('xls'):
            df= pd.read_excel(uploaded_file)

        else:
            df = pd.read_csv(uploaded_file)


        df.columns = df.columns.str.strip()
        all_columns_lower = [col.lower() for col in df.columns]


        if 'transaction details' in all_columns_lower:
            df = df.rename(columns={'Transaction Details' : 'Description'})
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        elif 'withdrawal amt.' in all_columns_lower:
            narration_col = find_column(df.columns, ['narration'])
            date_col = find_column(df.columns,['date'])


            df = df.rename(columns={
                narration_col: 'Description',
                date_col:      'Date'
            })

            credit_col = find_column(df.columns, ['deposit','credit'])
            debit_col = find_column(df.columns, ['withdrawal'])

            credit_amount = df[credit_col].apply(clean_amount).fillna(0)
            debit_amount = df[debit_col].apply(clean_amount).fillna(0)

            df['Amount'] = credit_amount - debit_amount


        elif 'debit' in all_columns_lower:
            desc_col = find_column(df.columns, ['desc','narr','remark','particular'])
            date_col = find_column(df.columns, ['date'])
            credit_col = find_column(df.columns, ['credit'])
            debit_col = find_column(df.columns, ['debit'])

            df = df.rename(columns={

                desc_col: 'Description',
                date_col: 'Date'
            })

            credit_amount = df[credit_col].apply(clean_amount).fillna(0)
            debit_amount = df[debit_col].apply(clean_amount).fillna(0)
            df['Amount'] = credit_amount - debit_amount


        else:
            desc_col = find_column(df.columns,['desc','narr','particular','remark'])
            date_col = find_column(df.columns, ['date'])
            amount_col = find_column(df.columns, ['amount'])

            rename_map = {}
            if date_col : rename_map[date_col] = 'Date'
            if desc_col : rename_map[desc_col] = 'Description'
            if amount_col : rename_map[amount_col] = 'Amount'

            df = df.rename(columns=rename_map)

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        if 'Amount' in df.columns:
            df['Amount'] = df['Amount'].apply(clean_amount)

        df = df.dropna(subset=['Amount', 'Date'])
        df = df.sort_values('Date')


        df['Amount']  = df['Amount'].round().astype(int)
        df['Abs_Amount']  = df['Amount'].abs()

        df['Kind'] = df['Amount'].apply(
            lambda amount: 'Income' if amount > 0 else 'Expense'
        )


        df['Category'] = df.apply(
            lambda row: 'Income' if row['Kind'] == 'Income'
            else get_category(row['Description'], row.get('Tags','')),
            axis = 1
        )

        df['Month'] = df['Date'].dt.strftime('%b %y')
        df['Merchant'] = df['Description'].apply(extract_merchant_name)
        df = df.reset_index(drop=True)

        return df, None

    except Exception as error:
        return None, str(error)


with st.sidebar:
    uploaded_file = st.file_uploader(
        label = 'Upload Statement (CSV/XLSX)',
        type = ['xlsx','csv']
    )


    monthly_budget = st.number_input(
        label = 'Monthly Budget(₹)',
        min_value = 1000,
        value = 50000
    )

if not uploaded_file:
    st.info(' 👈 Please upload your bank statement to get started')
    st.stop()


df, error_message  = load_bank_statement(uploaded_file)

if error_message:
    st.error(f'Could not read file: {error_message}')
    st.stop()



expenses_df = df[df['Kind'] == 'Expense']
income_df  = df[df['Kind'] == 'Income']
total_expense = int(expenses_df['Abs_Amount'].sum())
total_income = int(income_df['Abs_Amount'].sum())
net_savings = total_income - total_expense


st.subheader('Summary')

col1 , col2, col3, col4 = st.columns(4)


col1.metric(
    label = 'Total Income',
    value = f'₹ {total_income:,}'
)


col2.metric(
    label= 'Total Expense',
    value = f'₹ {total_expense:,}'
)


col3.metric(
    label = 'Net Savings',
    value = f'₹ {abs(net_savings):,}',
    delta=  'Deficit' if net_savings < 0 else 'Surplus',
    delta_color= 'inverse' if net_savings < 0 else 'normal'
)

col4.metric(

    label = 'Transactions',
    value = len(df)
)


st.divider()
st.subheader('Budget Status')


monthly_expenses = expenses_df.groupby('Month')['Abs_Amount'].sum().reset_index()

num_cols = min(len(monthly_expenses),3)
budget_cols = st.columns(num_cols)


for index, row in monthly_expenses.iterrows():
    month_name = row['Month']
    month_amount = int(row['Abs_Amount'])
    percentage = month_amount / monthly_budget * 100
    current_col = budget_cols[index % num_cols]
    message = f'**{month_name}**\n\n₹{month_amount:,} / ₹{monthly_budget:,} ({percentage:.0f}%)'



    if percentage > 100:
        current_col.error(f' 🚨 {message} - Over Budget! ')
    elif percentage >80:
        current_col.warning(f' {message} - Near Limit')

    else:
        current_col.success(f'✅  {message} - OK')

st.divider()


category_summary = (
    expenses_df
    .groupby('Category')['Abs_Amount']
    .sum()
    .reset_index()
    .sort_values('Abs_Amount', ascending = False)

)

left_col, right_col = st.columns(2)

with left_col:
    pie_chart = px.pie(
        category_summary,
        values= 'Abs_Amount',
        names = 'Category',
        title = 'Category Split',
        hole = 0.4
    )

    pie_chart.update_layout(**CHART_LAYOUT)
    st.plotly_chart(pie_chart, use_container_width=True)


with right_col:
    bar_chart = px.bar(
        category_summary,
        x = 'Abs_Amount',
        y = 'Category',
        orientation= 'h',
        title= 'Spending by Category'

    )

    bar_chart.update_layout(
        **CHART_LAYOUT,
        yaxis = dict(autorange = 'reversed')
    )

    st.plotly_chart(bar_chart, use_container_width=True)


st.divider()
st.subheader('Daily Spending Trend')


daily_expenses = (
    expenses_df
    .groupby(expenses_df['Date'].dt.date)['Abs_Amount']
    .sum()
    .reset_index()
)

daily_expenses.columns = ['Date', 'Amount']


line_chart = px.line(

    daily_expenses,
    x = 'Date',
    y = 'Amount',
    title = 'Day-wise Spending'

)

line_chart.update_layout(**CHART_LAYOUT)
line_chart.update_traces(line_color = '#f59e0b')
st.plotly_chart(line_chart, use_container_width=True)



st.divider()
st.subheader('Top 5 Merchants')


top_merchants = expenses_df.groupby('Merchant')['Abs_Amount'].sum().nlargest(5).reset_index()
top_merchants.columns = ['Merchants', 'Total Spent (₹)']
top_merchants.index = top_merchants.index + 1

st.table(top_merchants)


with st.expander('View All Transactions', expanded=False):

    display_df = df.copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%d %b %Y %H:%M')

    display_columns = ['Date', 'Description', 'Amount', 'Category', 'Kind']

    for extra_column in ['Remarks', 'Tags']:
        if extra_column in display_df.columns:
            display_columns.append(extra_column)


    st.dataframe(
        display_df[display_columns],
        use_container_width= True,
        hide_index= True
    )




csv_data = df.to_csv(index=False).encode('utf-8')


st.download_button(
    label = 'Download Categorized Data',
    data  = csv_data,
    file_name= 'analyzed_expenses.csv',
    mime = 'text/csv'
)

















