import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import timedelta


st.set_page_config(page_title= 'Healthcare Dashboard', layout='wide',page_icon='🏥')


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:        #030712;
    --bg2:       #050d1a;
    --surface:   #0b1628;
    --surface2:  #0f1e35;
    --border:    rgba(255,255,255,.07);
    --border-hi: rgba(0,212,170,.35);
    --teal:      #00d4aa;
    --sky:       #38bdf8;
    --rose:      #fb7185;
    --amber:     #fbbf24;
    --violet:    #a78bfa;
    --orange:    #fb923c;
    --text:      rgba(255,255,255,.92);
    --muted:     rgba(255,255,255,.50);
    --muted2:    rgba(255,255,255,.30);
    --r:         16px;
    --r-lg:      22px;
    --ease:      cubic-bezier(.2,.9,.2,1);
    --dur:       240ms;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80vw 55vh at 5%  0%,   rgba(0,212,170,.08)  0%, transparent 60%),
        radial-gradient(ellipse 60vw 50vh at 95% 5%,   rgba(56,189,248,.07) 0%, transparent 55%),
        radial-gradient(ellipse 70vw 45vh at 50% 100%, rgba(167,139,250,.05) 0%, transparent 60%),
        linear-gradient(160deg, #030712 0%, #050d1a 50%, #030c18 100%);
    pointer-events: none;
    z-index: 0;
    animation: mesh 18s var(--ease) infinite alternate;
}
@keyframes mesh {
    0%   { opacity: .9; transform: scale(1); }
    100% { opacity: 1;  transform: scale(1.04) translate(1%, -.8%); }
}

[data-testid="stAppViewContainer"] > .main { position: relative; z-index: 1; }
[data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
header[data-testid="stHeader"] {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}
.block-container {
    max-width: 1440px !important;
    padding-top: .5rem !important;
    padding-bottom: 1.4rem !important;
}

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
small, [data-testid="stCaptionContainer"], .stCaption {
    color: var(--muted) !important;
    font-size: .78rem !important;
    letter-spacing: .4px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(11,22,40,.97), rgba(5,13,26,.98)) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { font-size: .88rem; }

details[data-testid="stExpander"] {
    border-radius: var(--r) !important;
    border: 1px solid var(--border) !important;
    background: rgba(255,255,255,.03) !important;
    overflow: hidden;
    margin-bottom: 10px;
}
details[data-testid="stExpander"] summary {
    padding: .75rem 1rem !important;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    letter-spacing: .3px;
    color: var(--text) !important;
}
details[data-testid="stExpander"] summary:hover { background: rgba(0,212,170,.06) !important; }

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    border-radius: var(--r) !important;
    border: 1px solid var(--border) !important;
    background: rgba(255,255,255,.04) !important;
    color: var(--text) !important;
    transition: border-color var(--dur) var(--ease), box-shadow var(--dur) var(--ease);
}
[data-testid="stTextInput"] input:focus,
[data-testid="stDateInput"] input:focus {
    border-color: var(--border-hi) !important;
    box-shadow: 0 0 0 4px rgba(0,212,170,.12) !important;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    border-radius: var(--r) !important;
    border: 1px solid var(--border) !important;
    background: rgba(255,255,255,.04) !important;
    transition: border-color var(--dur) var(--ease), box-shadow var(--dur) var(--ease);
}
[data-testid="stSelectbox"] > div > div:focus-within,
[data-testid="stMultiSelect"] > div > div:focus-within {
    border-color: var(--border-hi) !important;
    box-shadow: 0 0 0 4px rgba(0,212,170,.12) !important;
}

[data-baseweb="tag"] {
    border-radius: 999px !important;
    background: rgba(0,212,170,.12) !important;
    border: 1px solid rgba(0,212,170,.30) !important;
    color: var(--teal) !important;
}

div[data-testid="stMetric"] {
    border-radius: var(--r-lg) !important;
    padding: 20px 18px 16px !important;
    background: linear-gradient(135deg, rgba(255,255,255,.055) 0%, rgba(255,255,255,.025) 100%) !important;
    border: 1px solid var(--border) !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,.07) inset,
        0 20px 50px rgba(0,0,0,.45),
        0 4px 12px rgba(0,0,0,.30);
    transition: transform var(--dur) var(--ease), box-shadow var(--dur) var(--ease), border-color var(--dur) var(--ease);
    position: relative;
    overflow: hidden;
}
div[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: 0; left: 15%; right: 15%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--teal), transparent);
    opacity: .55;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(0,212,170,.28) !important;
    box-shadow: 0 1px 0 rgba(255,255,255,.09) inset, 0 28px 60px rgba(0,0,0,.55), 0 0 30px rgba(0,212,170,.07);
}
div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    font-family: 'Syne', sans-serif !important;
    font-size: .72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: var(--muted) !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.75rem !important;
    font-weight: 800 !important;
    letter-spacing: -.5px;
    color: var(--text) !important;
}
div[data-testid="stMetricDelta"] { font-size: .78rem !important; font-weight: 600 !important; opacity: .85; }

