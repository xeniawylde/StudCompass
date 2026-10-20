import streamlit as st

st.title('Список продуктов')

if 'shop_list' not in st.session_state:
    st.session_state.shop_list=[]

new=st.text_input('Что купить?')
if st.button('Добавить'):
    if new.strip():
        st.session_state.shop_list.append({'name': new, 'bought': False})

st.subheader('Список')
for index, item in enumerate (st.session_state.shop_list): #получаем не только товар, но и его номер, чтобы понять у какого товара нажата кнопка
    col1,col2 = st.columns([4,1]) #ставим кнопку

    with col1:
        if item['bought']:
            st.write(f'~~{item["name"]}~~')
        else:
            st.write(item['name'])

    with col2:
        if st.button('✅', key=f'btn_{index}'):#даём кждой кнопке уникальное имя используя номер из enumerate
            st.session_state.shop_list[index]['bought'] = not item ['bought']#заходим в список по номеру, берем словарь товара, и меняем ключ на противопол
            st.rerun()#принудительно обновляем экран

#подсчет прогресса
bought_count = 0
total = len(st.session_state.shop_list)
for item in st.session_state.shop_list:
    if item['bought'] == True:
        bought_count+=1

if total>0:
    progress= bought_count / total
    st.progress(progress)
    st.write(f'bought {bought_count} из {total}')

    st.divider() 

    st.subheader("Твой прогресс:")
    st.progress(progress) 
    st.write(f"Куплено {bought_count} из {total}")