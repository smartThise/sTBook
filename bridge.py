from flask import Flask, request, Response
import requests, copy

app = Flask(__name__)
BAIDU_URL = "https://qianfan.baidubce.com/anthropic/coding/v1/messages"

def flatten_messages(messages):
    pdf_docs = []
    fixed = []

    for msg in messages:
        msg = copy.deepcopy(msg)
        content = msg.get("content", [])
        if msg.get("role") == "user" and isinstance(content, list):
            new_content = []
            for block in content:
                if not isinstance(block, dict):
                    new_content.append(block)
                    continue
                if block.get("type") == "tool_result":
                    inner = block.get("content", "")
                    block = dict(block)
                    if isinstance(inner, list):
                        text_parts = []
                        for b in inner:
                            if b.get("type") == "document":
                                pdf_docs.append(b)
                                text_parts.append("[PDF内容见system]")
                            elif b.get("type") == "text":
                                text_parts.append(b.get("text", ""))
                            else:
                                text_parts.append(str(b))
                        block["content"] = "\n".join(text_parts) if text_parts else "见system"
                    new_content.append(block)
                elif block.get("type") == "document":
                    pdf_docs.append(block)
                else:
                    new_content.append(block)
            msg["content"] = new_content
        fixed.append(msg)
    return fixed, pdf_docs

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def catch_all(path):
    print(f"收到请求: {request.method} /{path}")
    body = request.get_json(silent=True)
    if body and "messages" in body:
        body["messages"], pdf_docs = flatten_messages(body["messages"])
        if pdf_docs:
            existing_system = body.get("system", "")
            if isinstance(existing_system, str):
                existing_system = [{"type": "text", "text": existing_system}] if existing_system else []
            body["system"] = existing_system + [{"type": "text", "text": "以下是用户提供的PDF文件："}] + pdf_docs

    resp = requests.request(
        method=request.method,
        url=BAIDU_URL,
        json=body,
        headers={
            "Authorization": request.headers.get("Authorization", ""),
            "Content-Type": "application/json",
            "anthropic-version": request.headers.get("Anthropic-Version", "2023-06-01"),
            "anthropic-beta": request.headers.get("Anthropic-Beta", ""),
        },
        timeout=300,
        stream=True,
    )
    print(f"百度返回: {resp.status_code}")
    return Response(resp.iter_content(chunk_size=4096), status=resp.status_code,
                    content_type=resp.headers.get("Content-Type", "application/json"))

if __name__ == "__main__":
    app.run(port=8742, debug=True)