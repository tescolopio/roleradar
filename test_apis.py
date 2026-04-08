#!/usr/bin/env python3
"""Quick test script to verify Tavily and Groq API connections."""

import sys
from src.roleradar.config import config
from src.roleradar.services import TavilySearchService, BraveSearchService, GroqAnalysisService

def test_search_service():
    """Test Search API connection."""
    print("Testing Search API connection...")
    
    if getattr(config, 'TAVILY_API_KEY', None):
        print(f"  Using Tavily API Key: {config.TAVILY_API_KEY[:10]}...{config.TAVILY_API_KEY[-5:]}")
        try:
            tavily = TavilySearchService()
            if not tavily.client:
                print("  ❌ Tavily client not initialized")
                return False

            results = tavily.search("security engineer job", max_results=2)
            if results:
                print(f"  ✅ Tavily API working! Found {len(results)} results")
                return True
            else:
                print("  ⚠️  Tavily API returned no results")
                return False
        except Exception as e:
            print(f"  ❌ Tavily API error: {e}")
            return False
            
    elif getattr(config, 'BRAVE_API_KEY', None):
        print(f"  Using Brave API Key: {config.BRAVE_API_KEY[:10]}...{config.BRAVE_API_KEY[-5:]}")
        try:
            brave = BraveSearchService()
            if not brave.client:
                print("  ❌ Brave client not initialized")
                return False

            results = brave.search("security engineer job", max_results=2)
            if results:
                print(f"  ✅ Brave API working! Found {len(results)} results")
                return True
            else:
                print("  ⚠️  Brave API returned no results")
                return False
        except Exception as e:
            print(f"  ❌ Brave API error: {e}")
            return False
            
    else:
        print("  ❌ No Search API Key configured (Tavily or Brave)")
        return False

def test_groq():
    """Test Groq API connection."""
    print("\nTesting Groq API connection...")
    print(f"  API Key: {config.GROQ_API_KEY[:10]}...{config.GROQ_API_KEY[-5:]}")

    try:
        groq = GroqAnalysisService()
        if not groq.client:
            print("  ❌ Groq client not initialized")
            return False

        # Try a simple entity extraction
        test_text = "Google is hiring a Senior Security Engineer in Mountain View, CA."
        entities = groq.extract_entities(test_text)

        if entities.get("company_name"):
            print(f"  ✅ Groq API working! Extracted company: {entities['company_name']}")
            print(f"     Job title: {entities.get('job_title')}")
            print(f"     Model: {groq.model}")
            return True
        else:
            print("  ⚠️  Groq API returned incomplete results")
            return False
    except Exception as e:
        print(f"  ❌ Groq API error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("RoleRadar API Connection Test")
    print("=" * 60)

    search_ok = test_search_service()
    groq_ok = test_groq()

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Search API: {'✅ Working' if search_ok else '❌ Failed'}")
    print(f"  Groq API:   {'✅ Working' if groq_ok else '❌ Failed'}")
    print("=" * 60)

    sys.exit(0 if (search_ok and groq_ok) else 1)
