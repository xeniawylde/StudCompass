import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from database import add_subject, get_all_subjects, add_question, get_all_questions_by_subject, update_status, get_random_question, delete_question, delete_subject, add_questions_from_list, update_answer



st.title('Моя подготовка к сессии')
# создали список(память)
# if 'question' not in st.session_state:
#     st.session_state.question = []
# теперь этот блок не нужен вместо него вызываем ф-ию баз данных item in num..


# создаем память для выбранной папки
if 'current_subject' not in st.session_state:
    st.session_state.current_subject = None #сначала ни в одной папке
 
#если НЕ в папке (показываем меню папок)
if st.session_state.current_subject is None:
    st.subheader("📂 Выберите предмет")
    
    #форма создания новой папки
    with st.form("add_subject_form", clear_on_submit=True):
        new_subject = st.text_input("Название нового предмета")
        submit_subject = st.form_submit_button("Создать предмет")
        
        if submit_subject:
            # Убираем случайные пробелы в начале и конце
            clean_name = new_subject.strip()
            
            # Если после этого строка пустая — показываем ошибку
            if not clean_name:
                st.error("Название предмета не может быть пустым!")
            else:
                # Проверяем, нет ли уже такого предмета в базе
                subjects = get_all_subjects()
                existing_names = [s[1].lower() for s in subjects if s[1]]
                
                if clean_name.lower() in existing_names:
                    st.warning("Такой предмет уже есть в списке!")
                else:
                    add_subject(clean_name)
                    st.rerun()


    subjects = get_all_subjects()
    
    if subjects:
        st.write("Нажмите на кнопку, чтобы зайти в папку:")

        for i, s in enumerate(subjects):
            subject_id = s[0] #выводим каждую папку как кнопку
            subject_name = s[1]
            
            #выводим кнопку только если имя не пустое
            if subject_name and str(subject_name).strip():
                #Делим кнопку на две колонки: вход и удаление
                col_open, col_del = st.columns([4, 1])

                with col_open:
                    if st.button(f"📁 {subject_name}", key=f"folder_{i}_{subject_id}"):#сделали уникальные ключи
                        st.session_state.current_subject = (subject_id, subject_name)
                        st.rerun()


                with col_del:
                    if st.button("🗑️", key=f"del_subj_{subject_id}"):
                        delete_subject(subject_id)
                        st.rerun()
    else:
        st.info("У вас пока нет предметов. Создайте первый!")





# 3 если уже  папке (показываем вопросы)
else:
    #достаем айди и название папки из памяти
    subj_id, subj_name = st.session_state.current_subject
    
    #кнопка "Назад" (очищает память и возвращает к списку папок)
    if st.button("⬅️ Назад к предметам"):
        st.session_state.current_subject = None
        st.rerun()
        
    st.subheader(f"📁 Предмет: {subj_name}")

    st.divider()
    st.subheader("📥 Загрузка вопросов из файла")
    st.write("Загрузите текстовый файл (.txt), где каждая строка — это новый вопрос.")
    
    # Создаем память для загруженных файлов (чтобы не грузить дважды)
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

    uploaded_file = st.file_uploader("Выберите файл", type=["txt"])
    
    if uploaded_file is not None:
        # Проверяем, не загружали ли мы уже этот файл
        if uploaded_file.name in st.session_state.uploaded_files:
            st.success(f"✅ Файл '{uploaded_file.name}' уже успешно загружен в эту папку! Вы можете загрузить другой файл.")
        else:
            # Читаем файл
            string_data = uploaded_file.getvalue().decode("utf-8")
            questions_list = [line for line in string_data.split('\n') if line.strip()]
            
            st.info(f"В файле найдено вопросов: **{len(questions_list)}**")
            
            if st.button("Добавить эти вопросы в базу"):
                if questions_list:
                    add_questions_from_list(subj_id, questions_list)
                    # Запоминаем имя файла, чтобы кнопка больше не срабатывала
                    st.session_state.uploaded_files.append(uploaded_file.name)
                    st.success(f"Успешно добавлено {len(questions_list)} вопросов!")
                    st.rerun()
                else:
                    st.warning("Файл пуст или не содержит текста.")
    # дальше идет  старая форма ручного добавления


