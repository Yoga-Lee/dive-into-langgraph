# 草稿

**语法**：

`create_agent`方式创建agent，invoke方式调用

注解方式声明中间件

**数据结构**：

agent的input：

input: InputT | Command | None
只有这个参数是必要的，InputT（是一个**LangGraph** 库提供的TypeVar，即类型变量），用于**静态检查**各类变量的类型是否符合要求，类似于泛型的作用。通常是个dict。	

```
messages:
  - !HumanMessage
    content: 汽车有几个轮子，请简单回答
    additional_kwargs: {}
    response_metadata: {}
```

agent的output：

也是一个dict

```yaml
messages:
  - !HumanMessage
    content: 汽车有几个轮子，请简单回答
    additional_kwargs: {}
    response_metadata: {}
    id: '819d59f1-5e40-4439-93fb-a58bf090c887'
  - !AIMessage
    content: 汽车有4个轮子。
    additional_kwargs:
      refusal: null
    response_metadata:
      token_usage:
        completion_tokens: 7
        prompt_tokens: 15
        total_tokens: 22
        completion_tokens_details: null
        prompt_tokens_details:
          audio_tokens: null
          cached_tokens: 0
      model_provider: openai
      model_name: qwen3-coder-plus
      system_fingerprint: null
      id: chatcmpl-5c81af0f-5e58-9584-94b3-8756e63c2fe0
      finish_reason: stop
      logprobs: null
    id: lc_run--019df752-87f5-7ee3-a96d-4d924d242136-0
    tool_calls: []
    invalid_tool_calls: []
    usage_metadata:
      input_tokens: 15
      output_tokens: 7
      total_tokens: 22
      input_token_details:
        cache_read: 0
      output_token_details: {}
```

**发现agent的output只是比input多了一个AIMessage对象，都是一个带有key=“messages”的dict**

中间件的input：

一般是一个模型请求入参（ModelRequest）和一个handler。**模型请求入参用于1.获取信息（模型信息、message信息、state信息、tool调用情况、系统提示、结构化输出等等），2.修改请求，handler用于执行graph的下一个节点**。

```yaml
ModelRequest:
  model: <ChatOpenAI instance>
    model_name: "qwen3-coder-plus"
    openai_api_key: "**********"
    openai_api_base: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    # (其他字段如 client, async_client 等省略内部细节)
  messages:
    - HumanMessage:
        content: "汽车有几个轮子，请简单回答"
        additional_kwargs: {}
        response_metadata: {}
        id: "819d59f1-5e40-4439-93fb-a58bf090c887"
    - AIMessage:
        content: "汽车有4个轮子。"
        additional_kwargs:
          refusal: null
        response_metadata:
          token_usage:
            completion_tokens: 7
            prompt_tokens: 15
            total_tokens: 22
            completion_tokens_details: null
            prompt_tokens_details:
              audio_tokens: null
              cached_tokens: 0
          model_provider: "openai"
          model_name: "qwen3-coder-plus"
          system_fingerprint: null
          id: "chatcmpl-5c81af0f-5e58-9584-94b3-8756e63c2fe0"
          finish_reason: "stop"
          logprobs: null
        id: "lc_run--019df752-87f5-7ee3-a96d-4d924d242136-0"
        tool_calls: []
        invalid_tool_calls: []
        usage_metadata:
          input_tokens: 15
          output_tokens: 7
          total_tokens: 22
          input_token_details:
            cache_read: 0
          output_token_details: {}
    - HumanMessage:
        content: "飞机有几个轮子，请简单回答"
        additional_kwargs: {}
        response_metadata: {}
        id: "5c86e549-bee6-493c-8e95-8920db1ebc66"
  system_message: null
  tool_choice: null
  tools: []
  response_format: null
  state:
    messages:
      - HumanMessage: (同上第二个 HumanMessage 内容，为避免重复，合并说明)
      - AIMessage: (同上 AIMessage 内容)
      - HumanMessage: (同上第三个 HumanMessage 内容)
  runtime: <Runtime object> (包含 checkpoint_id: "1f1485f1-bcdd-60f6-8000-fe9adb820014" 等)
  model_settings: {}
```

中间件的output

**agent执行的langchain底层实现原理**：

这里有一个大模型的回答，目前还挺模糊的，插个眼，后面再复习：https://chat.deepseek.com/share/08jcbqmxv9emtcbaez

**几个概念**：

- graph：图

- state：状态
- context：上下文
- node：节点



# 中间件

| `@before_model`    | 在每次模型调用前执行逻辑     |
| ------------------ | ---------------------------- |
| `@after_model`     | 在每次模型收到响应后执行逻辑 |
| `@wrap_model_call` | 控制模型的调用过程           |