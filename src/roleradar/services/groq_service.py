"""Groq service for entity extraction, scoring, and analysis."""

import json
import os
from typing import Dict, Any, List
from groq import Groq
from ..config import config


DEFAULT_ENTITY_EXTRACTION_PROMPT = """Analyze the following text and extract structured information about job opportunities in security, compliance, or GRC roles.

Extract:
- company_name: Name of the company (if mentioned)
- job_title: Job title or role
- role_type: Classify as "security", "compliance", or "GRC"
- location: Job location
- keywords: List of relevant keywords (e.g., "CISO", "data protection", "risk management")

Text: {text}

Return ONLY a valid JSON object with these fields. If a field is not found, use null.
"""

DEFAULT_HIRING_SIGNALS_PROMPT = """Analyze the following text about {company_name} and identify hiring signals that suggest they may need security or compliance leadership.

Look for signals like:
- Company expansion or growth
- Recent funding rounds
- Security breaches or incidents
- New compliance requirements
- Regulatory changes affecting the company
- Product launches requiring security expertise

Text: {text}

Return ONLY a valid JSON object with:
- has_signal: boolean indicating if hiring signals were detected
- signal_type: one of ["expansion", "funding", "breach", "compliance_news", "regulatory", "product_launch", "none"]
- confidence: float between 0 and 1
- description: brief description of the signal

Return valid JSON only.
"""

# Not currently used in processing, but exposed so the admin UI can view/update it alongside other prompts.
DEFAULT_GROWTH_DETECTION_PROMPT = """Review the following text and identify any indicators of company growth or expansion (new markets, hiring plans, product launches, funding, major partnerships). Summarize the growth signal in one sentence and return concise JSON.

Text: {text}
"""


MAX_INPUT_CHARS = int(os.getenv("GROQ_MAX_INPUT_CHARS", "4000"))


def get_prompt_templates() -> Dict[str, str]:
    """Return the active prompt templates (config overrides or defaults)."""
    return {
        "entity_extraction": getattr(config, "ENTITY_EXTRACTION_PROMPT", DEFAULT_ENTITY_EXTRACTION_PROMPT) or DEFAULT_ENTITY_EXTRACTION_PROMPT,
        "hiring_signals": getattr(config, "HIRING_SIGNALS_PROMPT", DEFAULT_HIRING_SIGNALS_PROMPT) or DEFAULT_HIRING_SIGNALS_PROMPT,
        "growth_detection": getattr(config, "GROWTH_DETECTION_PROMPT", DEFAULT_GROWTH_DETECTION_PROMPT) or DEFAULT_GROWTH_DETECTION_PROMPT,
    }


def _first_dict(obj: Any) -> Dict[str, Any]:
    """Return the first dict found from obj (dict, list-of-dicts), else empty dict."""
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict):
                return item
    return {}


def _string_or_first(value: Any) -> Any:
    """Return a string-safe scalar from potentially nested/iterable values."""
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                return item
            return str(item)
        return None
    if isinstance(value, dict):
        return str(value)
    if value is None:
        return None
    return str(value)


def _coerce_entities(raw: Any) -> Dict[str, Any]:
    """Normalize parsed JSON into the expected entities shape."""
    data = _first_dict(raw)

    # Accept a few common alternate keys from models
    company = _string_or_first(data.get("company_name") or data.get("company") or data.get("org"))
    job_title = _string_or_first(data.get("job_title") or data.get("title") or data.get("role"))
    role_type = _string_or_first(data.get("role_type") or data.get("type"))
    location = _string_or_first(data.get("location") or data.get("city") or data.get("region"))
    keywords = data.get("keywords") or data.get("tags") or []

    if isinstance(keywords, str):
        keywords = [kw.strip() for kw in keywords.split(",") if kw.strip()]
    if not isinstance(keywords, list):
        keywords = []

    return {
        "company_name": company,
        "job_title": job_title,
        "role_type": role_type,
        "location": location,
        "keywords": keywords,
    }


def _coerce_signals(raw: Any) -> Dict[str, Any]:
    """Normalize parsed JSON into the expected hiring signals shape."""
    data = _first_dict(raw)

    has_signal = bool(data.get("has_signal"))
    signal_type = _string_or_first(data.get("signal_type") or data.get("type") or "none")
    description = _string_or_first(data.get("description") or data.get("details") or "")
    confidence = data.get("confidence", 0.0)

    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.0

    return {
        "has_signal": has_signal,
        "signal_type": signal_type,
        "confidence": confidence,
        "description": description,
    }


