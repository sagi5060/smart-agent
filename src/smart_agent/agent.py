import asyncio
from typing import List
from ollama import AsyncClient
from .tools.base_tool import BaseTool
from .registery import all_tools
from .logger import setup_logger

logger = setup_logger(__name__)

class LLaMA3Client:
    def __init__(self):
        self.client = AsyncClient()

    async def generate(self, prompt: str) -> str:
        messages = [{'role': 'user', 'content': prompt}]
        response = await self.client.chat(model='llama3.1:8b', messages=messages, tools=[tool.to_ollama_tool() for tool in all_tools])
        
        if response.message.tool_calls:
            # Add the assistant's tool call message
            messages.append(response.message)
            
            # Process each tool call
            for tool_call in response.message.tool_calls:
                logger.info(f'Calling function: {tool_call.function.name}')
                logger.debug(f'Arguments: {tool_call.function.arguments}')
                
                # Find the tool by name and call it
                tool_name = tool_call.function.name
                for tool in all_tools:
                    if tool.get_name() == tool_name:
                        result = await tool.run(**tool_call.function.arguments)
                        logger.info(f"Tool result: {result}")
                        
                        # Add tool result to conversation
                        messages.append({
                            'role': 'tool', 
                            'content': f"Tool '{tool.get_name()}' returned: {result.data}\nMetadata: {result.meta}",
                            'tool_name': tool.get_name()
                        })
                        break
            
            # Get final response from model with tool results
            final_response = await self.client.chat(model='llama3.1:8b', messages=messages)
            return final_response.message.content
        else:
            # No tool calls, return original response
            return response.message.content

class SmartAgent:
    def __init__(self, llm: LLaMA3Client, tools: List[BaseTool]):
        self.llm = llm
        self.tools = {tool.get_name().lower(): tool for tool in tools}

    async def run(self, user_query: str) -> str:
        return await self.llm.generate(user_query)

async def main():
    llm_client = LLaMA3Client()
    tools = all_tools
    agent = SmartAgent(llm_client, tools)

    queries = [
        "give me information about test.csv",
        "i want to understand the story.md in detail",
    ]

    for q in queries:
        response = await agent.run(q)
        print(f"Query: {q}\nResponse: {response}\n")

asyncio.run(main())