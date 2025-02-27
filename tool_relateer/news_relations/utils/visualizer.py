"""
Utilities for visualizing relationships between news articles.
"""

import json
import networkx as nx
from pathlib import Path
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
from pyvis.network import Network

def create_network_graph(
    main_article: Dict[str, Any],
    related_articles: List[Dict[str, Any]],
    analysis: Dict[str, Any]
) -> str:
    """
    Create an interactive network graph visualization using pyvis.
    
    Args:
        main_article: The main article
        related_articles: List of related articles
        analysis: Analysis of relationships
        
    Returns:
        Path to the HTML file
    """
    # Create network
    net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
    
    # Add main article node
    main_id = str(main_article.get("id", "main"))
    main_title = main_article.get("title", "Main Article")
    main_date = main_article.get("date", "Unknown")
    net.add_node(
        main_id,
        label=f"{main_title}\n({main_date})",
        title=f"{main_title} - {main_date}",
        color="#ff5733",
        size=25
    )
    
    # Add related article nodes and edges
    connections = analysis.get("connections", [])
    for article in related_articles:
        article_id = str(article.get("id", "unknown"))
        article_title = article.get("title", "Unknown")
        article_date = article.get("date", "Unknown")
        
        # Find connection details
        connection = next((c for c in connections if str(c.get("article_id")) == article_id), None)
        
        # Set node color based on connection strength
        color = "#4287f5"  # Default blue
        if connection:
            strength = connection.get("strength", "").lower()
            if strength == "strong":
                color = "#32a852"  # Green
            elif strength == "medium":
                color = "#a8a232"  # Yellow
            elif strength == "weak":
                color = "#a85932"  # Orange
        
        # Add node
        net.add_node(
            article_id,
            label=f"{article_title}\n({article_date})",
            title=f"{article_title} - {article_date}",
            color=color,
            size=15
        )
        
        # Add edge with connection details
        edge_title = "Related"
        if connection:
            connection_type = connection.get("connection_type", "")
            explanation = connection.get("explanation", "")
            edge_title = f"{connection_type}: {explanation}"
        
        net.add_edge(main_id, article_id, title=edge_title)
    
    # Add relationship type nodes if available
    relationship_types = analysis.get("relationship_types", [])
    for i, rel_type in enumerate(relationship_types):
        rel_id = f"rel_{i}"
        net.add_node(
            rel_id,
            label=rel_type,
            title=f"Relationship Type: {rel_type}",
            color="#9932a8",  # Purple
            shape="diamond",
            size=10
        )
        net.add_edge(main_id, rel_id, color="#9932a8", dashes=True)
    
    # Configure physics
    net.barnes_hut(
        gravity=-2000,
        central_gravity=0.3,
        spring_length=150,
        spring_strength=0.05,
        damping=0.09
    )
    
    # Enable physics controls
    net.show_buttons(filter_=['physics'])
    
    # Save to HTML file
    output_path = Path("static") / "network.html"
    net.save_graph(str(output_path))
    
    return str(output_path)


def create_plotly_graph(
    main_article: Dict[str, Any],
    related_articles: List[Dict[str, Any]],
    analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a Plotly graph visualization.
    
    Args:
        main_article: The main article
        related_articles: List of related articles
        analysis: Analysis of relationships
        
    Returns:
        Plotly figure as JSON
    """
    # Create graph
    G = nx.Graph()
    
    # Add main article node
    main_id = str(main_article.get("id", "main"))
    main_title = main_article.get("title", "Main Article")
    G.add_node(main_id, title=main_title, type="main")
    
    # Add related article nodes and edges
    connections = analysis.get("connections", [])
    for article in related_articles:
        article_id = str(article.get("id", "unknown"))
        article_title = article.get("title", "Unknown")
        
        # Find connection details
        connection = next((c for c in connections if str(c.get("article_id")) == article_id), None)
        
        # Add node
        G.add_node(article_id, title=article_title, type="related")
        
        # Add edge with connection details
        edge_attrs = {"weight": 1}
        if connection:
            strength = connection.get("strength", "").lower()
            if strength == "strong":
                edge_attrs["weight"] = 3
            elif strength == "medium":
                edge_attrs["weight"] = 2
            
            edge_attrs["connection_type"] = connection.get("connection_type", "")
        
        G.add_edge(main_id, article_id, **edge_attrs)
    
    # Create positions
    pos = nx.spring_layout(G)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Create node traces
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Node text
        node_attrs = G.nodes[node]
        node_text.append(node_attrs.get("title", node))
        
        # Node color
        if node_attrs.get("type") == "main":
            node_color.append('#ff5733')  # Red for main article
        else:
            node_color.append('#4287f5')  # Blue for related articles
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=False,
            color=node_color,
            size=15,
            line=dict(width=2, color='#fff')
        )
    )
    
    # Create figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text=f"Relationships for: {main_title}",
                font=dict(size=16)
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='#222',
            paper_bgcolor='#222',
            font=dict(color='#fff')
        )
    )
    
    return fig.to_dict() 