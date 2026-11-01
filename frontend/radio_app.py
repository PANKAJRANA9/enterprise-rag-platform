import gradio as gr
import requests

API = "http://localhost:8080/api"

def ask(source, query):
    r = requests.post(f"{API}/ask", json={"table": source, "text": query})
    return r.json().get("answer","Error") + f"\n\nSources: {r.json().get('sources')}"

def ask_all(query):
    r = requests.post(f"{API}/ask-all", json={"text": query})
    return r.json().get("answer","Error") + f"\n\nSources: {r.json().get('sources')}"

with gr.Blocks(title="Enterprise RAG") as demo:
    gr.Markdown("# Enterprise RAG - 6 Domains")
    with gr.Tab("Ask One Source"):
        src = gr.Dropdown(["crm_docs","odoo_docs","parking_docs","medical_kb","whatsapp_docs"], value="crm_docs")
        q = gr.Textbox(label="Query")
        btn = gr.Button("Ask")
        out = gr.Textbox(label="Answer", lines=10)
        btn.click(ask, [src, q], out)
    with gr.Tab("Ask All"):
        q2 = gr.Textbox(label="Query across all sources")
        btn2 = gr.Button("Ask All")
        out2 = gr.Textbox(label="Answer", lines=10)
        btn2.click(ask_all, q2, out2)

demo.launch(server_name="0.0.0.0", server_port=7860)