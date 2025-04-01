# RAG App with LLM

## Overview
This project implements a Retrieval-Augmented Generation (RAG) application that enhances an LLM's responses by incorporating retrieved documents from a knowledge base. The system combines information retrieval techniques with generative AI to provide more accurate and context-aware answers.

## Features


## Prerequisites

- install miniconda with python 3.10

```bash
wget https://repo.anaconda.com/miniconda Miniconda3-latest-Linux-x86_64.sh
```

```bash
chmod +x Miniconda3-latest-Linux-x86_64.sh 
```

```bash
./Miniconda3-latest-Linux-x86_64.sh
```

```bash
conda create -n env_name python=3.10
```

## Installation 

## Run the mian program 

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```