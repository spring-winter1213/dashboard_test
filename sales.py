import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv('sales_data.csv')
df['date'] = pd.to_datetime(df['date'])
# KPI 카드4개
col1, col2, col3, col4 = st.columns(4)
col1.metric('총 매출', f'₩{df["sales"].sum():,}', '+8.3%')
# TODO: col2, col3, col4 에 주문수/ 평균주문액/ 최다판매제품추가
# 탭구성
tab1, tab2 = st.tabs(['매출추이', '제품별매출'])
with tab1:
	monthly = df.groupby('date')['sales'].sum().reset_index()
	fig = px.line(monthly, x='date', y='sales', title='일별 매출 추이')
	st.plotly_chart(fig, use_container_width=True)
with tab2:
# TODO: 제품별막대차트추가
	pass
# 원본데이터expander
with st.expander('원본데이터'):
	st.dataframe(df, use_container_width=True)

@st.cache_data
def load_data():
	df = pd.read_csv('sales_data.csv')
	df['date'] = pd.to_datetime(df['date'])
	return df
df = load_data()
# 사이드바필터
with st.sidebar:
	st.title('필터')
	selected_regions = st.multiselect('지역', df['region'].unique(), default=df['region'].unique())
	date_range = st.date_input('기간', value=[df['date'].min(), df['date'].max()])
# 필터적용
df_f = df[
	df['region'].isin(selected_regions) &
	(df['date'] >= pd.Timestamp(date_range[0])) &
	(df['date'] <= pd.Timestamp(date_range[1]))
]
# KPI + 차트—df_f 를사용하도록수정
col1, col2 = st.columns(2)
col1.metric('필터적용후총매출', f'₩{df_f["sales"].sum():,}')
col2.metric('주문건수', f'{len(df_f):,}건')