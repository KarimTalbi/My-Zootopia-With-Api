# 🦁 Animal Repository Web Generator

A Python application that generates a static HTML web page to display detailed information about animals. Data is fetched from an external API, locally cached, and presented with a handy skin-type filter.

## ✨ Features

* **🔍 On-Demand Data Fetching:** Prompts the user for an animal name, retrieves taxonomy and characteristics from the Animal API (via API Ninjas).
* **💾 Local Caching:** Saves the API response to `data/animals_data.json` for persistent storage.
* **🌐 Static Web Generation:** Creates a styled, ready-to-view HTML page (`web/animals.html`) to display the animal data.
* **🎚️ Interactive Filtering:** Allows the user to select a skin type (e.g., *Fur*, *Scales*) to filter the displayed animals.

---

## ⚙️ Setup & Execution

### 📋 Prerequisites

1.  **Python:** Ensure Python is installed on your system.
2.  **Dependencies:** Install the necessary packages (`requests`, `python-dotenv`).

```bash
pip install -r requirements.txt
````

3.  **API Key:** Create a file named **`.env`** in the project's root directory and add your API Ninjas key:

<!-- end list -->

```env
API_NINJAS_KEY="YOUR_API_KEY_HERE"
```

### ▶️ Run the Application

Navigate to the root directory in your terminal and execute the main script:

```bash
python animals_web_generator.py
```

### 🚶 Execution Flow

1.  **Initial Prompt:** You'll be asked to **enter the name of the animal** you want to search for.
2.  **Filter Menu:** After data is fetched and saved, the program will present a numbered menu of unique skin types (e.g., `1. Fur`, `2. Scales`).
      * **Filter:** Enter the corresponding number (e.g., `1`) to filter the output.
      * **All Animals:** Leave the input **empty** and press **Enter**.
      * **Exit:** Select the **Exit** option to terminate the program.
3.  **View Output:** Upon completion, open the generated file **`web/animals.html`** in your web browser to see your new animal repository\!

-----

## 🏗️ Project Structure (For Developers)

The core logic is modularized for clarity:

| Module / Directory | Responsibility |
| :--- | :--- |
| `animals_web_generator.py` | Main entry point; orchestrates data fetch, user input, and generation. |
| `data/` | API interaction, JSON file handling (`json_manager.py`), and data storage (`animals_data.json`). |
| `web/` | HTML templating (`animals_template.html`), final output (`animals.html`), and HTML generation logic (`html_manager.py`). |
