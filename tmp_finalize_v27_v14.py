import json

# Read the generated particle data
with open('c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/particle_data.js', 'r') as f:
    data_content = f.read().replace('window.PARTICLE_DATA = ', '').rstrip(';')
    particle_data = json.loads(data_content)

html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BOLT — Industrial Particle Engine V27.12.2 FINAL</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');
        :root {{ --bg: #000; --pink: #fa02ea; --cyan: #00e3fd; --emerald: #b0ff00; --accent: var(--cyan); }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; cursor: none; }}
        body {{ background: var(--bg); color: #fff; font-family: 'Space Grotesk', sans-serif; height: 100vh; overflow: hidden; }}
        #webgl-container {{ position: fixed; inset: 0; z-index: 1; }}
        #loader {{ position: fixed; inset: 0; z-index: 100; background: #000; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 20px; transition: opacity 1s; }}
        .loading-bar {{ width: 200px; height: 1px; background: rgba(255,255,255,0.1); position: relative; }}
        .loading-progress {{ position: absolute; left: 0; top: 0; height: 100%; background: var(--accent); width: 100%; }}
        #canvas-ui {{ position: fixed; inset: 0; pointer-events: none; z-index: 10; padding: 40px; display: flex; flex-direction: column; justify-content: space-between; }}
        .brand {{ font-size: 24px; font-weight: 700; letter-spacing: 0.5em; color: var(--accent); transition: color 0.8s; text-shadow: 0 0 20px var(--accent); }}
        .nav {{ position: fixed; bottom: 60px; left: 50%; transform: translateX(-50%); display: flex; gap: 50px; z-index: 20; pointer-events: auto; }}
        .btn {{ display: flex; flex-direction: column; align-items: center; gap: 12px; text-decoration: none; opacity: 0.3; transition: 0.5s; font-size: 11px; letter-spacing: 0.4em; color: #fff; }}
        .btn:hover, .btn.active {{ opacity: 1; transform: translateY(-5px); }}
        .dot {{ width: 4px; height: 4px; border-radius: 50%; background: #fff; transition: 0.3s; }}
        .btn:hover .dot {{ background: var(--accent); box-shadow: 0 0 10px var(--accent); transform: scale(2); }}
        #cursor {{ position: fixed; width: 14px; height: 14px; border: 1px solid var(--accent); border-radius: 50%; pointer-events: none; z-index: 1000; transform: translate(-50%, -50%); }}
    </style>
</head>
<body>
    <div id="cursor"></div>
    <div id="loader">
        <div style="letter-spacing: 0.5em; font-size: 12px; margin-bottom: 20px;">SYSTEM INITIALIZING...</div>
        <div class="loading-bar"><div class="loading-progress"></div></div>
    </div>
    <div id="webgl-container"></div>
    <div id="canvas-ui">
        <div class="header" style="display:flex; justify-content:space-between;">
            <div class="brand">BOLT</div>
            <div style="font-size: 10px; opacity:0.4; letter-spacing:0.2em;">SYSTEM V27.12.2 // AUTONOMOUS GPU ENGINE</div>
        </div>
        <div style="font-size: 8px; opacity: 0.2; letter-spacing: 0.3em; display: flex; justify-content: space-between;">
            <div>LCID: BOLT-ULTRA-HD</div><div>STATUS: GPU_SHADER_MORPH_ACTIVE</div>
        </div>
    </div>
    <nav class="nav">
        <a href="#" class="btn" onmouseenter="morph('cyan')"> <div class="dot"></div><span>LISTEN</span> </a>
        <a href="#" class="btn" onmouseenter="morph('pink')"> <div class="dot"></div><span>SPEAK</span> </a>
        <a href="#" class="btn" onmouseenter="morph('emerald')"> <div class="dot"></div><span>MOVE</span> </a>
    </nav>

    <script id="vShader" type="x-shader/x-vertex">
        attribute vec3 aTarget;
        attribute vec3 aColor;
        varying vec3 vColor;
        uniform float uProgress;
        uniform float uTime;
        void main() {{
            vColor = aColor;
            vec3 pos = mix(position, aTarget, uProgress);
            pos.y += sin(uTime * 2.0 + pos.x * 5.0) * 0.03 * (1.0 - uProgress);
            vec4 mvPos = modelViewMatrix * vec4(pos, 1.0);
            gl_PointSize = 3.5 * (1.0 / -mvPos.z);
            gl_Position = projectionMatrix * mvPos;
        }}
    </script>
    <script id="fShader" type="x-shader/x-fragment">
        varying vec3 vColor;
        void main() {{
            if (length(gl_PointCoord - vec2(0.5)) > 0.5) discard;
            gl_FragColor = vec4(vColor, 1.0);
        }}
    </script>

    <script>
        const PARTICLE_DATA = {json.dumps(particle_data)};
        const COLORS_HEX = {{ cyan: '#00e3fd', pink: '#fa02ea', emerald: '#b0ff00' }};
        const COLORS_RGB = {{
            cyan: new THREE.Color('#00e3fd'),
            pink: new THREE.Color('#fa02ea'),
            emerald: new THREE.Color('#b0ff00')
        }};
        let scene, camera, renderer, material, geometry, points, currentKey = '';
        const COUNT = 10000;

        window.onload = () => {{
            init();
            setTimeout(() => {{
                document.getElementById('loader').style.opacity = '0';
                setTimeout(() => document.getElementById('loader').style.display = 'none', 1000);
            }}, 800);
        }};

        function init() {{
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 100);
            camera.position.z = 1.3;

            renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            document.getElementById('webgl-container').appendChild(renderer.domElement);

            geometry = new THREE.BufferGeometry();
            const pos = new Float32Array(COUNT * 3);
            for(let i=0; i<COUNT*3; i++) pos[i] = (Math.random()-0.5) * 4.0;
            
            geometry.setAttribute('position', new THREE.BufferAttribute(pos, 3));
            geometry.setAttribute('aTarget', new THREE.BufferAttribute(new Float32Array(COUNT * 3), 3));
            geometry.setAttribute('aColor', new THREE.BufferAttribute(new Float32Array(COUNT * 3), 3));

            material = new THREE.ShaderMaterial({{
                vertexShader: document.getElementById('vShader').textContent,
                fragmentShader: document.getElementById('fShader').textContent,
                uniforms: {{ uProgress: {{ value: 0 }}, uTime: {{ value: 0 }} }},
                transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
            }});

            points = new THREE.Points(geometry, material);
            scene.add(points);
            morph('cyan');
            animate();
        }}

        function morph(key) {{
            if (currentKey === key) return;
            const prevKey = currentKey;
            currentKey = key;
            document.documentElement.style.setProperty('--accent', COLORS_HEX[key]);

            const targetData = new Float32Array(PARTICLE_DATA[key]);
            const colorData = new Float32Array(COUNT * 3);
            const col = COLORS_RGB[key];
            for(let i=0; i<COUNT; i++) {{
                colorData[i*3] = col.r; colorData[i*3+1] = col.g; colorData[i*3+2] = col.b;
            }}

            if (prevKey) {{
                const cur = geometry.attributes.position.array;
                const tar = geometry.attributes.aTarget.array;
                const prg = material.uniforms.uProgress.value;
                for(let i=0; i<COUNT*3; i++) cur[i] = cur[i] + (tar[i] - cur[i]) * prg;
                geometry.attributes.position.needsUpdate = true;
            }}

            geometry.attributes.aTarget.array.set(targetData);
            geometry.attributes.aTarget.needsUpdate = true;
            geometry.attributes.aColor.array.set(colorData);
            geometry.attributes.aColor.needsUpdate = true;

            material.uniforms.uProgress.value = 0;
            gsap.to(material.uniforms.uProgress, {{ value: 1, duration: 2.2, ease: "power4.out" }});
        }}

        function animate(time) {{
            material.uniforms.uTime.value = time / 1000;
            renderer.render(scene, camera);
            requestAnimationFrame(animate);
        }}

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        document.addEventListener('mousemove', (e) => {{
            gsap.to('#cursor', {{ x: e.clientX, y: e.clientY, duration: 0.1 }});
            gsap.to(points.rotation, {{ y: (e.clientX/window.innerWidth - 0.5) * 0.1, x: (e.clientY/window.innerHeight - 0.5) * 0.1, duration: 1.5 }});
        }});
    </script>
</body>
</html>"""

with open('c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/MASTER_INDEX_V27.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Autonomous HTML V27.12.2 generated successfully.")
