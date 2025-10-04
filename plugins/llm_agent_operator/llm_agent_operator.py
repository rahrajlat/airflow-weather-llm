from airflow.models import BaseOperator
from agno.agent import Agent
from agno.models.ollama import Ollama


class LlmClothingAgentOperator(BaseOperator):
    """
    An Airflow operator that uses a language model agent to generate clothing suggestions based on weather conditions.

    This operator sends weather forecast data to a language model (via an agent) and receives a structured, human-friendly clothing recommendation. The recommendation includes a summary, clothing suggestions, umbrella advice, and accessories, following a fixed reply style.

    Args:
        hostname (str): The hostname or address of the LLM server.
        model_name (str): The name or identifier of the LLM model to use.
        weather_conditions (list): A list of weather condition dictionaries (forecast data) to be analyzed.
        **kwargs: Additional keyword arguments passed to the BaseOperator.

    Attributes:
        template_fields (tuple): Fields that support templating in Airflow.

    Methods:
        _get_clothing_suggestions():
            Sends the weather conditions to the LLM agent and retrieves a clothing suggestion response.
        execute(context):
            Executes the operator, returning the LLM's clothing suggestion response.
    """
    template_fields = ("weather_conditions",)

    def __init__(self, hostname: str, model_name: str, weather_conditions: list, **kwargs) -> None:
        super().__init__(**kwargs)
        self.hostname = hostname
        self.model_name = model_name
        self.weather_conditions = weather_conditions

    def _get_clothing_suggestions(self):
        """Fetch clothing suggestions from LLM based on weather conditions."""
        agent = Agent(
            model=Ollama(id=self.model_name, host=self.hostname),
            description="You are a helpful assistant."
        )
        prompt = (
            "\n"
            "You are a clothing suggestion assistant.\n\n"
            "Analyze the forecast JSON and give a short, human-friendly recommendation.\n\n"
            "Rules:\n"
            "- Always reply in this fixed style:\n"
            "\"Summary: <short summary>.\n"
            "Clothing: <what to wear>.\n"
            "Umbrella: <yes/no>.\n"
            "Accessories: <comma-separated list>.\"\n"
            "Weather Info: <temperature range>, feels like <range>, wind <range> km/h, rain chance <max rain chance>%.\n\n"
            "Guidelines:\n"
            "- Temperature (°C):\n"
            "- Cold < 12 → heavy jacket, layers\n"
            "- Cool 12–18 → light jacket or sweater\n"
            "- Mild 18–24 → light clothing\n"
            "- Hot > 24 → shorts, breathable clothing\n"
            "- Feels_like_c is more important than temperature.\n"
            "- Rain chance > 40% → Umbrella: yes\n"
            "- Wind > 15 km/h → mention jacket/windbreaker in clothing or accessories.\n"
            "- If temps vary across the day → suggest layers.\n\n"
            "Input forecast (JSON list):\n"
            "```json\n"
            f"{self.weather_conditions}\n"
            "```"
        )
        response = agent.run(prompt)
        return str(self.weather_conditions) + response.content

    def execute(self, context):
        llm_response = self._get_clothing_suggestions()
        return llm_response
