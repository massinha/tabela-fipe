
import streamlit as st
import pandas as pd
import fipe_requests as fipe
import altair as alt
from methods import *

st.title("O quanto seu carro desvalorizou?")

st.markdown(f'''
    <style>
        section[data-testid="stSidebar"] .css-1l02zno {{width: 24rem;}}
    </style>
''',unsafe_allow_html=True)

df_brands = pd.DataFrame(fipe.list_brands())
brand_option = st.sidebar.selectbox('Marca', df_brands)


brand_id = extract_option(df_brands, brand_option)
cars_list = fipe.list_models(brand_id)['Modelos']
df_models = pd.DataFrame(cars_list)
option_models = st.sidebar.selectbox('Modelo', df_models)


model_id = extract_option(df_models, option_models)
df_years = pd.DataFrame(fipe.get_years_by_model(brand_id, model_id))
option_year = st.sidebar.selectbox('Ano', df_years)
year_id = extract_option(df_years, option_year)


car_info = fipe.get_car_info(brand_id, model_id, year_id)
df_car_info = pd.DataFrame(car_info)
df_car_info.dropna(inplace = True)

raw_price_series = df_car_info['price']
price_series = extract_prices_series(df_car_info['price'])

month_series = df_car_info['month']
month_code = df_car_info['month_code']

df_car_info = pd.DataFrame({
    'preço': price_series,
    'mês': month_series,
    'preço real': raw_price_series,
    'month_code': month_code
}).sort_values('month_code', ascending=False)


final_chart = alt.Chart(df_car_info).mark_line(point = True).encode(
    alt.Y('preço', sort=alt.EncodingSortField(field='price', order='ascending')),
    alt.X('mês', sort=alt.EncodingSortField(field='month_code', order='ascending')),
    tooltip=['preço real', 'mês']
).configure_point(size=100)

st.altair_chart(final_chart, use_container_width=True)