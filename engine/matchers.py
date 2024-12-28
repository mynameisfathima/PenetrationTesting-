import re
from typing import Any, Dict, List
from requests import Response


def run_matchers(response: Response, matchers_config: List[Dict[str, Any]]) -> bool:
    """
    Given a list of matchers from a template, checks the response
    to see if any or all matchers pass (the logic can be extended).
    For simplicity, we do an 'all' match logic (all must pass).
    """
    for matcher in matchers_config:
        matcher_type = matcher.get("type")
        if matcher_type == "regex":
            if not regex_match(response, matcher):
                return False
        elif matcher_type == "word":
            if not word_match(response, matcher):
                return False
        elif matcher_type == "status":
            if not status_match(response, matcher):
                return False
        elif matcher_type == "method":
            if not method_match(response, matcher):
                return False
        elif matcher_type == "redirect":
            if not redirect_match(response, matcher):
                return False
        elif matcher_type == "subdomain":
            if not subdomain_match(response, matcher):
                return False
        elif matcher_type == "cookie":
            if not cookie_match(response, matcher):
                return False
        elif matcher_type == "time":
            if not time_match(response, matcher):
                return False
    return True


def regex_match(response: Response, matcher: Dict[str, Any]) -> bool:
    """
    Checks if the response body matches a given regex pattern.
    """
    pattern = matcher.get("pattern")
    if not pattern:
        return False
    return bool(re.search(pattern, response.text))

def word_match(response: Response, matcher: Dict[str, Any]) -> bool:
    """
    Checks if th respose body contains the word
    """
    word_to_search = matcher.get("word")
    if not word_to_search:
        return False
    pool_of_response_text = response.text
    return bool(pool_of_response_text.find(word_to_search) > 0) # returns false if not found, ie, returns -1


def status_match(response: Response, matcher: Dict[str, Any]) -> bool:
    """
    Checks if the response status code is in the expected list.
    """
    statuses = matcher.get("status", [])
    return response.status_code in statuses

def method_match(response: Response, matcher: Dict[str, Any]) -> bool:
    expected_method = matcher.get("method")
    return response.request.method.lower() == expected_method.lower()

def redirect_match(response: Response, matcher: Dict[str, Any]) -> bool:
    expected_redirect_url = matcher.get("redirect_url")
    return response.is_redirect and response.headers.get("Location") == expected_redirect_url

from urllib.parse import urlparse

def subdomain_match(response: Response, matcher: Dict[str, Any]) -> bool:
    subdomain_to_match = matcher.get("subdomain")
    if not subdomain_to_match:
        return False
    subdomain = urlparse(response.url).hostname.split('.')[0]
    return subdomain == subdomain_to_match

def cookie_match(response: Response, matcher: Dict[str, Any]) -> bool:
    cookies_to_match = matcher.get("cookies", {})
    for cookie, expected_value in cookies_to_match.items():
        if response.cookies.get(cookie) != expected_value:
            return False
    return True

def time_match(response: Response, matcher: Dict[str, Any]) -> bool:
    response_time = matcher.get("time")
    if response_time is None:
        return True  # No time constraint
    return response.elapsed.total_seconds() <= response_time

