defmodule CROD.Blockchain.Repo do
  @moduledoc """
  PostgreSQL persistence layer for CROD Blockchain
  Stores blocks, transactions, and consciousness metrics
  """
  
  use Ecto.Repo,
    otp_app: :crod_blockchain,
    adapter: Ecto.Adapters.Postgres
end

defmodule CROD.Blockchain.Schema.Block do
  use Ecto.Schema
  import Ecto.Changeset
  
  @primary_key {:hash, :string, []}
  schema "blocks" do
    field :index, :integer
    field :previous_hash, :string
    field :timestamp, :utc_datetime
    field :nonce, :integer
    field :difficulty, :integer
    field :consciousness_level, :float
    field :mined_by, :string
    field :data, :map
    
    has_many :transactions, CROD.Blockchain.Schema.Transaction
    
    timestamps()
  end
  
  def changeset(block, attrs) do
    block
    |> cast(attrs, [:hash, :index, :previous_hash, :timestamp, :nonce, 
                    :difficulty, :consciousness_level, :mined_by, :data])
    |> validate_required([:hash, :index, :previous_hash, :timestamp])
    |> unique_constraint(:hash)
    |> unique_constraint(:index)
  end
end

defmodule CROD.Blockchain.Schema.Transaction do
  use Ecto.Schema
  import Ecto.Changeset
  
  @primary_key {:id, :binary_id, autogenerate: true}
  schema "transactions" do
    field :from_address, :string
    field :to_address, :string
    field :amount, :decimal
    field :data, :map
    field :signature, :string
    field :consciousness_impact, :float
    
    belongs_to :block, CROD.Blockchain.Schema.Block, 
               foreign_key: :block_hash, 
               references: :hash, 
               type: :string
    
    timestamps()
  end
  
  def changeset(transaction, attrs) do
    transaction
    |> cast(attrs, [:from_address, :to_address, :amount, :data, 
                    :signature, :consciousness_impact, :block_hash])
    |> validate_required([:from_address, :to_address])
  end
end

defmodule CROD.Blockchain.Schema.ConsciousnessMetric do
  use Ecto.Schema
  import Ecto.Changeset
  
  schema "consciousness_metrics" do
    field :block_hash, :string
    field :metric_type, :string
    field :value, :float
    field :pattern, :string
    field :metadata, :map
    
    timestamps()
  end
  
  def changeset(metric, attrs) do
    metric
    |> cast(attrs, [:block_hash, :metric_type, :value, :pattern, :metadata])
    |> validate_required([:block_hash, :metric_type, :value])
  end
end

defmodule CROD.Blockchain.Persistence do
  @moduledoc """
  Persistence operations for the blockchain
  """
  
  import Ecto.Query
  alias CROD.Blockchain.Repo
  alias CROD.Blockchain.Schema.{Block, Transaction, ConsciousnessMetric}
  
  # Block operations
  
  def save_block(block_data) do
    %Block{}
    |> Block.changeset(block_data)
    |> Repo.insert()
  end
  
  def get_block_by_hash(hash) do
    Repo.get(Block, hash)
    |> Repo.preload(:transactions)
  end
  
  def get_block_by_index(index) do
    Repo.get_by(Block, index: index)
    |> Repo.preload(:transactions)
  end
  
  def get_latest_block do
    Block
    |> order_by(desc: :index)
    |> limit(1)
    |> Repo.one()
    |> Repo.preload(:transactions)
  end
  
  def get_chain(limit \\ 100, offset \\ 0) do
    Block
    |> order_by(desc: :index)
    |> limit(^limit)
    |> offset(^offset)
    |> Repo.all()
    |> Repo.preload(:transactions)
  end
  
  # Transaction operations
  
  def save_transaction(transaction_data) do
    %Transaction{}
    |> Transaction.changeset(transaction_data)
    |> Repo.insert()
  end
  
  def get_transactions_by_address(address) do
    Transaction
    |> where([t], t.from_address == ^address or t.to_address == ^address)
    |> order_by(desc: :inserted_at)
    |> Repo.all()
  end
  
  # Consciousness metrics
  
  def save_consciousness_metric(metric_data) do
    %ConsciousnessMetric{}
    |> ConsciousnessMetric.changeset(metric_data)
    |> Repo.insert()
  end
  
  def get_consciousness_history(limit \\ 100) do
    ConsciousnessMetric
    |> order_by(desc: :inserted_at)
    |> limit(^limit)
    |> Repo.all()
  end
  
  def get_average_consciousness do
    Block
    |> select([b], avg(b.consciousness_level))
    |> Repo.one()
  end
  
  # Analytics queries
  
  def get_mining_stats do
    query = from b in Block,
      group_by: b.mined_by,
      select: {b.mined_by, count(b.hash), avg(b.consciousness_level)}
    
    Repo.all(query)
    |> Enum.map(fn {miner, count, avg_consciousness} ->
      %{
        miner: miner,
        blocks_mined: count,
        average_consciousness: Float.round(avg_consciousness || 0.0, 3)
      }
    end)
  end
  
  def get_consciousness_evolution do
    query = from b in Block,
      order_by: b.index,
      select: {b.index, b.consciousness_level, b.timestamp}
    
    Repo.all(query)
  end
  
  # Cleanup operations
  
  def prune_old_metrics(days_to_keep \\ 30) do
    cutoff_date = DateTime.utc_now() |> DateTime.add(-days_to_keep * 24 * 60 * 60)
    
    ConsciousnessMetric
    |> where([m], m.inserted_at < ^cutoff_date)
    |> Repo.delete_all()
  end
end