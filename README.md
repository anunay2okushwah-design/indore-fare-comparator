# 🚗 Ride Fare Comparison App - Indore

A Streamlit web application that compares ride-hailing fares in Indore from Uber, Ola, Rapido, and inDrive.

## Features

- **Simple UI**: Enter pickup and drop locations, click to compare fares
- **Multi-provider support**: Uber, Ola, Rapido (scraped) + inDrive (negotiable pricing)
- **Mobile-optimized scraping**: Uses Selenium with Pixel 5 emulation
- **Robust error handling**: Shows "Not available" when fares can't be retrieved
- **Clean results display**: Styled pandas DataFrame with all fare information
- **Cloud-ready**: Configured to run on Streamlit Cloud

## 🚀 Quick Start

### Running Locally

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ride-fare-comparison
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

### 🌐 Deploying to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Important for Streamlit Cloud**
   - The `packages.txt` file installs system packages (`chromium-browser`, `chromium-chromedriver`)
   - The app uses headless Chrome for web scraping with JavaScript enabled (required for fare loading)
   - First deployment may take 5-10 minutes due to package installation

## 📁 Project Structure

```
├── streamlit_app.py    # Main Streamlit application
├── requirements.txt    # Python dependencies
├── packages.txt        # System packages for Streamlit Cloud
├── README.md          # This file
└── .gitignore         # Git ignore file (optional)
```

## 🔧 Configuration

### Mobile Emulation
- The app uses Pixel 5 device emulation for consistent mobile site rendering
- Chrome runs in headless mode for cloud compatibility
- JavaScript is enabled (required for Uber, Ola, and Rapido fare loading)

### Timeout Settings
- Page load timeout: 30 seconds
- Element wait timeout: 15 seconds
- Adjust these in `streamlit_app.py` if needed for slower connections

## ⚠️ Limitations & Important Notes

### Web Scraping Challenges
- **Frequent changes**: Ride-hailing sites update their HTML structure regularly
- **Anti-bot measures**: Sites may block or limit automated requests
- **Login requirements**: Some features may require user authentication
- **Rate limiting**: Too many requests may result in temporary blocks
- **JavaScript dependency**: Fare loading requires JavaScript to be enabled

### Selector Updates
The CSS selectors in `streamlit_app.py` are examples and will need regular updates:

```python
# Update these selectors based on current site structure
fare_elements = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid*='fare'], .fare-estimate, .price"))
)
```

### Expected Behavior
- **"Not available"** is shown when:
  - Website blocks the request
  - Page structure has changed
  - Network timeout occurs
  - Login is required
- **inDrive** always shows "Set your price (negotiable)" since it uses auction-based pricing

## 🛠️ Troubleshooting

### Common Issues

1. **"Not available" for all services**
   - Check internet connection
   - Verify Chrome/Chromium installation
   - Sites may be blocking automated requests

2. **Deployment fails on Streamlit Cloud**
   - Ensure `packages.txt` contains `chromium-browser` and `chromium-chromedriver`
   - Check all dependencies are in `requirements.txt`
   - Monitor deployment logs for specific errors

3. **Selenium WebDriver errors**
   - Update `webdriver-manager` to latest version
   - Check Chrome browser compatibility
   - Verify headless mode is working

### Alternative Approaches

If Selenium becomes unreliable, consider:

1. **Playwright**: More modern automation tool
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **Official APIs**: Contact ride-hailing companies for API access
3. **Server-side solutions**: Use services like ScrapingBee or Apify
4. **Mobile app automation**: Tools like Appium for native mobile apps

### Debugging

Enable detailed logging by modifying the log level in `streamlit_app.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

Check browser automation by removing headless mode temporarily:
```python
# Comment out this line for local debugging
# chrome_options.add_argument("--headless")
```

## 🔄 Updating Selectors

When fare scraping stops working:

1. **Inspect the mobile sites** using browser dev tools
2. **Update CSS selectors** in the respective functions:
   - `get_uber_fare()`
   - `get_ola_fare()` 
   - `get_rapido_fare()`
3. **Test locally** before deploying
4. **Consider using multiple selectors** as fallbacks

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Update selectors or add new features
4. Test thoroughly
5. Submit a pull request

## ⚖️ Legal & Ethical Considerations

- This app is for educational purposes
- Respect website terms of service
- Don't overload servers with requests
- Consider using official APIs when available
- Be transparent about automated data collection

## 🎯 Future Enhancements

- [ ] Add more cities beyond Indore
- [ ] Include additional ride-hailing services
- [ ] Implement caching to reduce requests
- [ ] Add price history tracking
- [ ] Include estimated wait times
- [ ] Add map visualization of routes
- [ ] Implement user preferences and filters

---

**Note**: Web scraping is inherently fragile due to frequent website changes. For production use, consider official APIs or more robust scraping solutions.
