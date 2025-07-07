defmodule Crod.Parasite.Memory do
  @moduledoc """
  Memory management for CROD Parasite.
  Stores and retrieves conversation history and learned patterns.
  """

  alias Crod.Repo
  alias Crod.Schemas.Memory

  defstruct [:store, :patterns, :embeddings]

  @doc """
  Creates a new memory store.
  """
  def new do
    %__MODULE__{
      store: %{},
      patterns: [],
      embeddings: %{}
    }
  end

  @doc """
  Stores a message in memory.
  """
  def store(memory, session_id, type, content) do
    entry = %{
      type: type,
      content: content,
      timestamp: DateTime.utc_now(),
      embedding: generate_embedding(content)
    }
    
    session_memories = Map.get(memory.store, session_id, [])
    updated_memories = session_memories ++ [entry]
    
    %{memory | store: Map.put(memory.store, session_id, updated_memories)}
  end

  @doc """
  Retrieves relevant memories based on similarity.
  """
  def retrieve_similar(memory, query, limit \\ 5) do
    query_embedding = generate_embedding(query)
    
    memory.store
    |> Map.values()
    |> List.flatten()
    |> Enum.map(fn entry ->
      similarity = calculate_similarity(query_embedding, entry.embedding)
      {similarity, entry}
    end)
    |> Enum.sort_by(&elem(&1, 0), :desc)
    |> Enum.take(limit)
    |> Enum.map(&elem(&1, 1))
  end

  @doc """
  Persists memory to database.
  """
  def persist_to_db(memory, session_id) do
    session_memories = Map.get(memory.store, session_id, [])
    
    Enum.each(session_memories, fn entry ->
      %Memory{}
      |> Memory.changeset(%{
        session_id: session_id,
        type: to_string(entry.type),
        content: entry.content,
        embedding: entry.embedding,
        metadata: %{timestamp: entry.timestamp}
      })
      |> Repo.insert()
    end)
  end

  @doc """
  Loads memory from database.
  """
  def load_from_db(session_id) do
    memories = Repo.all(Memory, session_id: session_id)
    
    entries = Enum.map(memories, fn mem ->
      %{
        type: String.to_atom(mem.type),
        content: mem.content,
        timestamp: mem.metadata["timestamp"],
        embedding: mem.embedding
      }
    end)
    
    %__MODULE__{
      store: %{session_id => entries},
      patterns: [],
      embeddings: %{}
    }
  end

  @doc """
  Extracts patterns from stored memories.
  """
  def extract_patterns(memory) do
    all_messages = memory.store
    |> Map.values()
    |> List.flatten()
    |> Enum.map(&(&1.content))
    
    # Simple pattern extraction - can be enhanced
    patterns = all_messages
    |> Enum.chunk_every(2, 1, :discard)
    |> Enum.frequencies()
    |> Enum.filter(fn {_, count} -> count > 2 end)
    |> Enum.map(&elem(&1, 0))
    
    %{memory | patterns: patterns}
  end

  # Private functions

  defp generate_embedding(content) do
    # Placeholder for actual embedding generation
    # Could integrate with embedding services or local models
    content
    |> String.downcase()
    |> String.split()
    |> Enum.map(&:erlang.phash2/1)
    |> Enum.take(128) # Simple 128-dimensional "embedding"
  end

  defp calculate_similarity(embedding1, embedding2) do
    # Simple cosine similarity placeholder
    # Real implementation would use proper vector operations
    common = MapSet.intersection(MapSet.new(embedding1), MapSet.new(embedding2))
    MapSet.size(common) / max(length(embedding1), length(embedding2))
  end
end