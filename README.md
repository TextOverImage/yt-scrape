# Youtube thumbnail scraper

## Instructions
1. Initialize the virtual environment (optional). But if created, add the folder name in `.gitignore` file.

2. Install all the libraries mentioned in `requirements.txt` using the code:

   ```pip install -r requirements.txt```
   
3. Install pytesseract-ocr using the code:

    - For Linux/mac users:
    
      ```sudo apt-get install tesseract-ocr```
    - For windows users:

      Download the Tesseract-OCR installer from the official ([Github Repository](https://github.com/tesseract-ocr/tesseract)) and follow the installation instructions. Make sure to add the Tesseract-OCR executable directory to your system’s PATH variable (e.g., `C:\Program Files\Tesseract-OCR`).
4. Create a new file `.env` in the root folder and copy paster the below content:

    ```
    EMAIL=xyz@gmail.com
    PASSWORD=your_password
    ```
5. Run the command
   `python3 yt-thumbnails.py`
