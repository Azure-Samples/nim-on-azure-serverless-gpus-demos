# NIM on Azure Serverless GPU Demos

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://codespaces.new/Azure-Samples/python-ai-agent-frameworks-demos)
[![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/python-ai-agent-frameworks-demos)

## Purpose

This repository demonstrates how to use a variety of popular Python AI agent frameworks with **NIM models running on Azure Serverless GPUs**. The examples show how to integrate these frameworks with NIM endpoints, enabling scalable, cost-effective, and high-performance AI workloads on Azure.

Whether you're interested in LangChain, OpenAI Agents, PydanticAI, or other frameworks, these samples will help you connect your agents to NIM models deployed on Azure's serverless GPU infrastructure.

## Getting Started

You can run these examples in GitHub Codespaces, VS Code Dev Containers, or locally. The fastest way to get started is with GitHub Codespaces, which sets up everything for you.

See the sections below for setup instructions.

## Running the Python Examples

Each script in the `examples` directory demonstrates a different agent pattern or framework, all designed to work with NIM models on Azure Serverless GPUs.

## Using NIM Models on Azure Serverless GPUs

All examples are designed to connect to NIM model endpoints provisioned on Azure Serverless GPUs. This enables you to leverage powerful, scalable AI models with minimal infrastructure management.

To provision NIM models on Azure and obtain endpoint details, see the [Provisioning Azure AI resources](#provisioning-azure-ai-resources) section.

## Configuring Your Environment

You can run the scripts using GitHub Models for free, or connect to your own NIM endpoints on Azure. For Azure, set the appropriate environment variables with your endpoint and credentials.

See the setup instructions in the sections below for details.

## Provisioning Azure AI Resources

This project includes infrastructure as code (IaC) to provision NIM model deployments on Azure Serverless GPUs. Use the Azure Developer CLI to deploy resources and obtain endpoint details for your agents.

See the [Provisioning Azure AI resources](#provisioning-azure-ai-resources) section for step-by-step instructions.

## Resources

* [NIM on Azure Documentation](https://learn.microsoft.com/en-us/azure/ai-services/nim/)
* [AutoGen Documentation](https://microsoft.github.io/autogen/)
* [LangChain Documentation](https://python.langchain.com/)
* [OpenAI Agents Documentation](https://openai.github.io/openai-agents-python/)
* [PydanticAI Documentation](https://ai.pydantic.dev/multi-agent-applications/)
* [SmolAgents Documentation](https://huggingface.co/docs/smolagents/index)

---

For full setup, usage, and example details, see the sections below in this README.
