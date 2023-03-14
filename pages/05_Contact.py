import streamlit as st

# set the page name
st.set_page_config(page_title='Contacts')
# create a sidebar
st.sidebar.title('MIDST Team')



st.image(['midst/images/name.png', 'midst/images/logo_alone_small.png'], use_column_width=200)
st.write("# Meet the MIDST Team")


# define the list of contacts
contacts = [
    ('Tobias', 'Lewen', 'https://www.linkedin.com/in/tobias-lewen-983b61242/'),
    ('Israel', 'Maureira', 'https://www.linkedin.com/in/israelmaureira/'),
    ('Raffaele', 'Triggiano', 'https://www.linkedin.com/in/raffaele-triggiano-1926b616/'),
    ('Xiao', 'Zhou', 'https://www.linkedin.com/in/xiaozhou7/')
]

# set up the columns
num_cols = 2
col_list = [st.columns(num_cols) for i in range(len(contacts) // num_cols + 1)]

# loop through the contacts and add them to the columns
contact_idx = 0
for row in col_list:
    for col in row:
        if contact_idx < len(contacts):
            contact = contacts[contact_idx]
            with col:
                #st.image('profile_picture.png', use_column_width=True)
                st.title(contact[0] + ' ' + contact[1])
                st.markdown('*Software Developer*')
                st.markdown('[Connect on LinkedIn](' + contact[2] + ')')
            contact_idx += 1




# # set up sidebar with profile picture
# #st.sidebar.image('profile_picture.png', use_column_width=True)

# st.image(['midst/images/name.png', 'midst/images/logo_alone_small.png'], use_column_width=200)

# # set up main content area with name, surname, and LinkedIn link
# st.title('John Doe')
# st.markdown('*Software Developer*')
# st.markdown('[Connect on LinkedIn](https://www.linkedin.com/in/johndoe/)')

# # add border and round the profile picture
# st.sidebar.markdown('<p style="text-align: center;"><img style="border-radius:50%;" src="profile_picture.png" /></p>', unsafe_allow_html=True)



# col1, col2 = st.columns(2)

# with col1:
#     st.title('John Doe')
#     st.markdown('*Software Developer*')
#     st.markdown('[Connect on LinkedIn](https://www.linkedin.com/in/johndoe/)')

#     st.title('John Doe')
#     st.markdown('*Software Developer*')
#     st.markdown('[Connect on LinkedIn](https://www.linkedin.com/in/johndoe/)')

# with col2:
#     st.title('John Doe')
#     st.markdown('*Software Developer*')
#     st.markdown('[Connect on LinkedIn](https://www.linkedin.com/in/johndoe/)')

#     st.title('John Doe')
#     st.markdown('*Software Developer*')
#     st.markdown('[Connect on LinkedIn](https://www.linkedin.com/in/johndoe/)')
