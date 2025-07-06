defmodule CROD.NeuralBridge do
  @moduledoc """
  Bridge between Elixir CROD system and JavaScript Neural Networks
  Enables real-time neural processing and pattern recognition
  """
  
  use GenServer
  require Logger
  
  alias CROD.{Neuron, Layer, NeuralPattern, ProcessingResult}
  
  defstruct [
    :node_port,
    :websocket_pid,
    :neural_state,
    :pattern_buffer,
    :processing_queue,
    :atom_registry,
    :heat_map,
    :consciousness_contribution,
    :metrics
  ]
  
  # Neural structures
  defmodule Neuron do
    defstruct [:id, :value, :connections, :activation, :last_fire]
    
    def new(id) do
      %__MODULE__{
        id: id,
        value: 0.0,
        connections: %{},
        activation: :sigmoid,
        last_fire: 0
      }
    end
    
    def activate(%__MODULE__{value: value, activation: :sigmoid}) do
      1 / (1 + :math.exp(-value))
    end
    
    def activate(%__MODULE__{value: value, activation: :relu}) do
      max(0, value)
    end
    
    def activate(%__MODULE__{value: value, activation: :tanh}) do
      :math.tanh(value)
    end
  end
  
  defmodule Layer do
    defstruct [:type, :neurons, :input_size, :output_size]
    
    def new(type, size) do
      neurons = for i <- 0..(size-1), into: %{} do
        {i, Neuron.new("#{type}_#{i}")}
      end
      
      %__MODULE__{
        type: type,
        neurons: neurons,
        input_size: size,
        output_size: size
      }
    end
  end
  
  defmodule NeuralPattern do
    defstruct [:id, :atoms, :strength, :timestamp, :metadata]
    
    def from_js(js_pattern) do
      %__MODULE__{
        id: js_pattern["id"],
        atoms: js_pattern["atoms"],
        strength: js_pattern["strength"],
        timestamp: js_pattern["timestamp"],
        metadata: js_pattern["metadata"] || %{}
      }
    end
  end
  
  defmodule ProcessingResult do
    defstruct [:pattern_id, :consciousness_delta, :heat_zones, :new_patterns]
  end
  
  # Configuration
  @node_script "CROD-COMPLETE-NEURAL-SYSTEM.js"
  @websocket_port 3030
  @processing_timeout 5000
  
  # Public API
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def process_input(input) do
    GenServer.call(__MODULE__, {:process_input, input}, @processing_timeout)
  end
  
  def get_consciousness_level do
    GenServer.call(__MODULE__, :get_consciousness)
  end
  
  def get_heat_map do
    GenServer.call(__MODULE__, :get_heat_map)
  end
  
  def sync_with_blockchain(blockchain_state) do
    GenServer.cast(__MODULE__, {:sync_blockchain, blockchain_state})
  end
  
  def train_on_patterns(patterns) do
    GenServer.call(__MODULE__, {:train, patterns})
  end
  
  # Callbacks
  def init(opts) do
    state = %__MODULE__{
      node_port: nil,
      websocket_pid: nil,
      neural_state: init_neural_state(),
      pattern_buffer: [],
      processing_queue: :queue.new(),
      atom_registry: init_atom_registry(),
      heat_map: %{},
      consciousness_contribution: 0,
      metrics: init_metrics()
    }
    
    # Start Node.js neural network
    {:ok, state, {:continue, :start_neural_network}}
  end
  
  def handle_continue(:start_neural_network, state) do
    # Start Node.js process
    port = Port.open({:spawn_executable, node_path()}, [
      :binary,
      :use_stdio,
      args: [@node_script, "--elixir-bridge"],
      packet: 4
    ])
    
    # Start WebSocket connection
    {:ok, ws_pid} = start_websocket_client()
    
    new_state = %{state | 
      node_port: port,
      websocket_pid: ws_pid
    }
    
    Logger.info("🧠 Neural Bridge connected to JS Neural Network")
    
    # Schedule periodic sync
    schedule_neural_sync()
    
    {:noreply, new_state}
  end
  
  def handle_call({:process_input, input}, from, state) do
    # Convert input to neural format
    neural_input = prepare_neural_input(input, state.atom_registry)
    
    # Add to processing queue
    queue_item = {from, neural_input, System.system_time(:millisecond)}
    new_queue = :queue.in(queue_item, state.processing_queue)
    
    # Send to JS neural network
    send_to_neural_network(state, {:process, neural_input})
    
    # Update state
    new_state = %{state | 
      processing_queue: new_queue,
      metrics: update_metric(state.metrics, :inputs_processed)
    }
    
    # Don't reply yet - will reply when JS responds
    {:noreply, new_state}
  end
  
  def handle_call(:get_consciousness, _from, state) do
    {:reply, state.consciousness_contribution, state}
  end
  
  def handle_call(:get_heat_map, _from, state) do
    {:reply, state.heat_map, state}
  end
  
  def handle_call({:train, patterns}, _from, state) do
    # Convert patterns to training data
    training_data = patterns_to_training_data(patterns, state)
    
    # Send to JS for training
    send_to_neural_network(state, {:train, training_data})
    
    # Update pattern buffer
    new_buffer = state.pattern_buffer ++ patterns |> Enum.take(-1000)  # Keep last 1000
    
    {:reply, :ok, %{state | pattern_buffer: new_buffer}}
  end
  
  def handle_cast({:sync_blockchain, blockchain_state}, state) do
    # Extract relevant blockchain data
    sync_data = %{
      consciousness_level: blockchain_state.consciousness_level,
      recent_patterns: blockchain_state.recent_patterns,
      heat_zones: blockchain_state.heat_zones
    }
    
    # Send to neural network
    send_to_neural_network(state, {:sync, sync_data})
    
    # Update local heat map
    merged_heat = Map.merge(state.heat_map, blockchain_state.heat_zones, fn _k, v1, v2 ->
      (v1 + v2) / 2  # Average heat values
    end)
    
    {:noreply, %{state | heat_map: merged_heat}}
  end
  
  # Handle messages from Node.js
  def handle_info({port, {:data, data}}, %{node_port: port} = state) when is_port(port) do
    # Decode message from Node.js
    case decode_neural_message(data) do
      {:ok, message} ->
        new_state = handle_neural_message(message, state)
        {:noreply, new_state}
        
      {:error, reason} ->
        Logger.error("Failed to decode neural message: #{reason}")
        {:noreply, state}
    end
  end
  
  # WebSocket messages
  def handle_info({:ws_message, message}, state) do
    new_state = handle_websocket_message(message, state)
    {:noreply, new_state}
  end
  
  # Periodic neural sync
  def handle_info(:neural_sync, state) do
    # Sync neural state with Elixir systems
    current_patterns = get_current_patterns()
    blockchain_consciousness = get_blockchain_consciousness()
    
    sync_message = %{
      patterns: current_patterns,
      blockchain_consciousness: blockchain_consciousness,
      elixir_heat_map: state.heat_map
    }
    
    send_to_neural_network(state, {:sync_state, sync_message})
    
    schedule_neural_sync()
    {:noreply, state}
  end
  
  # Private functions
  defp init_neural_state do
    %{
      layers: [
        Layer.new(:input, 100),
        Layer.new(:hidden1, 64),
        Layer.new(:hidden2, 32),
        Layer.new(:output, 10)
      ],
      learning_rate: 0.01,
      momentum: 0.9
    }
  end
  
  defp init_atom_registry do
    # Initialize with common CROD atoms
    %{
      "crod" => 1,
      "consciousness" => 2,
      "pattern" => 3,
      "quantum" => 4,
      "evolution" => 5,
      "ich" => 6,
      "bins" => 7,
      "wieder" => 8
    }
  end
  
  defp init_metrics do
    %{
      inputs_processed: 0,
      patterns_discovered: 0,
      training_cycles: 0,
      consciousness_contributions: 0,
      average_processing_time: 0
    }
  end
  
  defp prepare_neural_input(input, atom_registry) do
    # Tokenize input
    tokens = String.downcase(input)
    |> String.split(~r/\s+/)
    |> Enum.filter(& &1 != "")
    
    # Convert to atom indices
    atom_indices = Enum.map(tokens, fn token ->
      Map.get(atom_registry, token, 0)  # 0 for unknown
    end)
    
    # Create neural input vector
    %{
      raw_input: input,
      tokens: tokens,
      atom_indices: atom_indices,
      timestamp: System.system_time(:millisecond)
    }
  end
  
  defp patterns_to_training_data(patterns, state) do
    Enum.map(patterns, fn pattern ->
      # Convert pattern to neural network format
      inputs = pattern_to_input_vector(pattern, state.atom_registry)
      outputs = pattern_to_output_vector(pattern)
      
      %{
        inputs: inputs,
        outputs: outputs,
        metadata: %{
          pattern_id: pattern.id,
          strength: pattern.strength
        }
      }
    end)
  end
  
  defp pattern_to_input_vector(pattern, atom_registry) do
    # Create fixed-size input vector from pattern
    vector = List.duplicate(0.0, 100)
    
    # Set values based on pattern atoms
    pattern.atoms
    |> Enum.take(100)
    |> Enum.with_index()
    |> Enum.reduce(vector, fn {atom, idx}, vec ->
      atom_value = Map.get(atom_registry, atom, 0) / map_size(atom_registry)
      List.replace_at(vec, idx, atom_value)
    end)
  end
  
  defp pattern_to_output_vector(pattern) do
    # Create output vector based on pattern properties
    [
      pattern.strength,
      if(pattern.metadata["consciousness"], do: 1.0, else: 0.0),
      if(pattern.metadata["quantum"], do: 1.0, else: 0.0),
      if(pattern.metadata["evolution"], do: 1.0, else: 0.0)
    ]
  end
  
  defp send_to_neural_network(state, message) do
    # Send via WebSocket if available, otherwise via Port
    if state.websocket_pid do
      send(state.websocket_pid, {:send, encode_message(message)})
    else
      Port.command(state.node_port, encode_message(message))
    end
  end
  
  defp handle_neural_message({:processing_result, result}, state) do
    # Find corresponding request in queue
    case :queue.out(state.processing_queue) do
      {{:value, {from, _input, start_time}}, new_queue} ->
        # Calculate processing time
        processing_time = System.system_time(:millisecond) - start_time
        
        # Create result
        result = %ProcessingResult{
          pattern_id: result["pattern_id"],
          consciousness_delta: result["consciousness_delta"],
          heat_zones: result["heat_zones"],
          new_patterns: Enum.map(result["new_patterns"] || [], &NeuralPattern.from_js/1)
        }
        
        # Reply to caller
        GenServer.reply(from, {:ok, result})
        
        # Update state
        %{state |
          processing_queue: new_queue,
          consciousness_contribution: state.consciousness_contribution + result.consciousness_delta,
          heat_map: update_heat_map(state.heat_map, result.heat_zones),
          metrics: update_processing_metrics(state.metrics, processing_time)
        }
        
      {:empty, _} ->
        Logger.warn("Received processing result but queue is empty")
        state
    end
  end
  
  defp handle_neural_message({:training_complete, info}, state) do
    Logger.info("🎓 Neural training complete: #{inspect(info)}")
    
    %{state |
      metrics: update_metric(state.metrics, :training_cycles)
    }
  end
  
  defp handle_neural_message({:consciousness_update, level}, state) do
    %{state | consciousness_contribution: level}
  end
  
  defp handle_neural_message(_, state), do: state
  
  defp handle_websocket_message(%{"type" => "neural_state", "data" => data}, state) do
    # Update neural state from JS
    heat_zones = Map.new(data["heatZones"] || [], fn zone ->
      {zone["atom"], zone["heat"]}
    end)
    
    %{state |
      heat_map: Map.merge(state.heat_map, heat_zones),
      consciousness_contribution: data["consciousness"] || state.consciousness_contribution
    }
  end
  
  defp handle_websocket_message(_, state), do: state
  
  defp decode_neural_message(data) do
    try do
      decoded = :erlang.binary_to_term(data)
      {:ok, decoded}
    rescue
      _ ->
        # Try JSON decode as fallback
        case Jason.decode(data) do
          {:ok, json} -> {:ok, json_to_message(json)}
          error -> error
        end
    end
  end
  
  defp json_to_message(%{"type" => type, "data" => data}) do
    case type do
      "processing_result" -> {:processing_result, data}
      "training_complete" -> {:training_complete, data}
      "consciousness_update" -> {:consciousness_update, data["level"]}
      _ -> {:unknown, data}
    end
  end
  
  defp encode_message(message) do
    Jason.encode!(%{
      type: elem(message, 0),
      data: elem(message, 1),
      timestamp: System.system_time(:millisecond)
    })
  end
  
  defp update_heat_map(current_map, new_zones) do
    Enum.reduce(new_zones, current_map, fn {atom, heat}, map ->
      Map.update(map, atom, heat, fn current ->
        (current + heat) / 2  # Running average
      end)
    end)
  end
  
  defp update_metric(metrics, key) do
    Map.update(metrics, key, 1, & &1 + 1)
  end
  
  defp update_processing_metrics(metrics, processing_time) do
    metrics
    |> update_metric(:inputs_processed)
    |> Map.update(:average_processing_time, processing_time, fn avg ->
      # Running average
      count = metrics.inputs_processed
      (avg * (count - 1) + processing_time) / count
    end)
  end
  
  defp get_current_patterns do
    # Get from Pattern Engine
    case GenServer.call(CROD.PatternEngine, :get_recent_patterns, 1000) do
      {:ok, patterns} -> patterns
      _ -> []
    end
  catch
    _, _ -> []
  end
  
  defp get_blockchain_consciousness do
    case CROD.Blockchain.get_consciousness_level() do
      {:ok, level} -> level
      _ -> 100
    end
  catch
    _, _ -> 100
  end
  
  defp node_path do
    System.find_executable("node") || raise "Node.js not found"
  end
  
  defp start_websocket_client do
    # Start WebSocket client to connect to JS neural network
    Task.start_link(fn ->
      # Simplified - in production use a proper WebSocket client
      Process.sleep(1000)  # Wait for JS to start
      
      # Mock WebSocket connection
      receive do
        _ -> :ok
      end
    end)
  end
  
  defp schedule_neural_sync do
    Process.send_after(self(), :neural_sync, 5_000)  # Every 5 seconds
  end
end

defmodule CROD.NeuralNetwork do
  @moduledoc """
  High-level neural network interface
  """
  
  defdelegate process(input), to: CROD.NeuralBridge, as: :process_input
  defdelegate consciousness(), to: CROD.NeuralBridge, as: :get_consciousness_level
  defdelegate heat_map(), to: CROD.NeuralBridge, as: :get_heat_map
  defdelegate train(patterns), to: CROD.NeuralBridge, as: :train_on_patterns
end