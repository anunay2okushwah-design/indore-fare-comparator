import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Indore Ride Fare Comparison",
    page_icon="🚗",
    layout="wide"
)

def setup_driver():
    """
    Set up Chrome WebDriver with mobile emulation and headless mode.
    Configured for Pixel 5 mobile device to ensure mobile pages load properly.
    """
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        
        # Mobile emulation for Pixel 5
        mobile_emulation = {
            "deviceName": "Pixel 5"
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # Use webdriver-manager to handle ChromeDriver installation
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        
        return driver
    except Exception as e:
        logger.error(f"Failed to setup driver: {str(e)}")
        return None

def get_uber_fare(pickup, drop, driver):
    """
    Attempt to scrape Uber fare estimate.
    Note: Uber's mobile site structure changes frequently. 
    Update selectors as needed.
    """
    try:
        # Construct Uber mobile URL with locations
        # This is a simplified approach - actual implementation may need geocoding
        uber_url = f"https://m.uber.com/looking?pickup={pickup.replace(' ', '%20')}&dropoff={drop.replace(' ', '%20')}"
        
        driver.get(uber_url)
        
        # Wait for fare elements to load (update selectors as needed)
        wait = WebDriverWait(driver, 15)
        
        # These selectors are examples and will need to be updated based on actual Uber mobile site
        fare_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid*='fare'], .fare-estimate, .price"))
        )
        
        if fare_elements:
            # Extract fare text from the first available element
            fare_text = fare_elements[0].text.strip()
            if fare_text and '₹' in fare_text:
                return fare_text
        
        return "Not available"
        
    except TimeoutException:
        logger.warning("Uber fare lookup timed out")
        return "Not available"
    except Exception as e:
        logger.error(f"Error fetching Uber fare: {str(e)}")
        return "Not available"

def get_ola_fare(pickup, drop, driver):
    """
    Attempt to scrape Ola fare estimate.
    Note: Ola's mobile site structure changes frequently.
    Update selectors as needed.
    """
    try:
        # Construct Ola mobile URL
        ola_url = f"https://book.olacabs.com/?pickup={pickup.replace(' ', '%20')}&drop={drop.replace(' ', '%20')}"
        
        driver.get(ola_url)
        
        wait = WebDriverWait(driver, 15)
        
        # These selectors are examples and will need to be updated
        fare_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".fare-display, .price-container, .estimated-fare"))
        )
        
        if fare_elements:
            fare_text = fare_elements[0].text.strip()
            if fare_text and '₹' in fare_text:
                return fare_text
        
        return "Not available"
        
    except TimeoutException:
        logger.warning("Ola fare lookup timed out")
        return "Not available"
    except Exception as e:
        logger.error(f"Error fetching Ola fare: {str(e)}")
        return "Not available"

def get_rapido_fare(pickup, drop, driver):
    """
    Attempt to scrape Rapido fare estimate.
    Note: Rapido's mobile site structure changes frequently.
    Update selectors as needed.
    """
    try:
        # Construct Rapido mobile URL
        rapido_url = f"https://rapido.bike/book?from={pickup.replace(' ', '%20')}&to={drop.replace(' ', '%20')}"
        
        driver.get(rapido_url)
        
        wait = WebDriverWait(driver, 15)
        
        # These selectors are examples and will need to be updated
        fare_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".fare-amount, .price-display, .estimated-price"))
        )
        
        if fare_elements:
            fare_text = fare_elements[0].text.strip()
            if fare_text and '₹' in fare_text:
                return fare_text
        
        return "Not available"
        
    except TimeoutException:
        logger.warning("Rapido fare lookup timed out")
        return "Not available"
    except Exception as e:
        logger.error(f"Error fetching Rapido fare: {str(e)}")
        return "Not available"

def get_indrive_fare(pickup, drop):
    """
    inDrive uses a negotiation model, so we return a standard message.
    """
    return "Set your price (negotiable)"

