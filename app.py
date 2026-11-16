import streamlit as st
import streamlit as st
from datetime import datetime, date
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_all_questions_by_subject, get_all_subjects




st.title("Добро пожаловать в СтудКомпас!")
st.title("Помощник для подготовки к сессии для студентов КЭиИТ")
st.write("Выбери страницу слева, чтобы начать подготовку.")
st.divider()# отрисовывает горизонтальную линию

# обратный отсчет до сессии
from datetime import datetime

today=datetime.now()
session_day =datetime(2027,1,15)
final = (session_day - today).days#убираем последним часы минуты оставив только дни

col1, col2 = st.columns(2)

with col1:
    if final > 0:
        st.info(f"⏳ До начала экзаменационной недели осталось **{final}** дней. Не откладывай подготовку на потом!")
    else:
        st.success("Сессия уже началась! Ни пуха, ни пера! 🍀")

with col2:
    # Красивая большая плашка с днями
    st.metric(label="Дней до сессии", value=f"{final}")

st.divider()

# --- БЛОК 2: Статистика (Сводка дня) ---
st.subheader("📊 Твой прогресс")
st.write("Краткая сводка по твоим предметам:")

subjects = get_all_subjects()

if not subjects:
    st.info("У тебя пока нет созданных предметов. Перейди во вкладку 'Сессия', чтобы начать!")
else:
    # Выводим статистику для каждого предмета
    for subj in subjects:
        subj_id = subj[0]
        subj_name = subj[1]
        
        # Получаем все вопросы для этого предмета
        questions = get_all_questions_by_subject(subj_id)
        total = len(questions)
        
        if total > 0:
            known = sum(1 for q in questions if q[3] == 'Знаю')
            progress = known / total
            
            # Создаем красивую карточку для каждого предмета
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.markdown(f"**{subj_name}**")
                    st.progress(progress)
                with c2:
                    st.write(f"Выучено: **{known}**")
                with c3:
                    st.write(f"Всего: **{total}**")
        else:
            st.write(f"📁 **{subj_name}** - пока нет вопросов")

st.divider()

# --- БЛОК 3: Полезный совет дня ---
import random
advices = [
    "💡 Совет: Не пытайся выучить всё за один день. Делай перерывы и повторяй пройденное!",
    "💡 Совет: Используй режим 'Карточки' для активного повторения — это работает лучше, чем просто чтение конспекта.",
    "💡 Совет: Учи сложные темы в первой половине дня, когда мозг наиболее продуктивен.",
    "💡 Совет: Метод Помодоро (25 минут учебы, 5 минут отдыха) помогает не перегореть."
]
st.info(random.choice(advices))



