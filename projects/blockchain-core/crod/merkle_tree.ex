defmodule CROD.MerkleTree do
  @moduledoc """
  Merkle Tree implementation for CROD blockchain.
  Provides efficient verification of transaction integrity.
  """

  @type leaf :: binary()
  @type node :: binary()
  @type tree :: %__MODULE__{
    root: node() | nil,
    leaves: [leaf()],
    levels: [[node()]]
  }

  defstruct [:root, :leaves, :levels]

  @doc """
  Creates a new Merkle tree from a list of transactions
  """
  def new(transactions) when is_list(transactions) do
    leaves = transactions
    |> Enum.map(&hash_transaction/1)
    
    tree = build_tree(leaves)
    
    %__MODULE__{
      root: tree.root,
      leaves: leaves,
      levels: tree.levels
    }
  end

  @doc """
  Verifies a transaction is included in the tree
  """
  def verify_inclusion(tree, transaction, proof) do
    leaf_hash = hash_transaction(transaction)
    verify_proof(tree.root, leaf_hash, proof)
  end

  @doc """
  Gets the Merkle proof for a transaction
  """
  def get_proof(tree, transaction) do
    leaf_hash = hash_transaction(transaction)
    
    case Enum.find_index(tree.leaves, &(&1 == leaf_hash)) do
      nil -> {:error, :not_found}
      index -> {:ok, build_proof(tree.levels, index)}
    end
  end

  @doc """
  Updates the tree with new transactions
  """
  def update(tree, new_transactions) do
    all_transactions = tree.leaves ++ Enum.map(new_transactions, &hash_transaction/1)
    new(all_transactions)
  end

  # Private functions

  defp build_tree([]), do: %{root: nil, levels: []}
  defp build_tree([single]), do: %{root: single, levels: [[single]]}
  
  defp build_tree(leaves) do
    levels = build_levels([leaves])
    %{root: hd(List.last(levels)), levels: levels}
  end

  defp build_levels(acc) do
    current_level = hd(acc)
    
    if length(current_level) == 1 do
      Enum.reverse(acc)
    else
      next_level = build_next_level(current_level)
      build_levels([next_level | acc])
    end
  end

  defp build_next_level(nodes) do
    nodes
    |> Enum.chunk_every(2)
    |> Enum.map(&hash_pair/1)
  end

  defp hash_pair([left, right]) do
    hash_nodes(left, right)
  end
  
  defp hash_pair([single]) do
    # For odd number of nodes, duplicate the last one
    hash_nodes(single, single)
  end

  defp hash_nodes(left, right) do
    combined = left <> right
    :crypto.hash(:sha256, combined)
  end

  defp hash_transaction(transaction) when is_map(transaction) do
    transaction
    |> Jason.encode!()
    |> hash_data()
  end

  defp hash_transaction(transaction) when is_binary(transaction) do
    hash_data(transaction)
  end

  defp hash_data(data) do
    :crypto.hash(:sha256, data)
  end

  defp build_proof(levels, index) do
    build_proof_recursive(levels, index, [])
  end

  defp build_proof_recursive([], _index, acc), do: Enum.reverse(acc)
  
  defp build_proof_recursive([level | rest], index, acc) do
    sibling_index = if rem(index, 2) == 0, do: index + 1, else: index - 1
    
    proof_element = if sibling_index < length(level) do
      sibling = Enum.at(level, sibling_index)
      position = if rem(index, 2) == 0, do: :right, else: :left
      {position, sibling}
    else
      nil
    end
    
    new_acc = if proof_element, do: [proof_element | acc], else: acc
    new_index = div(index, 2)
    
    build_proof_recursive(rest, new_index, new_acc)
  end

  defp verify_proof(root, leaf_hash, proof) do
    computed_root = Enum.reduce(proof, leaf_hash, fn
      {:left, sibling}, current ->
        hash_nodes(sibling, current)
      {:right, sibling}, current ->
        hash_nodes(current, sibling)
    end)
    
    computed_root == root
  end
end