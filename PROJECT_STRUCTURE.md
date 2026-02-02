# Project Structure

```
module_3/
├── config/                          # Configuration files
│   ├── agent.yml                    # Agent configuration (collection interval, server URL)
│   ├── alerts.yml                   # Alert thresholds and notification channels
│   └── database.yml                 # Time-series database connection settings
│
├── docs/                            # Documentation
│   └── system-resource-metrics-prd.md
│
├── src/
│   ├── agent/                       # Metrics Collection Agent
│   │   ├── collectors/              # OS-specific metric collectors
│   │   │   ├── cpu.js               # CPU metrics (usage, load, per-core)
│   │   │   ├── memory.js            # Memory metrics (RAM, swap)
│   │   │   ├── disk.js              # Disk metrics (usage, I/O)
│   │   │   ├── network.js           # Network metrics (traffic, bandwidth)
│   │   │   └── process.js           # Process-level metrics
│   │   ├── utils/                   # Agent utilities
│   │   │   ├── buffer.js            # Local buffering for offline mode
│   │   │   ├── retry.js             # Retry logic for failed transmissions
│   │   │   └── platform.js          # OS detection and abstraction
│   │   └── main.js                  # Agent entry point
│   │
│   ├── server/                      # Metrics Collection Server
│   │   ├── ingestion/               # Data ingestion layer
│   │   │   ├── receiver.js          # HTTP/gRPC metric receiver
│   │   │   ├── validator.js         # Metric data validation
│   │   │   └── aggregator.js        # Data aggregation logic
│   │   ├── storage/                 # Database interaction layer
│   │   │   ├── timeseries.js        # Time-series DB client
│   │   │   ├── retention.js         # Data retention policy implementation
│   │   │   └── query.js             # Query builder and optimizer
│   │   ├── api/                     # Internal server API
│   │   └── main.js                  # Server entry point
│   │
│   ├── alerts/                      # Alert Engine
│   │   ├── engine/                  # Alert processing
│   │   │   ├── evaluator.js         # Threshold evaluation
│   │   │   ├── deduplicator.js      # Alert deduplication (5-min window)
│   │   │   └── scheduler.js         # Alert checking scheduler
│   │   ├── channels/                # Notification channels
│   │   │   ├── email.js             # Email notifications
│   │   │   ├── slack.js             # Slack webhook integration
│   │   │   ├── discord.js           # Discord webhook integration
│   │   │   └── sms.js               # SMS notifications (optional)
│   │   └── main.js                  # Alert engine entry point
│   │
│   ├── api/                         # REST & WebSocket API Server
│   │   ├── routes/                  # API route handlers
│   │   │   ├── metrics.js           # GET /api/metrics/current, /history
│   │   │   ├── alerts.js            # POST/PUT/DELETE /api/alerts
│   │   │   └── health.js            # GET /api/health
│   │   ├── middleware/              # API middleware
│   │   │   ├── auth.js              # JWT authentication
│   │   │   ├── rbac.js              # Role-based access control
│   │   │   ├── ratelimit.js         # Rate limiting
│   │   │   └── logger.js            # Request logging
│   │   ├── websocket/               # WebSocket handlers
│   │   │   └── stream.js            # Real-time metric streaming
│   │   └── main.js                  # API server entry point
│   │
│   ├── dashboard/                   # Web Dashboard (React/Vue/etc.)
│   │   ├── components/              # UI components
│   │   │   ├── MetricChart.jsx      # Reusable chart component
│   │   │   ├── GaugeWidget.jsx      # Gauge visualization
│   │   │   ├── AlertPanel.jsx       # Alert list and status
│   │   │   └── TimeRangePicker.jsx  # Time range selector
│   │   ├── pages/                   # Dashboard pages
│   │   │   ├── Overview.jsx         # Main dashboard
│   │   │   ├── History.jsx          # Historical data view
│   │   │   ├── Alerts.jsx           # Alert configuration
│   │   │   └── Settings.jsx         # System settings
│   │   └── main.jsx                 # Dashboard entry point
│   │
│   └── common/                      # Shared code across all components
│       ├── types/                   # TypeScript types / data schemas
│       │   ├── metrics.js           # Metric data structures
│       │   └── alerts.js            # Alert data structures
│       ├── config/                  # Configuration loaders
│       │   └── loader.js            # YAML/JSON config file parser
│       └── logger/                  # Logging utilities
│           └── logger.js            # Structured logging
│
├── tests/                           # Test suites
│   ├── unit/                        # Unit tests
│   │   ├── agent/                   # Agent component tests
│   │   ├── server/                  # Server component tests
│   │   └── alerts/                  # Alert engine tests
│   ├── integration/                 # Integration tests
│   │   ├── pipeline.test.js         # End-to-end pipeline test
│   │   └── api.test.js              # API integration tests
│   └── performance/                 # Performance tests
│       ├── load.test.js             # Load testing (10k metrics/sec)
│       └── agent-overhead.test.js   # Agent resource usage test
│
├── scripts/                         # Utility scripts
│   ├── setup-db.sh                  # Database initialization
│   ├── seed-data.js                 # Sample data generator
│   └── deploy.sh                    # Deployment script
│
├── CLAUDE.md                        # Claude Code guidance
├── PROJECT_STRUCTURE.md             # This file
└── package.json / requirements.txt  # Dependencies
```

## Component Responsibilities

### Agent (`src/agent/`)
Lightweight process that runs on monitored servers. Collects system metrics and sends to collection server.

### Server (`src/server/`)
Central server that receives metrics from multiple agents, stores in time-series DB, and provides data to API layer.

### Alerts (`src/alerts/`)
Monitors incoming metrics against configured thresholds and sends notifications through various channels.

### API (`src/api/`)
Provides REST and WebSocket endpoints for dashboard and external integrations. Handles authentication and authorization.

### Dashboard (`src/dashboard/`)
Web-based UI for visualizing metrics, configuring alerts, and viewing historical data.

### Common (`src/common/`)
Shared utilities, types, and configuration logic used across all components.
