#!/usr/bin/
"""Manages API authentication."""

from Flask import 
from typing import List, TypeVar

class Auth:
    """Handles API authentication."""

    def require_auth(self, path: str, exluded_paths: List[str]) -> bool:
        """doc"""
        return False
    
    def authorization_header(self, request=None) -> str:
        """doc"""
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """doc"""
        return None