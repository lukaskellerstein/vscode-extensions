"""
Sequential Workflow Example - Agent Chain Pattern

Demonstrates a multi-step sequential workflow where the output of one agent
becomes the input to the next agent. This is useful for:
- Data processing pipelines
- Multi-stage analysis
- Progressive refinement tasks

Pattern: Agent A -> Agent B -> Agent C
"""

import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions


async def sequential_workflow():
    """
    Sequential workflow: Research -> Analyze -> Summarize

    Step 1: Research agent gathers information about a topic
    Step 2: Analysis agent examines the research findings
    Step 3: Summary agent creates a concise final report
    """

    # Step 1: Research Agent
    print("=" * 60)
    print("STEP 1: Research Phase")
    print("=" * 60)

    research_agent = ClaudeSDKClient(
        options=ClaudeAgentOptions(
            model="sonnet",
            system_prompt="You are a research assistant. Gather key information about the topic and provide detailed findings.",
        )
    )

    topic = "Benefits of Python's asyncio for concurrent programming"
    research_response = await research_agent.send_request(
        f"Research the following topic and provide 3-5 key points: {topic}"
    )

    research_findings = ""
    async for event in research_response:
        if hasattr(event, 'text'):
            research_findings += event.text
            print(event.text, end='', flush=True)

    print("\n")

    # Step 2: Analysis Agent
    print("=" * 60)
    print("STEP 2: Analysis Phase")
    print("=" * 60)

    analysis_agent = ClaudeSDKClient(
        options=ClaudeAgentOptions(
            model="sonnet",
            system_prompt="You are an analytical expert. Examine the research findings and identify strengths, weaknesses, and practical implications.",
        )
    )

    analysis_response = await analysis_agent.send_request(
        f"Analyze these research findings and provide critical insights:\n\n{research_findings}"
    )

    analysis_results = ""
    async for event in analysis_response:
        if hasattr(event, 'text'):
            analysis_results += event.text
            print(event.text, end='', flush=True)

    print("\n")

    # Step 3: Summary Agent
    print("=" * 60)
    print("STEP 3: Summary Phase")
    print("=" * 60)

    summary_agent = ClaudeSDKClient(
        options=ClaudeAgentOptions(
            model="sonnet",
            system_prompt="You are a summarization specialist. Create concise, actionable summaries suitable for executive review.",
        )
    )

    summary_response = await summary_agent.send_request(
        f"Create a concise executive summary based on this analysis:\n\n{analysis_results}"
    )

    print("\nFinal Summary:\n")
    async for event in summary_response:
        if hasattr(event, 'text'):
            print(event.text, end='', flush=True)

    print("\n")
    print("=" * 60)
    print("Sequential workflow completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(sequential_workflow())
