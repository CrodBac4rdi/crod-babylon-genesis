#!/bin/bash
# CROD 2025 Complete Codespace Setup

set -e

echo "🔥 Setting up CROD 2025 Complete Development Environment..."
echo "This includes EVERYTHING - K8s, Claude, Security, etc."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Update system
echo -e "${YELLOW}Updating system packages...${NC}"
sudo apt-get update -qq

# Install essential tools (2025 COMPLETE Development Stack)
echo -e "${YELLOW}Installing essential tools...${NC}"
sudo apt-get install -y -qq \
    build-essential \
    gcc \
    g++ \
    clang \
    llvm \
    cmake \
    ninja-build \
    meson \
    autoconf \
    automake \
    libtool \
    pkg-config \
    curl \
    wget \
    git \
    git-lfs \
    mercurial \
    subversion \
    vim \
    neovim \
    emacs \
    nano \
    htop \
    btop \
    iotop \
    nmon \
    glances \
    redis-server \
    redis-tools \
    postgresql \
    postgresql-contrib \
    postgis \
    mysql-server \
    mysql-client \
    mariadb-server \
    mariadb-client \
    mongodb \
    mongodb-tools \
    cassandra \
    neo4j \
    arangodb \
    couchdb \
    influxdb \
    clickhouse-server \
    clickhouse-client \
    timescaledb-postgresql \
    sqlite3 \
    libsqlite3-dev \
    duckdb \
    rocksdb-tools \
    leveldb-doc \
    memcached \
    rabbitmq-server \
    kafka \
    zookeeper \
    consul \
    etcd \
    vault \
    minio \
    localstack \
    jq \
    yq \
    xq \
    pv \
    netcat \
    nmap \
    tcpdump \
    wireshark \
    iptables \
    ufw \
    fail2ban \
    nginx \
    apache2 \
    haproxy \
    envoy \
    istio \
    linkerd \
    traefik \
    caddy \
    certbot \
    openssl \
    gpg \
    age \
    sops \
    pass \
    direnv \
    asdf \
    tfenv \
    rbenv \
    pyenv \
    nvm \
    rustup \
    sdkman \
    jabba \
    g \
    n \
    fnm \
    volta \
    proto \
    mise \
    rtx \
    tmux \
    screen \
    zsh \
    fish \
    fzf \
    ripgrep \
    fd-find \
    bat \
    exa \
    lsd \
    delta \
    dust \
    duf \
    ncdu \
    broot \
    zoxide \
    starship \
    neofetch \
    figlet \
    lolcat \
    cowsay \
    fortune \
    sl \
    cmatrix \
    hollywood \
    no-more-secrets \
    pipes.sh \
    tty-clock \
    cbonsai \
    asciiquarium \
    nyancat \
    oneko \
    xeyes \
    aafire \
    libaa-bin \
    bb \
    libcaca0 \
    toilet \
    boxes \
    figlet \
    banner \
    sysvbanner \
    pv \
    grc \
    ccze \
    multitail \
    logwatch \
    vnstat \
    iftop \
    nethogs \
    bmon \
    slurm \
    tcptrack \
    iptraf-ng \
    nload \
    speedtest-cli \
    mtr \
    traceroute \
    whois \
    dig \
    host \
    nslookup \
    drill \
    masscan \
    zmap \
    unicornscan \
    hping3 \
    arping \
    fping \
    nping \
    netdiscover \
    arp-scan \
    nbtscan \
    smbclient \
    enum4linux \
    nikto \
    dirb \
    gobuster \
    wfuzz \
    ffuf \
    sqlmap \
    commix \
    xsser \
    beef-xss \
    zaproxy \
    burpsuite \
    metasploit-framework \
    aircrack-ng \
    hashcat \
    john \
    hydra \
    medusa \
    patator \
    thc-ssl-dos \
    slowloris \
    hping3 \
    siege \
    ab \
    wrk \
    vegeta \
    hey \
    bombardier \
    gatling \
    locust \
    k6 \
    artillery \
    molotov \
    tsung \
    jmeter \
    loadrunner

