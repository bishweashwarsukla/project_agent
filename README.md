
[![CI/CD for Dockerized App](https://github.com/bishweashwarsukla/project_agent/actions/workflows/ci-cd.yml/badge.svg?branch=prod)](https://github.com/bishweashwarsukla/project_agent/actions/workflows/ci-cd.yml)

Here's a sample `README.md` that documents your entire project setup:

---

# Stock & Finance Query Assistant

This repository contains a Dockerized Streamlit application for answering stock, finance, and cryptocurrency-related queries. It leverages a vector database (ChromaDB) for data retrieval and integrates with Google Generative AI embeddings. The project also includes a CI/CD pipeline using GitHub Actions for automated Docker image building, testing, and deployment.

---

## Project Structure

- **Streamlit Application (`app.py`)**: Provides a user interface for querying financial information.
- **Vector Database (`build_vector_db` and `load_vector_db` functions)**: Retrieves financial data and supports querying.
- **CI/CD Pipeline (`.github/workflows/ci-cd.yaml`)**: Automated pipeline for building, testing, and deploying Docker images.
- **Dockerfile**: Defines the container environment to run the Streamlit app.

---

## Features

1. **User Querying with Streamlit**: An interactive user interface for querying insights on stocks, finance, and cryptocurrency.
2. **ChromaDB Vector Database**: 
   - `build_vector_db` creates and updates the vector database with financial data.
   - `load_vector_db` loads the existing vector database for queries.
3. **CI/CD with GitHub Actions**:
   - On every push or pull request to specified branches, the workflow builds and tests the Docker image.
   - After successful tests, the image is pushed to DockerHub.
4. **Dockerized Environment**: A consistent environment built on a slim Python 3.9 base image.

---

## Setup

### Prerequisites

- **Docker**: Ensure Docker is installed.
- **Python 3.9**
- **DockerHub Account**: For storing the Docker image.
- **Google API Key**: Required for Google Generative AI embeddings.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/stock-finance-query-assistant.git
   cd stock-finance-query-assistant
   ```

2. **Set Up Environment Variables**:
   - Create a `.env` file to store API keys and URLs for financial data sources.
   - Example `.env`:
     ```plaintext
     GOOGLE_API_KEY=your_google_api_key
     moneycontrol=https://example.com/data1
     economic_times=https://example.com/data2
     yahoo_fin=https://example.com/data3
     ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running Locally

1. **Start the Streamlit Application**:
   ```bash
   streamlit run app.py
   ```
2. **Create the Knowledge Base**: Click “Update Knowledge Base” in the Streamlit app to build the vector database.

### Running with Docker

1. **Build the Docker Image**:
   ```bash
   docker build -t stock-finance-query-assistant .
   ```
2. **Run the Docker Container**:
   ```bash
   docker run -p 8501:8501 kanukollugvt/flasktest-app:latest
   ```
3. Open `http://localhost:8501` in a browser to access the app.

---

## CI/CD Pipeline

GitHub Actions automatically builds, tests, and publishes the Docker image upon every push to `prod`, `bish_dev`, or `kgvt_dev` branches. 

- **Workflow Triggers**:
  - **Push** to `prod`, `bish_dev`, `kgvt_dev`
  - **Pull Requests** to `prod`

### Workflow File `.github/workflows/ci-cd.yaml`

The workflow includes:
- Building the Docker image.
- Running unit tests with `pytest`.
- Pushing the image to DockerHub on successful tests.

---

## Dockerfile

The `Dockerfile` creates a containerized environment:
- **Base Image**: `python:3.9-slim`
- **Working Directory**: `/project_agent`
- **Requirements Installation**: Installs packages listed in `requirements.txt`.
- **Port Exposure**: Exposes port `8501` for Streamlit.
- **Startup Command**: `CMD ["streamlit", "run", "app.py"]`

---

## Example Diagram

![System Architecture Diagram](./path/to/diagram.png)

---

## Contributing

1. Fork the repository.
2. Create your branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License.

---

## Contact

For queries, feel free to reach out at `your-email@example.com`. 

---

This `README.md` serves as a comprehensive guide for understanding, running, and contributing to the project. Let me know if there’s anything more you’d like to add!

# project_agent

---------------------------------------------------------------------------------------------------------------------------------
How to setup environment ?
steps
1. python - m venv <envname>
2. kill terminal and restart it again
3. pip install --upgrade pip setuptools
4. source .venv activate
5. pip3 install -r requirements.txt

![graph image](/project_agent/input/images/graph.jpg)

![graph image 2](/project_agent/input/images/graph2.jpg)

