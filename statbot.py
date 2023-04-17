import openai
import streamlit as st
import json
import pandas as pd
import socket
import os

from context import context

LOCAL_HOST = 'liestal'

# openai.api_key = os.getenv("OPENAI_API_KEY")
if socket.gethostname().lower() == LOCAL_HOST:
    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.organization = os.environ["OPENAI_ORGANISATION"]
else:
    openai.api_key = st.secrets['OPENAI_API_KEY']
    openai.organization = st.secrets["OPENAI_ORGANISATION"]

model = "gpt-3.5-turbo"
STATUS_OPTIONS = ['find_theme', 'find_product', ]
TEMPERATURE = 0
MAX_TOKENS = 2000
dont_know = "Ich habe die Frage leider nicht verstanden oder keine entsprechende Tabelle finden können. Bitte geben sie doch nochmals ihre Frage ein."

class StatBot():
    def __init__(self):
        self.user_prompts = []

        self.contexts = []
        self.results = []
        self.tokens = []
        self.status = [STATUS_OPTIONS[0]]
        self.themes_df = self.get_themes()
        self.themen_list = ','.join(set(list(self.themes_df['themenbereich'])))

    def get_themes(self):
        df = pd.read_csv('./webtabellen.csv', encoding='ANSI', sep=';')
        df.dropna(inplace=True)
        return df


    def get_product(self, question, theme):
        code = 400
        tables = self.get_tables(theme)

        tables_list = [x for x in list(tables['bezeichnung']) if x is not None]
        tables_list = ','.join(tables_list)
        prompt = context['find_product'].format(tables_list, question)
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        if "choices" in completion:
            json_str = completion["choices"][0]["message"]["content"].lstrip("\n")
            response = json.loads(json_str)
            response = response['product'] if 'product' in response else "unbekannt"
        else:
            response = "unbekannt"
        code = 400 if response == "unbekannt" else 200

        # print(st.session_state['messages'])
        total_tokens = completion.usage.total_tokens
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        return response, code

    def get_theme(self, question):
        code = 400
        prompt = context['find_theme'].format(question, self.themen_list)
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        if "choices" in completion:
            json_str = completion["choices"][0]["message"]["content"].lstrip("\n")
            response = json.loads(json_str)
            response = response['thema'] if 'thema' in response else "unbekannt"
        else:
            response = "unbekannt"
        code = 400 if response == "unbekannt" else 200

        # print(st.session_state['messages'])
        # total_tokens = completion.usage.total_tokens
        # prompt_tokens = completion.usage.prompt_tokens
        # completion_tokens = completion.usage.completion_tokens
        return response, code

    def get_url(self, table):
        record = self.themes_df[self.themes_df['bezeichnung'] == table]
        if len(record) > 0:
            return record.iloc[0]['url']

    def calc_costs(self):
         # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost

    def get_tables(self, theme):
        result = self.themes_df[(self.themes_df['themenbereich'] == theme) & (self.themes_df['url'].notna())]
        return result

    def act(self):
        model_name = "GPT-3.5"
        # counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

        # container for chat history
        
        # container for text box
        container = st.container()
        response_container = st.container()
        
        with container:
            code = 400
            has_submitted = False
            with st.form(key='my_form', clear_on_submit=False):
                default_prompt = self.user_prompts[-1] if len(self.user_prompts) > 0 else ''
                user_input = st.text_area("Deine Frage an den St@tBot:", key='input', height=100, value=default_prompt)
                self.user_prompts.append(user_input)
                
                submit_button = st.form_submit_button(label='Senden')
                if submit_button and user_input:
                    theme, code = self.get_theme(user_input)
                    if code == 200:
                        table, code = self.get_product(user_input, theme)
                    has_submitted = True
        

        if has_submitted:
            if code == 200:
                url = self.get_url(table)
                tables_df = self.get_tables(theme)
                st.write("🤖 St@tBot:")
                st.markdown(f'Sie finden Informationen zu diesem Thema in Datei [{table}]({url})')
                st.markdown(f"Falls diese Referenz nicht die gewünschten Informationen enthalten, so gibt es in unseren Webtabellen folgende Tabellen zum Thema *{theme}*")
                for index, row in tables_df.iterrows():
                    st.markdown(f"- [{row['bezeichnung']}]({row['url']})")
            else:
                st.write('Leider konnte ich keine Tabelle zu diesem Thema finden, kann ich dir mit einer anderen Frage weiterhelfen?')

