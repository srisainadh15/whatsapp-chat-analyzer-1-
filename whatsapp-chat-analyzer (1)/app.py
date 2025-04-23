import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
st.sidebar.title("whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("show analysis"):
        num_messages ,words,num_media_msg,links= helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_msg)

        with col4:
            st.header("Links Shared")
            st.title(links)

        # finding the busiest users in the group
        if selected_user == 'overall':
            st.title ('Most Busy users')
            x ,new_df= helper.most_busy_users(df)
            fig ,ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # wordcloud
        df_wc = helper.create_wordcloud(selected_user,df)
        fig ,ax = plt.subplots()
        ax = plt.imshow(df_wc)
        st.pyplot(fig)