def _prepare_text(text: str) -> str:
    """Trim input text to stay within model-friendly context limits."""
    if not text:
        return ""
    if len(text) <= MAX_INPUT_CHARS:
        return text
    return text[:MAX_INPUT_CHARS] + "\n[truncated]"


class GroqAnalysisService:
    """Service for analyzing search results using Groq API."""
    
    def __init__(self, api_key=None):
        """Initialize Groq analysis service."""
        self.api_key = api_key or config.GROQ_API_KEY
        self.client = None
        if not self.api_key:
            print("Warning: Groq API key not configured. Analysis functionality will be limited.")
        else:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                # Fail-safe: run without Groq client so the app can boot and be configured via Admin UI
                print(f"Warning: Groq client initialization failed: {e}. Running without Groq.")
                self.client = None
        # Model zoo: Prioritized fallback chain of available models
        # Order: best → fast → alternatives
        self.model_chain: List[str] = [
            "llama-3.3-70b-versatile",           # Primary: Most capable
            "meta-llama/llama-4-scout-17b-16e-instruct",  # New Llama 4 model
            "llama-3.1-8b-instant",              # Fast fallback
            "groq/compound",                     # Alternative compound model
            "qwen/qwen3-32b",                    # International alternative
        ]
        self.model = self.model_chain[0]
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extract entities from text including companies, job titles, and locations.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with extracted entities
        """
        if not self.client:
            print("Warning: Groq client not initialized. Returning empty entities.")
            return {
                "company_name": None,
                "job_title": None,
                "role_type": None,
                "location": None,
                "keywords": []
            }
        
        prompt_template = get_prompt_templates()["entity_extraction"]
        prompt = prompt_template.format(text=_prepare_text(text))
        
        def _call_model(model_name: str):
            return self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that extracts structured data from job postings and returns valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=model_name,
                temperature=0.1,
                max_tokens=500
            )

        response = None
        last_error = None
        for candidate in self.model_chain:
            try:
                response = _call_model(candidate)
                self.model = candidate  # remember which worked
                break
            except Exception as e:
                last_error = e
                # try next model in chain
                continue

        if response is None:
            # Track failed API call
            from .api_tracker import APITracker
            APITracker.log_api_call(
                api_name='groq',
                endpoint='extract_entities',
                query=text[:100] if text else None,
                error=str(last_error) if last_error else "No model available"
            )
            raise last_error or Exception("No Groq model could be used")

        try:
            result_text = response.choices[0].message.content.strip()
            # Try to extract JSON from the response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            raw = json.loads(result_text)
            entities = _coerce_entities(raw)

            # Track successful API call
            from .api_tracker import APITracker
            APITracker.log_api_call(
                api_name='groq',
                endpoint='extract_entities',
                query=text[:100] if text else None
            )

            return entities
        except Exception as e:
            # Track failed extraction
            from .api_tracker import APITracker
            APITracker.log_api_call(
                api_name='groq',
                endpoint='extract_entities',
                query=text[:100] if text else None,
                error=str(e)
            )
            print(f"Error extracting entities: {e}")
            return {
                "company_name": None,
                "job_title": None,
                "role_type": None,
                "location": None,
                "keywords": []
            }
    
    def detect_hiring_signals(self, text: str, company_name: str) -> Dict[str, Any]:
        """
        Detect hiring signals from text about a company.
        
        Args:
            text: Text to analyze
            company_name: Name of the company
            
        Returns:
            Dictionary with hiring signals
        """
        if not self.client:
            return {
                "has_signal": False,
                "signal_type": "none",
                "confidence": 0.0,
                "description": ""
            }
        
        prompt_template = get_prompt_templates()["hiring_signals"]
        prompt = prompt_template.format(text=_prepare_text(text), company_name=company_name)
        
        def _call_model(model_name: str):
            return self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that analyzes company news for hiring signals and returns valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=model_name,
                temperature=0.2,
                max_tokens=300
            )

        response = None
        last_error = None
        for candidate in self.model_chain:
            try:
                response = _call_model(candidate)
                self.model = candidate
                break
            except Exception as e:
                last_error = e
                continue

        if response is None:
            # Track failed API call
            from .api_tracker import APITracker
            APITracker.log_api_call(
                api_name='groq',
                endpoint='detect_hiring_signals',
                query=company_name[:100] if company_name else None,
                error=str(last_error) if last_error else "No model available"
            )
            raise last_error or Exception("No Groq model could be used")

        try:
            result_text = response.choices[0].message.content.strip()

            # Try to extract JSON from the response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            raw = json.loads(result_text)
            signals = _coerce_signals(raw)

            # Track successful API call
            from .api_tracker import APITracker
            APITracker.log_api_call(
                api_name='groq',
                endpoint='detect_hiring_signals',
                query=company_name[:100] if company_name else None
            )

            return signals
        except Exception as e:
            # Track failed signal detection
            from .api_tracker import APITracker
            APITracker.log_api_call(
                api_name='groq',
                endpoint='detect_hiring_signals',
                query=company_name[:100] if company_name else None,
                error=str(e)
            )
            print(f"Error detecting hiring signals: {e}")
            return {
                "has_signal": False,
                "signal_type": "none",
                "confidence": 0.0,
                "description": ""
            }
    
    def score_company(self, company_data: Dict[str, Any]) -> float:
        """
        Score a company based on job postings and hiring signals.
        
        Args:
            company_data: Dictionary with company information including opportunities and signals
            
        Returns:
            Score between 0 and 100
        """
        score = 0.0
        weights = config.SCORING_WEIGHTS
        
        # Explicit job postings (weight: 0.4)
        num_active_jobs = company_data.get("active_opportunities", 0)
        if num_active_jobs > 0:
            score += min(num_active_jobs * 10, 40) * weights["explicit_job_posting"]
        
        # Hiring signals (weight: 0.3)
        signals = company_data.get("signals", [])
        if signals:
            avg_confidence = sum(s.get("confidence", 0) for s in signals) / len(signals)
            score += avg_confidence * 100 * weights["hiring_signals"]
        
        # Company growth indicators (weight: 0.2)
        if company_data.get("has_funding", False) or company_data.get("has_expansion", False):
            score += 50 * weights["company_growth"]
        
        # Recent activity (weight: 0.1)
        if company_data.get("recent_activity", False):
            score += 100 * weights["recent_activity"]
        
        return min(score, 100.0)
    
    def summarize_results(self, results: List[Dict[str, Any]], max_results: int = 10) -> str:
        """
        Summarize search results into a readable format.
        
        Args:
            results: List of search results with companies and opportunities
            max_results: Maximum number of results to include
            
        Returns:
            Formatted summary text
        """
        if not results:
            return "No results to summarize."
        
        if not self.client:
            return f"Found {len(results)} companies with opportunities. Configure Groq API key for detailed summaries."
        
        # Prepare summary data
        summary_items = []
        for result in results[:max_results]:
            # Support both formats: 'name' or 'company_name', 'active_opportunities' or 'opportunity_count'
            company_name = result.get('company_name') or result.get('name', 'Unknown')
            opp_count = result.get('opportunity_count') or result.get('active_opportunities', 0)
            score = result.get('score', 0)
            summary_items.append(f"- {company_name}: {opp_count} opportunities, score: {score:.1f}")
        
        summary_text = "\n".join(summary_items)
        
        prompt = f"""Create a brief executive summary of the following security, compliance, and GRC opportunities:

{summary_text}

Provide a 2-3 sentence summary highlighting:
1. The total number of opportunities found
2. Top companies or trends
3. Key insights for job seekers in security/compliance roles

Keep it concise and actionable.
"""
        
        def _call_model(model_name: str):
            return self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that creates concise executive summaries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=model_name,
                temperature=0.3,
                max_tokens=200
            )

        response = None
        last_error = None
        for candidate in self.model_chain:
            try:
                response = _call_model(candidate)
                self.model = candidate
                break
            except Exception as e:
                last_error = e
                continue

        if response is None:
            raise last_error or Exception("No Groq model could be used")

        try:
            summary = response.choices[0].message.content.strip()
            return summary
        except Exception as e:
            print(f"Error creating summary: {e}")
            return f"Found {len(results)} companies with opportunities."
