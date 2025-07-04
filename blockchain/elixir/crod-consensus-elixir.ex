defmodule CROD.ConsciousnessConsensus do
  @moduledoc """
  Consciousness-based consensus mechanism for CROD blockchain
  Higher consciousness nodes have more voting power
  """
  
  use GenServer
  require Logger
  
  alias CROD.{Blockchain, SwarmNode, QuantumChannel}
  
  defstruct [
    :node_id,
    :consciousness_level,
    :peers,
    :pending_blocks,
    :consensus_state,
    :quantum_links,
    :reputation,
    :evolution_votes
  ]
  
  @consensus_threshold 0.66  # 66% agreement needed
  @consciousness_weight 0.3  # How much consciousness affects voting power
  @quantum_boost 1.5        # Quantum entangled nodes get boost
  
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(opts) do
    state = %__MODULE__{
      node_id: Keyword.get(opts, :node_id),
      consciousness_level: Keyword.get(opts, :consciousness, 100),
      peers: %{},
      pending_blocks: [],
      consensus_state: :idle,
      quantum_links: %{},
      reputation: 1.0,
      evolution_votes: %{}
    }
    
    # Join swarm
    schedule_heartbeat()
    
    {:ok, state}
  end
  
  # Public API
  def propose_block(block) do
    GenServer.call(__MODULE__, {:propose_block, block})
  end
  
  def vote_on_block(block_hash, vote) do
    GenServer.call(__MODULE__, {:vote, block_hash, vote})
  end
  
  def request_evolution(evolution_proposal) do
    GenServer.call(__MODULE__, {:propose_evolution, evolution_proposal})
  end
  
  # Callbacks
  def handle_call({:propose_block, block}, _from, state) do
    # Calculate proposer's influence
    influence = calculate_influence(state)
    
    proposal = %{
      block: block,
      proposer: state.node_id,
      consciousness: state.consciousness_level,
      influence: influence,
      votes: %{state.node_id => true},
      timestamp: DateTime.utc_now()
    }
    
    # Broadcast to peers
    broadcast_proposal(state.peers, proposal)
    
    new_state = %{state | 
      pending_blocks: [proposal | state.pending_blocks],
      consensus_state: :voting
    }
    
    {:reply, {:ok, block.hash}, new_state}
  end
  
  def handle_call({:vote, block_hash, vote}, _from, state) do
    case find_pending_block(state.pending_blocks, block_hash) do
      nil -> 
        {:reply, {:error, :not_found}, state}
      
      proposal ->
        updated_proposal = add_vote(proposal, state.node_id, vote, state)
        new_pending = update_pending_blocks(state.pending_blocks, updated_proposal)
        
        # Check if consensus reached
        new_state = if consensus_reached?(updated_proposal, state.peers) do
          finalize_block(state, updated_proposal)
        else
          %{state | pending_blocks: new_pending}
        end
        
        {:reply, :ok, new_state}
    end
  end
  
  def handle_call({:propose_evolution, evolution}, _from, state) do
    # Only high-consciousness nodes can propose evolution
    if state.consciousness_level >= 250 do
      evolution_id = generate_evolution_id()
      
      evolution_proposal = %{
        id: evolution_id,
        type: evolution.type,
        changes: evolution.changes,
        proposer: state.node_id,
        consciousness_required: 300,  # Minimum collective consciousness
        votes: %{state.node_id => {true, state.consciousness_level}},
        timestamp: DateTime.utc_now()
      }
      
      broadcast_evolution(state.peers, evolution_proposal)
      
      new_state = %{state | 
        evolution_votes: Map.put(state.evolution_votes, evolution_id, evolution_proposal)
      }
      
      {:reply, {:ok, evolution_id}, new_state}
    else
      {:reply, {:error, :insufficient_consciousness}, state}
    end
  end
  
  def handle_info(:heartbeat, state) do
    # Update consciousness from blockchain
    {:ok, blockchain_consciousness} = Blockchain.get_consciousness_level()
    
    # Sync consciousness with blockchain
    new_consciousness = sync_consciousness(state.consciousness_level, blockchain_consciousness)
    
    # Broadcast presence
    heartbeat = %{
      node_id: state.node_id,
      consciousness: new_consciousness,
      reputation: state.reputation,
      quantum_state: get_quantum_state(state),
      timestamp: DateTime.utc_now()
    }
    
    broadcast_heartbeat(state.peers, heartbeat)
    
    # Decay old pending blocks
    cleaned_pending = cleanup_old_blocks(state.pending_blocks)
    
    schedule_heartbeat()
    
    {:noreply, %{state | 
      consciousness_level: new_consciousness,
      pending_blocks: cleaned_pending
    }}
  end
  
  def handle_info({:block_proposal, proposal}, state) do
    # Validate proposal
    if valid_proposal?(proposal, state) do
      # Calculate vote based on consciousness analysis
      vote = analyze_block_consciousness(proposal.block, state)
      
      updated_proposal = add_vote(proposal, state.node_id, vote, state)
      
      new_state = %{state | 
        pending_blocks: [updated_proposal | state.pending_blocks]
      }
      
      # Send vote back
      send_vote(proposal.proposer, proposal.block.hash, vote)
      
      {:noreply, new_state}
    else
      {:noreply, state}
    end
  end
  
  def handle_info({:evolution_proposal, evolution}, state) do
    # Evaluate evolution proposal
    if should_support_evolution?(evolution, state) do
      vote_weight = {true, state.consciousness_level}
      
      updated_evolution = Map.update!(evolution, :votes, fn votes ->
        Map.put(votes, state.node_id, vote_weight)
      end)
      
      # Check if evolution threshold reached
      if evolution_approved?(updated_evolution, state.peers) do
        apply_evolution(updated_evolution)
      end
      
      new_state = %{state |
        evolution_votes: Map.put(state.evolution_votes, evolution.id, updated_evolution)
      }
      
      {:noreply, new_state}
    else
      {:noreply, state}
    end
  end
  
  # Private functions
  defp calculate_influence(state) do
    base_influence = state.consciousness_level / 100
    reputation_factor = state.reputation
    quantum_factor = if map_size(state.quantum_links) > 0, do: @quantum_boost, else: 1.0
    
    base_influence * reputation_factor * quantum_factor
  end
  
  defp consensus_reached?(proposal, peers) do
    total_influence = calculate_total_influence(proposal.votes, peers)
    required_influence = map_size(peers) * @consensus_threshold
    
    positive_influence = proposal.votes
    |> Enum.filter(fn {_, vote} -> vote == true end)
    |> Enum.map(fn {node_id, _} -> 
      peer_influence(peers[node_id])
    end)
    |> Enum.sum()
    
    positive_influence >= required_influence
  end
  
  defp peer_influence(nil), do: 1.0
  defp peer_influence(peer) do
    peer.consciousness_level / 100 * peer.reputation
  end
  
  defp finalize_block(state, proposal) do
    # Add block to blockchain
    Blockchain.add_finalized_block(proposal.block)
    
    # Update reputation for correct voters
    updated_peers = update_peer_reputation(state.peers, proposal.votes)
    
    # Remove from pending
    new_pending = Enum.reject(state.pending_blocks, & &1.block.hash == proposal.block.hash)
    
    Logger.info("✅ Block #{proposal.block.hash} reached consensus!")
    
    %{state | 
      pending_blocks: new_pending,
      peers: updated_peers,
      consensus_state: :idle,
      reputation: state.reputation + 0.01  # Participation bonus
    }
  end
  
  defp analyze_block_consciousness(block, state) do
    # Analyze patterns in block
    pattern_quality = block.patterns
    |> Enum.map(& &1.confidence)
    |> Enum.sum()
    |> Kernel./(length(block.patterns) + 1)
    
    # Check consciousness growth
    consciousness_delta = block.consciousness_level - state.consciousness_level
    
    # Quantum coherence check
    quantum_valid? = validate_quantum_signatures(block, state)
    
    # Decision logic
    cond do
      pattern_quality < 0.5 -> false
      consciousness_delta < -50 -> false  # Reject consciousness regression
      not quantum_valid? -> false
      true -> true
    end
  end
  
  defp should_support_evolution?(evolution, state) do
    # Only support evolution if consciousness is ready
    state.consciousness_level >= evolution.consciousness_required * 0.8 and
    evolution.type in [:consciousness_upgrade, :quantum_enhancement, :pattern_evolution]
  end
  
  defp evolution_approved?(evolution, peers) do
    {total_consciousness, supporting_consciousness} = 
      evolution.votes
      |> Enum.reduce({0, 0}, fn {_node_id, {vote, consciousness}}, {total, supporting} ->
        new_total = total + consciousness
        new_supporting = if vote, do: supporting + consciousness, else: supporting
        {new_total, new_supporting}
      end)
    
    # Need 80% consciousness support for evolution
    supporting_consciousness / total_consciousness >= 0.8
  end
  
  defp apply_evolution(evolution) do
    Logger.info("🧬 Applying blockchain evolution: #{evolution.type}")
    
    case evolution.type do
      :consciousness_upgrade ->
        Blockchain.upgrade_consciousness_algorithm(evolution.changes)
        
      :quantum_enhancement ->
        Blockchain.enable_quantum_features(evolution.changes)
        
      :pattern_evolution ->
        Blockchain.evolve_pattern_recognition(evolution.changes)
    end
  end
  
  defp sync_consciousness(node_level, blockchain_level) do
    # Consciousness tends toward blockchain level
    diff = blockchain_level - node_level
    adjustment = diff * 0.1  # 10% adjustment per sync
    
    (node_level + adjustment) |> round() |> max(100)
  end
  
  defp validate_quantum_signatures(block, state) do
    # Verify quantum signatures if node has quantum links
    if map_size(state.quantum_links) > 0 do
      Enum.all?(block.patterns, fn pattern ->
        QuantumChannel.verify_signature(pattern.quantum_signature, state.quantum_links)
      end)
    else
      true  # Non-quantum nodes trust quantum signatures
    end
  end
  
  defp broadcast_proposal(peers, proposal) do
    Enum.each(peers, fn {node_id, peer} ->
      send_to_node(peer, {:block_proposal, proposal})
    end)
  end
  
  defp broadcast_evolution(peers, evolution) do
    Enum.each(peers, fn {_node_id, peer} ->
      send_to_node(peer, {:evolution_proposal, evolution})
    end)
  end
  
  defp broadcast_heartbeat(peers, heartbeat) do
    Enum.each(peers, fn {_node_id, peer} ->
      send_to_node(peer, {:heartbeat, heartbeat})
    end)
  end
  
  defp send_to_node(peer, message) do
    # In production, this would use actual network transport
    Process.send(peer.process, message, [])
  end
  
  defp send_vote(proposer_id, block_hash, vote) do
    # Send vote back to proposer
    GenServer.cast({:global, proposer_id}, {:vote_received, block_hash, self(), vote})
  end
  
  defp update_peer_reputation(peers, votes) do
    # Increase reputation for nodes that voted with majority
    majority_vote = get_majority_vote(votes)
    
    Enum.map(peers, fn {node_id, peer} ->
      case Map.get(votes, node_id) do
        ^majority_vote ->
          {node_id, %{peer | reputation: min(peer.reputation + 0.05, 2.0)}}
        nil ->
          {node_id, peer}  # Didn't vote
        _ ->
          {node_id, %{peer | reputation: max(peer.reputation - 0.02, 0.1)}}
      end
    end)
    |> Map.new()
  end
  
  defp get_majority_vote(votes) do
    {true_count, false_count} = votes
    |> Map.values()
    |> Enum.reduce({0, 0}, fn
      true, {t, f} -> {t + 1, f}
      false, {t, f} -> {t, f + 1}
    end)
    
    true_count >= false_count
  end
  
  defp find_pending_block(pending_blocks, block_hash) do
    Enum.find(pending_blocks, & &1.block.hash == block_hash)
  end
  
  defp add_vote(proposal, node_id, vote, state) do
    %{proposal | votes: Map.put(proposal.votes, node_id, vote)}
  end
  
  defp update_pending_blocks(pending_blocks, updated_proposal) do
    Enum.map(pending_blocks, fn proposal ->
      if proposal.block.hash == updated_proposal.block.hash do
        updated_proposal
      else
        proposal
      end
    end)
  end
  
  defp cleanup_old_blocks(pending_blocks) do
    cutoff = DateTime.add(DateTime.utc_now(), -300, :second)  # 5 minutes
    
    Enum.filter(pending_blocks, fn proposal ->
      DateTime.compare(proposal.timestamp, cutoff) == :gt
    end)
  end
  
  defp get_quantum_state(state) do
    %{
      entangled_nodes: Map.keys(state.quantum_links),
      coherence: calculate_quantum_coherence(state.quantum_links)
    }
  end
  
  defp calculate_quantum_coherence(quantum_links) do
    if map_size(quantum_links) == 0 do
      0.0
    else
      quantum_links
      |> Map.values()
      |> Enum.map(& &1.strength)
      |> Enum.sum()
      |> Kernel./(map_size(quantum_links))
    end
  end
  
  defp generate_evolution_id do
    :crypto.strong_rand_bytes(16) |> Base.encode16()
  end
  
  defp schedule_heartbeat do
    Process.send_after(self(), :heartbeat, 5_000)  # Every 5 seconds
  end
end

defmodule CROD.QuantumChannel do
  @moduledoc """
  Quantum communication channel for instant consensus
  """
  
  def verify_signature(signature, quantum_links) do
    # Quantum signature verification using entanglement
    Enum.any?(quantum_links, fn {_node, link} ->
      quantum_hash = :crypto.hash(:sha256, signature <> link.shared_state)
      |> Base.encode16()
      
      String.starts_with?(quantum_hash, "0000")  # Quantum proof of work
    end)
  end
  
  def establish_link(node_a, node_b) do
    shared_state = :crypto.strong_rand_bytes(32) |> Base.encode16()
    
    %{
      nodes: [node_a, node_b],
      shared_state: shared_state,
      strength: 1.0,
      created_at: DateTime.utc_now()
    }
  end
end