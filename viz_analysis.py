import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set page configuration
st.set_page_config(layout="wide")

# Define the path to the CSV file
BET_ANALYSIS_B365H_PATH = "BET_ANALYSIS_B365H.csv"
BET_ANALYSIS_B365D_PATH = "BET_ANALYSIS_B365D.csv"
BET_ANALYSIS_B365A_PATH = "BET_ANALYSIS_B365A.csv"
BET_CORRELATION_PATH = "Correlation.csv"

# Load the dataset
@st.cache_data
def load_data(path, index = 0):
    data = pd.read_csv(path, index_col=index)
    return data

def plot_corr_matrix(correlation_matrix):
    fig, ax = plt.subplots(figsize=(10, 8))  
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", square=True, ax=ax)
    ax.set_title("Correlation Matrix Heatmap")
    return fig

def main():
    st.title("Betting BET365[H,D,A] Analizer")

    # Load data
    try:
        data_h = load_data(BET_ANALYSIS_B365H_PATH)
        data_d = load_data(BET_ANALYSIS_B365D_PATH)
        data_a = load_data(BET_ANALYSIS_B365A_PATH)
        data_corr = load_data(BET_CORRELATION_PATH)
        st.write("All Data Loaded Successfully!")

        if st.checkbox("Show correlation map"):
            st.pyplot(plot_corr_matrix(data_corr))

        # User input for odds
        st.sidebar.header("Enter Odds")

        # Home Win Odds
        home_checkbox = st.sidebar.checkbox("Use Home Win Odds")
        if home_checkbox:
            home_win_odds = st.sidebar.number_input("Home Win Odds", min_value=0.0, step=0.01)
        
        # Draw Odds
        draw_checkbox = st.sidebar.checkbox("Use Draw Odds")
        if draw_checkbox:
            draw_odds = st.sidebar.number_input("Draw Odds", min_value=0.0, step=0.01)

        # Away Win Odds
        away_checkbox = st.sidebar.checkbox("Use Away Win Odds")
        if away_checkbox:
            away_win_odds = st.sidebar.number_input("Away Win Odds", min_value=0.0, step=0.01)

        # Display matching rows based on selected filters
        if st.button("Find Matches"):          
            if home_checkbox:
                if home_win_odds in data_h['ODD'].values:
                    row = data_h.loc[data_h['ODD'] == home_win_odds]
                    st.write("[HOME WIN]:")
                    st.write(row)
                else:
                    st.write("[HOME] Value not found.")
            
            if draw_checkbox:
                if draw_odds in data_d['ODD'].values:
                    row = data_d.loc[data_d['ODD'] == draw_odds]
                    st.write("[DRAW]:")
                    st.write(row)
                else:
                    st.write("[DRAW] Value not found.")

            if away_checkbox:
                if away_win_odds in data_a['ODD'].values:
                    row = data_a.loc[data_a['ODD'] == away_win_odds]
                    st.write("[AWAY WIN]:")
                    st.write(row)
                else:
                    st.write("[AWAY] Value not found.")
    
    except FileNotFoundError:
        st.error(f"Could not load data!. Please check the file path.")

if __name__ == "__main__":
    main()
