# Airflow Weather LLM

A demonstration project that combines **Apache Airflow** for workflow orchestration, weather data ingestion, and the power of **Large Language Models (LLMs)** for data-driven insights and automation.

## 🚀 About the Project

This project showcases how to:

- **Automate weather data collection** using Airflow DAGs.
- **Process and transform weather datasets** in an efficient pipeline.
- **Leverage LLMs** (such as OpenAI's GPT or similar) to generate insights, forecasts, or reports from weather data.

It is designed as a reference solution for data engineers, ML practitioners, and anyone interested in orchestrating real-world data pipelines with AI-powered automation.

---

## 🛠️ Tech Stack

- **Apache Airflow**: Workflow scheduling and orchestration
- **Python**: Core logic, data processing, and LLM integration
- **OpenWeatherMap API** (or similar): Source for weather data
- **Large Language Model**: For text generation/insights (OpenAI GPT, HuggingFace, or Ollama)

---

## 💡 Features

- **End-to-end pipeline**: From raw weather data ingestion to AI-powered report generation.
- **Modular Airflow DAGs**: Easily extend or customize for other data sources or analyses.
- **LLM-powered insights**: Automate the creation of weather summaries, forecasts, or anomaly detection.
- **Ready for cloud or local deployment**: Compatible with various Airflow setups.

---

## 📊 Example Use Cases

- Daily weather summary emails powered by LLMs.
- Anomaly detection in weather patterns with AI explanations.
- Automated data quality checks and reporting.

---

## 🤖 LLM Integration

The DAG includes a task that sends processed weather data to an LLM, which then returns:
- Human-readable summaries
- Forecasts or trend descriptions
- Automated commentary (customizable)

Modify the LLM task to use your preferred model/provider or change the prompt for different insights.

## 🌐 Connect

If you find this project interesting, feel free to:
- ⭐ Star the repo
- Connect with me on [LinkedIn](https://www.linkedin.com/in/rahul-rajasekharan-012506121/)

---

## 📄 License

MIT License

---

## 🛠️ How to run -?

Start the Docker container by running the below commands 


> docker build . --tag airflow_local:latest

###### Initialise Docker Container based on the docker compose file

> docker compose up airflow-init

###### Run the Docker container

> docker compose up -d

###### Stopping the container

> docker compose down

Once the Airflow instance is up & running create the below variables from the UI -

- LLM_HOSTNAME (Hostname where Ollama is running and choose a model of your choice I have used - llama3.2:1b )
- PUSHOVER_USER_KEY (Create an API key from here -https://pushover.net/ )
- PUSHOVER_API_TOKEN (Create an API token from here - https://pushover.net/ )


