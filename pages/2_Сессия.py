import streamlit as st

st.title('Моя подготовка к сессии')

# создали список(память)
if 'question' not in st.session_state:
    st.session_state.question = []

# Создаем форму для вопросв которая сама очищается после отправки
with st.form("add_question_form", clear_on_submit=True):#когда вопрос отправляется то идет перехватывание текста и программа его забывает для очистки поля
    new_question = st.text_input('Создайте новый вопрос')
    submit = st.form_submit_button("Добавить")#создаем кнопку которая добавит вопрос в список

if submit and new_question:
     st.session_state.question.append({"text": new_question, "status": "Не знаю"})
     st.rerun()#обновляем и вопрос появляется в списке и поле ввода очищается


# Вывод списка и вычеркивание
st.subheader('Список вопросов')
for index, item in enumerate( st.session_state.question):#получаем не только вопрос, но и его номер, чтобы понять у какого товара нажата кнопка
    with st.container():# контейнер для каждого вопроса чтобы кнопки не путались 
        col1, col2 = st.columns([4,1]) #ставим кнопку


    with col1:
        text_place = st.empty()#пустое место для текста

        #проверка статуса
        if item['status']=='Знаю':
            #если знаем - зачеркиваем
            text_place.write(f"~~{item['text']}~~")#если выучили зачеркиваем

            #если не знаю то обычный текст без зачерк
        else:
            text_place.write(item['text'])



    with col2:
        button_place = st.empty()# пустое место для кнопки здесь может быть только одна

        #1
        if item['status']!='Знаю':
            with button_place:
                if st.button('✅', key=f'btn_{index}'):#даём кждой кнопке уник имя используя номер из enumerate
                    #если нажали то меняем статус на знаю
                    st.session_state.question[index]['status'] = 'Знаю' #заходим в список по номеру, берем словарь вопроса, и меняем ключ на противопол
                    st.rerun()#принудительно обновляем

                #если статус равер знаю
        #2
        else:
            with button_place:
                #делаем кнопку вернуть вопрос
                if st.button('Вернуть вопрос', key=f'undo_{index}'):
                #при нажатии меняем кнопку на не знаю
                    st.session_state.question[index]['status']='Не знаю'
                    st.rerun()
                

#  Подсчет прогресса
question_count=0
total=len(st.session_state.question)
for item in st.session_state.question:
    if item['status']=='Знаю':
        question_count+=1

if total>0:
    progress=question_count/total
    st.progress(progress)
    st.write(f'Знаю {question_count} из {total}')