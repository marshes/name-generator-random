import streamlit as st
import random
import pandas as pd

# Set page title
st.set_page_config(page_title="Name Grid Generator")

# Title
st.title("Name Grid Generator")

# Initialize session state for input data
if 'input_data' not in st.session_state:
    st.session_state.input_data = pd.DataFrame({'Name': ["Person's Name"], 'Occurrences': [1]})

# Sidebar for input and editing
st.sidebar.header("Enter Names and Occurrences")

# Function to clear all names and restore default
def clear_all_names():
    st.session_state.input_data = pd.DataFrame({'Name': ["Person's Name"], 'Occurrences': [1]})

# Display editable DataFrame
edited_df = st.sidebar.data_editor(
    st.session_state.input_data,
    num_rows="dynamic",
    column_config={
        "Name": st.column_config.TextColumn(
            "Name",
            help="Enter the name",
            max_chars=50,
            default="Person's Name",
        ),
        "Occurrences": st.column_config.NumberColumn(
            "Occurrences",
            help="Enter the number of occurrences",
            min_value=1,
            max_value=100,
            step=1,
            default=1,
        ),
    },
    hide_index=True,
)

# Clear button
if st.sidebar.button("Clear All Names"):
    clear_all_names()
    st.rerun()

# Generate grid button
if st.button("Generate Grid"):
    # Update the session state with the edited data
    st.session_state.input_data = edited_df

    # Create a list with names repeated according to their occurrences
    name_list = []
    for _, row in edited_df.iterrows():
        name = row['Name']
        occurrence = row['Occurrences']
        if pd.notna(name) and pd.notna(occurrence):
            try:
                occurrence = int(occurrence)
                name_list.extend([name] * occurrence)
            except ValueError:
                st.warning(f"Invalid occurrence value for {name}. Skipping this entry.")
    
    # Fill the remaining spots with blanks
    name_list.extend([''] * (100 - len(name_list)))
    
    # Shuffle the list
    random.shuffle(name_list)
    
    # Create a 10x10 grid
    grid = [name_list[i:i+10] for i in range(0, 100, 10)]
    
    # Display the grid using a DataFrame
    df = pd.DataFrame(grid)
    st.dataframe(df.style.set_properties(**{'text-align': 'center'}), hide_index=True)

# Instructions
st.markdown("""
## Instructions:
1. In the sidebar, enter names and their occurrences in the table.
2. You can copy and paste data directly into the table.
3. Click 'Generate Grid' to create and display the 10x10 grid based on your input.
4. Use 'Clear All Names' to start over with the default entry.

Note: The 'Occurrences' column should contain integer values between 1 and 100.
""")