.stTabs [data-baseweb="tab-list"] {
    gap: 6px !important;
    padding: 5px 6px !important;
    border-radius: 999px !important;
    border: 1px solid var(--border) !important;
    background: rgba(255,255,255,.03) !important;
    width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 999px !important;
    padding: .48rem .9rem !important;
    color: var(--muted) !important;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: .84rem;
    letter-spacing: .3px;
    transition: all var(--dur) var(--ease);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,212,170,.22), rgba(56,189,248,.16)) !important;
    color: var(--teal) !important;
    box-shadow: 0 0 18px rgba(0,212,170,.18);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: var(--r-lg) !important;
    border: 1px solid var(--border) !important;
    background: rgba(255,255,255,.025) !important;
    box-shadow: 0 12px 30px rgba(0,0,0,.30);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: transform var(--dur) var(--ease), border-color var(--dur) var(--ease);
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-2px);
    border-color: rgba(0,212,170,.20) !important;
}

.stButton > button {
    border-radius: 999px !important;
    background: linear-gradient(135deg, rgba(0,212,170,.75), rgba(56,189,248,.60)) !important;
    border: 1px solid rgba(0,212,170,.40) !important;
    color: #030712 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: .4px;
    padding: .55rem 1.1rem !important;
    transition: transform var(--dur) var(--ease), box-shadow var(--dur) var(--ease);
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(0,212,170,.25); }

[data-testid="stDataFrame"] {
    border-radius: var(--r-lg) !important;
    border: 1px solid var(--border) !important;
    overflow: hidden;
    box-shadow: 0 12px 30px rgba(0,0,0,.35);
}

hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