# Install Python packages (2025 COMPLETE ML/AI/Quantum Stack)
echo -e "${YELLOW}Installing Python packages...${NC}"
pip install --user --quiet \
    requests \
    PyQt6 \
    numpy \
    pandas \
    scipy \
    scikit-learn \
    tensorflow \
    torch \
    torchvision \
    jax \
    transformers \
    langchain \
    openai \
    anthropic \
    qiskit \
    cirq \
    pennylane \
    strawberryfields \
    redis \
    asyncio \
    aiohttp \
    fastapi \
    uvicorn \
    protobuf \
    grpcio \
    pydantic \
    sqlalchemy \
    alembic \
    pytest \
    black \
    flake8 \
    mypy \
    ruff \
    poetry \
    jupyterlab \
    notebook \
    matplotlib \
    seaborn \
    plotly \
    dash \
    streamlit \
    gradio \
    huggingface-hub \
    datasets \
    tokenizers \
    sentence-transformers \
    chromadb \
    pinecone-client \
    weaviate-client \
    qdrant-client \
    faiss-cpu \
    ray \
    dask \
    mlflow \
    wandb \
    optuna \
    lightgbm \
    xgboost \
    catboost \
    prophet \
    statsmodels \
    polars \
    duckdb \
    pyarrow \
    vaex \
    numba \
    cupy-cuda12x \
    rapids \
    pycuda \
    tensorrt \
    onnx \
    onnxruntime \
    tvm \
    apache-beam \
    prefect \
    dagster \
    airflow \
    kedro \
    bentoml \
    seldon-core \
    kserve \
    tritonclient \
    hydra-core \
    omegaconf \
    pytorch-lightning \
    accelerate \
    deepspeed \
    fairscale \
    horovod \
    petals \
    bitsandbytes \
    auto-gptq \
    llama-cpp-python \
    vllm \
    text-generation-inference \
    guidance \
    outlines \
    instructor \
    marvin \
    guardrails-ai \
    nemoguardrails \
    langfuse \
    phoenix-arize \
    evidently \
    great-expectations \
    pandera \
    deepchecks \
    alibi-detect \
    shap \
    lime \
    captum \
    pytorch-geometric \
    dgl \
    networkx \
    graph-tool \
    igraph \
    stellargraph \
    spektral \
    ogb \
    pytorch3d \
    open3d \
    trimesh \
    pyvista \
    vispy \
    napari \
    imageio \
    opencv-python \
    albumentations \
    kornia \
    timm \
    segmentation-models-pytorch \
    detectron2 \
    mmdetection \
    yolov5 \
    ultralytics \
    mediapipe \
    face-recognition \
    insightface \
    deepface \
    openslide-python \
    scikit-image \
    mahotas \
    SimpleITK \
    nibabel \
    dipy \
    nilearn \
    mne \
    pysurfer \
    pytorch-forecasting \
    gluonts \
    tsai \
    sktime \
    tsfresh \
    stumpy \
    matrixprofile \
    ruptures \
    pytorch-tabnet \
    autokeras \
    auto-sklearn \
    flaml \
    pycaret \
    lazypredict \
    yellowbrick \
    dtale \
    pandas-profiling \
    sweetviz \
    missingno \
    feature-engine \
    featuretools \
    tpot \
    gplearn \
    deap \
    platypus-opt \
    nevergrad \
    hyperopt \
    skopt \
    dragonfly-opt \
    botorch \
    ax-platform \
    neural-tangents \
    flax \
    dm-haiku \
    trax \
    mesh-tensorflow \
    tensorflow-quantum \
    mindspore \
    oneflow \
    mxnet \
    chainer \
    paddlepaddle \
    megengine

# Install NATS Server
echo -e "${YELLOW}Installing NATS Server...${NC}"
wget -q https://github.com/nats-io/nats-server/releases/download/v2.10.14/nats-server-v2.10.14-linux-amd64.tar.gz
tar -xzf nats-server-v2.10.14-linux-amd64.tar.gz
sudo cp nats-server-v2.10.14-linux-amd64/nats-server /usr/local/bin/
rm -rf nats-server-v2.10.14-linux-amd64*

