# Image Text Extraction Dashboard

This program is a note-taking tool designed to extract text from images, select a desired portion of the text, and produce a CSV with the extracted portion and a categorical summarization of the text. This tool is particularly useful for digitizing handwritten notes and organizing them using platforms such as Obsidian.

This tool was made to show the capabilities of combing pre-trained models available through different providers (Google and OpenAI), and expand the possible use cases.  You can easily create your own interactive dashboard and automate tedious processes such as uploading a ton of images.  Potential upgrades are detecting highlighted words, separating handwritten and printed notes, detecting underlined or bold words, and much more.

## Features

- Extract text from images using Google Cloud Vision API
- Select desired portion of the text by specifying start and end symbols
- Produce a CSV file containing extracted text and its categorical summarization
- Upload multiple images at once

## Dependencies

- Python 3.7 or later
- Google Cloud Vision API
- OpenAI API
- Dash
- Dash Bootstrap Components
- Dash Core Components
- Dash HTML Components
- Dash Table
- Pandas

## Installation

1. Install the required Python packages:

```
pip install google-cloud-vision openai dash dash-bootstrap-components pandas
```

2. Make sure to have a valid API key for both Google Cloud Vision and OpenAI, and replace 'your-api-key' in the code with your OpenAI API key.

3. Run the application:

```
python app.py
```

4. Open a web browser and navigate to http://127.0.0.1:8050/ to access the Image Text Extraction Dashboard.

## Usage

1. Drag and drop or select images containing text.
2. Enter the start and end symbols (optional) to extract a specific portion of the text.
3. Click the "Extract Text from Images" button.
4. The extracted text and its categorical summarization will be displayed in a table.
5. Click the "Download CSV" link to download the CSV file containing the extracted text and categories.

Note: The extraction of text and categories might take a while depending on the number and complexity of the images. Please be patient.

## Troubleshooting

- Make sure you have a valid API key for both Google Cloud Vision and OpenAI.
- Ensure that you have the required Python packages installed and up to date.
- If you're having issues with the extraction process, double-check the image quality and text legibility.
