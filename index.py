### Library Imports ###
import streamlit as st
import pandas as pd
import plotly.express as px


# CSV file fetching #
df = pd.read_csv("agridata.csv")

st.set_page_config(
    page_title="AgriStat",
    page_icon=':tractor:',
    layout="wide",
    initial_sidebar_state="collapsed")

def sidebar():
    st.sidebar.markdown(''' # <h1 class="si-title">AgriStat 🚜</h1>''', unsafe_allow_html=True)
    navItems = ["🏡 Home", "💹 Area and Production by State", "💹 Crop Yield Comparison", "👨‍💻 About "]
    navItemsKey = ['home', 'item1', 'item2', 'abt']

    for i in range(0, len(navItems)):
        # if st.sidebar.markdown(f'''<div class="si-item">{navItems[i]}</div>''', unsafe_allow_html=True):
        script = """
            <script>
                function test(){
                    alert('test')
                }
            </script>
        """
        st.markdown(script, unsafe_allow_html=True)
        link_html = f'''[<div class="si-item">{navItems[i]}</div>](#{navItemsKey[i]})'''
        # link_html = f'''<div class="si-item">{navItems[i]}</div>'''
        st.sidebar.markdown(link_html, unsafe_allow_html=True) 
    st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
    st.sidebar.markdown('''<small>[AgriStat](#git)  | Jan 2024 | [Dinesh J V](#dinesh)</small>''', unsafe_allow_html=True)
    return None

def barChart(data, yaxisList):
    agg_df = data.groupby('Year').agg({col: 'sum' for col in yaxisList}).reset_index()
    fig = px.bar(
            agg_df,
            x='Year',
            y=yaxisList,
            title='Crop Yields Over Years',
            labels={
                'value': 'Yield (bushels/acre)',
                'variable': 'Crop'
            },
        )

    return fig
    
def stackedBarChart(data, yaxisList):
    # Aggregate data for each State

    agg_df = data.groupby('State Name').agg({col: 'sum' for col in yaxisList}).reset_index()
    fig = px.bar(
        agg_df,
        x='State Name',
        y=yaxisList,
        title='Area and Production by State',
        labels={
            'value': 'Value',
            'variable': 'Category'
        },
        color_discrete_map={
            'Area (acres)': '#1f77b4',
            'Production (tons)': '#ff7f0e'
        },
    )

    return fig

def main():
    custom_styles = """
        <style>
            .st-emotion-cache-0 {
                width: 100%;
                height: 100%;
            }
            .div-block{
                border: solid;
            }
            .title {
                text-align: center;
                font-size: 110px;
                font-family: "Open Sans", sans-serif;
                letter-spacing: -0.02em;
            }
            .subheader {
                text-align: center;
                font-size: 35px;
                padding: 5rem 0px;
            }
            .sub-title {
                color: rgb(41, 181, 232);
                margin-left: 10px;
            }
            .si-title{
                # text-align: center;
                font-family: "Open Sans", sans-serif;
                color: gray;
            }
            .si-item{
                # text-align: center;
                letter-spacing: -0.02em;
                font-family: "Open Sans", sans-serif;
                margin-top: 10px;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transition: background-color 0.3s ease, transform 0.3s ease;
            }
            .si-item:hover {
                # background-color: rgb(41, 181, 232);
                # color: black;
                background-color: #e74c3c;
                transform: scale(1.05);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            }
        </style>
    """
   
    st.markdown(custom_styles, unsafe_allow_html=True)
    sidebar()
    
    with st.container():
        st.markdown("<div id='home'>", unsafe_allow_html=True)

        st.markdown("<h1 class='title'>Agri<span class='sub-title'>Stat</span>🚜</h1>", unsafe_allow_html=True)
        st.markdown("<h2 class='subheader'>Welcome to AgriStat - Transforming Agriculture with Data Visualization. Explore the power of insightful visualizations to make informed decisions and revolutionize your approach to farming and research.</h2>",  unsafe_allow_html=True)

    with st.container():
        st.markdown("<div id='item1'>", unsafe_allow_html=True)
        st.subheader("Area and Production by State")
        st.markdown("<div class='div-block'>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write('''Discover agricultural trends at a glance with our Stacked Bar Chart - "Area and Production by State". Effortlessly visualize crop production areas and yields across different states, gaining valuable insights for informed decision-making in the farming landscape.''')
        columns = st.columns((1.5, 6.5,), gap='medium')
        with columns[0]:
            yeildlist = ['RICE', 'WHEAT', 'RABI SORGHUM ']
            selected_corp = st.selectbox('Select a crop', yeildlist)
            matching_columns = [col for col in df.columns if selected_corp.upper() in col]
            yearList = list(df['Year'].unique())[::-1]
            selected_year = st.selectbox('Select a State', yearList)
            df_selected_year = df[df['Year'] == selected_year]

        with columns[1]:
            stackBarcht = stackedBarChart(df_selected_year, matching_columns)
            st.plotly_chart(stackBarcht, use_container_width=True)
        
    with st.container():
        
        st.markdown("<div id='item2'>", unsafe_allow_html=True)
        st.subheader("Crop Yield Comparison Bar Chart")
        st.markdown("<div class='div-block'>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write(''' Uncover historical crop performance with our Yield Comparison Bar Chart. Track yield variations across years, gaining valuable insights from past data ''')

        columns = st.columns((1.5, 6.5,), gap='medium')

        with columns[0]:
            state_list = list(df['State Name'].unique())[::-1]
            selected_state = st.selectbox('Select a State', state_list)
            df_selected_state = df[df['State Name'] == selected_state]
            yeildlist = ['RICE YIELD (Kg per ha)', 'WHEAT YIELD (Kg per ha)', 'RABI SORGHUM YIELD (Kg per ha)']
            selected_corp = st.multiselect('Select a crop', yeildlist, default=yeildlist)
            if not selected_corp:
                selected_corps_list = yeildlist
            else:
                selected_corps_list = selected_corp

        with columns[1]:
            cropYeildChart = barChart(df_selected_state, selected_corps_list)
            st.plotly_chart(cropYeildChart, use_container_width=True)

    with st.container():
        st.header("About")
        st.markdown("<div class='div-block' id='abt'>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras aliquet lacinia mauris ut vestibulum. Integer auctor tempor leo, quis lobortis purus aliquet quis. Donec non eleifend elit, et convallis dolor. Nunc ornare massa vel orci porta, id elementum sem rhoncus. Proin lobortis, urna ac feugiat fringilla, dui lectus congue dui.")

if __name__ == "__main__":
    main()