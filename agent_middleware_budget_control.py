import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState

# 加载模型配置
load_dotenv()

# 低费率模型
basic_model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    model="qwen3-coder-plus",
)

# 高费率模型
advanced_model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    model="qwen3-coder-plus",
)

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    print('进入中间件...')
    print(f'request: {request}')

    message_count = len(request.state["messages"])

    if message_count > 5:
        # Use a basic model for longer conversations
        model = basic_model
    else:
        model = advanced_model

    request.model = model
    print(f"message_count: {message_count}")
    print(f"model_name: {model.model_name}")

    print('完成中间件...')
    return handler(request)

if __name__ == '__main__':

    agent = create_agent(
        model=advanced_model,  # Default model
        middleware=[dynamic_model_selection]
    )

    state: MessagesState = {"messages": []}
    items = ['汽车', '飞机', '摩托车', '自行车']
    for idx, i in enumerate(items):
        print(f"\n=== Round {idx+1} ===")
        state["messages"] += [HumanMessage(content=f"{i}有几个轮子，请简单回答")]
        print(f'messages: {state["messages"]}')
        result = agent.invoke(state)
        print(f'agent result: {result}')
        state["messages"] = result["messages"]
        print(f'content: {result["messages"][-1].content}')