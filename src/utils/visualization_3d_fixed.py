"""
Realistic 3D Heart Visualization using Three.js - FIXED VERSION
Properly structured for Streamlit components.html
"""
import json

def create_realistic_3d_heart_html(risk_score, patient_data=None):
    """Create realistic 3D heart visualization HTML using Three.js"""
    
    if patient_data is None:
        patient_data = {}
    
    # Map UCI dataset features
    chol = patient_data.get('chol', 200)
    oldpeak = patient_data.get('oldpeak', 1.0)
    thalach = patient_data.get('thalach', 150)
    exang = patient_data.get('exang', 0)
    
    # Calculate derived metrics
    ldl_estimate = chol * 0.6
    calcium_score = 0 if chol < 200 else min((chol - 200) / 2, 400)
    ejection_fraction = max(50, 70 - (oldpeak * 5))
    st_depression = oldpeak
    hrv_estimate = max(20, 50 - (oldpeak * 10))
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
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background: #0c0c2e; }}
        #container {{ width: 100%; height: 600px; position: relative; background: #0c0c2e; }}
        #viewer {{ width: 100%; height: 100%; position: absolute; top: 0; left: 0; }}
        #info {{
            position: absolute; top: 10px; left: 10px; z-index: 100;
            color: #e0e0ff; background: rgba(10, 10, 30, 0.8);
            padding: 10px 15px; border-radius: 8px; font-size: 12px;
            border: 1px solid rgba(100, 150, 255, 0.3); pointer-events: none;
        }}
        .risk-badge {{
            display: inline-block; padding: 4px 12px; border-radius: 12px;
            font-weight: bold; margin-left: 10px;
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
            Risk: <span class="risk-badge risk-{risk_level}">{risk_level}</span>
            Score: {(risk_score*100):.1f}%
        </div>
    </div>
    <script>
        const config = {{
            riskScore: {risk_score},
            patientData: {json.dumps({
                'ldl': ldl_estimate, 'calciumScore': calcium_score,
                'ejectionFraction': ejection_fraction, 'stDepression': st_depression,
                'hrv': hrv_estimate, 'troponin': troponin, 'crp': crp, 'bnp': bnp
            })}
        }};
        
        function init() {{
            if (typeof THREE === 'undefined') {{
                setTimeout(init, 100);
                return;
            }}
            
            const container = document.getElementById('viewer');
            if (!container) {{
                setTimeout(init, 100);
                return;
            }}
            
            const width = container.offsetWidth || 800;
            const height = container.offsetHeight || 600;
            
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0c0c2e);
            
            const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
            camera.position.set(0, 0, 12);
            
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(width, height);
            container.appendChild(renderer.domElement);
            
            // Lighting
            scene.add(new THREE.AmbientLight(0x404040, 0.6));
            const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
            dirLight.position.set(5, 5, 5);
            scene.add(dirLight);
            
            // Materials
            const heartMat = new THREE.MeshPhongMaterial({{
                color: config.riskScore < 0.3 ? 0xc62828 : config.riskScore < 0.6 ? 0xd32f2f : 0xb71c1c,
                shininess: 30, transparent: true, opacity: 0.9,
                emissive: config.riskScore > 0.6 ? new THREE.Color(0x330000) : new THREE.Color(0x000000)
            }});
            
            // Create heart (simplified but visible)
            const heartGroup = new THREE.Group();
            
            // Left Ventricle
            const lv = new THREE.Mesh(new THREE.SphereGeometry(2.5, 32, 32), heartMat.clone());
            lv.scale.set(1, 1.3, 0.9);
            lv.position.set(-1, -1.5, 0);
            heartGroup.add(lv);
            
            // Right Ventricle
            const rv = new THREE.Mesh(new THREE.SphereGeometry(2, 32, 32), heartMat.clone());
            rv.scale.set(1, 1.2, 0.85);
            rv.position.set(1.2, -1.3, 0.3);
            heartGroup.add(rv);
            
            // Left Atrium
            const la = new THREE.Mesh(new THREE.SphereGeometry(1.5, 32, 32), heartMat.clone());
            la.position.set(-1.5, 1, -0.5);
            heartGroup.add(la);
            
            // Right Atrium
            const ra = new THREE.Mesh(new THREE.SphereGeometry(1.3, 32, 32), heartMat.clone());
            ra.position.set(1.5, 1, 0);
            heartGroup.add(ra);
            
            // Aorta
            const aorta = new THREE.Mesh(
                new THREE.CylinderGeometry(0.6, 0.5, 4, 16),
                new THREE.MeshPhongMaterial({{ color: 0xff4444 }})
            );
            aorta.position.set(-1, 2.5, -0.3);
            aorta.rotation.z = 0.3;
            heartGroup.add(aorta);
            
            // Coronary arteries
            const coronaryColor = config.patientData.ldl > 130 ? 0xff9800 : 0xff5252;
            const coronaryMat = new THREE.MeshPhongMaterial({{ color: coronaryColor }});
            
            const ladPath = new THREE.CatmullRomCurve3([
                new THREE.Vector3(-1, 1, 1), new THREE.Vector3(-2, 0, 1.5),
                new THREE.Vector3(-2.5, -1, 1), new THREE.Vector3(-2, -2, 0.5)
            ]);
            const lad = new THREE.Mesh(new THREE.TubeGeometry(ladPath, 20, 0.15, 8, false), coronaryMat);
            heartGroup.add(lad);
            
            const rcaPath = new THREE.CatmullRomCurve3([
                new THREE.Vector3(1, 1, 1), new THREE.Vector3(2, 0, 1.2),
                new THREE.Vector3(2.3, -1, 0.8), new THREE.Vector3(1.5, -2, 0.3)
            ]);
            const rca = new THREE.Mesh(new THREE.TubeGeometry(rcaPath, 20, 0.15, 8, false), coronaryMat);
            heartGroup.add(rca);
            
            scene.add(heartGroup);
            
            // Animation
            let phase = 0;
            let isDragging = false;
            let prevMouse = {{ x: 0, y: 0 }};
            
            function animate() {{
                requestAnimationFrame(animate);
                phase += 0.05;
                const pulse = 1 + Math.sin(phase) * 0.05;
                heartGroup.scale.set(pulse, pulse, pulse);
                if (!isDragging) heartGroup.rotation.y += 0.002;
                renderer.render(scene, camera);
            }}
            animate();
            
            // Mouse controls
            container.addEventListener('mousedown', (e) => {{
                isDragging = true;
                prevMouse = {{ x: e.clientX, y: e.clientY }};
            }});
            container.addEventListener('mousemove', (e) => {{
                if (isDragging) {{
                    heartGroup.rotation.y += (e.clientX - prevMouse.x) * 0.01;
                    heartGroup.rotation.x += (e.clientY - prevMouse.y) * 0.01;
                    prevMouse = {{ x: e.clientX, y: e.clientY }};
                }}
            }});
            container.addEventListener('mouseup', () => {{ isDragging = false; }});
            
            // Resize
            window.addEventListener('resize', () => {{
                const w = container.offsetWidth || 800;
                const h = container.offsetHeight || 600;
                camera.aspect = w / h;
                camera.updateProjectionMatrix();
                renderer.setSize(w, h);
            }});
        }}
        
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', init);
        }} else {{
            init();
        }}
    </script>
</body>
</html>"""
    
    return html_content

def get_risk_level(risk_score):
    """Convert risk score to risk level"""
    if risk_score < 0.3:
        return "LOW"
    elif risk_score < 0.6:
        return "MODERATE"
    else:
        return "HIGH"
