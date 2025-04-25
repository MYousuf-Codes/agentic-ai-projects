import streamlit as st
import os
from scraper import login_to_linkedin, search_profiles, scrape_profiles, save_to_csv, close_driver
import pandas as pd

# Set page config
st.set_page_config(
    page_title="LinkedIn Profile Scraper",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'scraping_in_progress' not in st.session_state:
    st.session_state.scraping_in_progress = False

# Title and description
st.title("LinkedIn Profile Scraper")
st.markdown("""
This tool helps you scrape LinkedIn profiles based on your search criteria.
Enter your LinkedIn credentials and search parameters below to get started.

**Note:** A Chrome browser window will open to perform the scraping. Please do not close it until the process is complete.
""")

# Sidebar for credentials
with st.sidebar:
    st.header("LinkedIn Credentials")
    email = st.text_input("LinkedIn Email")
    password = st.text_input("LinkedIn Password", type="password")
    
    st.header("Search Parameters")
    search_query = st.text_input("Search Query (e.g., 'Software Engineer')")
    search_location = st.text_input("Location (e.g., 'United States')")
    max_profiles = st.number_input("Maximum Profiles to Scrape", min_value=1, max_value=100, value=10)
    scroll_pause_time = st.slider("Scroll Pause Time (seconds)", min_value=1.0, max_value=5.0, value=2.0, step=0.5)

# Main content area
if st.button("Start Scraping", disabled=st.session_state.scraping_in_progress):
    if not all([email, password, search_query]):
        st.error("Please fill in all required fields: Email, Password, and Search Query")
    else:
        try:
            # Set scraping state
            st.session_state.scraping_in_progress = True
            
            # Set environment variables
            os.environ['LINKEDIN_EMAIL'] = email
            os.environ['LINKEDIN_PASSWORD'] = password
            os.environ['SEARCH_QUERY'] = search_query
            os.environ['SEARCH_LOCATION'] = search_location
            os.environ['MAX_PROFILES'] = str(max_profiles)
            os.environ['SCROLL_PAUSE_TIME'] = str(scroll_pause_time)
            
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Update status
                status_text.text("Logging into LinkedIn...")
                login_to_linkedin()
                progress_bar.progress(20)
                
                # Update status
                status_text.text("Searching for profiles...")
                search_profiles()
                progress_bar.progress(40)
                
                # Update status
                status_text.text("Scraping profiles...")
                profiles_data = scrape_profiles()
                progress_bar.progress(80)
                
                # Save to CSV
                if profiles_data:
                    status_text.text("Saving results...")
                    save_to_csv(profiles_data)
                    progress_bar.progress(100)
                    
                    # Display results
                    st.success("Scraping completed successfully!")
                    
                    # Create a DataFrame for display
                    df = pd.DataFrame(profiles_data)
                    st.dataframe(df)
                    
                    # Download button for CSV
                    with open('linkedin_profiles.csv', 'rb') as f:
                        st.download_button(
                            label="Download CSV",
                            data=f,
                            file_name='linkedin_profiles.csv',
                            mime='text/csv'
                        )
                else:
                    st.warning("No profiles were found matching your criteria.")
                    
            except Exception as e:
                st.error(f"An error occurred during scraping: {str(e)}")
                progress_bar.progress(0)
                status_text.text("")
            finally:
                # Clean up
                close_driver()
                st.session_state.scraping_in_progress = False
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.scraping_in_progress = False

# Add some helpful information
st.markdown("""
### Tips for Better Results:
1. Be specific with your search query
2. Use location filters to narrow down results
3. Start with a smaller number of profiles to test
4. If you get rate limited, try increasing the scroll pause time

### Note:
- The scraper respects LinkedIn's terms of service
- Use this tool responsibly and don't scrape too many profiles at once
- The process may take some time depending on the number of profiles
- A Chrome browser window will open to perform the scraping
- Please do not close the browser window until the process is complete
""") 