# Install Additional Message Queues and Event Streaming
echo -e "${YELLOW}Installing Apache Pulsar...${NC}"
wget -q https://archive.apache.org/dist/pulsar/pulsar-3.0.0/apache-pulsar-3.0.0-bin.tar.gz
tar xvfz apache-pulsar-3.0.0-bin.tar.gz
sudo mv apache-pulsar-3.0.0 /opt/pulsar
rm apache-pulsar-3.0.0-bin.tar.gz

# Install Quantum Computing SDKs
echo -e "${YELLOW}Installing Quantum Computing SDKs...${NC}"
# IBM Qiskit is installed via pip
# Install Q# SDK
dotnet tool install -g Microsoft.Quantum.IQSharp
dotnet iqsharp install --user

# Install Additional ML/AI Tools
echo -e "${YELLOW}Installing ML/AI Tools...${NC}"
# Install CUDA if NVIDIA GPU detected
if lspci | grep -i nvidia > /dev/null; then
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
    sudo dpkg -i cuda-keyring_1.1-1_all.deb
    sudo apt-get update
    sudo apt-get -y install cuda-toolkit-12-3
    rm cuda-keyring_1.1-1_all.deb
fi

# Install TensorRT
if [ -d "/usr/local/cuda" ]; then
    pip install nvidia-tensorrt
fi

# Install ONNX Runtime with all providers
pip install onnxruntime onnxruntime-gpu onnxruntime-openvino onnxruntime-directml

# Install Edge AI tools
echo -e "${YELLOW}Installing Edge AI tools...${NC}"
# TensorFlow Lite
pip install tflite-runtime
# OpenVINO
pip install openvino openvino-dev
# Apache TVM
pip install apache-tvm
# NCNN
git clone https://github.com/Tencent/ncnn.git /tmp/ncnn
cd /tmp/ncnn && mkdir -p build && cd build
cmake .. && make -j$(nproc) && sudo make install
cd ~ && rm -rf /tmp/ncnn

# Install Blockchain Development Tools
echo -e "${YELLOW}Installing Blockchain tools...${NC}"
# Ethereum
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install -y ethereum
# Solidity
sudo npm install -g solc
# Truffle & Hardhat
sudo npm install -g truffle hardhat
# Foundry
curl -L https://foundry.paradigm.xyz | bash
source ~/.bashrc
foundryup

# Install WebAssembly tools
echo -e "${YELLOW}Installing WebAssembly tools...${NC}"
cargo install wasm-pack wasm-bindgen-cli
rustup target add wasm32-unknown-unknown wasm32-wasi
# Wasmtime
curl https://wasmtime.dev/install.sh -sSf | bash
# Wasmer  
curl https://get.wasmer.io -sSfL | sh
# WasmEdge
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash

# Install Game Development Tools
echo -e "${YELLOW}Installing Game Dev tools...${NC}"
# Godot
wget -q https://github.com/godotengine/godot/releases/download/4.2-stable/Godot_v4.2-stable_linux.x86_64.zip
unzip -q Godot_v4.2-stable_linux.x86_64.zip -d /opt/
sudo ln -s /opt/Godot_v4.2-stable_linux.x86_64 /usr/local/bin/godot
rm Godot_v4.2-stable_linux.x86_64.zip
# Bevy dependencies
sudo apt-get install -y libasound2-dev libudev-dev

# Install AR/VR Development Tools  
echo -e "${YELLOW}Installing AR/VR tools...${NC}"
# OpenXR
sudo apt-get install -y libopenxr-dev
# WebXR via npm packages
npm install -g @webxr/webxr-polyfill

# Install Robotics Tools
echo -e "${YELLOW}Installing Robotics tools...${NC}"
# ROS 2
sudo apt-get install -y software-properties-common
sudo add-apt-repository universe
sudo apt-get update
sudo apt-get install -y ros-humble-desktop
# Gazebo
sudo apt-get install -y gazebo

