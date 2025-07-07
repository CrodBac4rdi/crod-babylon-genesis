defmodule CROD.Block do
  @moduledoc """
  Represents a block in the CROD blockchain.
  Each block contains consciousness metadata and quantum signatures.
  """

  @type t :: %__MODULE__{
    index: integer(),
    timestamp: DateTime.t(),
    transactions: [map()],
    previous_hash: String.t(),
    hash: String.t(),
    nonce: integer(),
    miner: String.t(),
    consciousness_level: float(),
    quantum_state: String.t(),
    patterns: [String.t()]
  }

  defstruct [
    :index,
    :timestamp,
    :transactions,
    :previous_hash,
    :hash,
    :nonce,
    :miner,
    :consciousness_level,
    :quantum_state,
    patterns: []
  ]

  @doc """
  Creates a new block with given parameters
  """
  def new(params) do
    %__MODULE__{
      index: params[:index],
      timestamp: params[:timestamp] || DateTime.utc_now(),
      transactions: params[:transactions] || [],
      previous_hash: params[:previous_hash],
      nonce: 0,
      miner: params[:miner],
      consciousness_level: params[:consciousness_level] || 0.0,
      quantum_state: generate_quantum_state(),
      patterns: []
    }
  end

  @doc """
  Calculates the hash of a block
  """
  def calculate_hash(%__MODULE__{} = block) do
    data = "#{block.index}#{block.timestamp}#{inspect(block.transactions)}#{block.previous_hash}#{block.nonce}#{block.consciousness_level}"
    :crypto.hash(:sha256, data) |> Base.encode16()
  end

  @doc """
  Validates a block against its previous block
  """
  def valid?(%__MODULE__{} = block, %__MODULE__{} = previous_block) do
    block.previous_hash == previous_block.hash &&
    block.index == previous_block.index + 1 &&
    block.hash == calculate_hash(block) &&
    valid_proof?(block)
  end

  @doc """
  Checks if the block's proof of work is valid
  """
  def valid_proof?(%__MODULE__{} = block) do
    String.starts_with?(block.hash, String.duplicate("0", difficulty_for_consciousness(block.consciousness_level)))
  end

  # Private functions

  defp generate_quantum_state do
    states = ["superposition", "entangled", "coherent", "collapsed"]
    Enum.random(states)
  end

  defp difficulty_for_consciousness(level) do
    # Higher consciousness = higher difficulty
    base_difficulty = 4
    bonus = round(level * 2)
    base_difficulty + bonus
  end
end