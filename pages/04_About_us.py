import streamlit as st

# set the page name
st.set_page_config(page_title='About MIDST')

# # create a sidebar
# menu = ['Home', 'About MIDST', 'Contact']
# choice = st.sidebar.selectbox('Menu', menu)

# # display content based on menu selection
# if choice == 'Home':
#     st.write('Welcome to the Home page!')
# elif choice == 'About MIDST':
#     st.write('Welcome to the About MIDST page!')
# else:
#     st.write('Welcome to the Contact page!')



# create a sidebar
st.sidebar.title('About MIDST')


st.image(['midst/images/name.png', 'midst/images/logo_alone_small.png'], use_column_width=200)
st.write("# Meet in the Middle is now Faire and Fun!")
#st.write("This is some **bold** and *italic* text.")
#st.write("Here's a [link](https://www.streamlit.io/) to Streamlit's website.")


st.write("Have you ever tried to plan a meet-up with a friend?\n")
st.write("...only to find yourselves **endlessly debating** the best place to meet?\n")
st.write("You want to **make sure it's convenient for both of you**, but also want to make it a fun experience.\n")
st.write("That's where **Midst** comes in! With Midst, you can easily identify **the perfect midpoint between your two locations while taking into consideration the travel time and travel mode**, whether you're driving, biking, or walking.")
st.write("This way, you can guarantee a fair investment of time for both you and your friend, without anyone feeling like they are traveling too far.\n")
st.write("And that's not all - once you've found your perfect midpoint, you can select the activity you want to do with your friend from a variety of suggestions provided by Midst. Whether it's trying out a new restaurant, visiting a local museum, or going on a scenic bike ride, Midst has got you covered! Finally, Midst provides you with a convenient Google Maps link to get to the midpoint, making the journey there a breeze. With Midst, you can take the stress out of planning your meet-up and make it a memorable experience for both you and your friend. It's like having a personal travel planner in your pocket!")
