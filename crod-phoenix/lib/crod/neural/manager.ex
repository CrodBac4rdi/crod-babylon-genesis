defmodule Crod.Neural.Manager do
  @moduledoc """
  Manages the CROD neural network integration.
  Loads and coordinates neural network configurations and operations.
  """

  use GenServer
  require Logger

  alias Crod.Neural.{Network, Trainer, Predictor}
  alias Crod.Services.NatsClient

  @neural_topic "crod.neural.events"

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @impl true
  def init(_opts) do
    # Load neural configurations
    {:ok, master_config} = load_master_config()
    {:ok, neural_network} = load_neural_network()
    
    # Subscribe to NATS topics
    NatsClient.subscribe(@neural_topic, self())
    
    state = %{
      master_config: master_config,
      neural_network: neural_network,
      active_networks: %{},
      training_queue: :queue.new()
    }
    
    # Initialize default network
    {:ok, initialize_default_network(state)}
  end

  # Public API

  @doc """
  Processes input through the neural network.
  """
  def process(input, network_id \\ :default) do
    GenServer.call(__MODULE__, {:process, input, network_id})
  end

  @doc """
  Trains the neural network with new data.
  """
  def train(training_data, network_id \\ :default) do
    GenServer.cast(__MODULE__, {:train, training_data, network_id})
  end

  @doc """
  Gets the current state of a neural network.
  """
  def get_network_state(network_id \\ :default) do
    GenServer.call(__MODULE__, {:get_network_state, network_id})
  end

  @doc """
  Creates a new neural network instance.
  """
  def create_network(config) do
    GenServer.call(__MODULE__, {:create_network, config})
  end

  # GenServer callbacks

  @impl true
  def handle_call({:process, input, network_id}, _from, state) do
    case Map.get(state.active_networks, network_id) do
      nil ->
        {:reply, {:error, :network_not_found}, state}
      
      network ->
        result = Network.forward_pass(network, input)
        
        # Publish result to NATS
        NatsClient.publish("crod.neural.processed", %{
          network_id: network_id,
          input: input,
          output: result,
          timestamp: DateTime.utc_now()
        })
        
        {:reply, {:ok, result}, state}
    end
  end

  @impl true
  def handle_call({:get_network_state, network_id}, _from, state) do
    case Map.get(state.active_networks, network_id) do
      nil ->
        {:reply, {:error, :network_not_found}, state}
      
      network ->
        network_state = Network.get_state(network)
        {:reply, {:ok, network_state}, state}
    end
  end

  @impl true
  def handle_call({:create_network, config}, _from, state) do
    network_id = generate_network_id()
    
    # Create network based on config
    network = Network.create(Map.merge(state.master_config, config))
    
    # Add to active networks
    new_state = %{state | 
      active_networks: Map.put(state.active_networks, network_id, network)
    }
    
    {:reply, {:ok, network_id}, new_state}
  end

  @impl true
  def handle_cast({:train, training_data, network_id}, state) do
    # Add to training queue
    training_task = %{
      network_id: network_id,
      data: training_data,
      timestamp: DateTime.utc_now()
    }
    
    new_queue = :queue.in(training_task, state.training_queue)
    
    # Start training if not already running
    if :queue.is_empty(state.training_queue) do
      send(self(), :process_training_queue)
    end
    
    {:noreply, %{state | training_queue: new_queue}}
  end

  @impl true
  def handle_info(:process_training_queue, state) do
    case :queue.out(state.training_queue) do
      {{:value, task}, new_queue} ->
        # Process training task
        process_training_task(task, state)
        
        # Continue processing queue
        if not :queue.is_empty(new_queue) do
          send(self(), :process_training_queue)
        end
        
        {:noreply, %{state | training_queue: new_queue}}
      
      {:empty, _} ->
        {:noreply, state}
    end
  end

  @impl true
  def handle_info({:nats_message, _topic, message}, state) do
    Logger.info("Neural manager received NATS message: #{inspect(message)}")
    # Handle neural network related NATS messages
    {:noreply, state}
  end

  # Private functions

  defp load_master_config do
    path = Application.get_env(:crod, :neural)[:master_config]
    
    case File.read(path) do
      {:ok, content} ->
        Jason.decode(content)
      
      {:error, reason} ->
        Logger.error("Failed to load master config: #{reason}")
        {:ok, %{}}
    end
  end

  defp load_neural_network do
    path = Application.get_env(:crod, :neural)[:neural_network]
    
    case File.read(path) do
      {:ok, content} ->
        {:ok, content}
      
      {:error, reason} ->
        Logger.error("Failed to load neural network: #{reason}")
        {:ok, ""}
    end
  end

  defp initialize_default_network(state) do
    # Create default network from master config
    default_network = Network.create(state.master_config)
    
    %{state | 
      active_networks: Map.put(state.active_networks, :default, default_network)
    }
  end

  defp process_training_task(task, state) do
    case Map.get(state.active_networks, task.network_id) do
      nil ->
        Logger.error("Network not found for training: #{task.network_id}")
      
      network ->
        # Train the network
        trained_network = Trainer.train(network, task.data)
        
        # Update the network in state
        GenServer.cast(self(), {:update_network, task.network_id, trained_network})
        
        # Publish training complete event
        NatsClient.publish("crod.neural.trained", %{
          network_id: task.network_id,
          training_completed: DateTime.utc_now()
        })
    end
  end

  defp generate_network_id do
    :crypto.strong_rand_bytes(8) |> Base.encode16()
  end
end