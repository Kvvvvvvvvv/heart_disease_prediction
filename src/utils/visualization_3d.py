"""
3D Heart Visualization with Risk-Based Mapping
Uses Plotly for interactive 3D visualization
"""
import plotly.graph_objects as go
import numpy as np

def create_3d_heart_visualization(risk_score, patient_data=None):
    """
    Create a 3D heart visualization based on risk score
    
    Parameters:
    -----------
    risk_score : float
        Risk score between 0 and 1
    patient_data : dict, optional
        Patient data for highlighting specific conditions
    
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        Interactive 3D visualization
    """
    
    # Determine risk level
    if risk_score < 0.3:
        risk_level = "LOW"
        heart_color = "rgb(255, 192, 203)"  # Pink
        artery_color = "rgb(200, 200, 200)"  # Gray
        glow_intensity = 0.1
    elif risk_score < 0.6:
        risk_level = "MODERATE"
        heart_color = "rgb(255, 255, 0)"  # Yellow
        artery_color = "rgb(255, 200, 0)"  # Yellow-orange
        glow_intensity = 0.3
    else:
        risk_level = "HIGH"
        heart_color = "rgb(255, 0, 0)"  # Red
        artery_color = "rgb(139, 0, 0)"  # Dark red
        glow_intensity = 0.6
    
    # Create heart shape (simplified 3D ellipsoid)
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x_heart = 1.2 * np.outer(np.cos(u), np.sin(v))
    y_heart = 1.0 * np.outer(np.sin(u), np.sin(v))
    z_heart = 0.8 * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Create coronary arteries (tubes)
    t = np.linspace(0, 2*np.pi, 50)
    artery_radius = 0.15
    
    # Left coronary artery
    x_artery_l = 0.5 + artery_radius * np.cos(t)
    y_artery_l = 0.3 + artery_radius * np.sin(t)
    z_artery_l = np.linspace(-0.3, 0.3, len(t))
    
    # Right coronary artery
    x_artery_r = -0.5 + artery_radius * np.cos(t)
    y_artery_r = 0.3 + artery_radius * np.sin(t)
    z_artery_r = np.linspace(-0.3, 0.3, len(t))
    
    # Create figure
    fig = go.Figure()
    
    # Add heart surface
    fig.add_trace(go.Surface(
        x=x_heart,
        y=y_heart,
        z=z_heart,
        colorscale=[[0, heart_color], [1, heart_color]],
        showscale=False,
        opacity=0.8,
        name="Heart"
    ))
    
    # Add coronary arteries
    if patient_data:
        # Highlight arteries if high LDL or high calcium score
        highlight_arteries = False
        if patient_data.get('chol', 0) > 240:  # High cholesterol
            highlight_arteries = True
            artery_color = "rgb(255, 100, 0)"  # Orange-red
        
        fig.add_trace(go.Scatter3d(
            x=x_artery_l,
            y=y_artery_l,
            z=z_artery_l,
            mode='lines',
            line=dict(color=artery_color, width=8),
            name="Coronary Arteries"
        ))
        
        fig.add_trace(go.Scatter3d(
            x=x_artery_r,
            y=y_artery_r,
            z=z_artery_r,
            mode='lines',
            line=dict(color=artery_color, width=8),
            showlegend=False
        ))
    
    # Add glow effect for high risk
    if risk_level == "HIGH":
        # Add multiple transparent layers for glow
        for i in range(3):
            scale = 1 + (i+1) * 0.1
            fig.add_trace(go.Surface(
                x=x_heart * scale,
                y=y_heart * scale,
                z=z_heart * scale,
                colorscale=[[0, heart_color], [1, heart_color]],
                showscale=False,
                opacity=glow_intensity / (i+2),
                name=f"Glow {i+1}"
            ))
    
    # Add markers for specific conditions
    if patient_data:
        # Low ejection fraction marker
        if patient_data.get('thalach', 0) < 120:  # Low max heart rate as proxy
            fig.add_trace(go.Scatter3d(
                x=[0],
                y=[0.5],
                z=[0],
                mode='markers',
                marker=dict(size=15, color='blue', symbol='diamond'),
                name="Low EF Indicator"
            ))
        
        # High troponin marker (using oldpeak as proxy)
        if patient_data.get('oldpeak', 0) > 2.0:
            fig.add_trace(go.Scatter3d(
                x=[0.3],
                y=[0.3],
                z=[0.2],
                mode='markers',
                marker=dict(size=12, color='red', symbol='x'),
                name="ST Depression Alert"
            ))
    
    # Update layout
    fig.update_layout(
        title=f"3D Heart Visualization - Risk Level: {risk_level} ({risk_score:.1%})",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            bgcolor="rgb(10, 10, 20)",
            xaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
            yaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
            zaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=800,
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig, risk_level

def get_risk_level(risk_score):
    """Convert risk score to risk level"""
    if risk_score < 0.3:
        return "LOW"
    elif risk_score < 0.6:
        return "MODERATE"
    else:
        return "HIGH"
