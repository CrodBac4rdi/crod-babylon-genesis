import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter';

interface ThreeDStudioProps {
  onSubmit: (creation: any) => void;
}

const ThreeDStudio: React.FC<ThreeDStudioProps> = ({ onSubmit }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const [selectedTool, setSelectedTool] = useState<string>('cube');
  const [gpuInfo, setGpuInfo] = useState<string>('');
  const [creationName, setCreationName] = useState<string>('');
  const [innovations, setInnovations] = useState<string[]>([]);

  useEffect(() => {
    if (!mountRef.current) return;

    // Initialize Three.js scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a1a);
    sceneRef.current = scene;

    // Camera
    const camera = new THREE.PerspectiveCamera(
      75,
      mountRef.current.clientWidth / mountRef.current.clientHeight,
      0.1,
      1000
    );
    camera.position.set(5, 5, 5);

    // Renderer with GPU detection
    const renderer = new THREE.WebGLRenderer({ 
      antialias: true,
      powerPreference: "high-performance"
    });
    renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    mountRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Check GPU capabilities
    const gl = renderer.getContext();
    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
    if (debugInfo) {
      const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
      const gpuRenderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
      setGpuInfo(`GPU: ${vendor} ${gpuRenderer}`);
    }

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    // Grid
    const gridHelper = new THREE.GridHelper(20, 20);
    scene.add(gridHelper);

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // Handle resize
    const handleResize = () => {
      if (!mountRef.current) return;
      camera.aspect = mountRef.current.clientWidth / mountRef.current.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      mountRef.current?.removeChild(renderer.domElement);
      renderer.dispose();
    };
  }, []);

  const addPrimitive = (type: string) => {
    if (!sceneRef.current) return;

    let geometry: THREE.BufferGeometry;
    let material = new THREE.MeshStandardMaterial({ 
      color: Math.random() * 0xffffff,
      metalness: 0.7,
      roughness: 0.3
    });

    switch (type) {
      case 'cube':
        geometry = new THREE.BoxGeometry(1, 1, 1);
        break;
      case 'sphere':
        geometry = new THREE.SphereGeometry(0.5, 32, 32);
        break;
      case 'cylinder':
        geometry = new THREE.CylinderGeometry(0.5, 0.5, 1, 32);
        break;
      case 'torus':
        geometry = new THREE.TorusGeometry(0.5, 0.2, 16, 100);
        break;
      case 'cone':
        geometry = new THREE.ConeGeometry(0.5, 1, 32);
        break;
      default:
        geometry = new THREE.BoxGeometry(1, 1, 1);
    }

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(
      (Math.random() - 0.5) * 5,
      Math.random() * 3,
      (Math.random() - 0.5) * 5
    );
    mesh.castShadow = true;
    mesh.receiveShadow = true;

    sceneRef.current.add(mesh);

    // Track if this is innovative
    if (!innovations.includes(type)) {
      setInnovations([...innovations, type]);
    }
  };

  const generateProceduralObject = () => {
    if (!sceneRef.current) return;

    // Create a procedural shape using parametric equations
    const geometry = new THREE.BufferGeometry();
    const vertices = [];
    const colors = [];

    const count = 10000;
    for (let i = 0; i < count; i++) {
      const t = i / count * Math.PI * 4;
      const x = Math.sin(t) * Math.cos(t * 3) * 2;
      const y = Math.cos(t) * 2;
      const z = Math.sin(t * 5) * 2;

      vertices.push(x, y, z);
      colors.push(Math.random(), Math.random(), Math.random());
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.05,
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      transparent: true,
      opacity: 0.8
    });

    const points = new THREE.Points(geometry, material);
    sceneRef.current.add(points);

    setInnovations([...innovations, 'procedural']);
  };

  const createParticleSystem = () => {
    if (!sceneRef.current) return;

    const particleCount = 5000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const velocities = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 10;
      positions[i + 1] = Math.random() * 10;
      positions[i + 2] = (Math.random() - 0.5) * 10;

      velocities[i] = (Math.random() - 0.5) * 0.02;
      velocities[i + 1] = Math.random() * 0.02;
      velocities[i + 2] = (Math.random() - 0.5) * 0.02;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));

    const material = new THREE.PointsMaterial({
      color: 0x88ccff,
      size: 0.05,
      blending: THREE.AdditiveBlending,
      transparent: true,
      opacity: 0.6,
      map: new THREE.TextureLoader().load('/particle.png')
    });

    const particles = new THREE.Points(geometry, material);
    sceneRef.current.add(particles);

    // Animate particles
    const animateParticles = () => {
      const positions = particles.geometry.attributes.position.array as Float32Array;
      const velocities = particles.geometry.attributes.velocity.array as Float32Array;

      for (let i = 0; i < particleCount * 3; i += 3) {
        positions[i] += velocities[i];
        positions[i + 1] += velocities[i + 1];
        positions[i + 2] += velocities[i + 2];

        if (positions[i + 1] > 10) {
          positions[i + 1] = 0;
        }
      }

      particles.geometry.attributes.position.needsUpdate = true;
      requestAnimationFrame(animateParticles);
    };

    animateParticles();
    setInnovations([...innovations, 'particles']);
  };

  const exportScene = async () => {
    if (!sceneRef.current) return;

    const exporter = new GLTFExporter();
    
    exporter.parse(
      sceneRef.current,
      (gltf) => {
        // Calculate innovation score based on complexity
        const objectCount = sceneRef.current!.children.length;
        const uniqueTools = innovations.length;
        const complexity = objectCount * uniqueTools;

        const creation = {
          type: '3d' as const,
          title: creationName || `3D Creation ${Date.now()}`,
          data: {
            gltf: gltf,
            stats: {
              objects: objectCount,
              vertices: calculateVertices(sceneRef.current!),
              innovations: innovations,
              gpuUsed: gpuInfo.includes('NVIDIA') || gpuInfo.includes('AMD'),
              techniques: innovations
            }
          },
          domains: ['3d', 'graphics', 'art'],
          technical_features: innovations.includes('procedural') ? ['new_algorithm'] : []
        };

        onSubmit(creation);
      },
      { binary: false }
    );
  };

  const calculateVertices = (scene: THREE.Scene): number => {
    let totalVertices = 0;
    scene.traverse((child) => {
      if (child instanceof THREE.Mesh && child.geometry) {
        const geo = child.geometry;
        if (geo.attributes.position) {
          totalVertices += geo.attributes.position.count;
        }
      }
    });
    return totalVertices;
  };

  return (
    <div className="three-d-studio">
      <div className="studio-header">
        <h2>🎨 3D Studio (GPU: {gpuInfo || 'Detecting...'})</h2>
        <input
          type="text"
          placeholder="Creation name..."
          value={creationName}
          onChange={(e) => setCreationName(e.target.value)}
        />
        <button onClick={exportScene} className="export-btn">
          💾 Submit Creation
        </button>
      </div>
      
      <div className="studio-layout">
        <div className="tools-panel">
          <h3>Primitives</h3>
          <button onClick={() => addPrimitive('cube')}>🟦 Cube</button>
          <button onClick={() => addPrimitive('sphere')}>🔵 Sphere</button>
          <button onClick={() => addPrimitive('cylinder')}>🟩 Cylinder</button>
          <button onClick={() => addPrimitive('torus')}>🟡 Torus</button>
          <button onClick={() => addPrimitive('cone')}>🔺 Cone</button>
          
          <h3>Advanced</h3>
          <button onClick={generateProceduralObject}>🌀 Procedural</button>
          <button onClick={createParticleSystem}>✨ Particles</button>
          
          <h3>Innovations Used</h3>
          <ul>
            {innovations.map((inn, idx) => (
              <li key={idx}>✅ {inn}</li>
            ))}
          </ul>
        </div>
        
        <div className="viewport" ref={mountRef} />
      </div>
    </div>
  );
};

export default ThreeDStudio;