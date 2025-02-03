import streamlit as st
import random
import pandas as pd

# Set page title
st.set_page_config(page_title="Name Grid Generator")

# Title
st.title("Name Grid Generator")

# Initialize session state for names and occurrences
if 'names' not in st.session_state:
    st.session_state.names = []
    st.session_state.occurrences = []

# Sidebar for input and editing
st.sidebar.header("Enter and Edit Names")

# Input for new name and occurrence
new_name = st.sidebar.text_input("Enter a name:")
new_occurrence = st.sidebar.number_input("Enter number of occurrences:", min_value=1, max_value=100, value=1, step=1)

# Add button
if st.sidebar.button("Add Name"):
    st.session_state.names.append(new_name)
    st.session_state.occurrences.append(new_occurrence)

# Edit existing names and occurrences
st.sidebar.subheader("Edit Names and Occurrences:")

# Add headers
col1, col2, col3 = st.sidebar.columns([3, 1, 1])
col1.write("Name")
col2.write("Occurrences")
col3.write("Delete?")

for i, (name, occurrence) in enumerate(zip(st.session_state.names, st.session_state.occurrences)):
    col1, col2, col3 = st.sidebar.columns([3, 1, 1])
    
    with col1:
        new_name = st.text_input(f"Name", value=name, key=f"name_{i}", label_visibility="collapsed")
    with col2:
        new_occurrence = st.number_input(f"Occurrences", min_value=1, max_value=100, value=occurrence, key=f"occurrence_{i}", step=1, label_visibility="collapsed")
    with col3:
        if st.button("Delete", key=f"delete_{i}"):
            del st.session_state.names[i]
            del st.session_state.occurrences[i]
            st.rerun()
    
    st.session_state.names[i] = new_name
    st.session_state.occurrences[i] = new_occurrence

# Clear button
if st.sidebar.button("Clear All Names"):
    st.session_state.names = []
    st.session_state.occurrences = []
    st.rerun()

# Generate grid button
if st.button("Generate Grid"):
    # Create a list with names repeated according to their occurrences
    name_list = []
    for name, occurrence in zip(st.session_state.names, st.session_state.occurrences):
        name_list.extend([name] * occurrence)
    
    # Fill the remaining spots with blanks
    name_list.extend([''] * (100 - len(name_list)))
    
    # Shuffle the list
    random.shuffle(name_list)
    
    # Create a 10x10 grid
    grid = [name_list[i:i+10] for i in range(0, 100, 10)]
    
    # Display the grid using a DataFrame
    df = pd.DataFrame(grid)
    st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

# Instructions
st.markdown("""
## Instructions:
1. Enter a name and the number of times it should appear in the sidebar.
2. Click 'Add Name' to add it to the list.
3. Edit existing names and occurrences directly in the sidebar.
4. Use the plus/minus buttons or type to adjust occurrences.
5. Use the 'Delete' button to remove a name from the list.
6. Click 'Generate Grid' to create and display the 10x10 grid.
7. Use 'Clear All Names' to start over.
""")