import streamlit as st

# Настройка страницы
st.set_page_config(page_title="СтудКомпас", page_icon="🧭", layout="wide")

# Определяем страницы с красивыми названиями
page_home = st.Page("app.py", title="Главная", icon="🏠", default=True)
page_schedule = st.Page("pages/1_Расписание.py", title="Расписание", icon="📅")
page_session = st.Page("pages/2_Сессия.py", title="Сессия", icon="📚")
page_timer = st.Page("pages/3_Таймер.py", title="Таймер", icon="🍅")

# Создаем навигацию
pg = st.navigation([page_home, page_schedule, page_session, page_timer])

# Запускаем выбранную страницу
pg.run()