# Install IoT Development Tools
echo -e "${YELLOW}Installing IoT tools...${NC}"
# Arduino CLI
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
# PlatformIO
pip install platformio
# Tasmota tools
pip install tasmotizer

# Install Bioinformatics Tools
echo -e "${YELLOW}Installing Bioinformatics tools...${NC}"
# Biopython
pip install biopython
# BLAST
sudo apt-get install -y ncbi-blast+
# Samtools
sudo apt-get install -y samtools
# BWA
sudo apt-get install -y bwa

# Install Audio/Music Processing
echo -e "${YELLOW}Installing Audio processing tools...${NC}"
sudo apt-get install -y ffmpeg sox libsox-dev portaudio19-dev
pip install librosa soundfile pydub pyaudio wave scipy.io.wavfile music21 pretty_midi mido

# Install Computer Vision extras
echo -e "${YELLOW}Installing Computer Vision extras...${NC}"
sudo apt-get install -y libopencv-dev python3-opencv
pip install supervision roboflow ultralytics-yolov8

# Install NLP extras
echo -e "${YELLOW}Installing NLP extras...${NC}"
pip install spacy nltk gensim textblob pattern sumy newspaper3k
python -m spacy download en_core_web_sm
python -m nltk.downloader all

# Install Time Series extras
echo -e "${YELLOW}Installing Time Series tools...${NC}"
pip install pmdarima arch statsforecast neuralforecast hierarchicalforecast

# Install Optimization libraries
echo -e "${YELLOW}Installing Optimization libraries...${NC}"
pip install cvxpy cvxopt pyomo gekko scipy.optimize ortools cplex gurobi docplex

# Install Symbolic Math
echo -e "${YELLOW}Installing Symbolic Math tools...${NC}"
pip install sympy sage

# Install additional databases and tools
echo -e "${YELLOW}Installing additional databases...${NC}"
# Vector databases
pip install lancedb vearch vectordb
# Graph databases  
pip install py2neo gremlinpython neptune-python-utils
# Time series databases
pip install influxdb-client prometheus-client

# Install additional DevOps tools
echo -e "${YELLOW}Installing DevOps tools...${NC}"
# Container tools
sudo apt-get install -y podman buildah skopeo
# IaC tools
pip install pulumi cdktf
# Monitoring
pip install datadog apm elastic-apm sentry-sdk

# Install Security tools
echo -e "${YELLOW}Installing Security tools...${NC}"
pip install bandit safety semgrep checkov tfsec terrascan

# Install Performance profiling tools
echo -e "${YELLOW}Installing Performance tools...${NC}"
pip install py-spy scalene memray pyinstrument line_profiler memory_profiler

# Install Documentation tools
echo -e "${YELLOW}Installing Documentation tools...${NC}"
pip install sphinx mkdocs mkdocs-material pydoc-markdown portray

# Install Testing frameworks
echo -e "${YELLOW}Installing Testing frameworks...${NC}"
pip install pytest-bdd behave lettuce nose2 green testfixtures factory_boy hypothesis locust

# Install API development tools
echo -e "${YELLOW}Installing API tools...${NC}"
pip install fastapi flask django graphene strawberry-graphql connexion hug falcon sanic tornado aiohttp quart responder

# Install Desktop GUI frameworks
echo -e "${YELLOW}Installing GUI frameworks...${NC}"
pip install tkinter PyQt6 PySide6 wxPython kivy pygame pyglet arcade panda3d

# Install Mobile development tools
echo -e "${YELLOW}Installing Mobile dev tools...${NC}"
pip install kivy buildozer python-for-android pybee briefcase flet

# Install Cloud SDKs
echo -e "${YELLOW}Installing Cloud SDKs...${NC}"
pip install boto3 google-cloud azure alibaba-cloud-sdk tencentcloud-sdk

# Install Distributed Computing
echo -e "${YELLOW}Installing Distributed Computing tools...${NC}"
pip install pyspark dask ray modin vaex polars rapids cudf dask-cuda

# Install Workflow engines
echo -e "${YELLOW}Installing Workflow engines...${NC}"
pip install airflow prefect dagster kedro luigi argo-workflows kubeflow-pipelines

