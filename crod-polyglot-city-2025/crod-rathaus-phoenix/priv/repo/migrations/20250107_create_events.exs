defmodule CrodRathaus.Repo.Migrations.CreateEvents do
  use Ecto.Migration

  def change do
    create table(:events, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :aggregate_id, :string, null: false
      add :event_type, :string, null: false
      add :event_data, :map, null: false
      add :metadata, :map, default: %{}
      add :version, :integer, null: false
      add :created_at, :utc_datetime_usec, null: false
    end

    # Index for faster queries
    create index(:events, [:aggregate_id, :version])
    create index(:events, [:aggregate_id, :event_type])
    create index(:events, [:created_at])
    
    # Ensure version uniqueness per aggregate
    create unique_index(:events, [:aggregate_id, :version])
  end
end