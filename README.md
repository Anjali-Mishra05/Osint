# OSINT Social Media Pipeline

A comprehensive **Open Source Intelligence (OSINT) pipeline** for collecting, cleaning, analyzing, and visualizing data from multiple social media platforms.  
This tool gathers posts, processes the text, performs **sentiment analysis**, and stores the results in a **SQLite database** for further research and insights.



##  Overview
The **OSINT Social Media Pipeline** is built for:
-  Researchers  
-  Security professionals  
-  Data analysts  

It provides a **unified workflow** to collect data from multiple sources, clean and normalize it, run **sentiment analysis**, and store structured results in a database.



## Platforms
- **Twitter**  
- **Reddit** 
- **Instagram** 
- **Telegram** 
- **Discord** 
- **GitHub** 


##  Installation

### **Prerequisites**
- Python 3.9+  
- `pip` (Python package manager)  
- API keys/tokens for platforms you want to use  

### **Setup**
```bash
# 1. Clone the repository
git clone https://github.com/Anjali-Mishra05/OSINT_PIPELINE_SOCIAL_MEDIA.git
cd OSINT_PIPELINE_SOCIAL_MEDIA

# 2. Create virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

````
## Configuration

Create a .env file in the project root with your credentials:
### **Twitter**
TWITTER_KEY=your_twitter_api_key
TWITTER_SECRET=your_twitter_secret

### **Discord**
DISCORD_BOT_TOKEN=your_discord_token

### **Reddit**
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent

### **GitHub**
GITHUB_TOKEN=your_github_token

### **Telegram**
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash

## Database

- Data is stored in SQLite (db/osint_data.db)
- Schema can be extended with new fields per platform
- Use utils/database.py for DB interactions

### Run the complete pipeline: 
- python main.py




