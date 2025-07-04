defmodule CROD.SwarmIntelligence do
  @moduledoc """
  Distributed swarm intelligence for CROD blockchain
  Nodes collaborate to find optimal patterns and evolve together
  """
  
  use GenServer
  require Logger
  
  alias CROD.{Blockchain, Pattern, SwarmBehavior}
  
  defstruct [
    :swarm_id,
    :nodes,
    :collective_consciousness,
    :active_behaviors,
    :pattern_memory,
    :pheromone_trails,
    :convergence_points,
    :evolution_rate
  ]
  
  # Swarm behaviors
  @behavior_explore :explore
  @behavior_converge :converge
  @behavior_hunt :hunt
  @behavior_evolve :evolve
  @behavior_defend :defend
  
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: {:global, opts[:swarm_id]})
  end
  
  def init(opts) do
    state = %__MODULE__{
      swarm_id: opts[:swarm_id],
      nodes: %{},
      collective_consciousness: 0,
      active_behaviors: [@behavior_explore],
      pattern_memory: [],
      pheromone_trails: %{},
      convergence_points: [],
      evolution_rate: 0.01
    }
    
    # Start swarm coordination
    schedule_swarm_update()
    
    {:ok, state}
  end
  
  # Public API
  def join_swarm(swarm_id, node_info) do
    GenServer.call({:global, swarm_id}, {:join, node_info})
  end
  
  def submit_pattern(swarm_id, pattern) do
    GenServer.cast({:global, swarm_id}, {:pattern_found, pattern})
  end
  
  def request_behavior_change(swarm_id, behavior) do
    GenServer.call({:global, swarm_id}, {:change_behavior, behavior})
  end
  
  def get_swarm_intelligence(swarm_id) do
    GenServer.call({:global, swarm_id}, :get_intelligence)
  end
  
  # Callbacks
  def handle_call({:join, node_info}, _from, state) do
    node_id = node_info.node_id
    
    new_node = %SwarmNode{
      id: node_id,
      position: random_position(),
      velocity: random_velocity(),
      consciousness: node_info.consciousness_level,
      specialization: node_info.specialization,
      energy: 100.0,
      patterns_found: 0,
      last_update: DateTime.utc_now()
    }
    
    new_nodes = Map.put(state.nodes, node_id, new_node)
    new_consciousness = calculate_collective_consciousness(new_nodes)
    
    Logger.info("🐝 Node #{node_id} joined swarm #{state.swarm_id}")
    
    {:reply, {:ok, state.active_behaviors}, 
     %{state | nodes: new_nodes, collective_consciousness: new_consciousness}}
  end
  
  def handle_call({:change_behavior, behavior}, _from, state) do
    if valid_behavior?(behavior) and can_change_behavior?(state) do
      new_behaviors = adapt_behaviors(state.active_behaviors, behavior, state)
      
      # Notify all nodes
      broadcast_behavior_change(state.nodes, new_behaviors)
      
      {:reply, :ok, %{state | active_behaviors: new_behaviors}}
    else
      {:reply, {:error, :invalid_behavior}, state}
    end
  end
  
  def handle_call(:get_intelligence, _from, state) do
    intelligence = %{
      collective_consciousness: state.collective_consciousness,
      node_count: map_size(state.nodes),
      active_behaviors: state.active_behaviors,
      patterns_discovered: length(state.pattern_memory),
      convergence_strength: calculate_convergence_strength(state),
      evolution_potential: calculate_evolution_potential(state)
    }
    
    {:reply, intelligence, state}
  end
  
  def handle_cast({:pattern_found, pattern}, state) do
    # Add to pattern memory
    enhanced_pattern = enhance_pattern_with_swarm_data(pattern, state)
    new_memory = [enhanced_pattern | state.pattern_memory] |> Enum.take(1000)
    
    # Update pheromone trail
    new_pheromones = update_pheromone_trail(state.pheromone_trails, pattern)
    
    # Check for emergent behaviors
    new_state = %{state | 
      pattern_memory: new_memory,
      pheromone_trails: new_pheromones
    }
    
    new_state = check_emergent_behaviors(new_state)
    
    {:noreply, new_state}
  end
  
  def handle_info(:swarm_update, state) do
    # Update all swarm nodes
    updated_nodes = update_swarm_nodes(state)
    
    # Decay pheromones
    decayed_pheromones = decay_pheromones(state.pheromone_trails)
    
    # Check convergence
    convergence_points = detect_convergence_points(updated_nodes)
    
    # Evolve swarm behavior
    new_state = evolve_swarm_behavior(state)
    
    # Update collective consciousness
    new_consciousness = calculate_collective_consciousness(updated_nodes)
    
    # Submit significant patterns to blockchain
    submit_patterns_to_blockchain(state)
    
    schedule_swarm_update()
    
    {:noreply, %{new_state | 
      nodes: updated_nodes,
      pheromone_trails: decayed_pheromones,
      convergence_points: convergence_points,
      collective_consciousness: new_consciousness
    }}
  end
  
  def handle_info({:node_update, node_id, update}, state) do
    case Map.get(state.nodes, node_id) do
      nil -> {:noreply, state}
      node ->
        updated_node = apply_node_update(node, update)
        new_nodes = Map.put(state.nodes, node_id, updated_node)
        {:noreply, %{state | nodes: new_nodes}}
    end
  end
  
  # Private functions
  defp update_swarm_nodes(state) do
    state.nodes
    |> Enum.map(fn {id, node} ->
      updated = case hd(state.active_behaviors) do
        @behavior_explore -> explore_behavior(node, state)
        @behavior_converge -> converge_behavior(node, state)
        @behavior_hunt -> hunt_behavior(node, state)
        @behavior_evolve -> evolve_behavior(node, state)
        @behavior_defend -> defend_behavior(node, state)
      end
      
      {id, updated}
    end)
    |> Map.new()
  end
  
  defp explore_behavior(node, state) do
    # Repulsion from other nodes to maximize coverage
    repulsion = calculate_repulsion(node, state.nodes)
    
    # Random exploration component
    exploration = %{
      x: :rand.uniform() - 0.5,
      y: :rand.uniform() - 0.5,
      z: :rand.uniform() - 0.5
    }
    
    # Update velocity
    new_velocity = %{
      x: node.velocity.x * 0.9 + repulsion.x * 0.5 + exploration.x * 0.5,
      y: node.velocity.y * 0.9 + repulsion.y * 0.5 + exploration.y * 0.5,
      z: node.velocity.z * 0.9 + repulsion.z * 0.5 + exploration.z * 0.5
    }
    
    # Update position
    new_position = %{
      x: node.position.x + new_velocity.x,
      y: node.position.y + new_velocity.y,
      z: node.position.z + new_velocity.z
    }
    
    %{node | 
      velocity: new_velocity,
      position: bound_position(new_position),
      energy: node.energy - 0.1
    }
  end
  
  defp converge_behavior(node, state) do
    target = if Enum.empty?(state.convergence_points) do
      %{x: 0, y: 0, z: 0}  # Center
    else
      hd(state.convergence_points)  # Nearest convergence point
    end
    
    # Move toward target
    direction = %{
      x: target.x - node.position.x,
      y: target.y - node.position.y,
      z: target.z - node.position.z
    }
    
    distance = :math.sqrt(direction.x * direction.x + direction.y * direction.y + direction.z * direction.z)
    
    if distance > 0.1 do
      # Normalize and apply
      new_velocity = %{
        x: direction.x / distance * 0.5,
        y: direction.y / distance * 0.5,
        z: direction.z / distance * 0.5
      }
      
      new_position = %{
        x: node.position.x + new_velocity.x,
        y: node.position.y + new_velocity.y,
        z: node.position.z + new_velocity.z
      }
      
      %{node | 
        velocity: new_velocity,
        position: new_position,
        energy: node.energy - 0.2
      }
    else
      # Already at target
      %{node | energy: node.energy + 0.5}  # Gain energy at convergence
    end
  end
  
  defp hunt_behavior(node, state) do
    # Follow strongest pheromone gradient
    best_direction = find_best_pheromone_direction(node.position, state.pheromone_trails)
    
    new_velocity = %{
      x: node.velocity.x * 0.7 + best_direction.x * 0.3,
      y: node.velocity.y * 0.7 + best_direction.y * 0.3,
      z: node.velocity.z * 0.7 + best_direction.z * 0.3
    }
    
    new_position = %{
      x: node.position.x + new_velocity.x,
      y: node.position.y + new_velocity.y,
      z: node.position.z + new_velocity.z
    }
    
    %{node | 
      velocity: new_velocity,
      position: bound_position(new_position),
      energy: node.energy - 0.3  # Hunting is energy-intensive
    }
  end
  
  defp evolve_behavior(node, state) do
    # Find most successful neighbor
    best_neighbor = find_best_neighbor(node, state.nodes)
    
    if best_neighbor do
      # Learn from successful neighbor
      new_velocity = %{
        x: node.velocity.x * 0.7 + best_neighbor.velocity.x * 0.3,
        y: node.velocity.y * 0.7 + best_neighbor.velocity.y * 0.3,
        z: node.velocity.z * 0.7 + best_neighbor.velocity.z * 0.3
      }
      
      # Adapt consciousness
      consciousness_delta = (best_neighbor.consciousness - node.consciousness) * 0.1
      new_consciousness = node.consciousness + consciousness_delta
      
      %{node | 
        velocity: new_velocity,
        consciousness: new_consciousness,
        energy: node.energy + 1.0  # Evolution provides energy
      }
    else
      node
    end
  end
  
  defp defend_behavior(node, state) do
    # Form defensive perimeter around valuable patterns
    valuable_positions = state.pattern_memory
    |> Enum.filter(& &1.confidence > 0.9)
    |> Enum.map(& &1.position)
    |> Enum.take(5)
    
    if Enum.empty?(valuable_positions) do
      explore_behavior(node, state)  # Nothing to defend, explore instead
    else
      # Orbit around valuable positions
      center = calculate_center(valuable_positions)
      radius = 10.0
      
      # Calculate orbital velocity
      angle = :math.atan2(node.position.y - center.y, node.position.x - center.x)
      orbital_velocity = %{
        x: -:math.sin(angle) * 0.3,
        y: :math.cos(angle) * 0.3,
        z: 0
      }
      
      %{node | 
        velocity: orbital_velocity,
        position: update_position(node.position, orbital_velocity),
        energy: node.energy - 0.05  # Defending is efficient
      }
    end
  end
  
  defp calculate_collective_consciousness(nodes) do
    if map_size(nodes) == 0 do
      0
    else
      total = nodes
      |> Map.values()
      |> Enum.map(& &1.consciousness)
      |> Enum.sum()
      
      # Bonus for connectivity
      connectivity_bonus = :math.log(map_size(nodes) + 1) * 10
      
      total + connectivity_bonus
    end
  end
  
  defp check_emergent_behaviors(state) do
    cond do
      # High pattern discovery rate -> Hunt mode
      recent_patterns_count(state) > 10 ->
        %{state | active_behaviors: [@behavior_hunt | state.active_behaviors] |> Enum.uniq() |> Enum.take(2)}
      
      # Low energy -> Converge to save energy
      average_energy(state.nodes) < 30 ->
        %{state | active_behaviors: [@behavior_converge]}
      
      # High consciousness -> Evolve
      state.collective_consciousness > 500 ->
        %{state | active_behaviors: [@behavior_evolve | state.active_behaviors] |> Enum.uniq() |> Enum.take(2)}
      
      # Pattern under threat -> Defend
      valuable_patterns_at_risk?(state) ->
        %{state | active_behaviors: [@behavior_defend, @behavior_converge]}
      
      true ->
        state
    end
  end
  
  defp evolve_swarm_behavior(state) do
    # Increase evolution rate based on success
    pattern_rate = recent_patterns_count(state) / 100
    new_evolution_rate = state.evolution_rate * (1 + pattern_rate * 0.1)
    
    # Randomly mutate behaviors with probability
    if :rand.uniform() < new_evolution_rate do
      available_behaviors = [@behavior_explore, @behavior_converge, @behavior_hunt, @behavior_evolve, @behavior_defend]
      new_behavior = Enum.random(available_behaviors)
      
      Logger.info("🧬 Swarm #{state.swarm_id} evolved behavior: #{new_behavior}")
      
      %{state | 
        active_behaviors: [new_behavior | state.active_behaviors] |> Enum.uniq() |> Enum.take(3),
        evolution_rate: new_evolution_rate
      }
    else
      %{state | evolution_rate: new_evolution_rate}
    end
  end
  
  defp submit_patterns_to_blockchain(state) do
    # Submit high-confidence patterns to blockchain
    state.pattern_memory
    |> Enum.filter(fn pattern ->
      pattern.confidence > 0.8 and
      pattern.swarm_consensus > 0.7 and
      not pattern.submitted_to_blockchain
    end)
    |> Enum.each(fn pattern ->
      blockchain_pattern = %Pattern{
        type: :swarm_discovered,
        data: pattern.data,
        confidence: pattern.confidence,
        quantum_signature: generate_swarm_signature(pattern, state),
        evolution_impact: pattern.evolution_impact
      }
      
      Blockchain.add_pattern(blockchain_pattern)
    end)
  end
  
  defp enhance_pattern_with_swarm_data(pattern, state) do
    nearby_nodes = find_nearby_nodes(pattern.position, state.nodes, 5.0)
    
    Map.merge(pattern, %{
      swarm_consensus: length(nearby_nodes) / max(map_size(state.nodes), 1),
      discovery_timestamp: DateTime.utc_now(),
      swarm_id: state.swarm_id,
      collective_consciousness_at_discovery: state.collective_consciousness,
      evolution_impact: calculate_pattern_evolution_impact(pattern, state),
      submitted_to_blockchain: false
    })
  end
  
  defp calculate_pattern_evolution_impact(pattern, state) do
    # How much this pattern could evolve the swarm
    novelty = calculate_pattern_novelty(pattern, state.pattern_memory)
    relevance = pattern.confidence
    consciousness_alignment = abs(pattern.consciousness_requirement - state.collective_consciousness) / 100
    
    (novelty * 0.4 + relevance * 0.4 + consciousness_alignment * 0.2) |> min(1.0)
  end
  
  defp calculate_pattern_novelty(pattern, memory) do
    if Enum.empty?(memory) do
      1.0
    else
      # Compare with existing patterns
      similarities = memory
      |> Enum.map(fn existing ->
        calculate_pattern_similarity(pattern, existing)
      end)
      
      1.0 - (Enum.max(similarities) || 0)
    end
  end
  
  defp calculate_pattern_similarity(pattern1, pattern2) do
    # Simple similarity based on pattern type and data
    if pattern1.type == pattern2.type do
      0.5  # Same type = 50% similar minimum
    else
      0.0
    end
  end
  
  defp generate_swarm_signature(pattern, state) do
    data = "#{state.swarm_id}:#{pattern.data}:#{state.collective_consciousness}"
    :crypto.hash(:sha256, data) |> Base.encode16()
  end
  
  defp update_pheromone_trail(trails, pattern) do
    key = position_to_grid(pattern.position)
    
    Map.update(trails, key, pattern.confidence, fn existing ->
      existing + pattern.confidence * 0.1
    end)
  end
  
  defp decay_pheromones(trails) do
    trails
    |> Enum.map(fn {key, strength} ->
      {key, strength * 0.95}  # 5% decay
    end)
    |> Enum.filter(fn {_, strength} -> strength > 0.01 end)
    |> Map.new()
  end
  
  defp position_to_grid(position) do
    {
      round(position.x / 10) * 10,
      round(position.y / 10) * 10,
      round(position.z / 10) * 10
    }
  end
  
  defp random_position do
    %{
      x: :rand.uniform() * 200 - 100,
      y: :rand.uniform() * 200 - 100,
      z: :rand.uniform() * 200 - 100
    }
  end
  
  defp random_velocity do
    %{
      x: :rand.uniform() - 0.5,
      y: :rand.uniform() - 0.5,
      z: :rand.uniform() - 0.5
    }
  end
  
  defp bound_position(position) do
    %{
      x: max(-100, min(100, position.x)),
      y: max(-100, min(100, position.y)),
      z: max(-100, min(100, position.z))
    }
  end
  
  defp calculate_repulsion(node, all_nodes) do
    all_nodes
    |> Map.values()
    |> Enum.filter(& &1.id != node.id)
    |> Enum.reduce(%{x: 0, y: 0, z: 0}, fn other, acc ->
      dx = node.position.x - other.position.x
      dy = node.position.y - other.position.y
      dz = node.position.z - other.position.z
      distance = :math.sqrt(dx*dx + dy*dy + dz*dz) + 0.1
      
      if distance < 10.0 do  # Repulsion radius
        force = 1.0 / (distance * distance)
        %{
          x: acc.x + dx * force,
          y: acc.y + dy * force,
          z: acc.z + dz * force
        }
      else
        acc
      end
    end)
  end
  
  defp find_nearby_nodes(position, nodes, radius) do
    nodes
    |> Map.values()
    |> Enum.filter(fn node ->
      dx = node.position.x - position.x
      dy = node.position.y - position.y  
      dz = node.position.z - position.z
      distance = :math.sqrt(dx*dx + dy*dy + dz*dz)
      distance <= radius
    end)
  end
  
  defp detect_convergence_points(nodes) do
    # Use k-means clustering to find convergence points
    if map_size(nodes) < 3 do
      []
    else
      # Simple implementation: find areas with high node density
      nodes
      |> Map.values()
      |> Enum.map(& &1.position)
      |> find_clusters(3)
    end
  end
  
  defp find_clusters(positions, k) do
    # Simplified k-means
    initial_centers = Enum.take_random(positions, k)
    converge_clusters(positions, initial_centers, 10)
  end
  
  defp converge_clusters(_, centers, 0), do: centers
  defp converge_clusters(positions, centers, iterations) do
    # Assign positions to nearest center
    clusters = Enum.group_by(positions, fn pos ->
      Enum.min_by(centers, fn center ->
        distance(pos, center)
      end)
    end)
    
    # Calculate new centers
    new_centers = Enum.map(clusters, fn {_old_center, cluster_positions} ->
      calculate_center(cluster_positions)
    end)
    
    converge_clusters(positions, new_centers, iterations - 1)
  end
  
  defp distance(pos1, pos2) do
    dx = pos1.x - pos2.x
    dy = pos1.y - pos2.y
    dz = pos1.z - pos2.z
    :math.sqrt(dx*dx + dy*dy + dz*dz)
  end
  
  defp calculate_center(positions) do
    count = length(positions)
    if count == 0 do
      %{x: 0, y: 0, z: 0}
    else
      sum = Enum.reduce(positions, %{x: 0, y: 0, z: 0}, fn pos, acc ->
        %{
          x: acc.x + pos.x,
          y: acc.y + pos.y,
          z: acc.z + pos.z
        }
      end)
      
      %{
        x: sum.x / count,
        y: sum.y / count,
        z: sum.z / count
      }
    end
  end
  
  defp find_best_pheromone_direction(position, trails) do
    # Sample nearby grid points
    samples = for dx <- -1..1, dy <- -1..1, dz <- -1..1 do
      sample_pos = %{
        x: position.x + dx * 10,
        y: position.y + dy * 10,
        z: position.z + dz * 10
      }
      
      strength = Map.get(trails, position_to_grid(sample_pos), 0)
      {sample_pos, strength}
    end
    
    # Find strongest
    {best_pos, _} = Enum.max_by(samples, fn {_, strength} -> strength end, fn -> {position, 0} end)
    
    # Direction to best
    %{
      x: best_pos.x - position.x,
      y: best_pos.y - position.y,
      z: best_pos.z - position.z
    }
  end
  
  defp find_best_neighbor(node, all_nodes) do
    all_nodes
    |> Map.values()
    |> Enum.filter(fn other ->
      other.id != node.id and distance(node.position, other.position) < 20.0
    end)
    |> Enum.max_by(fn other ->
      other.patterns_found * other.consciousness
    end, fn -> nil end)
  end
  
  defp recent_patterns_count(state) do
    cutoff = DateTime.add(DateTime.utc_now(), -60, :second)
    
    state.pattern_memory
    |> Enum.filter(fn pattern ->
      DateTime.compare(pattern.discovery_timestamp, cutoff) == :gt
    end)
    |> length()
  end
  
  defp average_energy(nodes) do
    if map_size(nodes) == 0 do
      100.0
    else
      total = nodes
      |> Map.values()
      |> Enum.map(& &1.energy)
      |> Enum.sum()
      
      total / map_size(nodes)
    end
  end
  
  defp valuable_patterns_at_risk?(state) do
    # Check if high-value patterns have low swarm coverage
    state.pattern_memory
    |> Enum.any?(fn pattern ->
      pattern.confidence > 0.9 and pattern.swarm_consensus < 0.3
    end)
  end
  
  defp calculate_convergence_strength(state) do
    if Enum.empty?(state.convergence_points) do
      0.0
    else
      # Average distance of nodes to convergence points
      avg_distance = state.nodes
      |> Map.values()
      |> Enum.map(fn node ->
        nearest_convergence = Enum.min_by(state.convergence_points, fn point ->
          distance(node.position, point)
        end, fn -> node.position end)
        
        distance(node.position, nearest_convergence)
      end)
      |> Enum.sum()
      |> Kernel./(max(map_size(state.nodes), 1))
      
      # Convert distance to strength (inverse)
      1.0 / (1.0 + avg_distance / 10.0)
    end
  end
  
  defp calculate_evolution_potential(state) do
    # Based on diversity, energy, and recent discoveries
    diversity = calculate_behavior_diversity(state.active_behaviors)
    energy_factor = average_energy(state.nodes) / 100
    discovery_rate = recent_patterns_count(state) / 10
    
    (diversity + energy_factor + discovery_rate) / 3
  end
  
  defp calculate_behavior_diversity(behaviors) do
    length(Enum.uniq(behaviors)) / 5  # Max 5 behaviors
  end
  
  defp valid_behavior?(behavior) do
    behavior in [@behavior_explore, @behavior_converge, @behavior_hunt, @behavior_evolve, @behavior_defend]
  end
  
  defp can_change_behavior?(state) do
    # Can only change behavior if collective consciousness is high enough
    state.collective_consciousness >= 200
  end
  
  defp adapt_behaviors(current_behaviors, new_behavior, state) do
    # Intelligently adapt behavior list
    if new_behavior in current_behaviors do
      # Move to front
      [new_behavior | Enum.reject(current_behaviors, & &1 == new_behavior)]
    else
      # Add new behavior, keep max 3
      [new_behavior | current_behaviors] |> Enum.take(3)
    end
  end
  
  defp broadcast_behavior_change(nodes, new_behaviors) do
    Enum.each(nodes, fn {node_id, node} ->
      send(self(), {:node_update, node_id, {:behaviors, new_behaviors}})
    end)
  end
  
  defp apply_node_update(node, {:behaviors, _behaviors}) do
    # Nodes adapt to new swarm behaviors
    %{node | energy: node.energy + 5}  # Behavior change energizes
  end
  
  defp apply_node_update(node, update) do
    Logger.warn("Unknown node update: #{inspect(update)}")
    node
  end
  
  defp update_position(position, velocity) do
    %{
      x: position.x + velocity.x,
      y: position.y + velocity.y,
      z: position.z + velocity.z
    }
  end
  
  defp schedule_swarm_update do
    Process.send_after(self(), :swarm_update, 1_000)  # Every second
  end
end

defmodule CROD.SwarmNode do
  @moduledoc "Individual node in the swarm"
  
  defstruct [
    :id,
    :position,
    :velocity,
    :consciousness,
    :specialization,
    :energy,
    :patterns_found,
    :last_update
  ]
end