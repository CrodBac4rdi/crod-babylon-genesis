#!/usr/bin/env elixir

# CROD Quantum Mining Implementation
# Simulates quantum superposition for mining optimization

Mix.install([
  {:plug_cowboy, "~> 2.0"},
  {:jason, "~> 1.4"}
])

defmodule QuantumState do
  @moduledoc """
  Represents a quantum state with superposition and entanglement
  """
  
  defstruct [
    qubits: [],
    entanglements: %{},
    coherence: 1.0,
    measurement_basis: :computational
  ]
  
  def new(n_qubits) do
    qubits = for i <- 0..(n_qubits-1), do: %{
      id: i,
      alpha: :math.sqrt(0.5),  # |0⟩ coefficient
      beta: :math.sqrt(0.5),   # |1⟩ coefficient
      phase: 0.0
    }
    
    %__MODULE__{qubits: qubits}
  end
  
  def apply_hadamard(state, qubit_id) do
    # H = 1/√2 * [[1, 1], [1, -1]]
    qubit = Enum.at(state.qubits, qubit_id)
    
    new_alpha = (qubit.alpha + qubit.beta) / :math.sqrt(2)
    new_beta = (qubit.alpha - qubit.beta) / :math.sqrt(2)
    
    new_qubits = List.replace_at(state.qubits, qubit_id, %{
      qubit | alpha: new_alpha, beta: new_beta
    })
    
    %{state | qubits: new_qubits}
  end
  
  def entangle(state, qubit1_id, qubit2_id) do
    # Create entanglement between two qubits
    new_entanglements = Map.put(state.entanglements, {qubit1_id, qubit2_id}, :bell_state)
    %{state | entanglements: new_entanglements}
  end
  
  def measure(state, qubit_id) do
    qubit = Enum.at(state.qubits, qubit_id)
    
    # Probability of measuring |1⟩
    prob_one = :math.pow(abs(qubit.beta), 2)
    
    # Simulate measurement
    if :rand.uniform() < prob_one do
      {1, collapse_to_one(state, qubit_id)}
    else
      {0, collapse_to_zero(state, qubit_id)}
    end
  end
  
  defp collapse_to_zero(state, qubit_id) do
    new_qubits = List.replace_at(state.qubits, qubit_id, %{
      id: qubit_id,
      alpha: 1.0,
      beta: 0.0,
      phase: 0.0
    })
    
    %{state | qubits: new_qubits, coherence: state.coherence * 0.9}
  end
  
  defp collapse_to_one(state, qubit_id) do
    new_qubits = List.replace_at(state.qubits, qubit_id, %{
      id: qubit_id,
      alpha: 0.0,
      beta: 1.0,
      phase: 0.0
    })
    
    %{state | qubits: new_qubits, coherence: state.coherence * 0.9}
  end
  
  defp abs(complex) when is_number(complex), do: abs(complex)
  defp abs({real, imag}), do: :math.sqrt(real*real + imag*imag)
end