# Создаем форму для вопросв которая сама очищается после отправки
    with st.form("add_question_form", clear_on_submit=True):#когда вопрос отправляется то идет перехватывание текста и программа его забывает для очистки поля
        new_question = st.text_input('Создайте новый вопрос')
        new_answer = st.text_input('Напишите краткий ответ (для карточек)')
        submit_q = st.form_submit_button("Добавить")#создаем кнопку которая добавит вопрос в список

    if submit_q:
        clean_q = new_question.strip()
        clean_a = new_answer.strip()
        if clean_q:
            add_question(subj_id, clean_q, clean_a)#передаем 3 аргумента папку, вопрос и ответ
            st.rerun()#обновляем и вопрос появляется в списке и поле ввода очищается
        else:
            st.warning("Вопрос не может быть пустым!")


    
    folder_questions = get_all_questions_by_subject(subj_id)


    # Создаем две вкладки
    tab1, tab2 = st.tabs(["📝 Список вопросов", "🎴 Карточки"])
    
    # ВСЁ, ЧТО БЫЛО НИЖЕ (вывод списка), ПЕРЕНЕСИ ВНУТРЬ tab1
    with tab1:
        st.subheader('Список вопросов')
        # Вывод списка и вычеркивание
    
        #вызываем ф-ию которая фильтрует вопросы по паке 
        folder_questions = get_all_questions_by_subject(subj_id)

        if not folder_questions:
            st.info('В этой папке пока нет вопросов.')


        for index, item in enumerate(folder_questions):#получаем не только вопрос но и номер
            with st.container():# контейнер для каждого вопроса чтобы кнопки не путались 
                col1, col2 = st.columns([4,1]) #ставим кнопку


                with col1:
                    text_place = st.empty()
                    if item[3] == 'Знаю':
                        text_place.write(f"~~{item[2]}~~")
                    else:
                        text_place.write(item[2])
                        
                    # --- НОВЫЙ БЛОК ДЛЯ ОТВЕТА ---
                    # Проверяем, есть ли уже ответ в базе (item[4] - это answer_text)
                    current_answer = item[4] if len(item) > 4 and item[4] else ""
                    
                    # Используем expander, чтобы не загромождать экран
                    with st.expander("✍️ Добавить/Изменить ответ для карточки"):
                        # Текстовое поле, в которое подставляется текущий ответ
                        new_ans = st.text_input("Ответ:", value=current_answer, key=f"ans_{item[0]}")
                        
                        if st.button("Сохранить ответ", key=f"save_ans_{item[0]}"):
                            update_answer(item[0], new_ans)
                            # Показываем всплывающее уведомление
                            st.toast("✅ Ответ успешно сохранен!", icon="💾")
                            # Небольшая пауза, чтобы пользователь увидел уведомление
                            time.sleep(0.5) 
                            st.rerun()



                with col2:
                    button_place = st.empty()# пустое место для кнопки здесь может быть только одна
                    
                    #1
                    if item[3]!='Знаю':
                        with button_place:
                            if st.button('✅', key=f'btn_{item[0]}'):#даём кждой кнопке уник имя используя номер из enumerate
                                #если нажали то меняем статус на знаю
                                update_status(item[0], 'Знаю') #заходим в список по номеру, берем словарь вопроса, и меняем ключ на противопол
                                st.rerun()#принудительно обновляем

                            #если статус равер знаю
                    #2
                    else:
                        with button_place:
                            #делаем кнопку вернуть вопрос
                            if st.button('Вернуть вопрос', key=f'undo_{item[0]}'):
                            #при нажатии меняем кнопку на не знаю
                                update_status(item[0], "Не знаю")
                                st.rerun()


                    # 3. КНОПКА УДАЛЕНИЯ (на том же уровне, что и if/else)
                    if st.button('🗑️', key=f'del_q_{item[0]}'):
                        delete_question(item[0])
                        st.rerun()            
    with tab2:
        
        st.subheader("Режим карточек")
        
        # Если мы только зашли в карточки или нажали "Оценить", берем НОВЫЙ вопрос
        if 'current_card' not in st.session_state or st.session_state.current_card is None:
            random_q = get_random_question(subj_id)
            st.session_state.current_card = random_q # Запоминаем его!
        else:
            random_q = st.session_state.current_card # Берем старый
            
        if not random_q:
            st.info("В этой папке нет вопросов для карточек.")
        else:
            question_id = random_q[0]
            question_text = random_q[2]
            answer_text = random_q[4] if random_q[4] else "Ответ не записан"
            
            # Проверяем, нажата ли кнопка переворота (она хранится в памяти)
            if 'show_answer' not in st.session_state:
                st.session_state.show_answer = False
                
            with st.container(border=True):
                st.markdown(f"### {question_text}")
                
                if not st.session_state.show_answer:
                    if st.button("🔄 Перевернуть карточку", use_container_width=True):
                        st.session_state.show_answer = True
                        st.rerun()
                else:
                    st.info(f"**Ответ:** {answer_text}")
                    
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("✅ Знаю", use_container_width=True):
                            update_status(question_id, 'Знаю')
                            # Сбрасываем память, чтобы в следующий раз выпал новый вопрос
                            st.session_state.current_card = None 
                            st.session_state.show_answer = False
                            st.rerun()
                    with col_no:
                        if st.button("❌ Не знаю", use_container_width=True):
                            update_status(question_id, 'Не знаю')
                            st.session_state.current_card = None
                            st.session_state.show_answer = False
                            st.rerun()






    #полуаем данные из базы
    all_questions = get_all_questions_by_subject(subj_id)

        #  Подсчет прогресса
    question_count=0
    total=len(all_questions)
        
    for item in all_questions:
        if item[3] == 'Знаю':
            question_count += 1

    if total>0:
        progress=question_count/total
        st.progress(progress)
        st.write(f'Знаю {question_count} из {total}')