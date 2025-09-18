# LinkedIn Automator for DevOps Content

Automate the generation and posting of high-quality DevOps content to LinkedIn using OpenAI and AWS Lambda.

---

## Overview

This project provides an end-to-end automation pipeline for generating engaging DevOps-related LinkedIn posts using OpenAI's GPT models and posting them directly to LinkedIn via the LinkedIn API. The workflow is orchestrated using AWS Lambda functions, making it suitable for serverless, event-driven automation.

---

## Features

- **Automated Content Generation:** Uses OpenAI's GPT models to create insightful, technical, and engaging LinkedIn posts on DevOps topics.
- **Content Quality Review:** Each generated post is reviewed for length, engagement, technical accuracy, and readability.
- **Automated LinkedIn Posting:** Posts are published to LinkedIn using the official API.
- **AWS Lambda Integration:** Serverless deployment and orchestration.
- **Environment-based Configuration:** Uses environment variables for secrets and configuration.
- **Extensible and Modular:** Easily add new content types, review checks, or notification mechanisms.

---

## Project Structure

```
.
├── BaseCode/
│   ├── DevOpsContentGenerator.py      # Async content generation and review logic
│   └── LinkedInPostAutomator.py      # Local automation and workflow runner
├── LambdaHandler/
│   ├── DevOpsContentGenerator.py     # Lambda handler for content generation
│   └── LinkedInPostAutomator.py      # Lambda handler for LinkedIn posting
├── .github/
│   └── workflows/
│       └── deploy.yml                # GitHub Actions workflow for Lambda deployment
├── requirements.txt                  # Python dependencies
├── .env                              # Environment variables (not committed)
├── LICENSE
└── readme.md                         # Project documentation
```

---

## How It Works

1. **Content Generation (LambdaHandler/DevOpsContentGenerator.py):**
   - Generates a LinkedIn post idea using OpenAI's API.
   - Reviews the post for quality.
   - Returns the post content and hashtags if approved.

2. **LinkedIn Posting (LambdaHandler/LinkedInPostAutomator.py):**
   - Invokes the content generator Lambda.
   - Receives the generated post.
   - Publishes the post to LinkedIn using the LinkedIn API.

3. **Workflow Automation (BaseCode/LinkedInPostAutomator.py):**
   - Can be run locally for testing or as part of a CI/CD pipeline.
   - Handles environment loading, content generation, and posting.

---

## Prerequisites

- Python 3.8+
- AWS account with Lambda permissions
- LinkedIn Developer account with API access
- OpenAI API key

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/linkedin-automator.git
   cd linkedin-automator
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your credentials:
     ```
     OPENAI_API_KEY=your-openai-key
     access_token=your-linkedin-access-token
     author_sub=your-linkedin-user-id
     ```

---

## Configuration

- **.env:** Store your API keys and LinkedIn credentials here. Do not commit this file.
- **AWS Lambda:** Deploy the Lambda functions using the provided GitHub Actions workflow or manually via the AWS Console/CLI.
- **GitHub Actions:** The `.github/workflows/deploy.yml` automates packaging and deployment of Lambda functions.

---

## Usage

### Local Testing

You can run the workflow locally for testing:

```sh
python BaseCode/LinkedInPostAutomator.py
```

This will:
- Generate a post using OpenAI
- Review the post
- Post to LinkedIn if approved

### AWS Lambda

- The Lambda functions are triggered by events (e.g., EventBridge, API Gateway, or SNS).
- The posting Lambda (`LinkedInPostAutomator.py`) invokes the content generator Lambda and then posts the result to LinkedIn.

---

## Environment Variables

| Variable              | Description                        |
|-----------------------|------------------------------------|
| OPENAI_API_KEY        | OpenAI API key                     |
| access_token          | LinkedIn API access token           |
| author_sub            | LinkedIn user ID (URN suffix)       |
| NOTIFICATION_SNS_TOPIC| (Optional) SNS topic for notifications |

---

## Deployment

Deployment is automated via GitHub Actions:

- On push to `main`, the workflow:
  - Packages each Lambda handler as a zip file.
  - Updates the corresponding AWS Lambda function code.

You can also deploy manually using the AWS CLI:

```sh
cd LambdaHandler
zip ../DevOpsContentGenerator.zip DevOpsContentGenerator.py
aws lambda update-function-code --function-name DevOpsContentGenerator --zip-file fileb://../DevOpsContentGenerator.zip
```

---

## Security

- **Never commit your `.env` file or secrets.**
- Use AWS Secrets Manager or Parameter Store for production deployments.
- Restrict LinkedIn and OpenAI API keys to necessary scopes.

---

## Extending

- Add new content types or review checks in [`DevOpsContentGenerator`](BaseCode/DevOpsContentGenerator.py).
- Implement notification logic (e.g., SNS) in [`LinkedInPostAutomator`](LambdaHandler/LinkedInPostAutomator.py).

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Pull requests and issues are welcome! Please open an issue to discuss major changes.

---

## Disclaimer

Use responsibly and comply with LinkedIn's terms of service. Excessive automation may result in account