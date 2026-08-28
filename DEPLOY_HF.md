# Hugging Face Spaces Deployment Configuration

This file outlines the deployment parameters and synchronization pipeline for hosting the static client build of IVA on Hugging Face Spaces.

## ⚙️ Space Configuration Metadata

This project is configured as a static HTML/JS application space. The following YAML configuration block is placed at the top of the main index file or within the Space environment to control the hosting container:

https://huggingface.co/spaces/AIHub-Mu/indus-valley-ai


```yaml
title: Indus Valley AI (IVA)
emoji: 🏛️
colorFrom: amber
colorTo: bronze
sdk: static
pinned: false
app_file: index.html