import logging
import random
from datetime import datetime
from typing import List, Dict
import aiohttp
from dataclasses import dataclass
from enum import Enum
from rich.console import Console
from rich.markdown import Markdown
import ssl
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

class ContentType(Enum):
    TECHNICAL_TIP = "technical_tip"
    PROBLEM_SOLUTION = "problem_solution"
    TOOL_DISCOVERY = "tool_discovery"
    BEST_PRACTICE = "best_practice"
    INDUSTRY_NEWS = "industry_news"
    PERSONAL_INSIGHT = "personal_insight"

@dataclass
class LinkedInPost:
    content: str
    hashtags: List[str]
    post_type: ContentType
    scheduled_time: datetime
    status: str = "pending"

class DevOpsContentGenerator:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.topics = {
            "tools": ["Kubernetes", "Docker", "Terraform", "Ansible", "Jenkins", 
                     "GitLab CI", "GitHub Actions", "ArgoCD", "Prometheus", "Grafana"],
            "concepts": ["CI/CD", "Infrastructure as Code", "GitOps", "Service Mesh",
                        "Observability", "Chaos Engineering", "SRE", "Platform Engineering"],
            "challenges": ["scaling", "monitoring", "security", "cost optimization",
                          "deployment failures", "debugging", "performance tuning"],
            "trends": ["AI in DevOps", "FinOps", "Platform Engineering", "Green Computing",
                      "Edge Computing", "Serverless", "WebAssembly"]
        }
        self.hashtag_pool = [
            "#DevOps", "#Python", "#CloudComputing", "#Kubernetes", "#Docker",
            "#CI/CD", "#InfrastructureAsCode", "#SRE", "#PlatformEngineering",
            "#TechTips", "#CloudNative", "#Automation", "#DevOpsLife"
        ]
        logging.info("DevOpsContentGenerator initialized.")

    async def generate_content_ideas(self) -> Dict:
        content_types = list(ContentType)
        content_type = random.choice(content_types)
        logging.info(f"Generating content idea for type: {content_type.value}")
        idea = await self._create_content_idea(content_type)
        return idea

    async def _create_content_idea(self, content_type: ContentType) -> Dict:
        prompts = {
            ContentType.TECHNICAL_TIP: self._get_technical_tip_prompt(),
            ContentType.PROBLEM_SOLUTION: self._get_problem_solution_prompt(),
            ContentType.TOOL_DISCOVERY: self._get_tool_discovery_prompt(),
            ContentType.BEST_PRACTICE: self._get_best_practice_prompt(),
            ContentType.INDUSTRY_NEWS: self._get_industry_news_prompt(),
            ContentType.PERSONAL_INSIGHT: self._get_personal_insight_prompt()
        }
        prompt = prompts[content_type]
        content = await self._call_ai_api(prompt)
        logging.info(f"Content generated for {content_type.value}")
        return {
            "type": content_type.value,
            "content": content,
            "hashtags": self._select_hashtags(content_type),
            "generated_at": datetime.now().isoformat()
        }

    def _get_technical_tip_prompt(self) -> str:
        tool = random.choice(self.topics["tools"])
        return f"""Write a LinkedIn post about a useful {tool} tip or trick that DevOps engineers should know.
        Requirements:
        - Start with a hook that grabs attention
        - Provide practical, actionable advice
        - Include a brief code snippet or command if relevant
        - Keep it under 300 words
        - End with a question to encourage engagement
        - Write in first person, conversational tone
        - Don't include hashtags (they'll be added separately)
        Make it feel authentic and based on real experience."""

    def _get_problem_solution_prompt(self) -> str:
        challenge = random.choice(self.topics["challenges"])
        return f"""Write a LinkedIn post about solving a {challenge} challenge in DevOps.
        Requirements:
        - Start with the problem statement
        - Describe the impact of the problem
        - Present your solution approach
        - Share the outcome or results
        - Keep it under 300 words
        - Write in first person, sharing a real experience feel
        - Include emoji where appropriate for readability
        - Don't include hashtags"""

    def _get_tool_discovery_prompt(self) -> str:
        return f"""Write a LinkedIn post about discovering or trying a new DevOps tool or technology.
        Requirements:
        - Share excitement about the discovery
        - Explain what the tool does
        - Mention specific use cases
        - Compare briefly with alternatives if relevant
        - Keep it under 300 words
        - Write enthusiastically but authentically
        - Don't include hashtags"""

    def _get_best_practice_prompt(self) -> str:
        concept = random.choice(self.topics["concepts"])
        return f"""Write a LinkedIn post about a {concept} best practice.
        Requirements:
        - Share a specific best practice
        - Explain why it matters
        - Provide a real-world example
        - Mention common mistakes to avoid
        - Keep it under 300 words
        - Write in an educational but not preachy tone
        - Don't include hashtags"""

    def _get_industry_news_prompt(self) -> str:
        trend = random.choice(self.topics["trends"])
        return f"""Write a LinkedIn post sharing thoughts on {trend} in the DevOps space.
        Requirements:
        - Start with an observation or recent development
        - Share your perspective on why it matters
        - Discuss potential impact on the industry
        - Keep it under 300 words
        - Write thoughtfully and forward-looking
        - Don't include hashtags"""

    def _get_personal_insight_prompt(self) -> str:
        return f"""Write a LinkedIn post sharing a personal insight or lesson learned as a DevOps engineer.
        Requirements:
        - Share a genuine learning moment
        - Be vulnerable about mistakes or challenges
        - Explain what you learned
        - How it changed your approach
        - Keep it under 300 words
        - Write authentically and personally
        - Don't include hashtags"""

    async def _call_ai_api(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an experienced DevOps Engineer and Python Developer with deep expertise in cloud automation (AWS, Azure), \
                CI/CD pipeline development (Jenkins, GitHub Actions, ArgoCD), Infrastructure-as-Code (Terraform, AWS CDK), Kubernetes (EKS, Helm), and system monitoring \
                (Prometheus, ELK Stack). Your goal is to write engaging, insightful, and technically accurate LinkedIn posts that share industry best practices, real-world \
                 challenges, useful tips, and personal achievements in DevOps and Cloud Engineering. Posts should be professional yet approachable, concise, and inspire \
                 discussions. Target an audience of developers, DevOps engineers, and cloud architects."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 500
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=headers, json=payload, ssl=ssl_context) as response:
                result = await response.json()
                logging.info("OpenAI API called successfully.")
                return result["choices"][0]["message"]["content"]

    def _select_hashtags(self, content_type: ContentType, count: int = 5) -> List[str]:
        base_tags = ["#DevOps", "#Python"]
        type_tags = {
            ContentType.TECHNICAL_TIP: ["#TechTips", "#DevOpsTools"],
            ContentType.PROBLEM_SOLUTION: ["#ProblemSolving", "#Engineering"],
            ContentType.TOOL_DISCOVERY: ["#DevOpsTools", "#Technology"],
            ContentType.BEST_PRACTICE: ["#BestPractices", "#DevOpsLife"],
            ContentType.INDUSTRY_NEWS: ["#TechNews", "#FutureOfTech"],
            ContentType.PERSONAL_INSIGHT: ["#CareerGrowth", "#LearningInPublic"]
        }
        selected = base_tags + type_tags.get(content_type, [])
        remaining = count - len(selected)
        if remaining > 0:
            additional = random.sample(
                [t for t in self.hashtag_pool if t not in selected], 
                min(remaining, len(self.hashtag_pool))
            )
            selected.extend(additional)
        return selected[:count]

