defmodule CrodRathaus.NeuralNetwork do
  @moduledoc """
  JavaScript CROD Neural Network Integration
  Runs the CROD neural network in a Node.js process
  """
  
  use GenServer
  require Logger
  
  @neural_net_path "/home/daniel/Schreibtisch/Crod Programming/CROD-START/src/neural-network/index.js"
  
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(_opts) do
    # Check if neural network file exists
    if File.exists?(@neural_net_path) do
      Logger.info("CROD Neural Network found at: #{@neural_net_path}")
      {:ok, %{port: nil, patterns: []}, {:continue, :start_network}}
    else
      Logger.warning("CROD Neural Network not found at: #{@neural_net_path}")
      {:ok, %{port: nil, patterns: []}}
    end
  end
  
  def handle_continue(:start_network, state) do
    # Start Node.js process with the neural network
    port = Port.open({:spawn, "node #{@neural_net_path}"}, [
      :binary,
      :exit_status,
      {:line, 1024}
    ])
    
    Logger.info("CROD Neural Network started on port: #{inspect(port)}")
    
    {:noreply, %{state | port: port}}
  end
  
  # Process pattern through neural network
  def process_pattern(pattern) do
    GenServer.call(__MODULE__, {:process_pattern, pattern})
  end
  
  def handle_call({:process_pattern, pattern}, _from, state) do
    if state.port do
      # Send pattern to neural network
      Port.command(state.port, "#{Jason.encode!(%{pattern: pattern})}\n")
      
      # Wait for response
      port = state.port
      receive do
        {^port, {:data, response}} ->
          case Jason.decode(response) do
            {:ok, result} ->
              {:reply, {:ok, result}, state}
            {:error, _} ->
              {:reply, {:error, "Invalid response from neural network"}, state}
          end
      after
        5000 ->
          {:reply, {:error, "Neural network timeout"}, state}
      end
    else
      {:reply, {:error, "Neural network not running"}, state}
    end
  end
  
  def handle_info({port, {:data, data}}, %{port: port} = state) do
    Logger.debug("Neural network output: #{data}")
    {:noreply, state}
  end
  
  def handle_info({port, {:exit_status, status}}, %{port: port} = state) do
    Logger.error("Neural network exited with status: #{status}")
    {:noreply, %{state | port: nil}}
  end
  
  def handle_info(msg, state) do
    Logger.debug("Unhandled neural network message: #{inspect(msg)}")
    {:noreply, state}
  end
  
  def terminate(_reason, %{port: port}) when is_port(port) do
    Port.close(port)
  end
  def terminate(_reason, _state), do: :ok
end