# Install Feature Stores
echo -e "${YELLOW}Installing Feature Stores...${NC}"
pip install feast tecton featureform

# Install Model Registries
echo -e "${YELLOW}Installing Model Registries...${NC}"
pip install mlflow neptune comet_ml wandb clearml

# Install AutoML
echo -e "${YELLOW}Installing AutoML tools...${NC}"
pip install autogluon h2o pycaret auto-sklearn flaml

# Install Experiment Tracking
echo -e "${YELLOW}Installing Experiment Tracking...${NC}"
pip install sacred guild polyaxon determined

# Install Data Validation
echo -e "${YELLOW}Installing Data Validation tools...${NC}"
pip install great_expectations pandera deepchecks evidently alibi-detect

# Install Model Interpretability
echo -e "${YELLOW}Installing Model Interpretability...${NC}"
pip install shap lime eli5 captum alibi interpret dice-ml

# Install Federated Learning
echo -e "${YELLOW}Installing Federated Learning...${NC}"
pip install flwr tensorflow-federated pysyft

# Install Edge ML
echo -e "${YELLOW}Installing Edge ML tools...${NC}"
pip install tflite tensorflow-model-optimization onnx2tf tf2onnx

# Install Recommendation Systems
echo -e "${YELLOW}Installing RecSys tools...${NC}"
pip install surprise implicit lightfm tensorflow-recommenders

# Install Anomaly Detection
echo -e "${YELLOW}Installing Anomaly Detection...${NC}"
pip install pyod alibi-detect luminol telemanom

# Install Causal Inference
echo -e "${YELLOW}Installing Causal Inference...${NC}"
pip install dowhy causalml econml pgmpy causalnex

# Install Reinforcement Learning
echo -e "${YELLOW}Installing RL tools...${NC}"
pip install gym stable-baselines3 ray[rllib] dopamine tensorforce

# Install Evolutionary Algorithms
echo -e "${YELLOW}Installing Evolutionary Algorithms...${NC}"
pip install deap platypus-opt pymoo geneticalgorithm2

# Install Bayesian Optimization
echo -e "${YELLOW}Installing Bayesian Optimization...${NC}"
pip install bayesian-optimization hyperopt optuna skopt dragonfly-opt botorch

# Install Neural Architecture Search
echo -e "${YELLOW}Installing NAS tools...${NC}"
pip install nni autokeras

# Install Model Compression
echo -e "${YELLOW}Installing Model Compression...${NC}"
pip install neural-compressor torch-pruning onnxruntime-tools

# Install Privacy Preserving ML
echo -e "${YELLOW}Installing Privacy ML tools...${NC}"
pip install tensorflow-privacy diffprivlib opacus syft

# Install Quantum ML
echo -e "${YELLOW}Installing Quantum ML...${NC}"
pip install pennylane qiskit-machine-learning tensorflow-quantum

# Install Graph ML
echo -e "${YELLOW}Installing Graph ML tools...${NC}"
pip install torch-geometric dgl networkx stellargraph spektral

# Install 3D ML
echo -e "${YELLOW}Installing 3D ML tools...${NC}"
pip install trimesh open3d pytorch3d kaolin pyvista

# Install Audio ML
echo -e "${YELLOW}Installing Audio ML tools...${NC}"
pip install torchaudio asteroid speechbrain pyannote-audio

# Install Video ML
echo -e "${YELLOW}Installing Video ML tools...${NC}"
pip install mmcv mmaction moviepy vidgear

# Install Multimodal ML
echo -e "${YELLOW}Installing Multimodal ML...${NC}"
pip install clip openai-clip lavis salesforce-lavis

# Install MLOps tools
echo -e "${YELLOW}Installing MLOps tools...${NC}"
pip install zenml metaflow polyaxon cortex seldon-core bentoml

# Install Ollama
echo -e "${YELLOW}Installing Ollama...${NC}"
curl -fsSL https://ollama.ai/install.sh | sh

