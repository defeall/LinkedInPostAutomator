import json
import logging
import random
import os
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict
from enum import Enum
import urllib3

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
    post_type: str
    scheduled_time: str
    status: str = "pending"

class DevOpsContentGenerator:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.model = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
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
            "#TechTips", "#CloudNative", "#Automation", "#DevOpsLife", "#AWS"
        ]

    def generate_content_ideas(self) -> Dict:
        content_types = list(ContentType)
        content_type = random.choice(content_types)
        logger.info(f"Generating content idea for type: {content_type.value}")
        idea = self._create_content_idea(content_type)
        return idea

    def _create_content_idea(self, content_type: ContentType) -> Dict:
        prompts = {
            ContentType.TECHNICAL_TIP: self._get_technical_tip_prompt(),
            ContentType.PROBLEM_SOLUTION: self._get_problem_solution_prompt(),
            ContentType.TOOL_DISCOVERY: self._get_tool_discovery_prompt(),
            ContentType.BEST_PRACTICE: self._get_best_practice_prompt(),
            ContentType.INDUSTRY_NEWS: self._get_industry_news_prompt(),
            ContentType.PERSONAL_INSIGHT: self._get_personal_insight_prompt()
        }
        prompt = prompts[content_type]
        content = self._call_openai_api(prompt)
        
        return {
            "type": content_type.value,
            "content": content,
            "hashtags": self._select_hashtags(content_type),
            "generated_at": datetime.now().isoformat()
        }

    def _call_openai_api(self, prompt: str) -> str:
        """Call OpenAI API using boto3 and Lambda layer or direct HTTP"""
        
        http = urllib3.PoolManager()
        
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
        
        try:
            response = http.request(
                'POST',
                'https://api.openai.com/v1/chat/completions',
                body=json.dumps(payload).encode('utf-8'),
                headers=headers
            )
            result = json.loads(response.data.decode('utf-8'))
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise

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

    def _select_hashtags(self, content_type: ContentType, count: int = 5) -> List[str]:
        base_tags = ["#DevOps", "#Python", "#AWS"]
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

    def review_post(self, post: LinkedInPost) -> Dict:
        scores = {}
        issues = []
        for check_name, check_func in self.quality_checks.items():
            score, issue = check_func(post.content)
            scores[check_name] = score
            if issue:
                issues.append(issue)
        overall_score = sum(scores.values()) / len(scores)
        
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
                     "automation", "infrastructure", "deployment", "pipeline", "aws", "lambda"]
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
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        if avg_sentence_length > 25:
            return (0.5, "Sentences might be too complex")
        elif avg_sentence_length < 5:
            return (0.5, "Sentences might be too simple")
        else:
            return (1.0, None)

def lambda_handler(event, context):
    """
    Main Lambda handler for content generation
    Can be triggered by EventBridge, API Gateway, or manual invocation
    """
    logger.info(f"Event received: {json.dumps(event)}")
    
    try:
        # Initialize components
        generator = DevOpsContentGenerator()
        reviewer = ContentReviewer()
        
        # Generate content
        idea = generator.generate_content_ideas()
        
        # Create post object for review
        post = LinkedInPost(
            content=idea["content"],
            hashtags=idea["hashtags"],
            post_type=idea["type"],
            scheduled_time=datetime.now().isoformat()
        )
        
        # Review the post
        review = reviewer.review_post(post)
        
        if review["approved"]:
            # Combine content with hashtags
            full_content = f"{idea['content']}\n\n{' '.join(idea['hashtags'])}"
            
            return {
                'statusCode': 200,
                'body': full_content
                # 'body': json.dumps({
                #     'message': 'Content generated and approved',
                #     'type': idea['type'],
                #     'score': review['overall_score'],
                #     'post': full_content
                # })
            }
        else:
            # Log rejected post
            logger.warning(f"Post rejected - Issues: {review['issues']}")
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Content generated but not approved',
                    'issues': review['issues'],
                    'score': review['overall_score']
                })
            }
            
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }