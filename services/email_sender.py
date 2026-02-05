import base64
import resend

from .attachment import AttachmentInfo


class EmailSender:
    def __init__(
        self,
        api_key: str,
        from_email: str,
    ):
        self.from_email = from_email
        resend.api_key = api_key

    async def send_with_attachments(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachments: list[AttachmentInfo],
    ) -> None:
        """Send email with attachments via Resend API."""
        # Prepare attachments for Resend
        resend_attachments = []
        for attachment in attachments:
            if attachment.content is None:
                continue
            resend_attachments.append({
                "filename": attachment.name,
                "content": list(attachment.content),  # Resend expects list of bytes
                "content_type": "application/octet-stream",  # Force as attachment, not inline
            })

        # Send email via Resend
        params = {
            "from": self.from_email,
            "to": [to_email],
            "subject": subject,
            "text": body,
        }
        if resend_attachments:
            params["attachments"] = resend_attachments

        resend.Emails.send(params)
