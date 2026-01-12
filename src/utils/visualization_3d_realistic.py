"""
Realistic 3D Heart Visualization using Three.js
Based on additional_3dimg_format.html structure
Creates an HTML component that can be embedded in Streamlit
"""
import json

def create_realistic_3d_heart_html(risk_score, patient_data=None):
    """
    Create realistic 3D heart visualization HTML using Three.js
    
    Parameters:
    -----------
    risk_score : float
        Risk score between 0 and 1
    patient_data : dict, optional
        Patient data for visualization
    
    Returns:
    --------
    html_content : str
        Complete HTML with embedded Three.js visualization
    """
    
    # Default patient data if not provided
    if patient_data is None:
        patient_data = {}
    
    # Map UCI dataset features to visualization parameters
    # Since UCI dataset doesn't have all fields, we'll map what we have
    chol = patient_data.get('chol', 200)
    oldpeak = patient_data.get('oldpeak', 1.0)
    thalach = patient_data.get('thalach', 150)
    exang = patient_data.get('exang', 0)
    cp = patient_data.get('cp', 0)
    
    # Calculate derived metrics for visualization
    ldl_estimate = chol * 0.6  # Rough estimate (LDL ~60% of total cholesterol)
    calcium_score = 0 if chol < 200 else min((chol - 200) / 2, 400)
    ejection_fraction = max(50, 70 - (oldpeak * 5))  # Estimate based on ST depression
    st_depression = oldpeak
    hrv_estimate = max(20, 50 - (oldpeak * 10))  # Estimate HRV
    troponin = 0.01 if exang == 1 and oldpeak > 1.5 else 0.0
    crp = 1.0 if chol > 240 else 0.5
    bnp = 50 if thalach < 120 else 30
    
    # Determine risk level
    if risk_score < 0.3:
        risk_level = "LOW"
    elif risk_score < 0.6:
        risk_level = "MODERATE"
    else:
        risk_level = "HIGH"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Heart Visualization</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #0c0c2e;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        #container {{
            width: 100%;
            height: 600px;
            min-height: 600px;
            position: relative;
            overflow: hidden;
            background: #0c0c2e;
        }}
        #viewer {{
            width: 100%;
            height: 100%;
            min-height: 600px;
            display: block;
            position: absolute;
            top: 0;
            left: 0;
        }}
        #info {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: #e0e0ff;
            background: rgba(10, 10, 30, 0.8);
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 12px;
            z-index: 100;
            border: 1px solid rgba(100, 150, 255, 0.3);
            pointer-events: none;
        }}
        .risk-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: bold;
            margin-left: 10px;
        }}
        .risk-LOW {{ background: #4caf50; color: white; }}
        .risk-MODERATE {{ background: #ff9800; color: white; }}
        .risk-HIGH {{ background: #f44336; color: white; }}
    </style>
</head>
<body>
    <div id="container">
        <div id="viewer"></div>
        <div id="info">
            Risk Level: <span class="risk-badge risk-{risk_level}">{risk_level}</span>
            <br>Risk Score: {(risk_score*100):.1f}%
        </div>
    </div>
    
    <script>
        // Configuration
        const config = {{
            riskScore: {risk_score},
            riskLevel: "{risk_level}",
            patientData: {json.dumps({
                'ldl': ldl_estimate,
                'calciumScore': calcium_score,
                'ejectionFraction': ejection_fraction,
                'stDepression': st_depression,
                'hrv': hrv_estimate,
                'troponin': troponin,
                'crp': crp,
                'bnp': bnp,
                'smoking': 0,
                'wallMotionAbnormality': oldpeak > 2.0
            })}
        }};
        
        // Wait for Three.js to load and DOM to be ready
        function initVisualization() {{
            if (typeof THREE === 'undefined') {{
                setTimeout(initVisualization, 100);
                return;
            }}
            
            const container = document.getElementById('viewer');
            if (!container) {{
                setTimeout(initVisualization, 100);
                return;
            }}
            
            // Get container dimensions (use fixed size for Streamlit iframe)
            const width = container.offsetWidth || container.clientWidth || 800;
            const height = container.offsetHeight || container.clientHeight || 600;
            
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0c0c2e);
            
            const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
            camera.position.set(0, 0, 12);
            
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(width, height);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(renderer.domElement);
            
            // Lighting
            const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
            scene.add(ambientLight);
            
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(5, 5, 5);
            scene.add(directionalLight);
            
            const pointLight = new THREE.PointLight(0x4fc3f7, 1, 100);
            pointLight.position.set(-5, 5, 5);
            scene.add(pointLight);
            
            // Heart components storage
            const heartComponents = {{
                chambers: {{}},
                coronaries: {{}},
                electrical: {{}},
                arteries: {{}}
            }};
        
        // Materials
        const materials = {{
            normal: new THREE.MeshPhongMaterial({{
                color: 0xc62828,
                shininess: 30,
                transparent: true,
                opacity: 0.9
            }}),
            stressed: new THREE.MeshPhongMaterial({{
                color: 0xd32f2f,
                shininess: 30,
                emissive: 0x220000,
                transparent: true,
                opacity: 0.9
            }}),
            highRisk: new THREE.MeshPhongMaterial({{
                color: 0xb71c1c,
                shininess: 30,
                emissive: 0x440000,
                transparent: true,
                opacity: 0.9
            }}),
            coronaryNormal: new THREE.MeshPhongMaterial({{
                color: 0xff5252,
                shininess: 50
            }}),
            coronaryRisky: new THREE.MeshPhongMaterial({{
                color: 0xff9800,
                shininess: 50,
                emissive: 0x331100
            }}),
            coronaryHighRisk: new THREE.MeshPhongMaterial({{
                color: 0xff5722,
                shininess: 50,
                emissive: 0x441100
            }}),
            electricalNormal: new THREE.MeshPhongMaterial({{
                color: 0x4fc3f7,
                emissive: 0x004444,
                transparent: true,
                opacity: 0.8
            }}),
            electricalAbnormal: new THREE.MeshPhongMaterial({{
                color: 0xbb86fc,
                emissive: 0x440044,
                transparent: true,
                opacity: 0.8
            }})
        }};
        
        // Create heart model
        function createHeartModel() {{
            const heartGroup = new THREE.Group();
            
            // Left Ventricle
            const leftVentricle = new THREE.Mesh(
                new THREE.SphereGeometry(2.5, 32, 32),
                materials.normal.clone()
            );
            leftVentricle.scale.set(1, 1.3, 0.9);
            leftVentricle.position.set(-1, -1.5, 0);
            heartComponents.chambers.leftVentricle = leftVentricle;
            heartGroup.add(leftVentricle);
            
            // Right Ventricle
            const rightVentricle = new THREE.Mesh(
                new THREE.SphereGeometry(2, 32, 32),
                materials.normal.clone()
            );
            rightVentricle.scale.set(1, 1.2, 0.85);
            rightVentricle.position.set(1.2, -1.3, 0.3);
            heartComponents.chambers.rightVentricle = rightVentricle;
            heartGroup.add(rightVentricle);
            
            // Left Atrium
            const leftAtrium = new THREE.Mesh(
                new THREE.SphereGeometry(1.5, 32, 32),
                materials.normal.clone()
            );
            leftAtrium.position.set(-1.5, 1, -0.5);
            heartComponents.chambers.leftAtrium = leftAtrium;
            heartGroup.add(leftAtrium);
            
            // Right Atrium
            const rightAtrium = new THREE.Mesh(
                new THREE.SphereGeometry(1.3, 32, 32),
                materials.normal.clone()
            );
            rightAtrium.position.set(1.5, 1, 0);
            heartComponents.chambers.rightAtrium = rightAtrium;
            heartGroup.add(rightAtrium);
            
            // Aorta
            const aorta = new THREE.Mesh(
                new THREE.CylinderGeometry(0.6, 0.5, 4, 16),
                new THREE.MeshPhongMaterial({{ color: 0xff4444, shininess: 50 }})
            );
            aorta.position.set(-1, 2.5, -0.3);
            aorta.rotation.z = 0.3;
            heartComponents.arteries.aorta = aorta;
            heartGroup.add(aorta);
            
            // Coronary Arteries
            createCoronaryArteries(heartGroup);
            
            // Electrical System
            createElectricalSystem(heartGroup);
            
            return heartGroup;
        }}
        
        function createCoronaryArteries(parent) {{
            // Left Anterior Descending (LAD)
            const ladPath = new THREE.CatmullRomCurve3([
                new THREE.Vector3(-1, 1, 1),
                new THREE.Vector3(-2, 0, 1.5),
                new THREE.Vector3(-2.5, -1, 1),
                new THREE.Vector3(-2, -2, 0.5)
            ]);
            const lad = new THREE.Mesh(
                new THREE.TubeGeometry(ladPath, 20, 0.15, 8, false),
                materials.coronaryNormal.clone()
            );
            heartComponents.coronaries.lad = lad;
            parent.add(lad);
            
            // Right Coronary Artery (RCA)
            const rcaPath = new THREE.CatmullRomCurve3([
                new THREE.Vector3(1, 1, 1),
                new THREE.Vector3(2, 0, 1.2),
                new THREE.Vector3(2.3, -1, 0.8),
                new THREE.Vector3(1.5, -2, 0.3)
            ]);
            const rca = new THREE.Mesh(
                new THREE.TubeGeometry(rcaPath, 20, 0.15, 8, false),
                materials.coronaryNormal.clone()
            );
            heartComponents.coronaries.rca = rca;
            parent.add(rca);
            
            // Circumflex Artery
            const circPath = new THREE.CatmullRomCurve3([
                new THREE.Vector3(-1.5, 0.5, 0),
                new THREE.Vector3(-2.5, 0, 0),
                new THREE.Vector3(-3, -0.5, 0),
                new THREE.Vector3(-2.5, -1, 0)
            ]);
            const circ = new THREE.Mesh(
                new THREE.TubeGeometry(circPath, 16, 0.12, 8, false),
                materials.coronaryNormal.clone()
            );
            heartComponents.coronaries.circ = circ;
            parent.add(circ);
        }}
        
        function createElectricalSystem(parent) {{
            // SA Node
            const saNode = new THREE.Mesh(
                new THREE.SphereGeometry(0.15, 16, 16),
                materials.electricalNormal.clone()
            );
            saNode.position.set(0, 2, 0);
            heartComponents.electrical.saNode = saNode;
            parent.add(saNode);
            
            // AV Node
            const avNode = new THREE.Mesh(
                new THREE.SphereGeometry(0.12, 16, 16),
                materials.electricalNormal.clone()
            );
            avNode.position.set(0, 0, 0.5);
            heartComponents.electrical.avNode = avNode;
            parent.add(avNode);
            
            // Bundle of His
            const bundlePath = new THREE.CatmullRomCurve3([
                new THREE.Vector3(0, 0, 0.5),
                new THREE.Vector3(0, -1, 0.5),
                new THREE.Vector3(0, -2, 0.3)
            ]);
            const bundle = new THREE.Mesh(
                new THREE.TubeGeometry(bundlePath, 12, 0.08, 8, false),
                materials.electricalNormal.clone()
            );
            heartComponents.electrical.bundle = bundle;
            parent.add(bundle);
        }}
        
        // Update visualization based on risk
        function updateVisualization() {{
            const riskScore = config.riskScore;
            const pd = config.patientData;
            
            // Global Risk State
            let heartColor, emissiveIntensity;
            if (riskScore < 0.3) {{
                heartColor = new THREE.Color(0xc62828); // Normal red
                emissiveIntensity = 0;
            }} else if (riskScore < 0.6) {{
                heartColor = new THREE.Color(0xd32f2f); // Brighter red
                emissiveIntensity = 0.1;
            }} else {{
                heartColor = new THREE.Color(0xb71c1c); // Dark red
                emissiveIntensity = 0.3;
            }}
            
            // Apply to chambers
            Object.values(heartComponents.chambers).forEach(chamber => {{
                chamber.material.color = heartColor;
                chamber.material.emissive = new THREE.Color(emissiveIntensity, 0, 0);
                chamber.material.needsUpdate = true;
            }});
            
            // Coronary Arteries
            let coronaryColor, coronaryEmissive;
            if (pd.ldl > 160 || pd.calciumScore > 100) {{
                coronaryColor = new THREE.Color(0xff5722); // Orange-red
                coronaryEmissive = 0.4;
            }} else if (pd.ldl > 130 || pd.calciumScore > 50) {{
                coronaryColor = new THREE.Color(0xff9800); // Orange
                coronaryEmissive = 0.2;
            }} else {{
                coronaryColor = new THREE.Color(0xff5252); // Light red
                coronaryEmissive = 0;
            }}
            
            Object.values(heartComponents.coronaries).forEach(artery => {{
                artery.material.color = coronaryColor;
                artery.material.emissive = new THREE.Color(coronaryEmissive * 0.5, 0, 0);
                artery.material.needsUpdate = true;
            }});
            
            // Electrical System
            let electricalColor;
            if (pd.stDepression > 1 || pd.hrv < 20) {{
                electricalColor = new THREE.Color(0xbb86fc); // Purple (abnormal)
            }} else {{
                electricalColor = new THREE.Color(0x4fc3f7); // Cyan (normal)
            }}
            
            Object.values(heartComponents.electrical).forEach(component => {{
                component.material.color = electricalColor;
                component.material.needsUpdate = true;
            }});
            
            // Chamber function (ejection fraction)
            if (pd.ejectionFraction < 45) {{
                heartComponents.chambers.leftVentricle.material.opacity = 0.6;
                heartComponents.chambers.leftVentricle.material.emissive = new THREE.Color(0.2, 0, 0);
            }}
            
            // Biochemical markers
            if (pd.troponin > 0.04) {{
                const marker = new THREE.Mesh(
                    new THREE.SphereGeometry(0.15, 8, 8),
                    new THREE.MeshBasicMaterial({{ color: 0xff0000 }})
                );
                marker.position.set(-1, -2, 1);
                scene.add(marker);
            }}
        }}
        
        // Create heart
        const heart = createHeartModel();
        scene.add(heart);
        
        // Update visualization
        updateVisualization();
        
        // Animation
        let heartBeatPhase = 0;
        function animate() {{
            requestAnimationFrame(animate);
            
            // Heartbeat animation
            heartBeatPhase += 0.05;
            const pulse = 1 + Math.sin(heartBeatPhase) * 0.05;
            heart.scale.set(pulse, pulse, pulse);
            
            // Slow rotation
            heart.rotation.y += 0.002;
            
            renderer.render(scene, camera);
        }}
        animate();
        
        // Mouse controls
        let isDragging = false;
        let previousMousePosition = {{ x: 0, y: 0 }};
        
        container.addEventListener('mousedown', (e) => {{
            isDragging = true;
            previousMousePosition = {{ x: e.clientX, y: e.clientY }};
        }});
        
        container.addEventListener('mousemove', (e) => {{
            if (isDragging) {{
                const deltaMove = {{
                    x: e.clientX - previousMousePosition.x,
                    y: e.clientY - previousMousePosition.y
                }};
                heart.rotation.y += deltaMove.x * 0.01;
                heart.rotation.x += deltaMove.y * 0.01;
                previousMousePosition = {{ x: e.clientX, y: e.clientY }};
            }}
        }});
        
        container.addEventListener('mouseup', () => {{
            isDragging = false;
        }});
        
        // Resize handler is already set up above
    </script>
</body>
</html>
"""
    
    return html_content

def get_risk_level(risk_score):
    """Convert risk score to risk level"""
    if risk_score < 0.3:
        return "LOW"
    elif risk_score < 0.6:
        return "MODERATE"
    else:
        return "HIGH"
