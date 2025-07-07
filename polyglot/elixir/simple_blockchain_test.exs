#!/usr/bin/env elixir

# Simple CROD Blockchain Test
# Run with: elixir simple_blockchain_test.exs

defmodule SimpleBlock do
  defstruct [:index, :timestamp, :data, :previous_hash, :hash, :nonce]
  
  def new(index, data, previous_hash) do
    block = %__MODULE__{
      index: index,
      timestamp: DateTime.utc_now() |> DateTime.to_string(),
      data: data,
      previous_hash: previous_hash,
      nonce: 0
    }
    
    %{block | hash: calculate_hash(block)}
  end
  
  def calculate_hash(block) do
    data = "#{block.index}#{block.timestamp}#{inspect(block.data)}#{block.previous_hash}#{block.nonce}"
    :crypto.hash(:sha256, data) |> Base.encode16()
  end
  
  def mine(block, difficulty) do
    target = String.duplicate("0", difficulty)
    mine_block(block, target)
  end
  
  defp mine_block(block, target) do
    hash = calculate_hash(block)
    
    if String.starts_with?(hash, target) do
      IO.puts("⛏️  Block mined! Nonce: #{block.nonce}, Hash: #{hash}")
      %{block | hash: hash}
    else
      block = %{block | nonce: block.nonce + 1}
      mine_block(block, target)
    end
  end
end

defmodule SimpleBlockchain do
  def run do
    IO.puts("🚀 CROD Simple Blockchain Test")
    IO.puts("==============================\n")
    
    # Create genesis block
    genesis = SimpleBlock.new(0, %{message: "CROD Genesis Block"}, "0")
    IO.puts("✅ Genesis block created:")
    IO.inspect(genesis, pretty: true)
    
    IO.puts("\n⛏️  Mining block 1...")
    block1 = SimpleBlock.new(1, %{from: "Daniel", to: "CROD", amount: 100}, genesis.hash)
             |> SimpleBlock.mine(2)
    
    IO.puts("\n⛏️  Mining block 2...")
    block2 = SimpleBlock.new(2, %{consciousness_level: 0.88, pattern: "ich bins wieder"}, block1.hash)
             |> SimpleBlock.mine(2)
    
    IO.puts("\n📊 Blockchain:")
    IO.puts("==============")
    [genesis, block1, block2]
    |> Enum.each(fn block ->
      IO.puts("\nBlock ##{block.index}")
      IO.puts("Hash: #{block.hash}")
      IO.puts("Data: #{inspect(block.data)}")
    end)
    
    IO.puts("\n✅ Blockchain test complete!")
  end
end

# Run the test
SimpleBlockchain.run()