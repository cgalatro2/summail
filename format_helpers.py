import re
import base64


def extract_text_from_html(html_content):
    """Extract readable text from HTML content by removing tags and cleaning up whitespace."""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", html_content)
    # Remove extra whitespace and normalize
    text = re.sub(r"\s+", " ", text)
    # Remove common email error messages
    error_patterns = [
        r"The email did not display correctly",
        r"Click here to view this email",
        r"If you are having trouble viewing this email",
        r"View this email in your browser",
        r"Unsubscribe",
        r"Click here to unsubscribe",
        r"This email was sent to",
        r"You received this email because",
    ]
    for pattern in error_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text.strip()


def extract_body_from_parts(parts):
    """Recursively extract text content from email parts."""
    body = ""

    for part in parts:
        mime_type = part.get("mimeType", "")

        # Handle nested parts
        if part.get("parts"):
            nested_body = extract_body_from_parts(part.get("parts"))
            if nested_body:
                body = nested_body
                break

        # Handle text content
        if mime_type.startswith("text/"):
            data = part.get("body", {}).get("data", "")
            if data:
                try:
                    decoded = base64.urlsafe_b64decode(data).decode(
                        "utf-8", errors="ignore"
                    )
                    if mime_type == "text/plain":
                        body = decoded
                        break
                    elif mime_type == "text/html" and not body:
                        # Clean HTML content
                        body = extract_text_from_html(decoded)
                except Exception:
                    continue

    return body
