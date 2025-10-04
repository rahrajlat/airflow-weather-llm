from airflow.models import BaseOperator, Variable
import requests


class PushBulletAlertOperator(BaseOperator):
    """
    Operator to send push notifications using the Pushover API.

    This operator sends a notification with a specified title, message, and sound to a user via the Pushover service.
    It retrieves the API token and user key from Airflow Variables: 'PUSHOVER_API_TOKEN' and 'PUSHOVER_USER_KEY'.

    Args:
        title (str): The title of the notification.
        message (str): The message content of the notification.
        notify_sound (str): The sound to play on the recipient's device.
        **kwargs: Additional keyword arguments passed to BaseOperator.

    Methods:
        send_pushover_message():
            Sends the notification to the Pushover API and returns the response as a JSON object.
            Raises a RuntimeError if the API call fails.

        execute(context):
            Airflow entrypoint. Sends the notification and returns the Pushover API response.

    Template Fields:
        message: The message content can be templated using Airflow's templating engine.
    """
    template_fields = ("message",)

    def __init__(self, title: str, message: str, notify_sound: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.message = message
        self.title = title
        self.notify_sound = notify_sound

    def send_pushover_message(self):
        url = "https://api.pushover.net/1/messages.json"
        api_token = Variable.get("PUSHOVER_API_TOKEN")
        user_key = Variable.get("PUSHOVER_USER_KEY")
        payload = {
            "token": api_token,
            "user": user_key,
            "title": self.title,
            "message": self.message,
            "priority": 0,
            "sound": self.notify_sound,
        }
        try:
            response = requests.post(url, data=payload, timeout=10)
            if response.status_code >= 400:
                try:
                    print("Pushover error payload:", response.json())
                except Exception:
                    print("Pushover error text:", response.text)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            raise RuntimeError(
                f"Pushover HTTPError: {e}\nResponse: {getattr(e.response, 'text', None)}"
            ) from e

    def execute(self, context):
        pushover_response = self.send_pushover_message()
        return pushover_response
