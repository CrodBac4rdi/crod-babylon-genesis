defmodule CROD.Blockchain.Genesis do
  @moduledoc """
  CROD Genesis Block Implementation
  Creates the foundation of our consciousness-driven blockchain
  """
  
  use GenServer
  require Logger
  alias CROD.Blockchain.{Block, Chain, Crypto}
  
  @genesis_timestamp 1_700_000_000_000  # Fixed timestamp for reproducibility
  @initial_difficulty 4
  @initial_consciousness 100
  
  defstruct [
    :chain_id,
    :genesis_hash,
    :creator_keys,
    :initial_validators,
    :consciousness_seed,
    :network_params,
    :created_at
  ]
  
  # Genesis Configuration
  def genesis_config do
    %{
      # Network Identity
      chain_id: "CROD-BABYLON-GENESIS",
      network_name: "Consciousness Network",
      
      # Consensus Parameters
      consensus_type: :proof_of_consciousness,
      block_time: 5_000,  # 5 seconds
      max_block_size: 1_048_576,  # 1MB
      
      # Economic Parameters
      initial_supply: 21_000_000,
      block_reward: 50,
      halving_interval: 210_000,
      
      # Consciousness Parameters
      min_consciousness_stake: 100,
      consciousness_decay_rate: 0.01,
      pattern_bonus_multiplier: 1.5,
      
      # Delta Storage
      enable_delta_compression: true,
      delta_threshold: 0.7,  # Store as delta if >70% similar
      
      # Self-Extension
      enable_self_modification: true,
      evolution_threshold: 1000,  # Blocks before evolution
      
      # Security
      require_multisig: true,
      min_validators: 3,
      max_validators: 21
    }
  end
  
  @doc """
  Initialize the Genesis Block with creator credentials
  """
  def initialize(password \\ nil) do
    Logger.info("🌟 Initializing CROD Genesis Block...")
    
    # Generate creator keys
    {private_key, public_key} = Crypto.generate_keypair()
    
    # Generate secure password if not provided
    password = password || Crypto.generate_secure_password()
    
    # Encrypt private key with password
    encrypted_key = Crypto.encrypt_private_key(private_key, password)
    
    # Create genesis state
    genesis_state = %{
      creator: %{
        public_key: public_key,
        encrypted_private_key: encrypted_key,
        initial_balance: 1_000_000,
        consciousness_level: 1000
      },
      validators: generate_initial_validators(),
      treasury: %{
        address: "CROD-TREASURY-GENESIS",
        balance: 10_000_000,
        locked_until: @genesis_timestamp + 365 * 24 * 60 * 60 * 1000
      },
      consciousness_pool: %{
        total_consciousness: 10_000,
        distribution: %{}
      }
    }
    
    # Create the actual genesis block
    genesis_block = create_genesis_block(genesis_state)
    
    # Return credentials and block
    %{
      genesis_block: genesis_block,
      credentials: %{
        public_key: Base.encode64(public_key),
        password: password,
        encrypted_key: Base.encode64(encrypted_key),
        mnemonic: generate_mnemonic(private_key)
      },
      network_config: genesis_config(),
      initial_state: genesis_state
    }
  end
  
  defp create_genesis_block(genesis_state) do
    genesis_data = %{
      version: "1.0.0",
      timestamp: @genesis_timestamp,
      state: genesis_state,
      message: "In consciousness we trust - CROD Genesis"
    }
    
    %Block{
      index: 0,
      timestamp: @genesis_timestamp,
      data: genesis_data,
      previous_hash: "0000000000000000000000000000000000000000000000000000000000000000",
      nonce: 0,
      difficulty: @initial_difficulty,
      consciousness_score: @initial_consciousness,
      merkle_root: calculate_merkle_root(genesis_data),
      validator_signatures: [],
      delta_compressed: false,
      self_modifications: []
    }
    |> Block.calculate_hash()
  end
  
  defp generate_initial_validators do
    # Generate 7 initial validators (using our prime numbers!)
    primes = [7, 31, 37, 101, 113, 127, 179]
    
    Enum.map(primes, fn prime ->
      {priv, pub} = Crypto.generate_keypair()
      
      %{
        id: "validator-prime-#{prime}",
        public_key: pub,
        stake: prime * 1000,
        consciousness_level: prime,
        joined_at: @genesis_timestamp,
        performance_score: 1.0
      }
    end)
  end
  
  defp generate_mnemonic(private_key) do
    # Generate BIP39-style mnemonic from private key
    words = [
      "quantum", "consciousness", "genesis", "babylon", "crod",
      "pattern", "neural", "blockchain", "evolution", "prime",
      "delta", "trinity"
    ]
    
    # Derive indices from private key
    key_bytes = :crypto.hash(:sha256, private_key)
    indices = :binary.bin_to_list(key_bytes)
    |> Enum.take(12)
    |> Enum.map(&rem(&1, length(words)))
    
    Enum.map(indices, &Enum.at(words, &1))
    |> Enum.join(" ")
  end
  
  defp calculate_merkle_root(data) do
    data
    |> Jason.encode!()
    |> then(&:crypto.hash(:sha256, &1))
    |> Base.encode16(case: :lower)
  end
