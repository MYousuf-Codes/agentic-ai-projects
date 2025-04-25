import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class YouTubeAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Assistant")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create and place widgets
        ttk.Label(main_frame, text="Enter Topic to Search on YouTube:").grid(row=0, column=0, pady=10)
        
        self.search_entry = ttk.Entry(main_frame, width=40)
        self.search_entry.grid(row=1, column=0, pady=10)
        
        self.search_button = ttk.Button(main_frame, text="Search & Play", command=self.search_and_play)
        self.search_button.grid(row=2, column=0, pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=3, column=0, pady=10)
        
        # Initialize webdriver
        self.driver = None
        
    def search_and_play(self):
        topic = self.search_entry.get().strip()
        if not topic:
            messagebox.showwarning("Warning", "Please enter a topic to search!")
            return
            
        self.status_label.config(text="Opening YouTube...")
        self.root.update()
        
        try:
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            
            # Initialize the driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Open YouTube
            self.driver.get("https://www.youtube.com")
            
            # Wait for search box and enter topic
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            search_box.send_keys(topic)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for search results and click first video
            first_video = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer #video-title"))
            )
            first_video.click()
            
            self.status_label.config(text="Playing video...")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Error occurred!")
            if self.driver:
                self.driver.quit()
                self.driver = None

    def __del__(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeAssistant(root)
    root.mainloop() 