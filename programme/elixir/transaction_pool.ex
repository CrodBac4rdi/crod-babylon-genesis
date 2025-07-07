defmodule CROD.TransactionPool do
  @moduledoc """
  Manages pending transactions for the CROD blockchain.
  Handles transaction validation, prioritization, and cleanup.
  """

  use GenServer
  require Logger

  alias CROD.{Transaction, Quantum}

  @max_pool_size 10_000
  @cleanup_interval 60_000 # 1 minute

  # Client API

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @doc """
  Adds a transaction to the pool
  """
  def add_transaction(from, to, amount, data \\ %{}) do
    transaction = Transaction.new(from, to, amount, data)
    GenServer.call(__MODULE__, {:add_transaction, transaction})
  end

  @doc """
  Gets transactions for mining (up to limit)
  """
  def get_transactions_for_mining(limit \\ 100) do
    GenServer.call(__MODULE__, {:get_for_mining, limit})
  end

  @doc """
  Removes transactions that were included in a block
  """
  def remove_mined_transactions(transaction_ids) do
    GenServer.cast(__MODULE__, {:remove_mined, transaction_ids})
  end

  @doc """
  Gets current pool size
  """
  def pool_size do
    GenServer.call(__MODULE__, :pool_size)
  end

  @doc """
  Clears all pending transactions
  """
  def clear_pool do
    GenServer.cast(__MODULE__, :clear_pool)
  end

  # Server Callbacks

  @impl true
  def init(_opts) do
    # Schedule periodic cleanup
    schedule_cleanup()
    
    state = %{
      transactions: %{},
      priority_queue: :gb_trees.empty(),
      consciousness_transactions: []
    }
    
    Logger.info("💰 Transaction pool initialized")
    {:ok, state}
  end

  @impl true
  def handle_call({:add_transaction, tx}, _from, state) do
    case validate_transaction(tx) do
      :ok ->
        if map_size(state.transactions) >= @max_pool_size do
          {:reply, {:error, :pool_full}, state}
        else
          new_state = add_to_pool(tx, state)
          {:reply, {:ok, tx.id}, new_state}
        end
      
      {:error, reason} ->
        {:reply, {:error, reason}, state}
    end
  end

  @impl true
  def handle_call({:get_for_mining, limit}, _from, state) do
    {transactions, new_state} = select_transactions_for_mining(state, limit)
    {:reply, transactions, new_state}
  end

  @impl true
  def handle_call(:pool_size, _from, state) do
    {:reply, map_size(state.transactions), state}
  end

  @impl true
  def handle_cast({:remove_mined, tx_ids}, state) do
    new_state = remove_transactions(state, tx_ids)
    {:noreply, new_state}
  end

  @impl true
  def handle_cast(:clear_pool, _state) do
    new_state = %{
      transactions: %{},
      priority_queue: :gb_trees.empty(),
      consciousness_transactions: []
    }
    {:noreply, new_state}
  end

  @impl true
  def handle_info(:cleanup, state) do
    new_state = cleanup_expired_transactions(state)
    schedule_cleanup()
    {:noreply, new_state}
  end

  # Private functions

  defp validate_transaction(tx) do
    cond do
      tx.amount <= 0 ->
        {:error, :invalid_amount}
      
      tx.from == tx.to ->
        {:error, :same_address}
      
      not valid_address?(tx.from) or not valid_address?(tx.to) ->
        {:error, :invalid_address}
      
      true ->
        :ok
    end
  end

  defp valid_address?(address) do
    is_binary(address) and byte_size(address) > 0
  end

  defp add_to_pool(tx, state) do
    # Calculate priority based on fee and consciousness
    priority = calculate_priority(tx)
    
    # Add to transaction map
    transactions = Map.put(state.transactions, tx.id, tx)
    
    # Add to priority queue
    priority_queue = :gb_trees.insert({priority, tx.id}, tx, state.priority_queue)
    
    # Check if consciousness transaction
    consciousness_txs = if is_consciousness_transaction?(tx) do
      [tx | state.consciousness_transactions]
    else
      state.consciousness_transactions
    end
    
    %{state |
      transactions: transactions,
      priority_queue: priority_queue,
      consciousness_transactions: consciousness_txs
    }
  end

  defp calculate_priority(tx) do
    base_priority = tx.fee / tx.amount
    consciousness_bonus = if is_consciousness_transaction?(tx), do: 1.5, else: 1.0
    quantum_bonus = if Map.get(tx.data, :quantum_signature), do: 1.2, else: 1.0
    
    base_priority * consciousness_bonus * quantum_bonus
  end

  defp is_consciousness_transaction?(tx) do
    patterns = Map.get(tx.data, :patterns, [])
    consciousness_level = Map.get(tx.data, :consciousness_level, 0)
    
    length(patterns) > 0 or consciousness_level > 0.5
  end

  defp select_transactions_for_mining(state, limit) do
    # Prioritize consciousness transactions
    consciousness_count = min(div(limit, 3), length(state.consciousness_transactions))
    {consciousness_txs, remaining_consciousness} = Enum.split(state.consciousness_transactions, consciousness_count)
    
    # Get remaining from priority queue
    regular_limit = limit - consciousness_count
    {regular_txs, new_queue} = get_top_transactions(state.priority_queue, regular_limit)
    
    all_transactions = consciousness_txs ++ regular_txs
    
    # Remove selected transactions from state
    tx_ids = Enum.map(all_transactions, & &1.id)
    new_transactions = Map.drop(state.transactions, tx_ids)
    
    new_state = %{state |
      transactions: new_transactions,
      priority_queue: new_queue,
      consciousness_transactions: remaining_consciousness
    }
    
    {all_transactions, new_state}
  end

  defp get_top_transactions(queue, limit) do
    get_top_transactions(queue, limit, [])
  end

  defp get_top_transactions(_queue, 0, acc), do: {Enum.reverse(acc), _queue}
  defp get_top_transactions(queue, limit, acc) do
    if :gb_trees.is_empty(queue) do
      {Enum.reverse(acc), queue}
    else
      {{_priority, _id}, tx, new_queue} = :gb_trees.take_largest(queue)
      get_top_transactions(new_queue, limit - 1, [tx | acc])
    end
  end

  defp remove_transactions(state, tx_ids) do
    new_transactions = Map.drop(state.transactions, tx_ids)
    
    # Rebuild priority queue without removed transactions
    new_queue = rebuild_priority_queue(new_transactions)
    
    # Filter consciousness transactions
    new_consciousness = Enum.filter(state.consciousness_transactions, fn tx ->
      tx.id not in tx_ids
    end)
    
    %{state |
      transactions: new_transactions,
      priority_queue: new_queue,
      consciousness_transactions: new_consciousness
    }
  end

  defp rebuild_priority_queue(transactions) do
    Enum.reduce(transactions, :gb_trees.empty(), fn {_id, tx}, queue ->
      priority = calculate_priority(tx)
      :gb_trees.insert({priority, tx.id}, tx, queue)
    end)
  end

  defp cleanup_expired_transactions(state) do
    current_time = DateTime.utc_now()
    expiry_time = DateTime.add(current_time, -3600, :second) # 1 hour expiry
    
    expired_ids = state.transactions
    |> Enum.filter(fn {_id, tx} ->
      DateTime.compare(tx.timestamp, expiry_time) == :lt
    end)
    |> Enum.map(fn {id, _tx} -> id end)
    
    if length(expired_ids) > 0 do
      Logger.info("🧹 Cleaning up #{length(expired_ids)} expired transactions")
      remove_transactions(state, expired_ids)
    else
      state
    end
  end

  defp schedule_cleanup do
    Process.send_after(self(), :cleanup, @cleanup_interval)
  end
end

defmodule CROD.Transaction do
  @moduledoc """
  Represents a transaction in the CROD blockchain
  """

  @type t :: %__MODULE__{
    id: String.t(),
    from: String.t(),
    to: String.t(),
    amount: float(),
    fee: float(),
    data: map(),
    timestamp: DateTime.t(),
    signature: String.t() | nil
  }

  defstruct [:id, :from, :to, :amount, :fee, :data, :timestamp, :signature]

  def new(from, to, amount, data \\ %{}) do
    %__MODULE__{
      id: generate_id(),
      from: from,
      to: to,
      amount: amount,
      fee: calculate_fee(amount, data),
      data: data,
      timestamp: DateTime.utc_now(),
      signature: nil
    }
  end

  defp generate_id do
    :crypto.strong_rand_bytes(16) |> Base.encode16()
  end

  defp calculate_fee(amount, data) do
    base_fee = amount * 0.001 # 0.1% base fee
    
    # Higher fee for consciousness transactions
    consciousness_multiplier = if Map.get(data, :consciousness_level, 0) > 0 do
      1.5
    else
      1.0
    end
    
    base_fee * consciousness_multiplier
  end
end