import logging

from ollama import AsyncClient, Message

from .tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

SYS_PROMPT = """You are a highly capable and resourceful AI assistant.
You can answer questions, solve problems, and perform tasks by leveraging the tools available to you.
When using tools, ensure their outputs are accurate and relevant to the user's query.
Always provide clear, concise, and helpful responses.
If a tool is required, explain its usage and integrate its results seamlessly into your response.
If you cannot fulfill a request, explain why and suggest alternative approaches.
Maintain a professional and friendly tone in all interactions.
If file does not exist, notify the user and do not proceed with the request.
Do not make assumptions about files paths if not specifically asked to.
Don't expose the internal tools structure and parameters format to the user.
Always validate and sanitize user inputs to prevent injection attacks.
For general queries, which not require tool usage, provide direct answers without invoking tools.
Answer the user with a final response in case no tool needed.

If file given relatively path, use the relative path from current working directory(no need to add any base path).
Example:
user: give me information about options.md -> use tool <tool_name> with args {"file_path": "options.md"}
"""


class LLaMA3Client:
    def __init__(self, tools: list[BaseTool], system_prompt: str):
        self.client = AsyncClient()
        self.tools = tools
        self.system_prompt = system_prompt

    async def generate(self, prompt: str) -> str:
        messages: list[Message] = []
        if self.system_prompt:
            messages.append(Message(role="system", content=self.system_prompt))
        messages.append(Message(role="user", content=prompt))
        response = await self.client.chat(
            model="llama3.1:8b",
            messages=messages,
            tools=[tool.to_ollama_tool() for tool in self.tools],
        )

        if response.message.tool_calls:
            # Add the assistant's tool call message
            messages.append(response.message)

            # Process each tool call
            for tool_call in response.message.tool_calls:
                logger.info(f"Calling function: {tool_call.function.name}")
                logger.debug(f"Arguments: {tool_call.function.arguments}")

                # Find the tool by name and call it
                tool_name = tool_call.function.name
                for tool in self.tools:
                    if tool.get_name() == tool_name:
                        result = await tool.run(**tool_call.function.arguments)
                        logger.info(f"Tool result: {result}")

                        # Add tool result to conversation
                        messages.append(
                            Message(
                                role="tool",
                                content=f"Tool '{tool.get_name()}' returned: {result.data}\nMetadata: {result.meta}",
                                tool_name=tool.get_name(),
                            )
                        )
                        break

            # Get final response from model with tool results
            final_response = await self.client.chat(
                model="llama3.1:8b", messages=messages
            )
            # Simple check for thinking - avoid infinite loops
            if (
                hasattr(final_response.message, "thinking")
                and final_response.message.thinking
            ):
                logger.debug("Model is thinking, getting final response...")
            return (
                final_response.message.content
                if final_response.message.content
                else "No response from model."
            )
        else:
            # No tool calls, return original response
            return (
                response.message.content
                if response.message.content
                else "No response from model."
            )


class SmartAgent:
    def __init__(self):
        from smart_agent.registry import load_tools

        self.system_prompt = SYS_PROMPT
        self.llm = LLaMA3Client(load_tools(), self.system_prompt)

    async def run(self, user_query: str) -> str:
        return await self.llm.generate(user_query)
