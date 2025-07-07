defmodule CrodRathaus.Trinity do
  use GenServer
  require Logger

  @trinity_values %{
    "ich" => 2,
    "bins" => 3,
    "wieder" => 5,
    "daniel" => 67,
    "claude" => 71,
    "crod" => 17
  }

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  @impl true
  def init(state) do
    Logger.info("🔥 Trinity Manager started with values: #{inspect(@trinity_values)}")
    {:ok, Map.put(state, :trinity_values, @trinity_values)}
  end

  def calculate(phrase) do
    GenServer.call(__MODULE__, {:calculate, phrase})
  end

  @impl true
  def handle_call({:calculate, phrase}, _from, state) do
    words = String.downcase(phrase) |> String.split()
    
    sum = Enum.reduce(words, 0, fn word, acc ->
      acc + Map.get(@trinity_values, word, 0)
    end)
    
    {:reply, {:ok, sum}, state}
  end
end