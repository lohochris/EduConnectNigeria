import uuid

def generate_jitsi_meeting_url(class_title):
    """Generate a unique Jitsi meeting URL."""
    meeting_id = uuid.uuid4().hex[:10]  # Unique identifier
    return f"https://meet.jit.si/{class_title.replace(' ', '')}-{meeting_id}"
