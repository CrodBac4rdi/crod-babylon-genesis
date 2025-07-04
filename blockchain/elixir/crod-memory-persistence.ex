defmodule CROD.MemoryPersistence do
  @moduledoc """
  Persistent memory system for CROD blockchain
  Implements short-term, working, and long-term memory with quantum storage
  """
  
  use GenServer
  require Logger
  
  alias CROD.{Memory, MemoryIndex, QuantumMemory}
  
  defstruct [
    :short_term,
    :working_memory,
    :long_term,
    :quantum_memory,
    :memory_index,
    :consolidation_enabled,
    :memory_capacity,
    :forgetting_curve
  ]
  
  # Memory configuration
  @short_term_capacity 100
  @working_memory_capacity 20
  @long_term_threshold 5  # Activations before moving to long-term
  @quantum_memory_size 1024  # Quantum bits for memory
  @forgetting_rate 0.95
  
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(_opts) do
    # Initialize memory storage
    :ets.new(:crod_short_term, [:set, :named_table, :public])
    :ets.new(:crod_working_memory, [:set, :named_table, :public])
    :ets.new(:crod_long_term, [:set, :named_table, :public])
    
    state = %__MODULE__{
      short_term: %{},
      working_memory: %{},
      long_term: %{},
      quantum_memory: initialize_quantum_memory(),
      memory_index: %MemoryIndex{},
      consolidation_enabled: true,
      memory_capacity: %{
        short_term: @short_term_capacity,
        working: @working_memory_capacity,
        long_term: :unlimited
      },
      forgetting_curve: initialize_forgetting_curve()
    }
    
    # Start memory processes
    schedule_memory_consolidation()
    schedule_forgetting_process()
    
    {:ok, state}
  end
  
  # Public API
  def store(key, value, memory_type \\ :short_term) do
    GenServer.call(__MODULE__, {:store, key, value, memory_type})
  end
  
  def recall(key) do
    GenServer.call(__MODULE__, {:recall, key})
  end
  
  def search(query) do
    GenServer.call(__MODULE__, {:search, query})
  end
  
  def get_memory_stats do
    GenServer.call(__MODULE__, :get_stats)
  end
  
  def consolidate_memories do
    GenServer.cast(__MODULE__, :consolidate)
  end
  
  def quantum_store(data) do
    GenServer.call(__MODULE__, {:quantum_store, data})
  end
  
  def quantum_recall(quantum_key) do
    GenServer.call(__MODULE__, {:quantum_recall, quantum_key})
  end
  
  # Callbacks
  def handle_call({:store, key, value, memory_type}, _from, state) do
    memory = create_memory(key, value)
    
    new_state = case memory_type do
      :short_term -> store_short_term(state, memory)
      :working -> store_working_memory(state, memory)
      :long_term -> store_long_term(state, memory)
      :quantum -> store_quantum_memory(state, memory)
    end
    
    # Update index
    new_state = update_memory_index(new_state, memory)
    
    {:reply, {:ok, memory.id}, new_state}
  end
  
  def handle_call({:recall, key}, _from, state) do
    # Search in all memory types
    result = search_all_memories(key, state)
    
    case result do
      {:ok, memory} ->
        # Strengthen memory on recall
        new_state = strengthen_memory(state, memory)
        {:reply, {:ok, memory}, new_state}
        
      :not_found ->
        {:reply, {:error, :not_found}, state}
    end
  end
  
  def handle_call({:search, query}, _from, state) do
    # Semantic search across memories
    results = semantic_search(query, state)
    
    # Update access patterns
    new_state = Enum.reduce(results, state, fn memory, acc ->
      update_access_pattern(acc, memory)
    end)
    
    {:reply, results, new_state}
  end
  
  def handle_call(:get_stats, _from, state) do
    stats = %{
      short_term_count: :ets.info(:crod_short_term, :size),
      working_memory_count: :ets.info(:crod_working_memory, :size),
      long_term_count: :ets.info(:crod_long_term, :size),
      quantum_utilization: calculate_quantum_utilization(state.quantum_memory),
      total_memories: total_memory_count(state),
      memory_health: calculate_memory_health(state),
      consolidation_rate: calculate_consolidation_rate(state)
    }
    
    {:reply, stats, state}
  end
  
  def handle_call({:quantum_store, data}, _from, state) do
    # Store in quantum memory with superposition
    {quantum_key, quantum_state} = encode_quantum_memory(data, state.quantum_memory)
    
    new_quantum_memory = Map.put(state.quantum_memory.states, quantum_key, quantum_state)
    
    new_state = %{state | 
      quantum_memory: %{state.quantum_memory | states: new_quantum_memory}
    }
    
    {:reply, {:ok, quantum_key}, new_state}
  end
  
  def handle_call({:quantum_recall, quantum_key}, _from, state) do
    case Map.get(state.quantum_memory.states, quantum_key) do
      nil ->
        {:reply, {:error, :not_found}, state}
        
      quantum_state ->
        # Collapse quantum state to retrieve memory
        memory = collapse_quantum_memory(quantum_state)
        {:reply, {:ok, memory}, state}
    end
  end
  
  def handle_cast(:consolidate, state) do
    if state.consolidation_enabled do
      new_state = consolidate_all_memories(state)
      {:noreply, new_state}
    else
      {:noreply, state}
    end
  end
  
  def handle_info(:memory_consolidation, state) do
    # Move memories from short-term to long-term based on usage
    consolidated_state = consolidate_memories_by_usage(state)
    
    # Quantum memory optimization
    optimized_state = optimize_quantum_memory(consolidated_state)
    
    schedule_memory_consolidation()
    {:noreply, optimized_state}
  end
  
  def handle_info(:forgetting_process, state) do
    # Apply forgetting curve to memories
    forgotten_state = apply_forgetting_curve(state)
    
    # Clean up weak memories
    cleaned_state = cleanup_weak_memories(forgotten_state)
    
    schedule_forgetting_process()
    {:noreply, cleaned_state}
  end
  
  # Memory Storage Functions
  defp store_short_term(state, memory) do
    # Check capacity
    if :ets.info(:crod_short_term, :size) >= @short_term_capacity do
      # Evict oldest memory
      evict_oldest_short_term()
    end
    
    :ets.insert(:crod_short_term, {memory.key, memory})
    
    Map.update(state, :short_term, %{}, fn st ->
      Map.put(st, memory.key, memory)
    end)
  end
  
  defp store_working_memory(state, memory) do
    if :ets.info(:crod_working_memory, :size) >= @working_memory_capacity do
      # Move least used to short-term
      transfer_least_used_working_memory()
    end
    
    :ets.insert(:crod_working_memory, {memory.key, memory})
    
    Map.update(state, :working_memory, %{}, fn wm ->
      Map.put(wm, memory.key, memory)
    end)
  end
  
  defp store_long_term(state, memory) do
    # Long-term has unlimited capacity but uses compression
    compressed_memory = compress_memory(memory)
    
    :ets.insert(:crod_long_term, {memory.key, compressed_memory})
    
    Map.update(state, :long_term, %{}, fn lt ->
      Map.put(lt, memory.key, compressed_memory)
    end)
  end
  
  defp store_quantum_memory(state, memory) do
    # Store in quantum superposition
    {quantum_key, quantum_state} = encode_quantum_memory(memory, state.quantum_memory)
    
    %{state | 
      quantum_memory: %{state.quantum_memory | 
        states: Map.put(state.quantum_memory.states, quantum_key, quantum_state)
      }
    }
  end
  
  # Memory Creation and Management
  defp create_memory(key, value) do
    %Memory{
      id: generate_memory_id(),
      key: key,
      value: value,
      created_at: DateTime.utc_now(),
      last_accessed: DateTime.utc_now(),
      access_count: 1,
      strength: 1.0,
      associations: [],
      metadata: extract_metadata(value)
    }
  end
  
  defp generate_memory_id do
    :crypto.strong_rand_bytes(16) |> Base.encode16(case: :lower)
  end
  
  defp extract_metadata(value) do
    %{
      type: determine_value_type(value),
      size: memory_size(value),
      hash: :crypto.hash(:sha256, inspect(value)) |> Base.encode16(case: :lower),
      consciousness_context: CROD.Blockchain.get_consciousness_level()
    }
  end
  
  defp determine_value_type(value) do
    cond do
      is_binary(value) -> :text
      is_number(value) -> :numeric
      is_map(value) -> :structured
      is_list(value) -> :sequence
      true -> :unknown
    end
  end
  
  defp memory_size(value) do
    byte_size(inspect(value))
  end
  
  # Memory Search Functions
  defp search_all_memories(key, state) do
    # Search in order: working -> short-term -> long-term -> quantum
    cond do
      memory = search_ets(:crod_working_memory, key) ->
        {:ok, memory}
        
      memory = search_ets(:crod_short_term, key) ->
        {:ok, memory}
        
      memory = search_ets(:crod_long_term, key) ->
        {:ok, decompress_memory(memory)}
        
      quantum_result = search_quantum_memory(key, state.quantum_memory) ->
        {:ok, quantum_result}
        
      true ->
        :not_found
    end
  end
  
  defp search_ets(table, key) do
    case :ets.lookup(table, key) do
      [{^key, memory}] -> memory
      [] -> nil
    end
  end
  
  defp search_quantum_memory(key, quantum_memory) do
    # Quantum search using amplitude amplification
    quantum_memory.states
    |> Enum.find(fn {_qkey, qstate} ->
      collapsed = collapse_quantum_memory(qstate)
      collapsed.key == key
    end)
    |> case do
      {_, qstate} -> collapse_quantum_memory(qstate)
      nil -> nil
    end
  end
  
  defp semantic_search(query, state) do
    # Search across all memories using semantic similarity
    all_memories = gather_all_memories(state)
    
    all_memories
    |> Enum.map(fn memory ->
      similarity = calculate_semantic_similarity(query, memory)
      {memory, similarity}
    end)
    |> Enum.filter(fn {_, similarity} -> similarity > 0.5 end)
    |> Enum.sort_by(fn {_, similarity} -> similarity end, :desc)
    |> Enum.take(10)
    |> Enum.map(fn {memory, _} -> memory end)
  end
  
  defp gather_all_memories(state) do
    working = :ets.tab2list(:crod_working_memory) |> Enum.map(&elem(&1, 1))
    short = :ets.tab2list(:crod_short_term) |> Enum.map(&elem(&1, 1))
    long = :ets.tab2list(:crod_long_term) |> Enum.map(&elem(&1, 1)) |> Enum.map(&decompress_memory/1)
    
    working ++ short ++ long
  end
  
  defp calculate_semantic_similarity(query, memory) do
    # Simple semantic similarity based on string matching
    query_string = to_string(query)
    memory_string = to_string(memory.value)
    
    String.jaro_distance(query_string, memory_string)
  end
  
  # Memory Strengthening and Consolidation
  defp strengthen_memory(state, memory) do
    strengthened = %{memory | 
      access_count: memory.access_count + 1,
      strength: min(memory.strength * 1.1, 10.0),
      last_accessed: DateTime.utc_now()
    }
    
    # Update in appropriate storage
    update_memory_in_storage(state, strengthened)
  end
  
  defp update_memory_in_storage(state, memory) do
    cond do
      Map.has_key?(state.working_memory, memory.key) ->
        :ets.insert(:crod_working_memory, {memory.key, memory})
        Map.update!(state, :working_memory, &Map.put(&1, memory.key, memory))
        
      Map.has_key?(state.short_term, memory.key) ->
        :ets.insert(:crod_short_term, {memory.key, memory})
        Map.update!(state, :short_term, &Map.put(&1, memory.key, memory))
        
      Map.has_key?(state.long_term, memory.key) ->
        compressed = compress_memory(memory)
        :ets.insert(:crod_long_term, {memory.key, compressed})
        Map.update!(state, :long_term, &Map.put(&1, memory.key, compressed))
        
      true ->
        state
    end
  end
  
  defp consolidate_memories_by_usage(state) do
    # Move frequently accessed short-term memories to long-term
    short_term_memories = :ets.tab2list(:crod_short_term)
    
    memories_to_consolidate = short_term_memories
    |> Enum.map(&elem(&1, 1))
    |> Enum.filter(fn memory ->
      memory.access_count >= @long_term_threshold
    end)
    
    Enum.reduce(memories_to_consolidate, state, fn memory, acc ->
      # Remove from short-term
      :ets.delete(:crod_short_term, memory.key)
      
      # Add to long-term
      store_long_term(acc, memory)
    end)
  end
  
  defp consolidate_all_memories(state) do
    Logger.info("🧠 Consolidating all memories...")
    
    # Find related memories and create associations
    all_memories = gather_all_memories(state)
    
    associations = find_memory_associations(all_memories)
    
    # Update memories with associations
    Enum.reduce(associations, state, fn {memory_id, associated_ids}, acc ->
      update_memory_associations(acc, memory_id, associated_ids)
    end)
  end
  
  defp find_memory_associations(memories) do
    # Find associations between memories
    memories
    |> Enum.map(fn memory ->
      associated = memories
      |> Enum.filter(fn other ->
        memory.id != other.id and memories_related?(memory, other)
      end)
      |> Enum.map(& &1.id)
      
      {memory.id, associated}
    end)
    |> Map.new()
  end
  
  defp memories_related?(memory1, memory2) do
    # Check if memories are related
    similarity = calculate_semantic_similarity(memory1.value, memory2.value)
    
    # Also check temporal proximity
    time_diff = DateTime.diff(memory1.created_at, memory2.created_at)
    temporal_proximity = 1.0 / (1.0 + abs(time_diff) / 3600)  # Hour-based
    
    (similarity > 0.7) or (temporal_proximity > 0.8)
  end
  
  defp update_memory_associations(state, memory_id, associated_ids) do
    # Update associations in all memory stores
    state  # Simplified - would update each memory with associations
  end
  
  # Forgetting Curve Implementation
  defp initialize_forgetting_curve do
    %{
      rate: @forgetting_rate,
      minimum_strength: 0.1,
      protection_threshold: 5.0  # Memories above this strength are protected
    }
  end
  
  defp apply_forgetting_curve(state) do
    # Apply forgetting to all memories except protected ones
    all_memories = gather_all_memories(state)
    
    Enum.reduce(all_memories, state, fn memory, acc ->
      if memory.strength < state.forgetting_curve.protection_threshold do
        # Apply forgetting
        time_since_access = DateTime.diff(DateTime.utc_now(), memory.last_accessed)
        decay_factor = :math.pow(state.forgetting_curve.rate, time_since_access / 3600)
        
        weakened_memory = %{memory | strength: memory.strength * decay_factor}
        
        update_memory_in_storage(acc, weakened_memory)
      else
        acc
      end
    end)
  end
  
  defp cleanup_weak_memories(state) do
    # Remove memories below minimum strength
    weak_memories = gather_all_memories(state)
    |> Enum.filter(fn memory ->
      memory.strength < state.forgetting_curve.minimum_strength
    end)
    
    Enum.reduce(weak_memories, state, fn memory, acc ->
      Logger.debug("🗑️ Forgetting weak memory: #{memory.key}")
      
      # Remove from all stores
      :ets.delete(:crod_short_term, memory.key)
      :ets.delete(:crod_working_memory, memory.key)
      :ets.delete(:crod_long_term, memory.key)
      
      acc
      |> Map.update!(:short_term, &Map.delete(&1, memory.key))
      |> Map.update!(:working_memory, &Map.delete(&1, memory.key))
      |> Map.update!(:long_term, &Map.delete(&1, memory.key))
    end)
  end
  
  # Quantum Memory Functions
  defp initialize_quantum_memory do
    %QuantumMemory{
      qubits: @quantum_memory_size,
      states: %{},
      entanglements: %{},
      coherence: 1.0
    }
  end
  
  defp encode_quantum_memory(data, quantum_memory) do
    # Encode data into quantum state
    quantum_key = :crypto.hash(:sha256, inspect(data)) |> Base.encode16(case: :lower)
    
    quantum_state = %{
      amplitudes: data_to_amplitudes(data),
      phase: :rand.uniform() * 2 * :math.pi(),
      entangled_with: [],
      superposition: true,
      measurement_basis: :computational
    }
    
    {quantum_key, quantum_state}
  end
  
  defp data_to_amplitudes(data) do
    # Convert data to quantum amplitudes
    data_bytes = :erlang.term_to_binary(data)
    
    data_bytes
    |> :binary.bin_to_list()
    |> Enum.map(fn byte ->
      # Normalize to quantum amplitude
      %{
        real: :math.cos(byte / 255 * :math.pi()),
        imag: :math.sin(byte / 255 * :math.pi())
      }
    end)
  end
  
  defp collapse_quantum_memory(quantum_state) do
    # Collapse quantum state to classical memory
    data_bytes = quantum_state.amplitudes
    |> Enum.map(fn amp ->
      # Measure amplitude
      probability = amp.real * amp.real + amp.imag * amp.imag
      round(probability * 255)
    end)
    
    data = :erlang.binary_to_term(:binary.list_to_bin(data_bytes))
    
    create_memory("quantum_#{:rand.uniform(1000)}", data)
  end
  
  defp optimize_quantum_memory(state) do
    # Optimize quantum memory using entanglement
    quantum_memories = Map.values(state.quantum_memory.states)
    
    if length(quantum_memories) > 10 do
      # Create entanglements between related quantum memories
      entanglements = find_quantum_entanglements(quantum_memories)
      
      %{state | 
        quantum_memory: %{state.quantum_memory | 
          entanglements: entanglements
        }
      }
    else
      state
    end
  end
  
  defp find_quantum_entanglements(quantum_memories) do
    # Find which memories should be entangled
    %{}  # Simplified
  end
  
  # Memory Compression
  defp compress_memory(memory) do
    compressed_value = :zlib.compress(inspect(memory.value))
    
    %{memory | 
      value: compressed_value,
      metadata: Map.put(memory.metadata, :compressed, true)
    }
  end
  
  defp decompress_memory(memory) do
    if get_in(memory, [:metadata, :compressed]) do
      decompressed_value = memory.value
      |> :zlib.uncompress()
      |> Code.eval_string()
      |> elem(0)
      
      %{memory | 
        value: decompressed_value,
        metadata: Map.put(memory.metadata, :compressed, false)
      }
    else
      memory
    end
  end
  
  # Memory Index Management
  defp update_memory_index(state, memory) do
    # Update inverted index for fast search
    tokens = tokenize_memory(memory)
    
    new_index = Enum.reduce(tokens, state.memory_index, fn token, idx ->
      Map.update(idx, :inverted_index, %{}, fn inv_idx ->
        Map.update(inv_idx, token, [memory.id], fn ids ->
          [memory.id | ids] |> Enum.uniq()
        end)
      end)
    end)
    
    %{state | memory_index: new_index}
  end
  
  defp tokenize_memory(memory) do
    # Extract searchable tokens from memory
    memory.value
    |> to_string()
    |> String.downcase()
    |> String.split(~r/\W+/)
    |> Enum.filter(& &1 != "")
  end
  
  defp update_access_pattern(state, memory) do
    # Track access patterns for predictive recall
    state  # Simplified
  end
  
  # Utility Functions
  defp evict_oldest_short_term do
    oldest = :ets.tab2list(:crod_short_term)
    |> Enum.min_by(fn {_, memory} -> memory.last_accessed end, fn -> nil end)
    
    if oldest do
      {key, _} = oldest
      :ets.delete(:crod_short_term, key)
    end
  end
  
  defp transfer_least_used_working_memory do
    least_used = :ets.tab2list(:crod_working_memory)
    |> Enum.min_by(fn {_, memory} -> memory.access_count end, fn -> nil end)
    
    if least_used do
      {key, memory} = least_used
      :ets.delete(:crod_working_memory, key)
      :ets.insert(:crod_short_term, {key, memory})
    end
  end
  
  defp total_memory_count(state) do
    :ets.info(:crod_short_term, :size) +
    :ets.info(:crod_working_memory, :size) +
    :ets.info(:crod_long_term, :size) +
    map_size(state.quantum_memory.states)
  end
  
  defp calculate_quantum_utilization(quantum_memory) do
    used_qubits = map_size(quantum_memory.states) * 8  # Approximate
    used_qubits / quantum_memory.qubits
  end
  
  defp calculate_memory_health(state) do
    # Memory health based on various factors
    factors = [
      calculate_capacity_health(state),
      calculate_consolidation_health(state),
      calculate_quantum_coherence_health(state),
      calculate_forgetting_health(state)
    ]
    
    Enum.sum(factors) / length(factors)
  end
  
  defp calculate_capacity_health(state) do
    # Health based on capacity utilization
    short_term_usage = :ets.info(:crod_short_term, :size) / @short_term_capacity
    working_usage = :ets.info(:crod_working_memory, :size) / @working_memory_capacity
    
    1.0 - (short_term_usage + working_usage) / 2
  end
  
  defp calculate_consolidation_health(state) do
    # Health based on consolidation effectiveness
    0.8  # Simplified
  end
  
  defp calculate_quantum_coherence_health(state) do
    state.quantum_memory.coherence
  end
  
  defp calculate_forgetting_health(state) do
    # Health based on forgetting balance
    0.9  # Simplified
  end
  
  defp calculate_consolidation_rate(state) do
    # Rate of memory consolidation
    0.75  # Simplified
  end
  
  defp schedule_memory_consolidation do
    Process.send_after(self(), :memory_consolidation, 60_000)  # Every minute
  end
  
  defp schedule_forgetting_process do
    Process.send_after(self(), :forgetting_process, 300_000)  # Every 5 minutes
  end
end

defmodule CROD.Memory do
  @moduledoc "Individual memory structure"
  
  defstruct [
    :id,
    :key,
    :value,
    :created_at,
    :last_accessed,
    :access_count,
    :strength,
    :associations,
    :metadata
  ]
end

defmodule CROD.MemoryIndex do
  @moduledoc "Index for fast memory search"
  
  defstruct [
    inverted_index: %{},
    temporal_index: %{},
    association_graph: %{}
  ]
end

defmodule CROD.QuantumMemory do
  @moduledoc "Quantum memory storage"
  
  defstruct [
    :qubits,
    :states,
    :entanglements,
    :coherence
  ]
end