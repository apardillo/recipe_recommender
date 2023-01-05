import streamlit as st
from streamlit_option_menu import option_menu
from functions import NetworkGraph

#Setup
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")
ng=NetworkGraph()



list_of_pages = [
    "Introduction",
    "Network",
]



# Left the inside blank so that it really looks like a navbar
# icons = ['building' , 'person','bar-chart-fill', 'gear']
# selection = option_menu("", list_of_pages, orientation='vertical', icons=icons,
#         styles={
#         "container": {"padding": "0!important", "background-color": "#448299"},
#         "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#AB5474"},  
#         "nav-link-selected": {"background-color": "#AB5474"},    
#         })

# if selection == "Introduction":
#     st.text("")

# elif selection == "Network":
#     st.text("")
    


# Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )

# Using "with" notation
with st.sidebar:

    ingredient_filter= st.text_input('Input Ingredient Filter', 'beef')
    #st.markdown("---")

    add_radio = st.radio(
    "Select Network Type",
    ("Similar", "Complementary")
    )

    st.markdown("---")
    threshold = st.slider('Set Similarity Threshold', 0.00, 1.00, 0.05)

    button=st.button("Generate Graph")




st.header("Philippine Recipes- Recommender Network")
#st.markdown("---")
#st.subheader("Instructions")
with st.expander("View Instructions- How to Use"):
    st.markdown(
        '''
        __Step 1-> Select Ingredient Filter__
           - Select one ingredient (ex-beef, chicken, coconut, etc)
           - This will narrow down the recipes that will be shown on the network graph
        
        
        __Step 2-> Select Network Type__ (Similar or Complementary)
           - __Similar__- Each recipe shown will contain the specified ingredient in step 1. (example- Select this when you only want to see beef dishes in the network)
           - __Complementary__- Recipes shown in the network wil either 1) Contain the specified ingredient in step 1 or 2) Doesn't contain the specified ingredient but
           has a high similarity score with at least one other recipe that contains the specified ingredient. (Example use case- Use this when you have a particular main dish
           in mind but you would want to use the leftover ingredients to create a complementary dish, like dessert for example)


        __Step 3-> Set Similarity Threshold__
        - Each recipe pair has a similarity score (between 0 and 1) computed using TFIDF and Cosine Similarity.
        - The slider would filter out only those pairs of recipes that have similarity scores above the specified threshold, meaning all recipes shown are connected by their degree of similarity.
        - The higher the threshold, the fewer the recipes shown in the network, and vice versa. Graph generation also gets slower if the thresold is set too low.

        __Step 4-> Generate and Analyze__
        - Click Generate Button after setting parameters.
        - Feel free to interact with any of the nodes, by doing so you will be able to see the recipe name as well as the ingredients for the recipe.
        - By focusing on the recipes with brightly colored nodes (those with high connections), you will be able to save money since their ingredients can also be used to create 
        many other dishes. This could help with budgeting/meal planning, given inflation/the rising prices of goods.


        ''',
        unsafe_allow_html=False)

if button:
    #st.markdown("---")
    #prediction_class = Classifier.model_fit(input_features) 
    #prediction_reg = reg_model.predict(df_input)[0]
    #st.write(prediction_class)
    #st.write("Pressed Button")
    # st.write(ingredient_filter)
    # st.write(add_radio)
    ng.plot_network(threshold,ingredient_filter.lower(),f=add_radio)