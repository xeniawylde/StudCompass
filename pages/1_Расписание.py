import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Расписание", page_icon="📅")
st.title("📅 Расписание группы 11 ОП")

# Инициализируем память для расписания
if 'schedule_data' not in st.session_state:
    st.session_state.schedule_data = None

st.write("Загрузите файл Excel (.xlsx) с расписанием.")

uploaded_file = st.file_uploader("Выберите файл", type=["xlsx", "xls"])

# Если файл загружен, читаем его и сохраняем в память
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, header=None)
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        if str(df.iloc[0, 0]).strip() == 'День':
            df = df.iloc[1:].reset_index(drop=True)
            
        # СОХРАНЯЕМ ДАННЫЕ В ПАМЯТЬ
        st.session_state.schedule_data = df
        st.success("Файл успешно загружен и распознан!")
        
    except Exception as e:
        st.error(f"Ошибка при чтении файла. Детали: {e}")

# Если в памяти уже есть данные (или мы их только что загрузили) - показываем их
if st.session_state.schedule_data is not None:
    df = st.session_state.schedule_data
    days = df[0].dropna().unique()
    
    if len(days) > 0:
        tabs = st.tabs([str(d) for d in days])
        
        for i, day in enumerate(days):
            with tabs[i]:
                day_df = df[df[0] == day]
                
                for index, row in day_df.iterrows():
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([1, 4, 2])
                        with col1:
                            st.markdown(f"**{row[1]}**")
                        with col2:
                            st.markdown(f"**{row[2]}**")
                            st.caption(f"👤 {row[3]}")
                        with col3:
                            if len(row) > 4 and pd.notna(row[4]):
                                st.markdown(f"📍 Ауд. {row[4]}")
                            else:
                                st.markdown("📍 Ауд. -")
else:
    st.info("👆 Пожалуйста, загрузите файл, чтобы увидеть расписание.")