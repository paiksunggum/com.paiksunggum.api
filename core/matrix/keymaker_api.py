"""Backward-compatible import path for secret_manager."""

from core.matrix.secret_manager import Keymaker, get_keymaker, reset_keymaker_for_tests

__all__ = ["Keymaker", "get_keymaker", "reset_keymaker_for_tests"]
