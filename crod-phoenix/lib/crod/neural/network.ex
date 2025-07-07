defmodule Crod.Neural.Network do
  @moduledoc """
  Neural network implementation using Nx and Axon.
  Core neural processing for CROD.
  """

  require Axon

  defstruct [:model, :params, :config, :state]

  @doc """
  Creates a new neural network based on configuration.
  """
  def create(config) do
    model = build_model(config)
    params = initialize_params(model, config)
    
    %__MODULE__{
      model: model,
      params: params,
      config: config,
      state: %{
        created_at: DateTime.utc_now(),
        iterations: 0,
        last_loss: nil
      }
    }
  end

  @doc """
  Performs a forward pass through the network.
  """
  def forward_pass(%__MODULE__{model: model, params: params} = network, input) do
    input_tensor = prepare_input(input, network.config)
    
    output = Axon.predict(model, params, input_tensor)
    
    # Update state
    new_state = Map.update!(network.state, :iterations, &(&1 + 1))
    
    {post_process_output(output, network.config), %{network | state: new_state}}
  end

  @doc """
  Gets the current state of the network.
  """
  def get_state(%__MODULE__{} = network) do
    %{
      config: network.config,
      state: network.state,
      param_count: count_params(network.params),
      model_info: Axon.get_op_counts(network.model)
    }
  end

  @doc """
  Updates network parameters.
  """
  def update_params(%__MODULE__{} = network, new_params) do
    %{network | params: new_params}
  end

  @doc """
  Saves network to a file.
  """
  def save(%__MODULE__{} = network, path) do
    data = %{
      params: serialize_params(network.params),
      config: network.config,
      state: network.state
    }
    
    File.write!(path, Jason.encode!(data))
  end

  @doc """
  Loads network from a file.
  """
  def load(path) do
    {:ok, content} = File.read(path)
    {:ok, data} = Jason.decode(content)
    
    config = data["config"]
    model = build_model(config)
    params = deserialize_params(data["params"])
    
    %__MODULE__{
      model: model,
      params: params,
      config: config,
      state: data["state"]
    }
  end

  # Private functions

  defp build_model(config) do
    input_shape = get_input_shape(config)
    hidden_units = config["hidden_units"] || [128, 64, 32]
    output_units = config["output_units"] || 10
    activation = get_activation(config["activation"] || "relu")
    
    Axon.input("input", shape: input_shape)
    |> build_hidden_layers(hidden_units, activation)
    |> Axon.dense(output_units)
    |> apply_output_activation(config)
  end

  defp build_hidden_layers(input, units, activation) do
    Enum.reduce(units, input, fn unit_count, layer ->
      layer
      |> Axon.dense(unit_count)
      |> Axon.activation(activation)
      |> Axon.dropout(rate: 0.1)
    end)
  end

  defp apply_output_activation(layer, config) do
    case config["output_activation"] do
      "softmax" -> Axon.activation(layer, :softmax)
      "sigmoid" -> Axon.activation(layer, :sigmoid)
      "tanh" -> Axon.activation(layer, :tanh)
      _ -> layer
    end
  end

  defp get_input_shape(config) do
    case config["input_shape"] do
      nil -> {nil, 784}  # Default MNIST-like shape
      shape when is_list(shape) -> List.to_tuple([nil | shape])
      shape -> shape
    end
  end

  defp get_activation(name) do
    case name do
      "relu" -> :relu
      "tanh" -> :tanh
      "sigmoid" -> :sigmoid
      "leaky_relu" -> :leaky_relu
      _ -> :relu
    end
  end

  defp initialize_params(model, config) do
    key = Nx.Random.key(config["random_seed"] || 42)
    input_template = get_input_template(config)
    
    Axon.Loop.trainer(model, :mean_squared_error, :adam)
    |> Axon.Loop.metric(:mean_absolute_error)
    |> then(fn _ -> Axon.init(model, input_template, seed: key) end)
  end

  defp get_input_template(config) do
    shape = get_input_shape(config)
    Nx.template(shape, :f32)
  end

  defp prepare_input(input, _config) when is_list(input) do
    Nx.tensor(input, type: :f32)
  end

  defp prepare_input(input, _config) when is_map(input) do
    input
    |> Map.values()
    |> List.flatten()
    |> Nx.tensor(type: :f32)
  end

  defp prepare_input(input, _config) do
    Nx.tensor(input, type: :f32)
  end

  defp post_process_output(output, config) do
    output = Nx.to_list(output)
    
    case config["output_type"] do
      "classification" -> 
        output
        |> Enum.with_index()
        |> Enum.max_by(fn {val, _} -> val end)
        |> elem(1)
      
      "probabilities" ->
        output
      
      _ ->
        output
    end
  end

  defp count_params(params) do
    params
    |> Map.values()
    |> Enum.map(&Nx.size/1)
    |> Enum.sum()
  end

  defp serialize_params(params) do
    params
    |> Enum.map(fn {k, v} -> 
      {k, %{
        data: Nx.to_binary(v),
        shape: Nx.shape(v),
        type: Nx.type(v)
      }}
    end)
    |> Map.new()
  end

  defp deserialize_params(serialized) do
    serialized
    |> Enum.map(fn {k, v} -> 
      tensor = Nx.from_binary(v["data"], v["type"])
      |> Nx.reshape(List.to_tuple(v["shape"]))
      {k, tensor}
    end)
    |> Map.new()
  end
end