def fetch_all_fares(pickup, drop):
    """
    Fetch fares from all providers and return as a list of dictionaries.
    """
    results = []
    driver = None
    
    try:
        driver = setup_driver()
        
        if driver is None:
            # If driver setup fails, return "Not available" for all scraped services
            results = [
                {"App": "Uber", "Service": "UberGo", "Fare": "Not available"},
                {"App": "Ola", "Service": "Mini", "Fare": "Not available"},
                {"App": "Rapido", "Service": "Bike", "Fare": "Not available"},
                {"App": "inDrive", "Service": "Car", "Fare": get_indrive_fare(pickup, drop)}
            ]
            return results
        
        # Fetch Uber fare
        with st.spinner("Checking Uber fares..."):
            uber_fare = get_uber_fare(pickup, drop, driver)
            results.append({"App": "Uber", "Service": "UberGo", "Fare": uber_fare})
        
        # Fetch Ola fare
        with st.spinner("Checking Ola fares..."):
            ola_fare = get_ola_fare(pickup, drop, driver)
            results.append({"App": "Ola", "Service": "Mini", "Fare": ola_fare})
        
        # Fetch Rapido fare
        with st.spinner("Checking Rapido fares..."):
            rapido_fare = get_rapido_fare(pickup, drop, driver)
            results.append({"App": "Rapido", "Service": "Bike", "Fare": rapido_fare})
        
        # Add inDrive (no scraping needed)
        results.append({"App": "inDrive", "Service": "Car", "Fare": get_indrive_fare(pickup, drop)})
        
    except Exception as e:
        logger.error(f"Error during fare fetching: {str(e)}")
        st.error(f"An error occurred while fetching fares: {str(e)}")
    
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logger.error(f"Error closing driver: {str(e)}")
    
    return results

def main():
    """
    Main Streamlit application function.
    """
    st.title("🚗 Ride Fare Comparison - Indore")
    st.markdown("Compare fares across Uber, Ola, Rapido, and inDrive for your journey in Indore")
    
    # Create two columns for input fields
    col1, col2 = st.columns(2)
    
    with col1:
        pickup = st.text_input(
            "Pickup Location",
            placeholder="e.g., Rajwada, Indore",
            help="Enter your pickup location in Indore"
        )
    
    with col2:
        drop = st.text_input(
            "Drop Location", 
            placeholder="e.g., Vijay Nagar, Indore",
            help="Enter your destination in Indore"
        )
    
    # Center the button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        check_fares_button = st.button("🔍 Check Fares", type="primary", use_container_width=True)
    
    # Process fare checking
    if check_fares_button:
        if not pickup or not drop:
            st.warning("⚠️ Please enter both pickup and drop locations")
            return
        
        st.info(f"🔄 Checking fares from **{pickup}** to **{drop}**...")
        
        # Fetch fares
        fare_results = fetch_all_fares(pickup, drop)
        
        if fare_results:
            # Create and display results DataFrame
            df = pd.DataFrame(fare_results)
            
            st.success("✅ Fare comparison completed!")
            st.subheader("📊 Fare Comparison Results")
            
            # Style the dataframe
            styled_df = df.style.set_properties(**{
                'background-color': '#f0f2f6',
                'color': 'black',
                'border-color': 'white',
                'text-align': 'center'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('text-align', 'center')]},
                {'selector': 'td', 'props': [('text-align', 'center')]}
            ])
            
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # Show raw results in an expander for debugging
            with st.expander("🔍 Raw Results (for debugging)"):
                st.json(fare_results)
            
            # Add disclaimers
            st.markdown("---")
            st.markdown("""
            **📝 Important Notes:**
            - Fares are estimates and may vary based on demand, traffic, and time
            - Some services may require login or show different prices in their apps
            - inDrive uses negotiation-based pricing
            - If "Not available" is shown, the service may be temporarily inaccessible
            """)
        
        else:
            st.error("❌ Unable to fetch fare information. Please try again later.")

    # Add footer with additional information
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🏙️ Designed for Indore rides | Built with Streamlit & Selenium</p>
        <p><small>Note: Fare estimates are approximate and websites may block automated requests</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