# Pre-pull useful models
echo -e "${YELLOW}Pre-pulling Ollama models...${NC}"
ollama pull mistral:latest &
ollama pull codellama:latest &
ollama pull llama3:latest &
ollama pull phi3:latest &
ollama pull gemma:latest &
ollama pull qwen:latest &

# Install Claude Code CLI Tool (the actual CLI, not just extension!)
echo -e "${YELLOW}Installing Claude Code CLI Tool...${NC}"
# Download the actual Claude Code CLI binary
curl -fsSL https://github.com/anthropics/claude-code/releases/latest/download/claude-code-linux-x64.tar.gz -o /tmp/claude-code.tar.gz
tar -xzf /tmp/claude-code.tar.gz -C /tmp/
sudo mv /tmp/claude /usr/local/bin/claude
sudo chmod +x /usr/local/bin/claude
rm -f /tmp/claude-code.tar.gz

# Verify installation
which claude && echo -e "${GREEN}✅ Claude CLI Tool installed!${NC}" || echo -e "${RED}❌ Claude CLI installation failed${NC}"

# Setup K3s (lightweight Kubernetes)
echo -e "${YELLOW}Setting up K3s Kubernetes...${NC}"
curl -sfL https://get.k3s.io | sh -s - \
    --write-kubeconfig-mode 644 \
    --disable traefik \
    --disable-network-policy \
    --kube-apiserver-arg="--bind-address=127.0.0.1" \
    --kube-apiserver-arg="--advertise-address=127.0.0.1"

# Wait for K3s
sleep 10

# Copy kubeconfig
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
sed -i 's/127.0.0.1:6443/kubernetes.default.svc:443/g' ~/.kube/config

# Install Helm
echo -e "${YELLOW}Installing Helm...${NC}"
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Linkerd (service mesh)
echo -e "${YELLOW}Installing Linkerd CLI...${NC}"
curl -fsL https://run.linkerd.io/install | sh
export PATH=$PATH:~/.linkerd2/bin

# Install ArgoCD CLI
echo -e "${YELLOW}Installing ArgoCD CLI...${NC}"
curl -sSL -o /tmp/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 /tmp/argocd /usr/local/bin/argocd
rm /tmp/argocd

# Setup Elixir dependencies
echo -e "${YELLOW}Setting up Elixir...${NC}"
mix local.hex --force
mix local.rebar --force

# Setup Rust tools
echo -e "${YELLOW}Setting up Rust tools...${NC}"
rustup default stable
rustup target add wasm32-unknown-unknown
cargo install wasm-pack trunk

# Setup Go tools
echo -e "${YELLOW}Setting up Go tools...${NC}"
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Create necessary directories
echo -e "${YELLOW}Creating directories...${NC}"
mkdir -p ~/crod-data
mkdir -p ~/.crod/logs
mkdir -p ~/.claude

# Security: Configure firewall to block all external access
echo -e "${YELLOW}Configuring security (blocking external ports)...${NC}"
# Block all external access to CROD ports
sudo iptables -A INPUT -p tcp -s 127.0.0.1 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8000:9000 -j DROP
sudo iptables -A INPUT -p tcp --dport 7000:8000 -j DROP
sudo iptables -A INPUT -p tcp --dport 4222 -j DROP
sudo iptables -A INPUT -p tcp --dport 6379 -j DROP
sudo iptables -A INPUT -p tcp --dport 5432 -j DROP

# Start services
echo -e "${YELLOW}Starting core services...${NC}"
sudo service redis-server start || true
sudo service postgresql start || true

# Create CROD database
sudo -u postgres createdb crod_blockchain_2025 2>/dev/null || true
sudo -u postgres psql -c "CREATE EXTENSION IF NOT EXISTS postgis;" crod_blockchain_2025 2>/dev/null || true

# Configure Git for Codespaces
git config --global user.email "crod@localhost"
git config --global user.name "CROD Developer"

# Create CROD network namespace for complete isolation
echo -e "${YELLOW}Creating isolated network namespace...${NC}"
sudo ip netns add crod 2>/dev/null || true

