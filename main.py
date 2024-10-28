from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    chrome = webdriver.Chrome(options=options, service=service)

    # Get URL and XPath from event
    url = event.get('url', 'https://example.com/')
    xpath = event.get('xpath', '//html')

    chrome.get(url)

    # Wait for up to 8 seconds for the element to be present
    try:
        wait = WebDriverWait(chrome, 8)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        text = element.text
    except Exception as e:
        chrome.quit()
        return {'error': str(e)}

    chrome.quit()
    return text
