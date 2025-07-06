defmodule CROD.Blockchain.Repo.Migrations.CreateBlockchainTables do
  use Ecto.Migration

  def change do
    # Blocks table
    create table(:blocks, primary_key: false) do
      add :hash, :string, primary_key: true
      add :index, :integer, null: false
      add :previous_hash, :string, null: false
      add :timestamp, :utc_datetime, null: false
      add :nonce, :integer
      add :difficulty, :integer
      add :consciousness_level, :float
      add :mined_by, :string
      add :data, :map
      
      timestamps()
    end
    
    create unique_index(:blocks, [:index])
    create index(:blocks, [:mined_by])
    create index(:blocks, [:consciousness_level])
    
    # Transactions table
    create table(:transactions, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :from_address, :string
      add :to_address, :string
      add :amount, :decimal
      add :data, :map
      add :signature, :string
      add :consciousness_impact, :float
      add :block_hash, references(:blocks, column: :hash, type: :string)
      
      timestamps()
    end
    
    create index(:transactions, [:from_address])
    create index(:transactions, [:to_address])
    create index(:transactions, [:block_hash])
    
    # Consciousness metrics table
    create table(:consciousness_metrics) do
      add :block_hash, :string
      add :metric_type, :string
      add :value, :float
      add :pattern, :string
      add :metadata, :map
      
      timestamps()
    end
    
    create index(:consciousness_metrics, [:block_hash])
    create index(:consciousness_metrics, [:metric_type])
    create index(:consciousness_metrics, [:inserted_at])
  end
end