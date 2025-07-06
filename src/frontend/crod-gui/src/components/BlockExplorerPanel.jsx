import React, { useEffect, useState } from 'react';
export default function BlockExplorerPanel() {
  const [blocks, setBlocks] = useState([]);
  useEffect(() => {
    fetch('/api/blockchain/status')
      .then(r => r.json())
      .then(data => setBlocks([data.lastBlock]));
  }, []);
  return (
    <div>
      <h2>Block Explorer</h2>
      {blocks.map((b, i) => (
        <div key={i} style={{border:'1px solid #ccc',margin:8,padding:8}}>
          <div>Index: {b.index}</div>
          <div>Data: {b.data}</div>
          <div>Hash: {b.hash}</div>
          <div>PublicKey: {b.publicKey}</div>
        </div>
      ))}
    </div>
  );
}