*::-webkit-scrollbar { width: 8px; height: 8px; }
*::-webkit-scrollbar-track { background: transparent; }
*::-webkit-scrollbar-thumb { background: rgba(255,255,255,.12); border-radius: 999px; }
*::-webkit-scrollbar-thumb:hover { background: rgba(0,212,170,.35); }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.block-container > div { animation: fadeUp 360ms var(--ease) both; }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<h1 style="
    font-family: 'Syne', sans-serif;
    background: linear-gradient(120deg, #00d4aa 0%, #38bdf8 60%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 4px;
"> Healthcare Intelligence Dashboard</h1>
<p style="color: rgba(255,255,255,.40); font-size: .85rem; margin-top: 0; margin-bottom: 1rem;">
    Real-time patient & financial analytics
</p>
""", unsafe_allow_html=True)


PALETTE = ['#00d4aa', '#38dbf8' , '#fb7185', '#fbbf24', '#a78bfa', '#fb923c']


CHART_THEME = dict(
    plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor = 'rgba(0,0,0,0)',
    font = dict(color = 'rgba(255,255,255,.07)', size = 12 , family = 'DM Sans'),
    xaxis = dict(gridcolor = 'rgba(255,255,255,.06)', showline = False , zeroline = False),
    yaxis = dict(gridcolor = 'rgba(255,255,255,.06)', showline = False , zeroline = False),
    margin = dict(l = 10 ,r = 10, t = 40 , b = 10),
    legend = dict(bgcolor = 'rgba(0,0,0,0)'),
    colorway = PALETTE,
)

# Load The Data
@st.cache_data
def load_data():
    df = pd.read_csv(r'C:\Users\Aman\Desktop\CF\Console Flare\DataSets\healthcare.csv')
    return df

df = load_data()

base_df = df.copy()



# Load the Data from Google Sheet

# @st.cache_data(ttl=5)
# def load_data():
#     sheet_id = "1Q0I7_e2aNRfQULO5e1vY1Kde62I3e9cKIEUXUvaeiC4"
#     sheet_name = "healthcare"  # apni sheet ka naam
#     url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
#     df = pd.read_csv(url)
#     return df
#
# df = load_data()
#
# base_df = df.copy()



# Load the Data from Private Google Sheet

# import gspread
# from google.oauth2.service_account import Credentials
#
# @st.cache_data(ttl=60)
# def load_data():
#     scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
#     creds = Credentials.from_service_account_file("healthcare911-cf8c04bc7834.json", scopes=scopes)
#     client = gspread.authorize(creds)
#     sheet = client.open_by_key("1Q0I7_e2aNRfQULO5e1vY1Kde62I3e9cKIEUXUvaeiC4").worksheet("healthcare")
#     data = sheet.get_all_records()
#     return pd.DataFrame(data)
#
#
# df = load_data()
#
# base_df = df.copy()



base_df['Date of Admission'] = pd.to_datetime(base_df['Date of Admission'], format = '%d-%m-%Y')

base_df['Discharge Date'] = pd.to_datetime(base_df['Discharge Date'], format = '%d-%m-%Y')

base_df['Stay Days'] = (base_df['Discharge Date'] - base_df['Date of Admission']).dt.days


base_df['Age Group'] = pd.cut(
    base_df['Age'],
    bins = [0, 18, 30, 40, 50, 120],
    labels = ['Kids','Adult','Mid','Senior', 'Old']

)

base_df['Name']  = base_df['Name'].str.title()


st.sidebar.title('🏥  Filters')

with st.sidebar.expander('Basic Filter', expanded= True):
    min_date = base_df['Date of Admission'].min().date()
    max_date = base_df['Date of Admission'].max().date()

    date_range = st.date_input('Date Range', value = (min_date,max_date), min_value= min_date, max_value= max_date)


    if isinstance(date_range, (list,tuple)) and len(date_range) == 2:
        start_date, end_date = date_range

    else:
        start_date, end_date = min_date, max_date



    medical_condition = st.multiselect('Medical Condition',
                                       options= sorted(base_df['Medical Condition'].unique()),
                                       default= sorted(base_df['Medical Condition'].unique()))


    admission_type = st.multiselect('Admission Type',
                                    options = sorted(base_df['Admission Type'].unique()),
                                    default = sorted(base_df['Admission Type'].unique()))


with st.sidebar.expander('Advanced Filters'):

    insurance_provider = st.multiselect(
        'Insurance Provider',
        options = sorted(base_df['Insurance Provider'].unique()),
        default = sorted(base_df['Insurance Provider'].unique())
                         )


    gender = st.multiselect(
        'Gender',
        options=sorted(base_df['Gender'].unique()),
        default=sorted(base_df['Gender'].unique())
    )

    age_group = st.multiselect(
        'Age Group',
        options=['Kids', 'Adult', 'Mid', 'Senior', 'Old'],
        default= ['Kids', 'Adult', 'Mid', 'Senior', 'Old']
    )


df = base_df[
    (base_df['Date of Admission'] >= pd.to_datetime(start_date)) &
    (base_df['Date of Admission'] <= pd.to_datetime(end_date)) &
    (base_df['Medical Condition'].isin(medical_condition)) &
    (base_df['Admission Type'].isin(admission_type))  &
    (base_df['Insurance Provider'].isin(insurance_provider))  &
    (base_df['Gender'].isin(gender))  &
    (base_df['Age Group'].isin(age_group))

]

total_days = (end_date - start_date).days + 1

prev_start = start_date - timedelta(days = total_days)

prev_end = start_date - timedelta(days= 1)



prev_df = base_df[
    (base_df['Date of Admission'] >= pd.to_datetime(prev_start)) &
    (base_df['Date of Admission'] <= pd.to_datetime(prev_end)) &
    (base_df['Medical Condition'].isin(medical_condition)) &
    (base_df['Admission Type'].isin(admission_type))  &
    (base_df['Insurance Provider'].isin(insurance_provider))  &
    (base_df['Gender'].isin(gender))  &
    (base_df['Age Group'].isin(age_group))

]

def get_delta(current, previous):

    if previous == 0 or pd.isna(previous) or pd.isna(current):
        return 'N/A (no prev data)'

    change = ((current - previous) / previous) * 100

    return f'{change:.1f}% vs prev'


cur_bill = df['Billing Amount'].sum()

prev_bill = prev_df['Billing Amount'].sum()

cur_adm = len(df)

prev_adm = len(prev_df)


cur_avg = df['Billing Amount'].mean()  if len(df)  else 0

prev_avg = prev_df['Billing Amount'].mean() if len(prev_df)  else 0


cur_stay = df['Stay Days'].mean()  if len(df) else 0

prev_stay = prev_df['Stay Days'].mean()  if len(df)  else 0


st.caption(f'Previous:  {prev_start}  ->  {prev_end}   | Current: {start_date}   -> {end_date} ')


col1, col2, col3, col4  = st.columns(4)

col1.metric('Total Billing', f'₹{cur_bill:,.0f}', get_delta(cur_bill,prev_bill))

col2.metric('Total Admission',f'{cur_adm:,}',get_delta(cur_adm,prev_adm))

col3.metric('AVG Billing / Admission', f'₹{cur_avg:,.0f}', get_delta(cur_avg,prev_avg))

col4.metric('AVG Stay Days', f'{cur_stay:,.1f}', get_delta(cur_stay,prev_stay))


st.divider()


tab1, tab2, tab3 = st.tabs(['Patient Intelligence', '💰 Financial Intelligence', ' 🗎 Raw Data'])



with tab1:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Unique Patient (by name)', f'{df['Name'].nunique():}')
    col2.metric('Average Age', f'{df['Age'].mean():.0f} yrs ')
    col3.metric('Avg Stay', f'{df['Stay Days'].mean():.1f} days')
    col4.metric('Emergency Rate', f'{(df['Admission Type'] == 'Emergency').mean() *100:.1f}%')

    st.divider()


    st.subheader('Demographics')


    col1, col2, col3 = st.columns(3)


    with col1:
        age_data = df['Age Group'].value_counts().reset_index()
        age_data.columns = ['Age Group', 'Count']


        fig = px.bar(age_data, x = 'Age Group', y = 'Count', text = 'Count',
                     title = 'Age Group Distribution',
                     color = 'Age Group', color_discrete_sequence= PALETTE)


        fig.update_traces(textposition = 'outside', marker_line_width = 0)

        fig.update_layout(**CHART_THEME, showlegend = False)

        st.plotly_chart(fig, use_container_width= True)



    with col2:

        gender_data = df['Gender'].value_counts().reset_index()
        gender_data.columns = ['Gender', 'Count']

        fig = px.pie(gender_data, names= 'Gender', values= 'Count',
                     title = 'Gender Distribution',
                     color_discrete_sequence= PALETTE, hole= 0.5)

        fig.update_layout(**CHART_THEME)

        st.plotly_chart(fig, use_container_width= True)



    with col3:
        cond_data =  df['Medical Condition'].value_counts().reset_index()
        cond_data.columns = ['Condition', 'Count']

        fig = px.bar(cond_data, x = 'Condition', y = 'Count',
                     title = 'Medical Condition',
                     color = 'Condition',
                     color_discrete_sequence = PALETTE )

        fig.update_traces(textposition = 'outside', marker_line_width = 0)

        fig.update_layout(**CHART_THEME, showlegend = False, xaxis_tickangle = -30)

        st.plotly_chart(fig, use_container_width= True)


    blood_data = df['Blood Type'].value_counts().sort_values().reset_index()

    blood_data.columns = ['Blood Type', 'Count']

    blood_data['Pct'] = (blood_data['Count'] / blood_data['Count'].sum() * 100).round(1)

    fig = px.bar(
        blood_data,
        x = 'Count', y = 'Blood Type',
        orientation= 'h',
        text = blood_data['Pct'].astype(str) + '%',
        title = 'Blood Type Distribution',
        color = 'Blood Type', color_discrete_sequence= PALETTE

    )

    fig.update_traces(textposition = 'outside', marker_line_width =0)
    fig.update_layout(**CHART_THEME, showlegend = False)
    st.plotly_chart(fig, use_container_width= True)


with tab2:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Total Revenue', f'{df['Billing Amount'].sum():,.0f}')
    col2.metric('Avg Billing', f'{df['Billing Amount'].mean():,.0f}')
    col3.metric('Max Bill', f'{df['Billing Amount'].max():,.0f}')
    col4.metric('Min Bill', f'{df['Billing Amount'].min():,.0f}')

    st.divider()

    col1, col2 = st.columns(2)


    with col1:

        cond_rev = df.groupby('Medical Condition')['Billing Amount'].sum().reset_index()
        cond_rev.columns = ['Condition', 'Revenue']

        cond_rev = cond_rev.sort_values('Revenue', ascending= True)

        fig = px.bar(
            cond_rev,
            x = 'Revenue' , y = 'Condition',
            orientation= 'h',
            title = 'Revenue by Medical Condition',
            color = 'Condition', color_discrete_sequence= PALETTE,
            text = 'Revenue'

        )

        fig.update_traces(texttemplate =  '₹%{text:,.0f},', textposition = 'outside', marker_line_width = 0)

        fig.update_layout(**CHART_THEME)

        st.plotly_chart(fig,use_container_width= True)

    with col2:

        ins_rev = df.groupby('Insurance Provider')['Billing Amount'].sum().reset_index()

        ins_rev.columns = ['Provider', 'Revenue']

        fig = px.pie(
            ins_rev,
            names = 'Provider',
            values= 'Revenue',
            title = 'Revenue by Insurance Provider',
            color_discrete_sequence= PALETTE, hole =0.45

        )

        fig.update_layout(**CHART_THEME)

        st.plotly_chart(fig, use_container_width= True)


with tab3:

    st.markdown(f'{len(df):,} Records')

    st.dataframe(
        df.sort_values('Date of Admission', ascending= False),
        use_container_width= True,
        height = 500
    )










