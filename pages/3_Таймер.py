import streamlit as st
import time

st.set_page_config(page_title="Таймер Помодоро", page_icon="🍅")

st.title("🍅 Таймер Помодоро")
st.write("Метод Помодоро: 25 минут учебы, 5 минут отдыха. Работай сфокусированно!")

# Инициализируем память для таймера
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'time_left' not in st.session_state:
    st.session_state.time_left = 25 * 60 # 25 минут в секундах

# Функция для форматирования времени (переводит секунды в ММ:СС)
def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

# Создаем две колонки: для кнопок и для таймера
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Управление")
    
    # Кнопка Старт / Пауза
    if not st.session_state.timer_running:
        if st.button("▶️ Старт", use_container_width=True):
            st.session_state.timer_running = True
            st.rerun()
    else:
        if st.button("⏸️ Пауза", use_container_width=True):
            st.session_state.timer_running = False
            st.rerun()
            
    # Кнопка Сброса
    if st.button("🔄 Сброс (25:00)", use_container_width=True):
        st.session_state.timer_running = False
        st.session_state.time_left = 25 * 60
        st.rerun()

    # Кнопка короткого перерыва (5 мин)
    if st.button(" Перерыв (5:00)", use_container_width=True):
        st.session_state.timer_running = False
        st.session_state.time_left = 5 * 60
        st.rerun()

with col2:
    st.subheader("Осталось времени")
    
    # Большое табуло с временем
    time_placeholder = st.empty()
    
    # Если таймер запущен, запускаем цикл
    if st.session_state.timer_running:
        while st.session_state.time_left > 0:
            # Обновляем текст таймера
            time_placeholder.markdown(f"# ⏳ {format_time(st.session_state.time_left)}")
            
            # Ждем 1 секунду
            time.sleep(1)
            # Уменьшаем время на 1 секунду
            st.session_state.time_left -= 1
            
        # Когда время вышло
        st.session_state.timer_running = False
        time_placeholder.markdown("# ⏰ Время вышло!")
        st.balloons() # Салют!
        st.success("Пора сделать перерыв или начать новую задачу!")
    else:
        # Если таймер на паузе, просто показываем текущее время
        time_placeholder.markdown(f"# ⏳ {format_time(st.session_state.time_left)}")
        if st.session_state.time_left == 0:
            st.success("Время вышло! Нажми 'Сброс'.")