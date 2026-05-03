from langgraph.graph import StateGraph, START, END
from app.agents.state import AgentState
from app.agents.nodes import determine_role_node, gap_analyst_node, pathmaker_node

# Initialize the StateGraph with our state schema
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("determine_role", determine_role_node)
workflow.add_node("gap_analyst", gap_analyst_node)
workflow.add_node("pathmaker", pathmaker_node)

# Define the edges/flow
workflow.add_edge(START, "determine_role")
workflow.add_edge("determine_role", "gap_analyst")
workflow.add_edge("gap_analyst", "pathmaker")
workflow.add_edge("pathmaker", END)

# Compile the graph
career_agent_graph = workflow.compile()
