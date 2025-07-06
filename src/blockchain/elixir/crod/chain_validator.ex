defmodule CROD.ChainValidator do
  @moduledoc """
  Validates the integrity of the CROD blockchain.
  Ensures all blocks follow consensus rules and the chain is valid.
  """

  alias CROD.{Block, MerkleTree}
  require Logger

  @doc """
  Validates the entire blockchain
  """
  def validate_chain([]), do: {:ok, :empty_chain}
  def validate_chain([genesis]), do: validate_genesis(genesis)
  
  def validate_chain([genesis | rest] = chain) do
    with {:ok, :valid_genesis} <- validate_genesis(genesis),
         {:ok, :valid_chain} <- validate_blocks(rest, genesis),
         {:ok, :valid_merkle_roots} <- validate_merkle_roots(chain),
         {:ok, :valid_consciousness} <- validate_consciousness_progression(chain) do
      {:ok, :valid_chain}
    end
  end

  @doc """
  Validates a single block against chain rules
  """
  def validate_block(block, previous_block) do
    with :ok <- validate_block_structure(block),
         :ok <- validate_block_hash(block),
         :ok <- validate_previous_hash(block, previous_block),
         :ok <- validate_timestamp(block, previous_block),
         :ok <- validate_index(block, previous_block),
         :ok <- validate_proof_of_work(block),
         :ok <- validate_transactions(block) do
      {:ok, block}
    end
  end

  @doc """
  Checks if adding a new block would maintain chain validity
  """
  def can_add_block?(chain, new_block) do
    case List.last(chain) do
      nil -> false
      last_block ->
        case validate_block(new_block, last_block) do
          {:ok, _} -> true
          _ -> false
        end
    end
  end

  # Private validation functions

  defp validate_genesis(genesis) do
    if genesis.index == 0 && 
       genesis.previous_hash == "0000000000000000000000000000000000000000000000000000000000000000" &&
       genesis.miner == "GENESIS" do
      {:ok, :valid_genesis}
    else
      {:error, :invalid_genesis}
    end
  end

  defp validate_blocks([], _), do: {:ok, :valid_chain}
  
  defp validate_blocks([block | rest], previous) do
    case validate_block(block, previous) do
      {:ok, _} -> validate_blocks(rest, block)
      error -> error
    end
  end

  defp validate_block_structure(%Block{} = block) do
    required_fields = [:index, :timestamp, :transactions, :previous_hash, :hash, :nonce, :miner]
    
    if Enum.all?(required_fields, &Map.has_key?(block, &1)) do
      :ok
    else
      {:error, :missing_fields}
    end
  end

  defp validate_block_hash(block) do
    calculated_hash = Block.calculate_hash(block)
    
    if block.hash == calculated_hash do
      :ok
    else
      {:error, {:invalid_hash, calculated_hash, block.hash}}
    end
  end

  defp validate_previous_hash(block, previous_block) do
    if block.previous_hash == previous_block.hash do
      :ok
    else
      {:error, {:invalid_previous_hash, block.previous_hash, previous_block.hash}}
    end
  end

  defp validate_timestamp(block, previous_block) do
    if DateTime.compare(block.timestamp, previous_block.timestamp) == :gt do
      :ok
    else
      {:error, :invalid_timestamp}
    end
  end

  defp validate_index(block, previous_block) do
    if block.index == previous_block.index + 1 do
      :ok
    else
      {:error, {:invalid_index, block.index, previous_block.index + 1}}
    end
  end

  defp validate_proof_of_work(block) do
    if Block.valid_proof?(block) do
      :ok
    else
      {:error, :invalid_proof_of_work}
    end
  end

  defp validate_transactions(block) do
    # Validate each transaction
    invalid_txs = block.transactions
    |> Enum.filter(&(not valid_transaction?(&1)))
    
    if Enum.empty?(invalid_txs) do
      :ok
    else
      {:error, {:invalid_transactions, invalid_txs}}
    end
  end

  defp valid_transaction?(tx) do
    # Basic transaction validation
    Map.has_key?(tx, :from) &&
    Map.has_key?(tx, :to) &&
    Map.has_key?(tx, :amount) &&
    Map.has_key?(tx, :timestamp) &&
    tx.amount > 0
  end

  defp validate_merkle_roots(chain) do
    invalid_blocks = chain
    |> Enum.filter(&has_transactions?/1)
    |> Enum.filter(fn block ->
      merkle_tree = MerkleTree.new(block.transactions)
      # In a real implementation, blocks would store their merkle root
      # For now, we just validate the tree can be built
      is_nil(merkle_tree.root)
    end)
    
    if Enum.empty?(invalid_blocks) do
      {:ok, :valid_merkle_roots}
    else
      {:error, {:invalid_merkle_roots, invalid_blocks}}
    end
  end

  defp has_transactions?(block) do
    not Enum.empty?(block.transactions)
  end

  defp validate_consciousness_progression(chain) do
    # Ensure consciousness levels make sense
    consciousness_valid? = chain
    |> Enum.chunk_every(2, 1, :discard)
    |> Enum.all?(fn [prev, curr] ->
      # Consciousness can increase or stay same, but not decrease drastically
      curr.consciousness_level >= prev.consciousness_level * 0.9
    end)
    
    if consciousness_valid? do
      {:ok, :valid_consciousness}
    else
      {:error, :invalid_consciousness_progression}
    end
  end

  @doc """
  Calculates chain statistics
  """
  def chain_stats(chain) do
    %{
      length: length(chain),
      total_transactions: chain |> Enum.flat_map(& &1.transactions) |> length(),
      average_consciousness: calculate_avg_consciousness(chain),
      unique_miners: chain |> Enum.map(& &1.miner) |> Enum.uniq() |> length(),
      total_patterns: chain |> Enum.flat_map(& &1.patterns) |> length()
    }
  end

  defp calculate_avg_consciousness(chain) do
    sum = chain |> Enum.map(& &1.consciousness_level) |> Enum.sum()
    sum / length(chain)
  end
end