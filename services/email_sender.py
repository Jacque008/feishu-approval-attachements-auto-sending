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
                "headers": {
                    "Content-Disposition": f'attachment; filename="{attachment.name}"',
                },
            })

        # Send email via Resend
        # Use HTML format to prevent email clients from auto-inlining images
        html_body = body.replace("\n", "<br>")
        params = {
            "from": self.from_email,
            "to": [to_email],
            "subject": subject,
            "text": body,
            "html": f"<html><body><p>{html_body}</p></body></html>",
        }
        if resend_attachments:
            params["attachments"] = resend_attachments

        resend.Emails.send(params)
