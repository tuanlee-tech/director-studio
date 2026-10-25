import React from "react";
import { Canvas } from "@react-three/fiber";
import { Physics, RigidBody } from "@react-three/rapier";
import { Environment, Float, Text3D, Center } from "@react-three/drei";

function GoldCoin({ position }: { position: [number, number, number] }) {
  return (
    <RigidBody restitution={0.7} position={position} colliders="cylinder">
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[1, 1, 0.2, 32]} />
        <meshStandardMaterial
          color="#FFD700"
          metalness={0.9}
          roughness={0.1}
          emissive="#FF8C00"
          emissiveIntensity={0.2}
        />
      </mesh>
    </RigidBody>
  );
}

export const CoinPhysics3D: React.FC = () => {
  const coins = Array.from({ length: 25 }, (_, i) => ({
    x: (Math.random() - 0.5) * 6,
    y: 8 + i * 1.5,
    z: (Math.random() - 0.5) * 4,
  }));

  return (
    <div style={{ width: "100%", height: "100%", backgroundColor: "#020617" }}>
      <Canvas camera={{ position: [0, 4, 12], fov: 45 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 15, 10]} intensity={1.5} />
        <Environment preset="city" />

        <Physics gravity={[0, -9.81, 0]}>
          {/* Ground */}
          <RigidBody type="fixed" position={[0, -2, 0]}>
            <mesh>
              <boxGeometry args={[20, 0.5, 20]} />
              <meshStandardMaterial color="#1E293B" metalness={0.5} roughness={0.2} />
            </mesh>
          </RigidBody>

          {/* Falling Coins */}
          {coins.map((c, idx) => (
            <GoldCoin key={idx} position={[c.x, c.y, c.z]} />
          ))}
        </Physics>
      </Canvas>
    </div>
  );
};
