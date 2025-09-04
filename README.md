# HealthChat Pro

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-3178C6?style=for-the-badge&logo=chainlink&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-4255FF?style=for-the-badge&logo=pinecone&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

A medical AI assistant powered by LLM technology that provides health information and guidance.

</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [AWS Deployment](#aws-deployment)

## 🔍 Overview

HealthChat Pro is an AI-powered medical assistant application that uses large language models to answer health-related questions. The application features a responsive chat interface built with Flask and leverages LangChain for document retrieval and RAG (Retrieval Augmented Generation) capabilities.

## ✨ Features

- **Medical Knowledge Base**: Access to comprehensive medical information
- **Contextual Responses**: AI responses based on medical literature
- **Clean, Responsive UI**: Modern dark-themed interface
- **Session Management**: Persistent chat sessions
- **Source Citations**: References to medical sources
- **Vector Database Integration**: Efficient document retrieval using Pinecone

## 📁 Repository Structure

```
.
├── data/                   # Medical PDF documents
│   └── Medical_book.pdf    # Sample medical document
├── src/                    # Source code
│   ├── __init__.py
│   ├── helper.py           # Utility functions for document processing
│   └── prompt.py           # System prompts for the AI assistant
├── static/                 # Static assets
│   ├── bot-avatar.svg
│   ├── favicon.svg
│   ├── logo.svg
│   ├── style.css          # CSS styling
│   └── user-avatar.svg
├── templates/              # HTML templates
│   └── chat.html          # Main chat interface
├── .env                    # Environment variables (API keys)
├── .env.example           # Example environment variables file
├── .github/               # GitHub configuration
│   └── workflows/         # GitHub Actions workflows
│       └── deploy.yml     # AWS deployment workflow
├── .gitignore             # Git ignore file
├── app.py                 # Main Flask application
├── Dockerfile             # Docker configuration for containerization
├── LICENSE                # Apache License 2.0
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── research/              # Research and development notebooks
│   └── trials.ipynb       # Experimental notebook
├── setup.py              # Package setup file
├── store_index.py        # Script to create and store embeddings
└── template.sh           # Shell script for project setup
```

## 🚀 Installation

### Prerequisites

- Python 3.10+
- Conda (recommended for environment management)
- Pinecone account
- OpenAI API key

### Setup

1. Clone the repository

```bash
git clone https://github.com/Kaleemullah-Younas/HealthChat-Pro
cd HealthChat-Pro
```

2. Create a conda environment

```bash
conda create -n healthbot python=3.10 -y
conda activate healthbot
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys (see `.env.example` for reference)

```bash
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

5. Store embeddings in Pinecone

```bash
python store_index.py
```

6. Run the application

```bash
python app.py
```

7. Open your browser and navigate to `http://localhost:8080`
```

## 🌐 Usage

After installation and setup:

1. The application will be running at `http://localhost:8080`
2. Enter your health-related questions in the chat interface
3. The AI will respond with relevant medical information
4. You can clear the chat history using the "Clear Chat" button

## ☁️ AWS Deployment

This project includes CI/CD setup for AWS deployment using GitHub Actions.

### Prerequisites

1. AWS Account
2. GitHub Account
3. Docker installed locally (for testing)

### AWS Setup

#### 1. Create IAM User

Create an IAM user with the following policies:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess`

Save the access key and secret key for later use.

#### 2. Create ECR Repository

1. Go to AWS ECR console
2. Create a new repository named `healthchat-pro`
3. Note the repository URI (e.g., `315865595366.dkr.ecr.us-east-1.amazonaws.com/healthchat-pro`)

#### 3. Set Up EC2 Instance

1. Launch an EC2 instance (Ubuntu recommended)
2. Connect to your instance via SSH
3. Install Docker:

```bash
sudo apt-get update -y
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

#### 4. Configure GitHub Actions

1. In your GitHub repository, go to Settings > Actions > Runners
2. Click "New self-hosted runner"
3. Select Linux as the operating system
4. Follow the instructions to set up the runner on your EC2 instance

#### 5. Add GitHub Secrets

In your GitHub repository, go to Settings > Secrets and add the following secrets:

- `AWS_ACCESS_KEY_ID`: Your IAM user access key
- `AWS_SECRET_ACCESS_KEY`: Your IAM user secret key
- `AWS_DEFAULT_REGION`: Your AWS region (e.g., `us-east-1`)
- `ECR_REPO`: Your ECR repository name (e.g., `healthchat-pro`)
- `PINECONE_API_KEY`: Your Pinecone API key
- `OPENAI_API_KEY`: Your OpenAI API key

### Deployment Process

1. Push your changes to the main branch
2. GitHub Actions will automatically:
   - Build a Docker image
   - Push the image to ECR
   - Deploy the application on your EC2 instance
3. Access your application at `http://<your-ec2-public-ip>:8080`

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.



```bash
python store_index.py
```

## 💻 Usage

1. Start the Flask server

```bash
python app.py
```

2. Open your browser and navigate to:

```
http://localhost:8080
```

3. Start chatting with the HealthChat Pro AI assistant

## 🌐 AWS Deployment

### Prerequisites

- AWS Account
- GitHub Account
- Docker installed locally (for testing)

### AWS Setup

1. **Create IAM User for Deployment**

   Create a new IAM user with the following policies:
   - AmazonEC2ContainerRegistryFullAccess
   - AmazonEC2FullAccess

2. **Create ECR Repository**

   Create an Elastic Container Registry repository to store your Docker image.
   - Note the URI: `315865595366.dkr.ecr.us-east-1.amazonaws.com/medicalbot` (replace with your actual URI)

3. **Launch EC2 Instance**

   Launch an Ubuntu EC2 instance with appropriate security groups (allow HTTP/HTTPS/SSH).

4. **Install Docker on EC2**

   Connect to your EC2 instance and run:

   ```bash
   sudo apt-get update -y
   sudo apt-get upgrade -y
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```

5. **Configure GitHub Actions**

   - Go to your GitHub repository
   - Navigate to Settings > Actions > Runners
   - Click "New self-hosted runner"
   - Select Linux as the operating system
   - Follow the instructions to set up the runner on your EC2 instance

6. **Set Up GitHub Secrets**

   Add the following secrets to your GitHub repository:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - ECR_REPO
   - PINECONE_API_KEY
   - OPENAI_API_KEY
   - OPENAI_API_BASE

7. **Create GitHub Actions Workflow**

   Create a `.github/workflows/deploy.yml` file in your repository with appropriate CI/CD configuration.

### Deployment Process

1. Push changes to your GitHub repository
2. GitHub Actions will:
   - Build a Docker image
   - Push the image to ECR
   - Pull and run the image on your EC2 instance

---

<div align="center">

**HealthChat Pro** - Developed by [Kaleemullah Younas](https://github.com/Kaleemullah-Younas)

</div>