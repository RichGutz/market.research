import json
import base64
import os

def get_b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

# Assets
cyan_b64 = get_b64('c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_hd_v12.png')
pink_b64 = get_b64('c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/pink_hd_v12.png')
emerald_b64 = get_b64('c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/emerald_hd_v12.png')

# Particles
with open('c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/particle_data.js', 'r') as f:
    data_js = f.read().replace('window.PARTICLE_DATA = ', '').rstrip(';')
    particle_data = json.loads(data_js)

html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BOLT — Universal Surgical Engine V27.18</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');
        :root {{ --bg: #000; --pink: #fa02ea; --cyan: #00e3fd; --emerald: #b0ff00; --accent: var(--cyan); }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; cursor: none; }}
        body {{ background: var(--bg); color: #fff; font-family: 'Space Grotesk', sans-serif; height: 100vh; overflow: hidden; }}
        #webgl-container {{ position: fixed; inset: 0; z-index: 1; background: #000; }}
        #canvas-ui {{ position: fixed; inset: 0; pointer-events: none; z-index: 10; padding: 40px; display: flex; flex-direction: column; justify-content: space-between; }}
        .brand {{ font-size: 24px; font-weight: 700; letter-spacing: 0.5em; color: var(--accent); transition: color 0.8s; text-shadow: 0 0 20px var(--accent); }}
        .nav {{ position: fixed; bottom: 60px; left: 50%; transform: translateX(-50%); display: flex; gap: 50px; z-index: 20; pointer-events: auto; }}
        .btn {{ display: flex; flex-direction: column; align-items: center; gap: 12px; text-decoration: none; opacity: 0.3; transition: 0.5s; font-size: 11px; letter-spacing: 0.4em; color: #fff; }}
        .btn:hover, .btn.active {{ opacity: 1; transform: translateY(-5px); }}
        .dot {{ width: 4px; height: 4px; border-radius: 50%; background: #fff; transition: 0.3s; }}
        .btn:hover .dot {{ background: var(--accent); box-shadow: 0 0 10px var(--accent); transform: scale(2); }}
        #cursor {{ position: fixed; width: 14px; height: 14px; border: 1px solid var(--accent); border-radius: 50%; pointer-events: none; z-index: 1000; transform: translate(-50%, -50%); }}
        #loader {{ position: fixed; inset: 0; z-index: 100; background: #000; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 20px; transition: opacity 1s; }}
    </style>
</head>
<body>
    <div id="cursor"></div>
    <div id="loader"><div style="letter-spacing: 0.5em; font-size: 10px;">INITIALIZING UNIVERSAL ENGINE...</div></div>
    <div id="webgl-container"></div>
    <div id="canvas-ui">
        <div class="header" style="display:flex; justify-content:space-between;">
            <div class="brand">BOLT</div>
            <div style="font-size: 10px; opacity:0.4; letter-spacing:0.2em;">SYSTEM V27.18 // UNIVERSAL AUTONOMOUS ENGINE</div>
        </div>
        <div style="font-size: 8px; opacity: 0.2; letter-spacing: 0.3em; display: flex; justify-content: space-between;">
            <div>LCID: BOLT-SURGICAL-ULTRA</div><div>STATUS: GPU_AUTONOMOUS_ACTIVE</div>
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
        varying float vAlpha;
        uniform float uProgress;
        uniform float uTime;
        uniform float uGlobalAlpha;
        void main() {{
            vColor = aColor;
            vAlpha = uGlobalAlpha;
            vec3 pos = mix(position, aTarget, uProgress);
            pos.y += sin(uTime * 3.0 + pos.x * 5.0) * 0.02 * (1.0 - uProgress);
            vec4 mvPos = modelViewMatrix * vec4(pos, 1.0);
            gl_PointSize = 4.0 * (1.0 / -mvPos.z);
            gl_Position = projectionMatrix * mvPos;
        }}
    </script>
    <script id="fShader" type="x-shader/x-fragment">
        varying vec3 vColor;
        varying float vAlpha;
        void main() {{
            if (length(gl_PointCoord - vec2(0.5)) > 0.5) discard;
            gl_FragColor = vec4(vColor, vAlpha);
        }}
    </script>

    <script>
        const PARTICLE_DATA = {json.dumps(particle_data)};
        const ASSET_B64 = {{
            cyan: "{cyan_b64}",
            pink: "{pink_b64}",
            emerald: "{emerald_b64}"
        }};
        const COLORS_HEX = {{ cyan: '#00e3fd', pink: '#fa02ea', emerald: '#b0ff00' }};
        const COLORS_RGB = {{ cyan: new THREE.Color('#00e3fd'), pink: new THREE.Color('#fa02ea'), emerald: new THREE.Color('#b0ff00') }};
        let scene, camera, renderer, material, geometry, points, sprites = {{}}, currentKey = '';
        const COUNT = 10000;

        async function init() {{
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 100);
            camera.position.z = 1.35;

            renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            document.getElementById('webgl-container').appendChild(renderer.domElement);

            const loader = new THREE.TextureLoader();
            for(let key in ASSET_B64) {{
                const tex = await loader.loadAsync(ASSET_B64[key]);
                const mat = new THREE.SpriteMaterial({{ map: tex, transparent: true, opacity: 0 }});
                const spr = new THREE.Sprite(mat);
                spr.scale.set(1.42, 1.42, 1);
                spr.visible = false;
                scene.add(spr);
                sprites[key] = spr;
            }}

            geometry = new THREE.BufferGeometry();
            const pos = new Float32Array(COUNT * 3);
            for(let i=0; i<COUNT*3; i++) pos[i] = (Math.random()-0.5) * 5.0;
            
            geometry.setAttribute('position', new THREE.BufferAttribute(pos, 3));
            geometry.setAttribute('aTarget', new THREE.BufferAttribute(new Float32Array(COUNT * 3), 3));
            geometry.setAttribute('aColor', new THREE.BufferAttribute(new Float32Array(COUNT * 3), 3));

            material = new THREE.ShaderMaterial({{
                vertexShader: document.getElementById('vShader').textContent,
                fragmentShader: document.getElementById('fShader').textContent,
                uniforms: {{ uProgress: {{ value: 0 }}, uTime: {{ value: 0 }}, uGlobalAlpha: {{ value: 1.0 }} }},
                transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
            }});

            points = new THREE.Points(geometry, material);
            scene.add(points);
            
            document.getElementById('loader').style.opacity = '0';
            setTimeout(() => document.getElementById('loader').style.display = 'none', 1000);
            
            morph('cyan');
            animate();
        }}

        function morph(key) {{
            if (currentKey === key) return;
            const prevKey = currentKey;
            currentKey = key;
            document.documentElement.style.setProperty('--accent', COLORS_HEX[key]);

            Object.values(sprites).forEach(s => {{ s.visible = false; s.material.opacity = 0; }});
            points.visible = true;
            gsap.to(material.uniforms.uGlobalAlpha, {{ value: 1.0, duration: 0.3 }});

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
            gsap.to(material.uniforms.uProgress, {{ 
                value: 1, duration: 1.8, ease: "power4.out",
                onComplete: () => {{
                    sprites[key].visible = true;
                    gsap.to(sprites[key].material, {{ opacity: 1.0, duration: 0.5 }});
                    gsap.to(material.uniforms.uGlobalAlpha, {{ value: 0, duration: 0.3, onComplete: () => {{ points.visible = false; }}}});
                }}
            }});
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
            const rx = (e.clientX/window.innerWidth - 0.5) * 0.1;
            const ry = (e.clientY/window.innerHeight - 0.5) * 0.1;
            gsap.to(points.rotation, {{ y: rx, x: ry, duration: 1.5 }});
            Object.values(sprites).forEach(s => gsap.to(s.rotation, {{ z: rx * 0.3, duration: 2 }}));
        }});

        init();
    </script>
</body>
</html>"""

with open('c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/MASTER_INDEX_V27.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("Universal Autonomous HTML V27.18 generated successfully.")
