import requests
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

class NewsAPIService:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.ai/api/v1"
        
        if not self.api_key:
            print("WARNING: NEWS_API_KEY not found. Using mock data for news service.")
            print("To enable real news data:")
            print("1. Sign up at https://newsapi.ai/")
            print("2. Get your API key from your account dashboard")
            print("3. Add NEWS_API_KEY=your_key_here to your .env file")
    
    def search_news(self, 
                   query: str, 
                   company_name: str = None,
                   risk_type: str = None,
                   days_back: int = 30) -> Dict:
        """
        Search for relevant news articles using NewsAPI.ai
        
        Args:
            query: Main search query
            company_name: Company name for additional context
            risk_type: Type of risk (regulatory, operational, etc.)
            days_back: Number of days to look back for news
            
        Returns:
            Dictionary containing news articles and metadata
        """
        
        # If no API key, return mock data
        if not self.api_key:
            return self._get_mock_news_data(query, company_name, risk_type)
        
        # Hard code news keywords
        keywords = ["oil, gas, iran"]
        
        # Prepare API request for NewsAPI.ai
        payload = {
            "action": "getArticles",
            "keyword": keywords,
            # "sourceLocationUri": [
            #     "http://en.wikipedia.org/wiki/United_States",
            #     "http://en.wikipedia.org/wiki/Canada",
            #     "http://en.wikipedia.org/wiki/United_Kingdom"
            # ],
            "ignoreSourceGroupUri": "paywall/paywalled_sources",
            "articlesPage": 1,
            "articlesCount": 20,
            "articlesSortBy": "date",
            "articlesSortByAsc": False,
            "dateStart": "2025-05-01",
            "dataType": [
                "news",
                "pr"
            ],
            "forceMaxDataTimeWindow": days_back,
            "resultType": "articles",
            "apiKey": self.api_key
        }
        
        try:
            print(f"Attempting to fetch news for keyword: {keywords}")
            response = requests.post(
                f"{self.base_url}/article/getArticles",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"API returned status {response.status_code}: {response.text}")
                return self._get_mock_news_data(query, company_name, risk_type)
            
            response.raise_for_status()
            return self._process_news_response(response.json(), query, company_name)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            print("Falling back to mock data for development/testing")
            return self._get_mock_news_data(query, company_name, risk_type)
    
    def _get_mock_news_data(self, query: str, company_name: str, risk_type: str) -> Dict:
        """
        Return mock news data for development/testing when API is unavailable
        """
        company_display = company_name or "the company"
        risk_display = risk_type or "business"
        
        mock_articles = [
            {
                "title": f"Regulatory Update: New {risk_display} requirements affecting {company_display}",
                "description": f"Recent developments in {risk_display} regulations may impact {company_display}'s operations and compliance requirements.",
                "content": f"Industry experts are monitoring the evolving {risk_display} landscape and its potential impact on companies like {company_display}. The regulatory environment continues to change rapidly, requiring businesses to stay vigilant about compliance requirements and potential risks.",
                "url": "https://example.com/mock-article-1",
                "source": "Business News Daily",
                "published_date": "2024-01-15T10:00:00Z",
                "relevance_score": 0.85,
                "sentiment": "neutral"
            },
            {
                "title": f"{company_display} faces {risk_display} challenges in current market",
                "description": f"Analysis of how {company_display} is navigating {risk_display} related challenges in the current business environment.",
                "content": f"The {risk_display} landscape continues to evolve, presenting both challenges and opportunities for companies like {company_display}. Market analysts suggest that proactive risk management strategies are becoming increasingly important in today's volatile business climate.",
                "url": "https://example.com/mock-article-2",
                "source": "Financial Times",
                "published_date": "2024-01-14T15:30:00Z",
                "relevance_score": 0.78,
                "sentiment": "positive"
            },
            {
                "title": f"Industry trends: {risk_display} considerations for modern businesses",
                "description": f"Comprehensive analysis of {risk_display} factors affecting businesses across various sectors.",
                "content": f"As businesses navigate an increasingly complex regulatory and operational environment, understanding {risk_display} factors has become crucial for long-term success. Companies must develop robust risk management frameworks to address these challenges effectively.",
                "url": "https://example.com/mock-article-3",
                "source": "Industry Weekly",
                "published_date": "2024-01-13T09:15:00Z",
                "relevance_score": 0.72,
                "sentiment": "neutral"
            }
        ]
        
        return {
            "articles": mock_articles,
            "total_results": len(mock_articles),
            "query": query,
            "company_name": company_name,
            "search_metadata": {
                "api_version": "v1",
                "timestamp": "2024-01-15T12:00:00Z",
                "status": "mock_data",
                "note": "Using mock data due to API authentication issues. Please check your NEWS_API_KEY configuration."
            }
        }
    
    def _process_news_response(self, response: Dict, query: str, company_name: str) -> Dict:
        """
        Process and format the NewsAPI.ai response
        """
        articles = response.get("articles", {}).get("results", [])
        
        processed_articles = []
        for article in articles:
            processed_articles.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "content": article.get("body", ""),
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("title", ""),
                "published_date": article.get("dateTime", ""),
                "sentiment": article.get("sentiment", "neutral")
            })
        
        return {
            "articles": processed_articles,
            "total_results": len(processed_articles),
            "query": query,
            "company_name": company_name,
            "search_metadata": {
                "api_version": "v1",
                "timestamp": response.get("timestamp", ""),
                "status": "success"
            }
        }
    
    def get_company_specific_news(self, company_name: str, days_back: int = 30) -> Dict:
        """
        Get news specifically about a company
        """
        return self.search_news(
            query=company_name,
            company_name=company_name,
            days_back=days_back
        )
    
    def get_risk_specific_news(self, risk_description: str, risk_type: str, company_name: str = None) -> Dict:
        """
        Get news related to a specific risk scenario
        """
        # Use company name if provided, otherwise use risk description
        keyword = company_name if company_name else risk_description[:50]  # Limit to first 50 chars
        
        return self.search_news(
            query=risk_description,
            company_name=company_name,
            risk_type=risk_type,
            days_back=30
        ) 