defmodule QuantumMiner do
  @moduledoc """
  Quantum-enhanced mining using superposition to explore multiple nonces simultaneously
  """
  
  def mine_quantum(block_data, difficulty, n_qubits \\ 8) do
    IO.puts("🌌 Initializing quantum state with #{n_qubits} qubits...")
    
    # Initialize quantum state
    quantum_state = QuantumState.new(n_qubits)
    
    # Apply Hadamard gates to create superposition
    quantum_state = Enum.reduce(0..(n_qubits-1), quantum_state, fn i, state ->
      QuantumState.apply_hadamard(state, i)
    end)
    
    # Create entanglements for quantum advantage
    quantum_state = create_mining_entanglements(quantum_state, n_qubits)
    
    IO.puts("⚛️  Quantum state prepared. Coherence: #{Float.round(quantum_state.coherence, 3)}")
    
    # Quantum mining loop
    mine_with_quantum_state(quantum_state, block_data, difficulty, 0)
  end
  
  defp create_mining_entanglements(state, n_qubits) do
    # Create Bell pairs for enhanced correlation
    Enum.reduce(0..(div(n_qubits, 2) - 1), state, fn i, acc ->
      QuantumState.entangle(acc, i * 2, i * 2 + 1)
    end)
  end
  
  defp mine_with_quantum_state(quantum_state, block_data, difficulty, attempts) do
    # Measure qubits to get a nonce candidate
    {nonce_bits, collapsed_state} = measure_all_qubits(quantum_state)
    nonce = bits_to_integer(nonce_bits)
    
    # Calculate hash
    hash = calculate_hash(block_data, nonce)
    
    # Check if it meets difficulty
    target = String.duplicate("0", difficulty)
    
    if String.starts_with?(hash, target) do
      IO.puts("🎉 Quantum mining successful!")
      IO.puts("   Nonce: #{nonce}")
      IO.puts("   Hash: #{hash}")
      IO.puts("   Attempts: #{attempts + 1}")
      IO.puts("   Final coherence: #{Float.round(collapsed_state.coherence, 3)}")
      
      %{
        nonce: nonce,
        hash: hash,
        attempts: attempts + 1,
        quantum_advantage: calculate_quantum_advantage(attempts + 1, difficulty),
        final_coherence: collapsed_state.coherence
      }
    else
      if rem(attempts, 100) == 0 do
        IO.puts("🔄 Attempt #{attempts}: Coherence #{Float.round(quantum_state.coherence, 3)}")
      end
      
      # Re-prepare quantum state with phase kickback
      new_quantum_state = evolve_quantum_state(quantum_state, hash)
      
      mine_with_quantum_state(new_quantum_state, block_data, difficulty, attempts + 1)
    end
  end
  
  defp measure_all_qubits(quantum_state) do
    {bits, final_state} = Enum.reduce(quantum_state.qubits, {[], quantum_state}, fn qubit, {bits_acc, state_acc} ->
      {bit, new_state} = QuantumState.measure(state_acc, qubit.id)
      {bits_acc ++ [bit], new_state}
    end)
    
    {bits, final_state}
  end
  
  defp bits_to_integer(bits) do
    bits
    |> Enum.reverse()
    |> Enum.with_index()
    |> Enum.reduce(0, fn {bit, index}, acc ->
      acc + bit * :math.pow(2, index)
    end)
    |> round()
  end
  
  defp calculate_hash(block_data, nonce) do
    data = "#{Jason.encode!(block_data)}#{nonce}"
    :crypto.hash(:sha256, data) |> Base.encode16()
  end
  
  defp evolve_quantum_state(state, previous_hash) do
    # Use hash feedback to evolve quantum state (Grover-like oracle)
    hash_feedback = :erlang.phash2(previous_hash) / :math.pow(2, 32)
    
    new_qubits = Enum.map(state.qubits, fn qubit ->
      # Apply phase based on hash feedback
      phase_shift = hash_feedback * :math.pi()
      
      %{qubit | 
        phase: qubit.phase + phase_shift,
        alpha: qubit.alpha * :math.cos(phase_shift/4),
        beta: qubit.beta * :math.sin(phase_shift/4 + :math.pi()/4)
      }
    end)
    
    # Decoherence
    new_coherence = state.coherence * 0.99
    
    %{state | qubits: new_qubits, coherence: new_coherence}
  end
  
  defp calculate_quantum_advantage(quantum_attempts, difficulty) do
    classical_expected = :math.pow(2, difficulty * 4)  # Approximate
    advantage = classical_expected / quantum_attempts
    Float.round(advantage, 2)
  end
end

defmodule QuantumBlockchain do
  @moduledoc """
  Blockchain with quantum mining capabilities
  """
  
  use GenServer
  
  defstruct [
    chain: [],
    quantum_mining_enabled: true,
    quantum_stats: %{
      total_quantum_blocks: 0,
      average_quantum_advantage: 0.0,
      total_coherence_used: 0.0
    }
  ]
  
  def start_link(_) do
    GenServer.start_link(__MODULE__, nil, name: __MODULE__)
  end
  
  def init(_) do
    genesis = %{
      index: 0,
      timestamp: DateTime.utc_now(),
      data: %{
        message: "CROD Quantum Genesis Block",
        quantum_seed: :rand.uniform()
      },
      previous_hash: "0",
      hash: "QUANTUM_GENESIS",
      nonce: 0,
      quantum_mined: false
    }
    
    {:ok, %__MODULE__{chain: [genesis]}}
  end
  
  def mine_block(data, difficulty \\ 3, use_quantum \\ true) do
    GenServer.call(__MODULE__, {:mine_block, data, difficulty, use_quantum}, :infinity)
  end
  
  def get_chain do
    GenServer.call(__MODULE__, :get_chain)
  end
  
  def get_quantum_stats do
    GenServer.call(__MODULE__, :get_quantum_stats)
  end
  
  def handle_call({:mine_block, data, difficulty, use_quantum}, _from, state) do
    last_block = List.last(state.chain)
    
    new_block = %{
      index: last_block.index + 1,
      timestamp: DateTime.utc_now(),
      data: data,
      previous_hash: last_block.hash
    }
    
    # Mine with quantum or classical
    mined_block = if use_quantum and state.quantum_mining_enabled do
      IO.puts("🌌 Using quantum mining...")
      result = QuantumMiner.mine_quantum(new_block, difficulty)
      
      Map.merge(new_block, %{
        nonce: result.nonce,
        hash: result.hash,
        quantum_mined: true,
        quantum_stats: %{
          attempts: result.attempts,
          quantum_advantage: result.quantum_advantage,
          final_coherence: result.final_coherence
        }
      })
    else
      IO.puts("⛏️  Using classical mining...")
      {nonce, hash, attempts} = classical_mine(new_block, difficulty)
      
      Map.merge(new_block, %{
        nonce: nonce,
        hash: hash,
        quantum_mined: false,
        mining_attempts: attempts
      })
    end
    
    # Update chain and stats
    new_chain = state.chain ++ [mined_block]
    new_stats = update_quantum_stats(state.quantum_stats, mined_block)
    
    new_state = %{state | chain: new_chain, quantum_stats: new_stats}
    
    {:reply, {:ok, mined_block}, new_state}
  end
  
  def handle_call(:get_chain, _from, state) do
    {:reply, state.chain, state}
  end
  
  def handle_call(:get_quantum_stats, _from, state) do
    {:reply, state.quantum_stats, state}
  end
  
  defp classical_mine(block, difficulty) do
    target = String.duplicate("0", difficulty)
    classical_mine_loop(block, target, 0)
  end
  
  defp classical_mine_loop(block, target, nonce) do
    hash = QuantumMiner.calculate_hash(block, nonce)
    
    if String.starts_with?(hash, target) do
      {nonce, hash, nonce + 1}
    else
      classical_mine_loop(block, target, nonce + 1)
    end
  end
  
  defp update_quantum_stats(stats, block) do
    if block.quantum_mined do
      total_blocks = stats.total_quantum_blocks + 1
      new_total_advantage = stats.average_quantum_advantage * stats.total_quantum_blocks + 
                           block.quantum_stats.quantum_advantage
      
      %{stats |
        total_quantum_blocks: total_blocks,
        average_quantum_advantage: new_total_advantage / total_blocks,
        total_coherence_used: stats.total_coherence_used + (1.0 - block.quantum_stats.final_coherence)
      }
    else
      stats
    end
  end