class ContentReviewer:
    def __init__(self):
        self.quality_checks = {
            "length": self._check_length,
            "engagement": self._check_engagement,
            "technical_accuracy": self._check_technical,
            "readability": self._check_readability
        }
        logging.info("ContentReviewer initialized.")

    def review_post(self, post: LinkedInPost) -> Dict:
        scores = {}
        issues = []
        for check_name, check_func in self.quality_checks.items():
            score, issue = check_func(post.content)
            scores[check_name] = score
            if issue:
                issues.append(issue)
        overall_score = sum(scores.values()) / len(scores)
        logging.info(f"Post reviewed. Overall score: {overall_score:.2f}")
        return {
            "scores": scores,
            "overall_score": overall_score,
            "issues": issues,
            "approved": overall_score >= 0.7
        }

    def _check_length(self, content: str) -> tuple:
        word_count = len(content.split())
        if word_count < 50:
            return (0.3, "Post is too short")
        elif word_count > 400:
            return (0.5, "Post might be too long")
        elif 100 <= word_count <= 300:
            return (1.0, None)
        else:
            return (0.8, None)

    def _check_engagement(self, content: str) -> tuple:
        has_question = "?" in content
        has_emoji = any(ord(char) > 127 for char in content)
        has_call_to_action = any(phrase in content.lower() for phrase in 
                                ["let me know", "what do you think", "share your", "comment below"])
        score = 0.3
        if has_question: score += 0.3
        if has_emoji: score += 0.2
        if has_call_to_action: score += 0.2
        issue = "Missing engagement elements" if score < 0.5 else None
        return (score, issue)

    def _check_technical(self, content: str) -> tuple:
        tech_terms = ["devops", "python", "cloud", "kubernetes", "docker", "ci/cd", 
                     "automation", "infrastructure", "deployment", "pipeline"]
        content_lower = content.lower()
        term_count = sum(1 for term in tech_terms if term in content_lower)
        if term_count == 0:
            return (0.2, "No technical terms found")
        elif term_count >= 3:
            return (1.0, None)
        else:
            return (0.6, None)

    def _check_readability(self, content: str) -> tuple:
        sentences = content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        if avg_sentence_length > 25:
            return (0.5, "Sentences might be too complex")
        elif avg_sentence_length < 5:
            return (0.5, "Sentences might be too simple")
        else:
            return (1.0, None)

class DevOpsContentWorkflow:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.generator = DevOpsContentGenerator(api_key=api_key, model=model)
        self.reviewer = ContentReviewer()
        self.console = Console()
        logging.info("DevOpsContentWorkflow initialized.")

    async def run(self):
        logging.info("Starting content generation workflow.")
        idea = await self.generator.generate_content_ideas()
        approved_posts = []
        temp_post = LinkedInPost(
            content=idea["content"],
            hashtags=idea["hashtags"],
            post_type=ContentType(idea["type"]),
            scheduled_time=datetime.now()
        )
        review = self.reviewer.review_post(temp_post)
        if review["approved"]:
            approved_posts.append(idea)
            logging.info(f"✅ Approved: {idea['type']} (score: {review['overall_score']:.2f})")
            self.console.print(Markdown(idea.get("content")))
        else:
            logging.warning(f"❌ Rejected: {idea['type']} - Issues: {review['issues']}")
        if approved_posts:
            text_to_post = approved_posts[0]['content'] + "\n\n" + " ".join(approved_posts[0]['hashtags'])
            logging.info("Post sent to LinkedIn automation.")
            return text_to_post
        return None