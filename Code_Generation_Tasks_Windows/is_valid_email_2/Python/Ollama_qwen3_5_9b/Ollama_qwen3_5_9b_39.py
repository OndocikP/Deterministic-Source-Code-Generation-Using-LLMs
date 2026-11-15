def is_valid_email(email):
    """
    Validates an email address based on structural rules without DNS lookups.

    Returns True if the email is structurally valid, False otherwise.
    Handles non-string inputs, empty strings, whitespace issues, and format errors.
    Uses only Python standard library (regex).
    """
    import re

    # Requirement 4: If input is not a string (including None), return False
    if not isinstance(email, str):
        return False

    # Requirement 5: Reject empty strings or those with leading/trailing whitespace
    if email == "" or email != email.strip():
        return False

    # Requirement 8: Reject spaces or control characters anywhere
    if any(c.isspace() or ord(c) < 32 for c in email):
        return False

    # Basic structure check: must contain exactly one @
    at_count = email.count('@')
    if at_count != 1:
        return False

    local_part, domain = email.split('@')

    # Requirement 6 & 7: Validate local part
    # No consecutive dots, no starting or ending with dot (implied by RFC), no spaces
    # We already checked spaces. Check for consecutive dots and start/end dots.
    if local_part.startswith('.') or local_part.endswith('.'):
        return False
    if '..' in local_part:
        return False

    # Local part should not be empty
    if len(local_part) == 0:
        return False

    # Requirement 6 & 7: Validate domain
    parts = domain.split('.')
    
    # Must have at least two parts (domain.tld)
    if len(parts) < 2:
        return False

    for part in parts:
        # Domain labels cannot be empty
        if len(part) == 0:
            return False
        
        # Labels should not start or end with hyphen
        if part.startswith('-') or part.endswith('-'):
            return False
            
        # Length check (optional but good practice, keeping simple here)
        # RFC allows up to 63 chars per label and total domain length limits.
        # We will assume standard length constraints for robustness without complex regex.
        
    # Additional structural checks for the whole email using regex for common patterns
    # This covers things like invalid characters in local part beyond our manual checks
    # A simple heuristic: local part shouldn't contain unescaped special chars that break logic
    # However, strict RFC 5322 parsing is complex. We'll stick to explicit rules + basic regex for safety.
    
    # Check for allowed characters in local part roughly (alphanumeric and some symbols)
    # But since we already checked dots and spaces, let's ensure no other wildcards like newlines exist (already covered by control chars)
    # The regex below ensures the general shape is close to RFC 5322 simplified version
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        # The regex ensures:
        # - Local part has valid chars (alphanumeric and ._%+-)
        # - Domain has alphanumeric, dots, hyphens
        # - TLD is at least 2 letters
        # This catches cases like @ without domain, or weird symbols in local part not caught by manual checks
        return False

    return True