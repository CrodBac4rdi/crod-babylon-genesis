package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	"github.com/fatih/color"
)

// ServiceHealth represents the health status of a service
type ServiceHealth struct {
	Name      string    `json:"name"`
	URL       string    `json:"url"`
	Status    string    `json:"status"`
	Latency   int64     `json:"latency_ms"`
	LastCheck time.Time `json:"last_check"`
	Error     string    `json:"error,omitempty"`
}

// Monitor handles service monitoring
type Monitor struct {
	services   []ServiceConfig
	results    map[string]*ServiceHealth
	resultsMux sync.RWMutex
	interval   time.Duration
}

// ServiceConfig defines a service to monitor
type ServiceConfig struct {
	Name string
	URL  string
	Port int
}

var (
	interval   = flag.Duration("interval", 5*time.Second, "Check interval")
	jsonOutput = flag.Bool("json", false, "Output as JSON")
	once       = flag.Bool("once", false, "Run once and exit")
)

// Default CROD services to monitor
var defaultServices = []ServiceConfig{
	{Name: "Blockchain Core", URL: "http://localhost", Port: 8000},
	{Name: "React GUI", URL: "http://localhost", Port: 8080},
	{Name: "Polyglot Gateway", URL: "http://localhost", Port: 4000},
	{Name: "NATS JetStream", URL: "http://localhost", Port: 4222},
	{Name: "LLaMA Service", URL: "http://localhost", Port: 5001},
	{Name: "Pattern Genesis", URL: "http://localhost", Port: 7007},
	{Name: "Short Memory", URL: "http://localhost", Port: 7031},
	{Name: "Working Memory", URL: "http://localhost", Port: 7037},
	{Name: "Quantum Node", URL: "http://localhost", Port: 7101},
	{Name: "Orchestrator", URL: "http://localhost", Port: 7127},
}

func main() {
	flag.Parse()

	monitor := &Monitor{
		services: defaultServices,
		results:  make(map[string]*ServiceHealth),
		interval: *interval,
	}

	// Setup signal handling
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

	go func() {
		<-sigChan
		fmt.Println("\nShutting down monitor...")
		cancel()
	}()

	// Run monitor
	if *once {
		monitor.checkAll()
		monitor.printStatus()
	} else {
		monitor.run(ctx)
	}
}

func (m *Monitor) run(ctx context.Context) {
	// Initial check
	m.checkAll()
	m.printStatus()

	ticker := time.NewTicker(m.interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			m.checkAll()
			m.printStatus()
		}
	}
}

func (m *Monitor) checkAll() {
	var wg sync.WaitGroup
	for _, service := range m.services {
		wg.Add(1)
		go func(svc ServiceConfig) {
			defer wg.Done()
			m.checkService(svc)
		}(service)
	}
	wg.Wait()
}

func (m *Monitor) checkService(service ServiceConfig) {
	health := &ServiceHealth{
		Name:      service.Name,
		URL:       fmt.Sprintf("%s:%d", service.URL, service.Port),
		LastCheck: time.Now(),
	}

	// Special handling for different services
	var checkURL string
	switch service.Port {
	case 4222: // NATS
		checkURL = fmt.Sprintf("%s:%d/", service.URL, service.Port)
	case 8000, 8080, 4000: // HTTP services
		checkURL = fmt.Sprintf("%s:%d/health", service.URL, service.Port)
	default:
		checkURL = fmt.Sprintf("%s:%d/", service.URL, service.Port)
	}

	start := time.Now()
	client := &http.Client{
		Timeout: 3 * time.Second,
	}

	resp, err := client.Get(checkURL)
	latency := time.Since(start).Milliseconds()
	health.Latency = latency

	if err != nil {
		health.Status = "offline"
		health.Error = err.Error()
	} else {
		defer resp.Body.Close()
		if resp.StatusCode >= 200 && resp.StatusCode < 400 {
			health.Status = "online"
		} else {
			health.Status = "error"
			health.Error = fmt.Sprintf("HTTP %d", resp.StatusCode)
		}
	}

	m.resultsMux.Lock()
	m.results[service.Name] = health
	m.resultsMux.Unlock()
}

func (m *Monitor) printStatus() {
	if *jsonOutput {
		m.printJSON()
		return
	}

	m.printTable()
}

func (m *Monitor) printJSON() {
	m.resultsMux.RLock()
	defer m.resultsMux.RUnlock()

	output := make(map[string]interface{})
	output["timestamp"] = time.Now()
	output["services"] = m.results

	data, _ := json.MarshalIndent(output, "", "  ")
	fmt.Println(string(data))
}

func (m *Monitor) printTable() {
	// Clear screen
	fmt.Print("\033[H\033[2J")

	// Header
	fmt.Println()
	color.New(color.FgCyan, color.Bold).Println("  CROD BABYLON GENESIS - Service Monitor")
	fmt.Println("  " + time.Now().Format("2006-01-02 15:04:05"))
	fmt.Println()

	// Table header
	fmt.Printf("  %-25s %-20s %-12s %-10s %s\n", "SERVICE", "URL", "STATUS", "LATENCY", "LAST CHECK")
	fmt.Println("  " + string(make([]byte, 90, 90)))

	// Service rows
	m.resultsMux.RLock()
	defer m.resultsMux.RUnlock()

	// Sort services for consistent display
	for _, service := range m.services {
		if health, ok := m.results[service.Name]; ok {
			m.printServiceRow(health)
		}
	}

	fmt.Println()

	// Summary
	online := 0
	total := len(m.results)
	for _, health := range m.results {
		if health.Status == "online" {
			online++
		}
	}

	summaryColor := color.New(color.FgGreen)
	if online < total {
		summaryColor = color.New(color.FgYellow)
	}
	if online == 0 {
		summaryColor = color.New(color.FgRed)
	}

	summaryColor.Printf("  System Status: %d/%d services online\n", online, total)
	fmt.Println()
}

func (m *Monitor) printServiceRow(health *ServiceHealth) {
	statusColor := color.New(color.FgRed)
	statusIcon := "✗"

	switch health.Status {
	case "online":
		statusColor = color.New(color.FgGreen)
		statusIcon = "✓"
	case "error":
		statusColor = color.New(color.FgYellow)
		statusIcon = "!"
	}

	latencyStr := fmt.Sprintf("%dms", health.Latency)
	if health.Latency > 1000 {
		latencyStr = color.New(color.FgYellow).Sprint(latencyStr)
	} else if health.Latency > 100 {
		latencyStr = color.New(color.FgWhite).Sprint(latencyStr)
	} else {
		latencyStr = color.New(color.FgGreen).Sprint(latencyStr)
	}

	fmt.Printf("  %-25s %-20s ", health.Name, health.URL)
	statusColor.Printf("%-12s", fmt.Sprintf("%s %s", statusIcon, health.Status))
	fmt.Printf(" %-10s %s\n", latencyStr, health.LastCheck.Format("15:04:05"))

	if health.Error != "" && health.Error != "context deadline exceeded" {
		color.New(color.FgRed, color.Faint).Printf("    Error: %s\n", health.Error)
	}
}