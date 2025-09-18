# LinkedIn Automator
Automate LinkedIn post

## Features

- Automated login to LinkedIn
- Send connection requests
- Send personalized messages
- Scrape profile data
- Configurable delays and limits

## Prerequisites

- Python 3.8+
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/linkedin-automator.git
   cd linkedin-automator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver:**
   - [Get ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
   - Place the executable in your PATH or project root.

## Configuration

1. **Edit `config.json`:**
   - Add your LinkedIn credentials and desired automation settings.

   ```json
   {
     "username": "your_email@example.com",
     "password": "your_password",
     "message": "Hi, I'd like to connect!",
     "max_requests_per_day": 20
   }
   ```

2. **(Optional) Update target profiles:**
   - Add LinkedIn profile URLs to `targets.txt`, one per line.

## Usage

- **Run the automator:**
  ```bash
  python main.py
  ```

- **Logs and output:**
  - Check `logs/` for activity logs and errors.

## Project Structure

```
linkedin-automator/
├── main.py
├── config.json
├── targets.txt
├── requirements.txt
├── README.md
└── utils/
    └── linkedin.py
```

## Notes

- Use responsibly and comply with LinkedIn's terms of service.
- Excessive automation may result in account restrictions.

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first.
