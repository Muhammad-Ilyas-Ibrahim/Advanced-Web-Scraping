# Advanced Web Scraping: Python + JavaScript Cloudflare Bypass

This project demonstrates a unique approach to web scraping that combines Python and JavaScript to bypass Cloudflare protection. By leveraging the strengths of both languages, we've created a powerful tool for data extraction from protected websites.

## 🌟 Key Features

- **Cloudflare Bypass**: Utilizes JavaScript in the browser console to scrape the data and Cloudflare does not block that scraping.
- **Automated Browser Interaction**: Uses PyAutoGUI for automated browser control.
- **Data Persistence**: Stores scraped data in SQLite databases for efficient retrieval and analysis.
- **Robust Error Handling**: Implements multiple retry mechanisms and error checks to ensure reliable scraping.
- **Scalable Architecture**: Designed to handle large-scale scraping tasks with ease.

## 🛠️ Technologies Used

- Python 3.x
- JavaScript
- SQLite
- PyAutoGUI
- Pyperclip

## 📋 Prerequisites

- Python 3.x installed
- A modern web browser (Chrome recommended)
- Required Python libraries: `pyautogui`, `pyperclip`

## 🚀 Setup and Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Muhammad-Ilyas-Ibrahim/Advanced-Web-Scraping.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Advanced-Web-Scraping
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure you have the necessary JavaScript files in the `scripts` directory:
   - `scrape_urls.js`
   - `scrape_details.js`
   - `scrape_number.js`

## 🏃‍♂️ How to Run

1. Open your target website in a browser and navigate to the developer console.

2. Run the main Python script:
   ```bash
   python scrape.py
   ```

3. Follow the on-screen prompts to start the scraping process.

## 🧠 How It Works

1. **URL Scraping**: The script first scrapes property URLs from the main page using JavaScript injected into the browser console.

2. **Detail Extraction**: For each URL, it navigates to the property page and extracts detailed information using another JavaScript snippet.

3. **Phone Number Retrieval**: The script first checks the existing database of agents' profiles to retrieve the contact number. If it's not found in the database, it visits the agent's profile page to extract their contact number.

4. **Data Storage**: All scraped data is stored in SQLite databases for easy access and analysis.

5. **Error Handling**: The script implements various checks and retry mechanisms to handle common scraping issues like network errors or missing data.

## 🔧 Modify JavaScript and Python Code

If you need to adapt the scraping logic to your specific requirements, you can modify both the JavaScript and Python parts of the project:

- **JavaScript Modifications**: Customize the JavaScript files located in the `scripts` directory to match the structure of the website you are scraping. For example, if the target page's elements have changed or new data is needed, update the selectors and logic in `scrape_urls.js`, `scrape_details.js`, or `scrape_number.js`.

- **Python Modifications**: In the `scrape.py` file, you can adjust the Python code to modify the workflow, add additional processing steps, or change how the data is stored in the SQLite database. You can also tweak the retry mechanisms or error handling based on your needs.

- **Images Replacement**: Replace the images as well. Take screenshots of the same widgets on your screen and save the Images.

## ⚠️ Disclaimer

This project is for educational purposes only. Always respect website terms of service and scraping policies. Use responsibly and ethically.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/Muhammad-Ilyas-Ibrahim/Advanced-Web-Scraping/issues).
```
