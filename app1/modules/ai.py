"""
AI Module - Claude + GPT-4 Integration
Features:
- Real-time data validation
- Web research capability
- Self-improvement (log monitoring and suggestions)
"""
import json
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp


class AIManager:
    """Manages AI operations using Claude and GPT-4"""

    def __init__(self):
        # API keys (loaded from environment or config)
        self.anthropic_key = "your-anthropic-api-key"
        self.openai_key = "your-openai-api-key"

        # API endpoints
        self.claude_api = "https://api.anthropic.com/v1/messages"
        self.openai_api = "https://api.openai.com/v1/chat/completions"

        # Models
        self.claude_model = "claude-3-5-sonnet-20241022"
        self.gpt_model = "gpt-4o"

        # Self-improvement settings
        self.improvement_suggestions = []
        self.log_file = "data/ai_logs.json"

    async def query_claude(self, prompt: str, context: Optional[str] = None) -> Dict:
        """
        Query Claude AI
        """
        try:
            headers = {
                "x-api-key": self.anthropic_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }

            messages = [{"role": "user", "content": prompt}]
            if context:
                messages.insert(0, {"role": "user", "content": f"Context: {context}"})

            payload = {
                "model": self.claude_model,
                "max_tokens": 1024,
                "messages": messages
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.claude_api,
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'success': True,
                            'response': data['content'][0]['text'],
                            'model': 'claude'
                        }
                    else:
                        return {
                            'success': False,
                            'error': f"API error: {response.status}"
                        }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def query_gpt4(self, prompt: str, context: Optional[str] = None) -> Dict:
        """
        Query GPT-4
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.openai_key}",
                "Content-Type": "application/json"
            }

            messages = [{"role": "user", "content": prompt}]
            if context:
                messages.insert(0, {"role": "system", "content": context})

            payload = {
                "model": self.gpt_model,
                "messages": messages,
                "max_tokens": 1024
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.openai_api,
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'success': True,
                            'response': data['choices'][0]['message']['content'],
                            'model': 'gpt-4'
                        }
                    else:
                        return {
                            'success': False,
                            'error': f"API error: {response.status}"
                        }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def validate_data(self, data: Dict, validation_rules: str) -> Dict:
        """
        Real-time data validation using AI
        """
        prompt = f"""
        Validate the following data according to these rules:
        {validation_rules}

        Data to validate:
        {json.dumps(data, indent=2)}

        Return a JSON response with:
        - valid: boolean
        - errors: list of error messages
        - warnings: list of warnings
        """

        result = await self.query_claude(prompt)
        if result['success']:
            try:
                validation = json.loads(result['response'])
                return validation
            except json.JSONDecodeError:
                return {
                    'valid': False,
                    'errors': ['Failed to parse validation response'],
                    'warnings': []
                }
        return {
            'valid': False,
            'errors': [result.get('error', 'Validation failed')],
            'warnings': []
        }

    async def web_research(self, query: str) -> Dict:
        """
        Perform web research using AI
        """
        prompt = f"""
        Research the following query and provide comprehensive information:
        {query}

        Include:
        - Key findings
        - Relevant facts
        - Sources (if known)
        - Summary
        """

        # Use GPT-4 for web research
        result = await self.query_gpt4(prompt)
        return result

    async def analyze_logs(self, log_file: str) -> List[Dict]:
        """
        Analyze logs and suggest improvements
        """
        try:
            with open(log_file, 'r') as f:
                logs = f.read()

            prompt = f"""
            Analyze these application logs and suggest improvements:

            {logs[-10000:]}  # Last 10KB of logs

            Provide suggestions for:
            - Performance improvements
            - Error handling
            - User experience enhancements
            - Security improvements

            Return as JSON array of suggestions.
            """

            result = await self.query_claude(prompt)
            if result['success']:
                try:
                    suggestions = json.loads(result['response'])
                    self.improvement_suggestions = suggestions
                    return suggestions
                except json.JSONDecodeError:
                    return []
            return []

        except Exception as e:
            print(f"Log analysis error: {e}")
            return []

    def get_improvement_suggestions(self) -> List[Dict]:
        """Get pending improvement suggestions"""
        return self.improvement_suggestions

    async def apply_suggestion(self, suggestion_id: int, approved: bool) -> Dict:
        """
        Apply or reject an improvement suggestion
        Requires admin approval
        """
        if suggestion_id >= len(self.improvement_suggestions):
            return {'success': False, 'error': 'Invalid suggestion ID'}

        suggestion = self.improvement_suggestions[suggestion_id]

        if approved:
            # Log the approval
            self.log_improvement(suggestion, approved=True)
            return {
                'success': True,
                'message': 'Suggestion approved and logged for implementation'
            }
        else:
            # Log the rejection
            self.log_improvement(suggestion, approved=False)
            return {
                'success': True,
                'message': 'Suggestion rejected'
            }

    def log_improvement(self, suggestion: Dict, approved: bool):
        """Log improvement suggestion and approval status"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'suggestion': suggestion,
            'approved': approved
        }

        try:
            # Load existing logs
            try:
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                logs = []

            # Add new entry
            logs.append(log_entry)

            # Save logs
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)

        except Exception as e:
            print(f"Failed to log improvement: {e}")

    def query(self, prompt: str, use_claude: bool = True) -> Dict:
        """
        Synchronous wrapper for AI queries
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if use_claude:
            result = loop.run_until_complete(self.query_claude(prompt))
        else:
            result = loop.run_until_complete(self.query_gpt4(prompt))

        loop.close()
        return result
