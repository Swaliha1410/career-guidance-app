"""
Validators for Career Guidance Application
Backend validation logic: mandatory fields, password, age, and email domain checks.
All functions return tuple (is_valid: bool, message: str).
"""
import re
from typing import Tuple, Dict


ALLOWED_EMAIL_DOMAINS = ("gmail.com", "yahoo.com", "rediffmail.com")


def is_non_empty_fields(fields: Dict[str, object]) -> Tuple[bool, str]:
    """Ensure all provided fields are not empty or None."""
    for name, value in fields.items():
        if value is None:
            return False, "All fields are required. Please fill in all details."
        if isinstance(value, str) and value.strip() == "":
            return False, "All fields are required. Please fill in all details."
    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password length (minimum 6 characters)."""
    if not isinstance(password, str):
        return False, "Password must be a valid string."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format and allowed domains."""
    if not isinstance(email, str) or not email:
        return False, "Please enter a valid email address (Gmail, Yahoo, or Rediffmail only)."

    email = email.strip()
    # basic email regex (not exhaustive but practical)
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Please enter a valid email address (Gmail, Yahoo, or Rediffmail only)."

    domain = email.split("@")[-1].lower()
    if domain not in ALLOWED_EMAIL_DOMAINS:
        return False, "Please enter a valid email address (Gmail, Yahoo, or Rediffmail only)."

    return True, ""


def validate_age_for_level(age: int, academic_level: str) -> Tuple[bool, str]:
    """Validate age according to academic level rules.

    - 10th grade: age must be 15 or above
    - 12th grade: age must be 17 or above
    """
    try:
        age_val = int(age)
    except Exception:
        return False, "Please enter a valid age for the selected academic level."

    if academic_level == "10th":
        if age_val < 15:
            return False, "Please enter a valid age for the selected academic level."
    elif academic_level == "12th":
        if age_val < 17:
            return False, "Please enter a valid age for the selected academic level."
    else:
        return False, "Please enter a valid academic level."

    return True, ""


def validate_signup(full_name: str, username: str, email: str, password: str, age: int, academic_level: str) -> Tuple[bool, str]:
    """Run all signup validations and return consolidated result."""
    # Mandatory fields
    ok, msg = is_non_empty_fields({
        "full_name": full_name,
        "username": username,
        "email": email,
        "password": password,
        "age": age,
        "academic_level": academic_level,
    })
    if not ok:
        return False, msg

    # Password
    ok, msg = validate_password(password)
    if not ok:
        return False, msg

    # Email
    ok, msg = validate_email(email)
    if not ok:
        return False, msg

    # Age vs academic level
    ok, msg = validate_age_for_level(age, academic_level)
    if not ok:
        return False, msg

    return True, ""


def validate_login(username: str, password: str) -> Tuple[bool, str]:
    """Validate login inputs are present (backend decision)."""
    ok, msg = is_non_empty_fields({"username": username, "password": password})
    if not ok:
        return False, msg
    return True, ""