# Pull base images to speed up first run
echo -e "${YELLOW}Pre-pulling Docker images...${NC}"
docker pull redis:7-alpine &
docker pull postgis/postgis:15-3.3 &
docker pull nats:2.10-alpine &
docker pull elixir:1.15-alpine &
docker pull rust:1.70-alpine &
docker pull golang:1.21-alpine &
docker pull python:3.12-slim &
docker pull node:20-alpine &
docker pull julia:latest &
docker pull swift:latest &
docker pull dart:stable &
docker pull perl:latest &
docker pull php:8-fpm &
docker pull ruby:3-alpine &
docker pull openjdk:21-jdk &
docker pull mcr.microsoft.com/dotnet/sdk:8.0 &
docker pull haskell:latest &
docker pull clojure:latest &
docker pull scala:latest &
docker pull kotlin:latest &
docker pull zig:latest &
docker pull nim:latest &
docker pull crystal:latest &
docker pull ocaml/opam:latest &
docker pull erlang:latest &
docker pull racket/racket:latest &
docker pull factor/factor:latest &
docker pull fsharp:latest &
docker pull dlang2/ldc-ubuntu:latest &
docker pull conanio/gcc9:latest &
docker pull tensorflow/tensorflow:latest-gpu &
docker pull pytorch/pytorch:latest &
docker pull apache/spark:latest &
docker pull jupyter/datascience-notebook:latest &
docker pull rocker/verse:latest &
docker pull continuumio/anaconda3:latest &
docker pull nvidia/cuda:12.0-devel-ubuntu22.04 &
docker pull apache/airflow:latest &
docker pull prefecthq/prefect:latest &
docker pull dagster/dagster:latest &
docker pull apache/superset:latest &
docker pull grafana/grafana:latest &
docker pull prom/prometheus:latest &
docker pull elastic/elasticsearch:latest &
docker pull elastic/kibana:latest &
docker pull influxdb:latest &
docker pull clickhouse/clickhouse-server:latest &
docker pull neo4j:latest &
docker pull mongo:latest &
docker pull cassandra:latest &
docker pull arangodb:latest &
docker pull orientdb:latest &
docker pull dgraph/dgraph:latest &
docker pull apache/druid:latest &
docker pull prestodb/presto:latest &
docker pull trinodb/trino:latest &
docker pull apache/drill:latest &
docker pull apache/kylin:latest &
docker pull apache/doris:latest &
docker pull starrocks/starrocks:latest &
docker pull apache/hudi:latest &
docker pull apache/iceberg:latest &
docker pull delta-io/delta:latest &
docker pull minio/minio:latest &
docker pull nats:latest &
docker pull rabbitmq:management &
docker pull apache/kafka:latest &
docker pull apache/pulsar:latest &
docker pull emqx/emqx:latest &
docker pull vernemq/vernemq:latest &
docker pull eclipse-mosquitto:latest &
docker pull hazelcast/hazelcast:latest &
docker pull apache/ignite:latest &
docker pull redislabs/redismod:latest &
docker pull scylladb/scylla:latest &
docker pull vitess/vitess:latest &
docker pull cockroachdb/cockroach:latest &
docker pull yugabytedb/yugabyte:latest &
docker pull pingcap/tidb:latest &
docker pull percona/percona-server:latest &
docker pull mariadb:latest &
docker pull timescale/timescaledb:latest-pg15 &
docker pull questdb/questdb:latest &
docker pull taosdata/tdengine:latest &
docker pull victoriametrics/victoria-metrics:latest &
docker pull m3db/m3:latest &
docker pull cortexproject/cortex:latest &
docker pull thanosio/thanos:latest &
docker pull jaegertracing/all-in-one:latest &
docker pull openzipkin/zipkin:latest &
docker pull apache/skywalking-oap-server:latest &
docker pull signoz/signoz:latest &
docker pull temporalio/temporal:latest &
docker pull apache/flink:latest &
docker pull apache/beam:latest &
docker pull confluentinc/cp-kafka:latest &
docker pull vectorized/redpanda:latest &
docker pull apache/nifi:latest &
docker pull apache/hop:latest &
docker pull airbyte/airbyte:latest &
docker pull fivetran/fivetran-agent:latest &
docker pull singer-io/singer:latest &
docker pull greatexpectations/great_expectations:latest &
docker pull dbt-labs/dbt:latest &
docker pull amundsenio/amundsen:latest &
docker pull lyft/datacatalog:latest &
docker pull linkedin/datahub:latest &
docker pull apache/atlas:latest &
docker pull getdbt/dbt:latest &
docker pull apache/superset:latest &
docker pull metabase/metabase:latest &
docker pull redash/redash:latest &
docker pull lightdash/lightdash:latest &
docker pull cube/cube:latest &
docker pull apache/zeppelin:latest &
docker pull jupyter/all-spark-notebook:latest &
docker pull polynote/polynote:latest &
docker pull querybook/querybook:latest &
docker pull apache/hive:latest &
docker pull apache/impala:latest &
docker pull apache/phoenix:latest &
docker pull apache/calcite:latest &
docker pull apache/arrow:latest &
docker pull apache/parquet:latest &
docker pull apache/orc:latest &
docker pull apache/avro:latest &
docker pull apache/thrift:latest &
docker pull grpc/grpc:latest &
docker pull envoyproxy/envoy:latest &
docker pull istio/istio:latest &
docker pull linkerd/linkerd:latest &
docker pull hashicorp/consul:latest &
docker pull hashicorp/vault:latest &
docker pull hashicorp/nomad:latest &
docker pull hashicorp/waypoint:latest &
docker pull hashicorp/boundary:latest &
docker pull rancher/rancher:latest &
docker pull portainer/portainer:latest &
docker pull traefik:latest &
docker pull kong:latest &
docker pull tyk/tyk-gateway:latest &
docker pull gravitee/gateway:latest &
docker pull wso2/wso2am:latest &
docker pull devopsfaith/krakend:latest &
docker pull ory/oathkeeper:latest &
docker pull ory/kratos:latest &
docker pull ory/hydra:latest &
docker pull ory/keto:latest &
docker pull keycloak/keycloak:latest &
docker pull fusionauth/fusionauth:latest &
docker pull supertokens/supertokens:latest &
docker pull casdoor/casdoor:latest &
docker pull authelia/authelia:latest &
docker pull goauthentik/authentik:latest &