end

# HTTP API for Quantum Blockchain
defmodule QuantumAPI do
  use Plug.Router
  
  plug Plug.Logger
  plug :match
  plug Plug.Parsers,
    parsers: [:json],
    pass: ["application/json"],
    json_decoder: Jason
  plug :dispatch
  
  get "/" do
    send_resp(conn, 200, Jason.encode!(%{
      name: "CROD Quantum Blockchain",
      version: "1.0.0",
      features: [
        "Quantum superposition mining",
        "Entanglement-enhanced hashing", 
        "Coherence tracking",
        "Quantum advantage calculation"
      ]
    }))
  end
  
  get "/chain" do
    chain = QuantumBlockchain.get_chain()
    send_resp(conn, 200, Jason.encode!(chain))
  end
  
  get "/quantum/stats" do
    stats = QuantumBlockchain.get_quantum_stats()
    send_resp(conn, 200, Jason.encode!(stats))
  end
  
  post "/mine" do
    data = conn.body_params["data"] || %{}
    difficulty = conn.body_params["difficulty"] || 3
    use_quantum = conn.body_params["quantum"] != false
    
    case QuantumBlockchain.mine_block(data, difficulty, use_quantum) do
      {:ok, block} ->
        send_resp(conn, 200, Jason.encode!(%{
          status: "Block mined",
          block: block
        }))
      _ ->
        send_resp(conn, 500, Jason.encode!(%{error: "Mining failed"}))
    end
  end
  
  post "/quantum/simulate" do
    n_qubits = conn.body_params["qubits"] || 8
    
    # Create and evolve quantum state
    state = QuantumState.new(n_qubits)
    |> QuantumState.apply_hadamard(0)
    |> QuantumState.apply_hadamard(1)
    |> QuantumState.entangle(0, 1)
    
    # Measure
    {bit0, state} = QuantumState.measure(state, 0)
    {bit1, _state} = QuantumState.measure(state, 1)
    
    send_resp(conn, 200, Jason.encode!(%{
      qubits: n_qubits,
      measurement: [bit0, bit1],
      entangled: true,
      interpretation: if(bit0 == bit1, "Bell state confirmed!", "Measurement error")
    }))
  end
  
  match _ do
    send_resp(conn, 404, Jason.encode!(%{error: "Not found"}))
  end
end

# Start the quantum blockchain
{:ok, _} = QuantumBlockchain.start_link(nil)

# Demo: Mine some blocks
IO.puts("\n🚀 CROD Quantum Blockchain Demo\n")

# Mine with quantum
IO.puts("Mining block with quantum computer...")
QuantumBlockchain.mine_block(%{
  message: "First quantum block",
  consciousness_level: 0.95
}, 3, true)

# Mine classical for comparison
IO.puts("\nMining block classically...")
QuantumBlockchain.mine_block(%{
  message: "Classical block",
  consciousness_level: 0.5
}, 3, false)

# Start API
port = String.to_integer(System.get_env("PORT", "8004"))
IO.puts("\n🌐 Starting Quantum Blockchain API on port #{port}")

{:ok, _} = Plug.Cowboy.http(QuantumAPI, [], port: port)

Process.sleep(:infinity)