import os
from datetime import datetime

import pendulum
from airflow import DAG

from weather_api_operator import WeatherApiOperator
from llm_agent_operator import LlmClothingAgentOperator
from push_notifications_operator import PushBulletAlertOperator
from airflow.models import Variable

dag_id = os.path.splitext(os.path.basename(__file__))[0]

dag_markdown = """
# dag_llm_weather_suggestions

**Overview:**  
This Airflow DAG provides automated, twice-daily clothing suggestions for Bromley based on the latest weather forecast. 
It integrates weather data retrieval, LLM-powered recommendation generation, and push notification delivery.

## Schedule
- **Runs:** Twice daily at 7:00 AM and 2:00 PM (Europe/London timezone)

## Workflow Steps
1. **get_bromley_weather:**  
    Fetches the weather forecast based on lattitdue and longitude for the next hour.
2. **get_clothing_suggestions:**  
    Uses an LLM agent to generate clothing recommendations based on the fetched weather data.
3. **send_clothing_suggestions:**  
    Sends the generated clothing suggestions as a PushBullet notification.

## Tags
- Clothing_Suggestions

## Author
- Rahul (update as needed)
"""
with DAG(
    dag_id=dag_id,
    schedule_interval="0 7,14 * * *",  # 7:00 AM and 2:00 PM daily
    start_date=datetime(2024, 1, 1, tzinfo=pendulum.timezone("Europe/London")),
    catchup=False,
    tags=["Clothing_Suggestions"],
    doc_md=dag_markdown,
) as dag:

    weather_info = WeatherApiOperator(
        task_id="get_weather",
        lattitude=99.406,# Example latitude
        longitude=0.015,# Example longitude
        hours_ahead=1,
        do_xcom_push=True,
    )

    clothing_suggestions = LlmClothingAgentOperator(
        task_id="get_clothing_suggestions",
        hostname=Variable.get("LLM_HOSTNAME"),
        model_name="llama3.2:1b",
        weather_conditions="{{ ti.xcom_pull(task_ids='get_weather') }}",
        do_xcom_push=True,
    )

    send_notification = PushBulletAlertOperator(
        task_id="send_clothing_suggestions",
        title="Clothing Suggestion",
        message="{{ ti.xcom_pull(task_ids='get_clothing_suggestions') }}",
        notify_sound="falling",
    )

    weather_info >> clothing_suggestions >> send_notification