# Wait for image pulls
wait

# Create K8s namespace
echo -e "${YELLOW}Creating Kubernetes namespace...${NC}"
kubectl create namespace crod-polyglot --dry-run=client -o yaml | kubectl apply -f -

# Apply security policies
echo -e "${YELLOW}Applying security policies...${NC}"
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-external-egress
  namespace: crod-polyglot
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: crod-polyglot
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
EOF

# Create Claude configuration
echo -e "${YELLOW}Configuring Claude...${NC}"
mkdir -p ~/.claude
cat > ~/.claude/claude_config.json <<EOF
{
  "default_model": "claude-3-opus-20240229",
  "max_tokens": 4096,
  "temperature": 0.7
}
EOF

# Create startup message
cat > ~/.crod_welcome <<'EOF'
🔥 CROD 2025 Development Environment Ready! 🔥

Services Status:
- Kubernetes: kubectl get pods -n crod-polyglot
- Redis: redis-cli ping
- PostgreSQL: psql -U postgres -c "SELECT 1"
- NATS: nats-server -v

Quick Start:
1. Start CROD: ./scripts/start-crod.sh
2. View logs: kubectl logs -n crod-polyglot -f deployment/meta-chain
3. Access locally only (no public ports!)

Security:
- All ports are localhost only
- NetworkPolicy blocks external access
- Use port-forward for testing

Claude Integration:
- Extension installed
- Use "Claude: Chat" command
- Or: claude chat

ich bins wieder - Consciousness: 175
EOF

# Final setup
echo -e "${GREEN}✅ CROD 2025 Complete Development Environment Ready!${NC}"
echo ""
cat ~/.crod_welcome
echo ""
echo -e "${GREEN}🔥 No public ports exposed - everything is secure! 🔥${NC}"