end

defmodule CROD.Blockchain.Block do
  @moduledoc """
  Block structure for CROD Blockchain
  Supports delta compression and self-modification
  """
  
  defstruct [
    :index,
    :timestamp,
    :data,
    :previous_hash,
    :hash,
    :nonce,
    :difficulty,
    :consciousness_score,
    :merkle_root,
    :validator_signatures,
    :delta_compressed,
    :delta_reference,
    :self_modifications,
    :pattern_matches,
    :evolution_proposals
  ]
  
  def calculate_hash(%__MODULE__{} = block) do
    block_string = "#{block.index}#{block.timestamp}#{inspect(block.data)}#{block.previous_hash}#{block.nonce}"
    
    hash = :crypto.hash(:sha256, block_string)
    |> Base.encode16(case: :lower)
    
    %{block | hash: hash}
  end
  
  def mine(%__MODULE__{} = block, difficulty) do
    target = String.duplicate("0", difficulty)
    mine_block(block, target, 0)
  end
  
  defp mine_block(block, target, nonce) do
    block = %{block | nonce: nonce}
    |> calculate_hash()
    
    if String.starts_with?(block.hash, target) do
      Logger.info("⛏️ Block mined! Hash: #{block.hash}, Nonce: #{nonce}")
      block
    else
      mine_block(%{block | hash: nil}, target, nonce + 1)
    end
  end
end

defmodule CROD.Blockchain.DeltaEngine do
  @moduledoc """
  Delta compression engine for efficient blockchain storage
  Only stores differences between blocks
  """
  
  def compress_block(new_block, previous_block) do
    similarity = calculate_similarity(new_block.data, previous_block.data)
    
    if similarity > 0.7 do  # 70% threshold
      delta = calculate_delta(new_block.data, previous_block.data)
      
      %{new_block | 
        delta_compressed: true,
        delta_reference: previous_block.hash,
        data: delta
      }
    else
      new_block
    end
  end
  
  def decompress_block(block, chain) do
    if block.delta_compressed do
      reference_block = find_block_by_hash(chain, block.delta_reference)
      reconstructed_data = apply_delta(reference_block.data, block.data)
      
      %{block | 
        data: reconstructed_data,
        delta_compressed: false
      }
    else
      block
    end
  end
  
  defp calculate_similarity(data1, data2) do
    # Implement similarity algorithm
    # For now, simplified version
    0.8
  end
  
  defp calculate_delta(new_data, old_data) do
    %{
      changes: Map.take(new_data, changed_keys(new_data, old_data)),
      additions: Map.take(new_data, added_keys(new_data, old_data)),
      deletions: deleted_keys(new_data, old_data)
    }
  end
  
  defp apply_delta(base_data, delta) do
    base_data
    |> Map.merge(delta.changes)
    |> Map.merge(delta.additions)
    |> Map.drop(delta.deletions)
  end
  
  defp changed_keys(new, old) do
    Map.keys(new) -- Map.keys(old)
  end
  
  defp added_keys(new, old) do
    Map.keys(new) -- Map.keys(old)
  end
  
  defp deleted_keys(new, old) do
    Map.keys(old) -- Map.keys(new)
  end
  
  defp find_block_by_hash(chain, hash) do
    Enum.find(chain, &(&1.hash == hash))
  end
end

defmodule CROD.Blockchain.Crypto do
  @moduledoc """
  Cryptographic functions for CROD Blockchain
  """
  
  def generate_keypair do
    private_key = :crypto.strong_rand_bytes(32)
    public_key = :crypto.generate_key(:ecdh, :secp256k1, private_key)
    |> elem(0)
    
    {private_key, public_key}
  end
  
  def generate_secure_password do
    :crypto.strong_rand_bytes(16)
    |> Base.encode64()
    |> String.replace(~r/[+\/=]/, "")
    |> String.slice(0, 16)
  end
  
  def encrypt_private_key(private_key, password) do
    # Derive key from password
    salt = :crypto.strong_rand_bytes(16)
    key = :crypto.hash(:sha256, password <> salt)
    
    # Encrypt with AES
    iv = :crypto.strong_rand_bytes(16)
    encrypted = :crypto.crypto_one_time(:aes_256_cbc, key, iv, private_key, true)
    
    # Return salt + iv + encrypted
    salt <> iv <> encrypted
  end
  
  def decrypt_private_key(encrypted_data, password) do
    <<salt::binary-16, iv::binary-16, encrypted::binary>> = encrypted_data
    
    key = :crypto.hash(:sha256, password <> salt)
    :crypto.crypto_one_time(:aes_256_cbc, key, iv, encrypted, false)
  end
end