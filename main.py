import base64
import io
from typing import List

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_table import DataTable
import pandas as pd

from google.cloud import vision
import io
import openai

openai.api_key = 'your-api-key'

# Dummy function for text extraction
def extract_text(image):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description  # Return the first text annotation (entire text)
    else:
        return "No text found"

def extract_text_between_symbols(text, symbol1, symbol2):
    start_index = text.find(symbol1)
    if start_index == -1:
        return ""
    end_index = text.find(symbol2, start_index + 1)
    if end_index == -1:
        return ""
    return text[start_index + 1:end_index]

def extract_categories(text):
    chat_role = "Your sole purpose is to compile information and summarize it.  You will only output data in a csv format, and no other text will be returned by you."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": chat_role},
            {"role": "user", "content": "Give me a relevant number of categories that summarize this text, and would be useful to relate this text to similar texts.  Do not return anything else besides the categorizations of this text separated into commas."},
            {"role": "user", "content": text},
        ],
    )

    return response.choices[0].message.content

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Image Text Extraction Dashboard"),
    dcc.Upload(
        id='upload-images',
        children=html.Div(['Drag and Drop or ', html.A('Select Images')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    dbc.Row([
        dbc.Col(dcc.Input(id="symbol1", type="text", placeholder="Enter first symbol")),
        dbc.Col(dcc.Input(id="symbol2", type="text", placeholder="Enter second symbol")),
    ]),
    html.Button('Extract Text from Images', id='extract-text-button'),
    html.Div(id='output-data-upload'),
    DataTable(
        id='datatable',
        style_table={
            'width': '600px',
            'overflowX': 'auto'
        },
        style_cell={
            'maxWidth': '200px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'
        },
        # specify columns to apply width style to
        style_data_conditional=[
            {
                'if': {'column_id': c},
                'width': '75px'
            } for c in ['column1', 'column2', 'column3']
        ],
    ),
    html.A(
        "Download CSV",
        id="download-button",
        download="extracted_texts.csv",
        href="",
        target="_blank",
        style={"margin-top": "20px"},
    )
])

@app.callback(
    Output('output-data-upload', 'children'),
    Output('datatable', 'data'),
    Output('datatable', 'columns'),
    Input('extract-text-button', 'n_clicks'),
    State('upload-images', 'contents'),
    State('symbol1', 'value'),
    State('symbol2', 'value'))
def update_output(n_clicks, images_contents, symbol1, symbol2):
    if n_clicks is None or images_contents is None:
        return [], [], []

    extracted_texts = []
    extracted_categories = []

    for content in images_contents:
        content_type, content_string = content.split(',')

        image = base64.b64decode(content_string)

        extracted_text = extract_text(image)

        if symbol1 is not None and symbol2 is not None:
            extracted_text = extract_text_between_symbols(extracted_text, symbol1, symbol2)

        extracted_texts.append(extracted_text)

        extracted_category = extract_categories(extracted_text)
        extracted_categories.append(extracted_category)

    data = pd.DataFrame({'Extracted Text': extracted_texts, 'Extracted Categories': extracted_categories})

    return html.Div([
            html.H5(f"{len(images_contents)} Image(s) Uploaded"),
        ], style={'margin-top': '20px'}), data.to_dict('records'), [{"name": i, "id": i} for i in data.columns]


@app.callback(
    Output("download-button", "href"),
    Input("datatable", "data"))
def update_download_button(data):
    if not data:
        return ""

    df = pd.DataFrame(data)
    csv_string = df.to_csv(index=False, encoding="utf-8")
    csv_data_uri = f"data:text/csv;charset=utf-8,{csv_string}"

    return csv_data_uri



if __name__ == '__main__':
    app.run_server(debug=True)
