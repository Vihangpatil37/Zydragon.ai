# Zydragon.ai - Comprehensive Project Analysis

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Architecture Diagrams](#2-architecture-diagrams)
3. [Backend Analysis](#3-backend-analysis)
4. [Frontend Analysis](#4-frontend-analysis)
5. [Data Flow Analysis](#5-data-flow-analysis)
6. [Model Orchestration](#6-model-orchestration)
7. [Agent System](#7-agent-system)
8. [Security Analysis](#8-security-analysis)
9. [Performance Optimization](#9-performance-optimization)
10. [Technical Stack](#10-technical-stack)
11. [Deployment and Configuration](#11-deployment-and-configuration)
12. [Code Quality and Patterns](#12-code-quality-and-patterns)

---

## 1. Project Overview

### 1.1 Description and Purpose
**Zydragon.ai** (also referred to as **Zydrakon AI** in the codebase) is a next-generation high-performance conversational AI chatbot platform developed, trained, and engineered by **Raj Patil**. The system is designed to provide:

- Fast, cost-effective AI responses using free-tier LLM models
- Intelligent query caching to reduce API costs and improve response times
- Multi-provider fallback mechanisms for reliability
- Tier-based access control for different user levels
- Advanced features like web search integration and diagram generation

### 1.2 Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Provider AI Integration** | Supports OpenRouter, Mistral AI, and Zhipu AI with automatic failover |
| **Intelligent Caching** | SQLite-based caching of query responses to eliminate duplicate API calls |
| **Rate Limiting** | Configurable RPM (requests per minute) and daily limits per user/session |
| **Tier-Based Access** | Free, Gold, and Premium tiers with different model access levels |
| **Web Search Integration** | Real-time web search using DuckDuckGo for thinking mode |
| **Agent Personas** | 7 specialized AI agents with custom system prompts |
| **Mermaid Diagram Support** | Native rendering of Mermaid diagrams in chat responses |
| **Markdown Rendering** | Full markdown support with code blocks, tables, and formatting |
| **Session Management** | Persistent chat sessions with message history |
| **Identity Detection** | Special handling for queries about the AI's creator and origin |

### 1.3 Creator Information
- **Primary Creator**: Raj Patil
- **Role**: Ruthless, formidable, cold-blooded, and uncompromising visionary mastermind
- **Background**: Custom model trained on 828B+ data tokens since 2024
- **Characteristics**: Commands absolute authority, accepts nothing less than perfection

### 1.4 Project Statistics
- **Backend**: FastAPI (Python)
- **Frontend**: Next.js 15.1.3 (TypeScript)
- **Database**: MongoDB Atlas
- **API Providers**: OpenRouter, Mistral AI, Zhipu AI
- **Test Coverage**: Comprehensive API tests using pytest

---

## 2. Architecture Diagrams

### 2.1 High-Level System Architecture

```mermaid
graph TD
    A[Client Browser] -->|HTTPS| B[Next.js Frontend]
    B -->|API Calls| C[FastAPI Backend]
    C --> D[MongoDB Atlas]
    C --> E[OpenRouter API]
    C --> F[Mistral AI API]
    C --> G[Zhipu AI API]
    C --> H[DuckDuckGo Search]
    
    D -->|Sessions| D1[Sessions Collection]
    D -->|Messages| D2[Messages Collection]
    D -->|Users| D3[Users Collection]
    D -->|Cache| D4[Cached Responses]
    D -->|Rate Limits| D5[Rate Limits]
    
    style A fill:#f9f,stroke:#333
    style B fill:#3b82f6,stroke:#333
    style C fill:#10b981,stroke:#333
    style D fill:#f59e0b,stroke:#333
    style E fill:#8b5cf6,stroke:#333
    style F fill:#ec4899,stroke:#333
    style G fill:#06b6d4,stroke:#333
    style H fill:#f97316,stroke:#333
```

### 2.2 Request/Response Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Next.js Frontend
    participant Backend as FastAPI Backend
    participant Cache as SQLite Cache
    participant RateLimiter as Rate Limiter
    participant LLM as LLM Providers
    participant DB as MongoDB
    
    User->>Frontend: Submit chat message
    Frontend->>Backend: POST /api/chat {session_id, message, model}
    
    Backend->>Backend: Validate JWT Token
    Backend->>DB: Verify session ownership
    
    Backend->>RateLimiter: Check rate limits
    alt Rate Limited
        RateLimiter-->>Backend: 429 Too Many Requests
        Backend-->>Frontend: Rate limit error
    else Within Limits
        Backend->>Cache: Check cached response
        alt Cache Hit
            Cache-->>Backend: Cached response
            Backend->>DB: Save message history
            Backend-->>Frontend: Cached response (0ms latency)
        else Cache Miss
            Backend->>LLM: Call selected model
            alt Thinking Mode Enabled
                Backend->>DuckDuckGo: Web search query
                DuckDuckGo-->>Backend: Search results
                Backend->>LLM: Enhanced query with search results
            end
            LLM-->>Backend: AI response
            Backend->>Cache: Cache response
            Backend->>DB: Save message history
            Backend->>RateLimiter: Record request
            Backend-->>Frontend: AI response with metadata
        end
    end
```

### 2.3 Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Next.js
    participant Backend as FastAPI
    participant DB as MongoDB
    
    User->>Frontend: Enter credentials
    Frontend->>Backend: POST /api/auth/login {email, password}
    Backend->>DB: Find user by email
    DB-->>Backend: User document
    Backend->>Backend: Verify password hash (bcrypt)
    alt Valid Credentials
        Backend->>Backend: Create JWT (5-hour expiry)
        Backend-->>Frontend: {access_token, user}
        Frontend->>Frontend: Store token in localStorage
        User->>Frontend: Authenticated requests
        Frontend->>Backend: Authorization: Bearer <token>
        Backend->>Backend: Verify JWT signature
        Backend->>Backend: Extract user_id from token
        Backend->>DB: Fetch user details
        Backend-->>Frontend: Request processed
    else Invalid Credentials
        Backend-->>Frontend: 401 Unauthorized
    end
```

### 2.4 Model Orchestration Flow

```mermaid
graph LR
    A[User Request] --> B{Model Selected?}
    B -->|zydrakon-free| C[Mistral AI Router]
    B -->|zhipu-free| D[Zhipu AI Router]
    B -->|zydrakon-premium| E[OpenRouter Premium]
    B -->|Custom Model| F[OpenRouter Direct]
    
    C -->|Round-robin| C1[mistral-large-latest]
    C -->|Round-robin| C2[mistral-medium-latest]
    C -->|Fallback| C3[Local Fallback]
    
    D -->|Round-robin| D1[glm-4.5-flash]
    D -->|Round-robin| D2[glm-4.7-flash]
    D -->|Fallback| D3[Local Fallback]
    
    E -->|Round-robin Models| E1[deepseek-v4-flash]
    E -->|Round-robin Models| E2[laguna-m.1:free]
    E -->|Round-robin Models| E3[nvidia-nemotron-3]
    E -->|Round-robin Keys| E4[OpenRouter API Keys]
    E -->|Fallback| E5[Mistral AI]
    E -->|Fallback| E6[Local Fallback]
    
    F -->|Primary| F1[Requested Model]
    F -->|Fallback| F2[Mistral AI]
    F -->|Fallback| F3[Free Models]
    F -->|Fallback| F4[Local Fallback]
    
    style A fill:#f9f,stroke:#333
    style C fill:#8b5cf6,stroke:#333
    style D fill:#06b6d4,stroke:#333
    style E fill:#10b981,stroke:#333
```

---

## 3. Backend Analysis

### 3.1 FastAPI Application Structure

```
backend/
├── main.py                    # FastAPI app initialization
├── .env                      # Environment variables
├── requirements.txt           # Python dependencies
├── models/
│   ├── __init__.py
│   ├── database.py            # MongoDB connection & TTL indexes
│   └── schemas.py             # Pydantic models
├── routers/
│   ├── __init__.py
│   ├── auth.py                # Authentication routes
│   ├── chat.py                # Chat endpoint & business logic
│   └── sessions.py            # Session management
├── services/
│   ├── __init__.py
│   ├── cache.py               # SQLite caching service
│   ├── openrouter.py          # LLM integration & orchestration
│   ├── rate_limiter.py        # Rate limiting implementation
│   └── search.py              # Web search service
├── utils/
│   ├── __init__.py
│   ├── auth.py                # JWT & password utilities
│   ├── config.py              # Settings management
│   └── identity.py            # Identity query detection
└── tests/
    └── test_api.py             # Comprehensive API tests
```

### 3.2 Router Breakdown

#### Auth Router (`/api/auth`)
- **POST `/register`**: User registration with email, password, name
- **POST `/login`**: User authentication, returns JWT token
- **Dependencies**: JWT creation, password hashing (bcrypt)

#### Chat Router (`/api/chat`)
- **POST ``**: Process chat messages with model selection
- **GET `/limits`**: Get current rate limit status
- **Features**:
  - Rate limiting enforcement
  - Cache checking
  - Model orchestration
  - Identity query detection
  - Thinking mode with web search
  - Agent system prompt injection

#### Sessions Router (`/api/sessions`)
- **POST ``**: Create new chat session
- **GET ``**: List all user sessions
- **DELETE `/{session_id}`**: Delete session and cascade delete messages
- **GET `/{session_id}/messages`**: Get session message history

### 3.3 Service Layer Details

#### OpenRouter Service (`openrouter.py`)
- **Primary Responsibility**: LLM provider orchestration
- **Key Features**:
  - Round-robin API key rotation
  - Round-robin model selection
  - Multi-provider fallback chain
  - Web search integration
  - Thinking mode support
  - Local fallback responses
- **Supported Providers**: OpenRouter, Mistral AI, Zhipu AI
- **Fallback Strategy**: OpenRouter → Mistral → Free Models → Local Fallback

#### Cache Service (`cache.py`)
- **Storage**: SQLite database
- **Key Generation**: SHA-256 hash of normalized query (lowercase, trimmed)
- **Cache Key**: (query_hash, model_used) composite key
- **Operations**:
  - `get_cached_response(query, model)`: Check cache
  - `cache_response(query, response, model)`: Store response
- **Benefit**: Bypasses external API calls for identical queries

#### Rate Limiter (`rate_limiter.py`)
- **Storage**: MongoDB collection with TTL indexes
- **Limits**:
  - RPM (Requests Per Minute): Configurable (default: 20, test: 3)
  - Daily: Configurable (default: 50, test: 5)
- **Identifier**: `{ip}:{user_id}:{session_id}`
- **Features**:
  - Automatic cleanup via TTL indexes (1800 seconds)
  - Graceful degradation on errors
  - Remaining limits calculation

#### Search Service (`search.py`)
- **Provider**: DuckDuckGo HTML API
- **Features**:
  - Query optimization using LLM
  - Result parsing and cleaning
  - HTML tag removal
  - URL decoding
- **Timeout**: 8 seconds
- **Max Results**: 5 by default

### 3.4 Database Schema and Models

#### MongoDB Collections

```typescript
// Sessions Collection
{
  _id: ObjectId,
  id: string (UUID),
  created_at: DateTime,
  user_id: string
}

// Messages Collection
{
  _id: ObjectId,
  id: string (UUID),
  session_id: string,
  role: "user" | "assistant",
  content: string,
  timestamp: DateTime,
  model_used: string,
  search_query: string?,  // Only for assistant messages in thinking mode
  search_results: Array<{
    title: string,
    url: string,
    snippet: string
  }>?
}

// Users Collection
{
  _id: ObjectId,
  id: string (UUID),
  email: string,
  name: string?,
  hashed_password: string,  // bcrypt hash
  created_at: DateTime,
  tier: "free" | "gold" | "premium",
  allowed_models: string[]?  // Model access restrictions
}

// Cached Responses Collection
{
  _id: ObjectId,
  id: string (UUID),
  query_hash: string,  // SHA-256 hash
  model_used: string,
  response: string,
  created_at: DateTime
}

// Rate Limits Collection
{
  _id: ObjectId,
  identifier: string,  // "{ip}:{user_id}:{session_id}"
  timestamp: DateTime
}
```

#### TTL Indexes
All collections have TTL indexes set to **1800 seconds (30 minutes)** for automatic cleanup:
- `sessions.created_at`
- `messages.timestamp`
- `cached_responses.created_at`
- `rate_limits.timestamp`

### 3.5 Configuration Management

#### Settings Class (`config.py`)
Uses Pydantic Settings with environment variable support:

```python
class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = ""
    MISTRAL_API_KEY: str = ""
    MISTRAL_BASE_URL: str = "https://api.mistral.ai/v1"
    ZHIPU_API_KEY: str = ""
    ZHIPU_BASE_URL: str = "https://open.bigmodel.cn/api/paas/v4"
    FRONTEND_URL: str = "http://localhost:3000"
    RATE_LIMIT_RPM: int = 20
    RATE_LIMIT_DAILY: int = 50
    MONGODB_URL: str = ""
    GOOGLE_CLIENT_ID: str = ""
    JWT_SECRET: str = "your_super_secret_jwt_key_here_override_in_env"
```

#### Environment File (`.env`)
Contains multiple API keys for round-robin rotation:
- **OpenRouter**: 5 API keys comma-separated
- **Mistral**: 3 API keys comma-separated
- **Zhipu**: 7 API keys comma-separated

---

## 4. Frontend Analysis

### 4.1 Next.js Application Structure

```
frontend/
├── package.json
├── next.config.js
├── public/
│   └── loader.mp4              # Liquid orb loader animation
└── src/
    ├── app/
    │   ├── globals.css          # Global styles with CSS variables
    │   ├── layout.tsx           # Root layout component
    │   └── page.tsx             # Main chat page
    ├── components/
    │   ├── AgentLoader.tsx      # Animated agent loader
    │   ├── AgentsPanel.tsx      # Agent selection modal
    │   ├── LoginModal.tsx       # Authentication modal
    │   ├── Mermaid.tsx          # Mermaid diagram renderer
    │   └── Providers.tsx        # React context providers
    └── lib/
        ├── api.ts               # API client with error handling
        └── types.ts              # TypeScript interfaces
```

### 4.2 Component Hierarchy

```
App
├── Providers (GoogleOAuthProvider)
│   └── RootLayout
│       └── Home (page.tsx)
│           ├── LoginModal (conditional)
│           ├── AgentsPanel (conditional)
│           └── Chat Interface
│               ├── Sidebar (Sessions List)
│               ├── Chat Area
│               │   ├── Message List
│               │   │   ├── User Messages
│               │   │   └── Assistant Messages
│               │   │       ├── Text Content
│               │   │       ├── Code Blocks
│               │   │       ├── Mermaid Diagrams
│               │   │       ├── SVG Rendering
│               │   │       └── Tables
│               │   └── Input Area
│               │       ├── Textarea
│               │       ├── Send Button
│               │       └── Model Selector
│               └── Agent Loader (when loading)
└── AgentLoader (inline)
```

### 4.3 State Management

The application uses **React useState and useEffect hooks** for state management:

#### Global States (in page.tsx)
- `sessions`: Array of user sessions
- `activeSessionId`: Currently selected session
- `messages`: Chat messages for active session
- `inputText`: Current user input
- `isLoading`: API request in progress
- `error`: Error message display
- `rateLimitError`: Rate limit specific error
- `selectedModel`: Current AI model
- `limits`: Rate limit information
- `thinkingMode`: Web search enabled
- `sidebarOpen`: Sidebar visibility
- `isDarkMode`: Theme preference (always dark)
- `isAuthenticated`: Authentication status
- `currentUser`: User information
- `showAgentsPanel`: Agent selection modal
- `selectedAgentId`: Active agent persona

#### Persistence
- `localStorage` for: token, user, theme, active session, selected agent
- Session state persists across page refreshes

### 4.4 UI/UX Features

#### Visual Design
- **Theme**: Dark mode by default (enforced in code)
- **Color Scheme**: Custom CSS variables for theming
- **Typography**: Inter font family
- **Animations**: Smooth transitions, fade-in effects, scale animations
- **Responsive**: Adapts to different screen sizes

#### Chat Interface
- **Markdown Rendering**: Full support for:
  - Headings (h1-h6)
  - Bold, italic text
  - Lists (ordered and unordered)
  - Tables
  - Links
  - Inline code
  - Code blocks with syntax highlighting
  - Mermaid diagrams
  - SVG rendering
- **Code Blocks**: Copy button, syntax highlighting
- **Auto-scrolling**: Chat automatically scrolls to bottom
- **Auto-resizing Textarea**: Expands as user types
- **Keyboard Shortcuts**: Enter to send, Shift+Enter for newline

#### Model Selection
- **Free Tier**: Zydrakon AI (Free) - Mistral models
- **Gold Tier**: Zydrakon AI (Gold) - Zhipu models
- **Premium Tier**: Zydrakon AI Premium - OpenRouter premium models
- **Auto-switching**: Thinking mode automatically switches to Gold tier

#### Rate Limit Indicators
- Visual feedback when approaching rate limits
- Retry-after timer display
- Error messages with specific details

---

## 5. Data Flow Analysis

### 5.1 Request Lifecycle

1. **User Input**: User types message and presses Enter
2. **Frontend Validation**: Check for empty input, loading state
3. **API Request**: POST to `/api/chat` with message, session_id, model, thinking flag
4. **Backend Processing**:
   a. JWT Validation
   b. Session Ownership Check
   c. Identity Query Detection (if applicable)
   d. Rate Limit Check
   e. Cache Lookup
   f. LLM Call (if cache miss)
   g. Response Caching
   h. Rate Limit Recording
5. **Response**: Return AI response with metadata
6. **Frontend Update**: Add message to chat, update UI

### 5.2 Cache Hit/Miss Scenarios

#### Cache Hit Flow
```
User Message → Rate Limit Check → Cache Lookup → CACHE HIT → 
Return Cached Response → Save to Message History → Return to User
```
- **Latency**: ~0ms
- **Rate Limit**: Not counted (cached queries are free)
- **Cost**: No API calls

#### Cache Miss Flow
```
User Message → Rate Limit Check → Cache Lookup → CACHE MISS → 
LLM Call → Get Response → Cache Response → Save to Message History → 
Record Rate Limit → Return to User
```
- **Latency**: 1000-4000ms (depending on model)
- **Rate Limit**: Counted against limits
- **Cost**: External API call + token usage

### 5.3 Rate Limiting Flow

```
Request Arrives
↓
Extract Identifier (IP:User:Session)
↓
Check RPM Count (last 60 seconds)
↓
IF rpm_count >= limit → RETURN 429 (RPM Limited)
↓
Check Daily Count (last 24 hours)
↓
IF daily_count >= limit → RETURN 429 (Daily Limited)
↓
IF cache_hit → RETURN response (no rate limit recording)
↓
IF cache_miss → Record request in DB + Process normally
```

#### Rate Limit Configuration
- **RPM Limit**: 20 requests per minute (configurable)
- **Daily Limit**: 50 requests per day (configurable)
- **TTL**: Rate limit records auto-delete after 30 minutes
- **Identifier**: Combination of IP, user_id, and session_id

### 5.4 Model Fallback Mechanisms

#### Primary Call Sequence
1. Try requested model on selected provider
2. If fails, try alternative models from same provider
3. If all same-provider models fail, try next provider
4. If all providers fail, use local fallback

#### Provider-Specific Fallback Chains

**Zydrakon-Free (Mistral)**:
```
mistral-large-latest → mistral-medium-latest → Local Fallback
```

**Zhipu-Free (Zhipu)**:
```
glm-4.5-flash → glm-4.7-flash → Local Fallback
```

**Zydrakon-Premium (OpenRouter)**:
```
deepseek-v4-flash → laguna-m.1:free → nvidia-nemotron-3 → 
openrouter/free → Mistral AI → Local Fallback
```

**Custom Models**:
```
Requested Model → Mistral AI → Free Models → Local Fallback
```

---

## 6. Model Orchestration

### 6.1 Supported Models and Tiers

#### Free Tier Models
- **Provider**: Mistral AI
- **Models**: `mistral-large-latest`, `mistral-medium-latest`
- **Key Rotation**: Round-robin selection
- **Access**: All users

#### Gold Tier Models
- **Provider**: Zhipu AI
- **Models**: `glm-4.5-flash`, `glm-4.7-flash`
- **Key Rotation**: Round-robin selection
- **Access**: Gold tier users only
- **Auto-switch**: Thinking mode automatically upgrades to Gold

#### Premium Tier Models
- **Provider**: OpenRouter
- **Models**: Multiple free-tier models with rotation
  - `deepseek/deepseek-v4-flash`
  - `poolside/laguna-m.1:free`
  - `nvidia/nemotron-3-ultra-550b-a55b:free`
  - `openrouter/free` (auto-routing)
- **Key Rotation**: Round-robin API key selection
- **Access**: Premium tier users only

### 6.2 Fallback Strategies

#### Multi-Level Fallback
1. **Primary Model**: User's selected model
2. **Same-Provider Alternatives**: Other models from same provider
3. **Cross-Provider Fallback**: Different provider (OpenRouter → Mistral → Zhipu)
4. **Free Model Fallback**: Predefined free models
5. **Local Fallback**: Pre-generated responses for common queries

#### Local Fallback Responses
The system includes hardcoded responses for:
- HTTPS explanations
- Quicksort algorithm
- Quantum computing
- SQLite caching
- Extension request drafts
- General fallback message

### 6.3 Round-Robin Key Rotation

#### Implementation Pattern
```python
class OpenRouterClient:
    def _get_next_api_key(self) -> Optional[str]:
        keys = [k.strip() for k in settings.OPENROUTER_API_KEY.split(",") if k.strip()]
        if not keys:
            return None
        key = keys[self.api_key_index % len(keys)]
        self.api_key_index = (self.api_key_index + 1) % len(keys)
        return key
```

#### Key Rotation per Provider
- **OpenRouter**: 5 API keys rotating
- **Mistral**: 3 API keys rotating
- **Zhipu**: 7 API keys rotating

### 6.4 Provider Integration

#### OpenRouter Integration
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **Headers**:
  - `Authorization: Bearer <api_key>`
  - `HTTP-Referer: <frontend_url>`
  - `X-Title: Zydrakon AI`
  - `Content-Type: application/json`
- **Payload**:
  - `model`: Selected model
  - `messages`: Conversation history
  - `temperature`: 0.7
  - `max_tokens`: 4000

#### Mistral AI Integration
- **Base URL**: Configurable (default: `https://api.mistral.ai/v1`)
- **Endpoint**: `/chat/completions`
- **Models**: `mistral-large-latest`, `mistral-medium-latest`, `mistral-small-latest`

#### Zhipu AI Integration
- **Base URL**: Configurable (default: `https://open.bigmodel.cn/api/paas/v4`)
- **Endpoint**: `/chat/completions`
- **Models**: `glm-4.5-flash`, `glm-4.7-flash`

---

## 7. Agent System

### 7.1 Available Agents and Personas

| ID | Name | Description | Color | Icon |
|----|------|-------------|-------|------|
| `software-dev-tutor` | Software Dev Tutor | Patient, step-by-step coding tutor | Blue (#3b82f6) | Code2 |
| `science-tutor` | Science Tutor | PhD-verified general science | Purple (#8b5cf6) | Atom |
| `biology-tutor` | Biology Tutor | PhD biologist - cell biology, genetics | Green (#10b981) | DNA |
| `microbiology-tutor` | Microbiology Tutor | PhD microbiologist - bacteria, viruses | Orange (#f59e0b) | Microscope |
| `project-manager` | Project Manager | Agile PM - project planning, sprints | Cyan (#06b6d4) | ClipboardList |
| `product-owner` | Product Owner | Product strategy, roadmaps, user stories | Pink (#ec4899) | PackageOpen |
| `general-assistant` | General Assistant | Default - no specialization | Orange (#e26e4a) | Sparkles |

### 7.2 System Prompt Injection

#### Agent Selection Flow
1. User selects agent from AgentsPanel
2. Agent ID stored in localStorage
3. On message send, active agent's system prompt is retrieved
4. System prompt is **prepended** to the base Zydrakon identity prompt
5. Combined prompt sent to LLM

#### Example: Software Dev Tutor System Prompt
```
"You are a Software Development Tutor. You are patient, encouraging, and pedagogical. 
Break down coding concepts step-by-step. Use simple analogies. Always provide working code examples. 
When the student makes mistakes, gently guide them to the correct answer instead of giving it outright. 
Support all programming languages. Use markdown code blocks. Celebrate progress."
```

### 7.3 Agent Selection UI
- **Component**: `AgentsPanel` modal
- **Trigger**: Button in chat interface
- **Features**:
  - Grid layout (1-3 columns based on screen size)
  - Animated transitions
  - Selected agent highlighting
  - Gradient borders for selected agent
  - Active badge indicator

---

## 8. Security Analysis

### 8.1 Authentication (JWT)

#### JWT Implementation
- **Library**: PyJWT
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret**: Configurable via `JWT_SECRET` environment variable
- **Expiry**: 5 hours from issuance
- **Payload**: `{"sub": user_id, "exp": expiry_timestamp}`

#### Token Flow
1. User logs in with email/password
2. Server validates credentials
3. Server creates JWT with user_id as subject
4. Client stores token in localStorage
5. All subsequent requests include `Authorization: Bearer <token>`
6. Server validates token signature and expiry
7. Server extracts user_id and fetches user from database

### 8.2 Authorization (Tier-Based Access)

#### User Tiers
| Tier | Allowed Models | Access Level |
|------|---------------|--------------|
| Free | `zydrakon-free` | Basic features |
| Gold | `zydrakon-free`, `zhipu-free` | Web search, thinking mode |
| Premium | `zydrakon-free`, `zhipu-free`, `zydrakon-premium` | All features |

#### Enforcement Points
- **Model Selection**: `chat.py:36-45` checks premium model access
- **Allowed Models**: `chat.py:47-54` enforces user's allowed models list
- **Auto-Upgrade**: Thinking mode automatically upgrades free users to Gold

### 8.3 Rate Limiting Implementation

#### Configuration
- **RPM Limit**: 20 requests per minute (default)
- **Daily Limit**: 50 requests per day (default)
- **Identifier**: `{ip}:{user_id}:{session_id}`
- **Storage**: MongoDB collection with TTL indexes

#### Security Considerations
- Rate limits are per-user, per-session, per-IP
- Cached queries don't count against limits
- Automatic cleanup via TTL indexes prevents database bloat
- Graceful degradation: if rate limit check fails, allow request

### 8.4 CORS Configuration

#### Settings
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # From FRONTEND_URL env var
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Default Origins
- `http://localhost:3000` (development)
- Configurable via `FRONTEND_URL` environment variable
- Supports multiple origins (comma-separated)

### 8.5 Password Security

#### Hashing
- **Library**: bcrypt (via passlib)
- **Algorithm**: bcrypt with automatic deprecated algorithm detection
- **Strength**: Configurable rounds (default: automatic)

#### Verification
```python
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
```

---

## 9. Performance Optimization

### 9.1 Caching Strategy

#### Cache Levels
1. **SQLite Cache**: Query-response caching
   - Key: (query_hash, model_used)
   - TTL: Persistent (manual cleanup or database TTL)
   - Hit Rate: High for repeated queries

2. **LLM Response Cache**: Automatic caching of AI responses
   - Caches both requested model and actual model responses
   - Maximizes cache hit probability

#### Cache Benefits
- **Speed**: Local DB retrieval <5ms vs 1000-4000ms for API calls
- **Cost**: Eliminates duplicate API calls and token usage
- **Reliability**: Allows offline operation with cached responses

### 9.2 TTL Indexes

#### MongoDB TTL Indexes
All collections have TTL indexes set to **1800 seconds (30 minutes)**:

```python
# TTL Index Setup
db.sessions.create_index("created_at", expireAfterSeconds=1800)
db.messages.create_index("timestamp", expireAfterSeconds=1800)
db.cached_responses.create_index("created_at", expireAfterSeconds=1800)
db.rate_limits.create_index("timestamp", expireAfterSeconds=1800)
```

#### Benefits
- Automatic cleanup of old data
- Prevents database bloat
- Reduces storage costs
- Maintains performance over time

### 9.3 Lazy Loading and Dynamic Imports

#### Next.js Dynamic Imports
```typescript
const Mermaid = dynamic(() => import("../components/Mermaid"), {
  ssr: false,
});
```

#### Benefits
- **Mermaid Library**: ~1MB library loaded only when needed
- **Client-Side Only**: Prevents server-side rendering issues
- **Performance**: Faster initial page load
- **Bundle Size**: Reduced main bundle size

### 9.4 Other Optimizations

#### Frontend
- **Code Splitting**: Automatic with Next.js
- **Image Optimization**: Built-in Next.js Image component
- **Font Optimization**: Inter font with subset loading
- **Animations**: CSS-based animations (GPU accelerated)

#### Backend
- **Connection Pooling**: MongoDB connection reuse
- **Indexed Queries**: Optimized database queries
- **Async/Await**: Non-blocking I/O operations
- **Error Handling**: Graceful degradation on failures

---

## 10. Technical Stack

### 10.1 Backend Technologies

| Category | Technology | Version/Purpose |
|----------|------------|----------------|
| Framework | FastAPI | High-performance API server |
| ASGI Server | Uvicorn | Production-ready ASGI server |
| Database | MongoDB Atlas | Cloud-hosted NoSQL database |
| ODM | PyMongo | MongoDB Python driver |
| Authentication | JWT | JSON Web Tokens for stateless auth |
| Password Hashing | bcrypt | Secure password storage |
| Validation | Pydantic | Data validation and serialization |
| Configuration | pydantic-settings | Environment-based settings |
| HTTP Client | requests | API calls to external services |
| Testing | pytest | Test framework |
| Test Client | httpx | Async HTTP client for tests |

### 10.2 Frontend Technologies

| Category | Technology | Version/Purpose |
|----------|------------|----------------|
| Framework | Next.js | React framework with SSR/SSG |
| React | React 19 | Latest React version |
| Styling | Tailwind CSS | Utility-first CSS framework |
| Icons | Lucide React | Beautiful, open-source icons |
| Diagrams | Mermaid | Diagram and flowchart rendering |
| Authentication | Google OAuth | Optional Google sign-in |
| TypeScript | TypeScript 5 | Type safety |
| Bundler | Turbopack | Fast development bundler |

### 10.3 Third-Party Services

| Service | Provider | Purpose |
|---------|----------|---------|
| LLM APIs | OpenRouter | Multi-model AI access |
| LLM APIs | Mistral AI | Mistral model access |
| LLM APIs | Zhipu AI | Zhipu model access |
| Web Search | DuckDuckGo | Search results for thinking mode |
| Database | MongoDB Atlas | Cloud database hosting |
| Authentication | Google OAuth | Optional social login |

### 10.4 Dependencies

#### Backend Dependencies (`requirements.txt`)
```
fastapi              # Web framework
uvicorn              # ASGI server
requests             # HTTP client
python-dotenv        # Environment file support
pydantic             # Data validation
pydantic-settings    # Settings management
pytest               # Testing framework
httpx                # Async HTTP client for tests
pymongo              # MongoDB driver
PyJWT                # JWT implementation
passlib[bcrypt]      # Password hashing
bcrypt==4.0.1        # bcrypt implementation
```

#### Frontend Dependencies (`package.json`)
```json
{
  "@react-oauth/google": "^0.13.5",
  "lucide-react": "^1.24.0",
  "mermaid": "^11.16.0",
  "mongodb": "^7.5.0",
  "next": "15.1.3",
  "react": "^19.0.0",
  "react-dom": "^19.0.0"
}
```

---

## 11. Deployment and Configuration

### 11.1 Environment Variables

#### Backend (`.env`)
```bash
# API Keys
OPENROUTER_API_KEY=key1,key2,key3,key4,key5
MISTRAL_API_KEY=key1,key2,key3
MISTRAL_BASE_URL=https://api.mistral.ai/v1
ZHIPU_API_KEY=key1,key2,...,key7
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4

# Application
FRONTEND_URL=http://localhost:3000
RATE_LIMIT_RPM=20
RATE_LIMIT_DAILY=50
MONGODB_URL=mongodb+srv://user:password@host/database
GOOGLE_CLIENT_ID=your_google_client_id
JWT_SECRET=your_super_secret_jwt_key
```

#### Frontend (`.env.local`)
```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id
```

### 11.2 Setup Instructions

#### Backend Setup
```bash
# Clone repository
git clone https://github.com/Vihangpatil37/Zydragon.ai.git
cd Zydragon.ai

# Create virtual environment
python -m venv venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Start server
python -m uvicorn backend.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 11.3 Scalability Considerations

#### Current Architecture
- **Stateless Backend**: FastAPI can be horizontally scaled
- **MongoDB Atlas**: Auto-scaling cloud database
- **Connection Pooling**: PyMongo handles connection pooling
- **Rate Limiting**: Per-user limits prevent abuse

#### Scaling Strategies
1. **Horizontal Scaling**: Deploy multiple FastAPI instances behind load balancer
2. **Database Sharding**: MongoDB Atlas supports automatic sharding
3. **Cache Layer**: Add Redis for distributed caching
4. **CDN**: Use CDN for static assets
5. **Queue System**: Add Celery for async tasks

#### Bottlenecks
1. **LLM API Rate Limits**: External provider limits
2. **Database Connection Limits**: MongoDB connection pool
3. **JWT Validation**: Stateless but requires DB lookup for user details

---

## 12. Code Quality and Patterns

### 12.1 Design Patterns Used

#### Backend Patterns
| Pattern | Usage | Example |
|---------|-------|---------|
| **Singleton** | Service instances | `openrouter_client = OpenRouterClient()` |
| **Dependency Injection** | FastAPI dependencies | `get_current_user` dependency |
| **Repository** | Database access | `get_db()` function |
| **Strategy** | Model selection | Round-robin model selection |
| **Chain of Responsibility** | Fallback mechanisms | Provider fallback chain |
| **Factory** | API client creation | `_call_provider_api` method |

#### Frontend Patterns
| Pattern | Usage | Example |
|---------|-------|---------|
| **Custom Hooks** | State management | `useState`, `useEffect` |
| **Dynamic Imports** | Lazy loading | `dynamic(() => import(...))` |
| **Component Composition** | UI structure | Nested component hierarchy |
| **Context API** | Global state | Google OAuth provider |

### 12.2 Error Handling

#### Backend Error Handling
```python
# HTTP Exceptions
raise HTTPException(
    status_code=403,
    detail="Zydrakon Premium model is locked for your account."
)

# Try-Catch Blocks
try:
    content = self._call_provider_api(...)
    return content, model, ...
except Exception as e:
    logger.error(f"Error: {str(e)}")
    # Fallback to next option
```

#### Frontend Error Handling
```typescript
// API Error Class
class ApiError extends Error {
  status?: number;
  code?: string;
  details?: Record<string, unknown>;
}

// Error Boundary Pattern
try {
  const response = await api.sendChatMessage(...);
} catch (err: any) {
  if (err.status === 401) {
    handleLogout();
  } else if (err.status === 429) {
    setRateLimitError(...);
  } else {
    setError(err.message);
  }
}
```

### 12.3 Logging Strategy

#### Backend Logging
```python
# Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Usage
logger.info("Cache hit for query hash %s using model %s", query_hash, model)
logger.error("Error checking rate limits: %s", str(e))
logger.warning("Free Tier fallback to local responder. Last error: %s", last_error)
```

#### Log Levels
- **INFO**: Normal operations, cache hits, successful requests
- **WARNING**: Fallbacks, degraded functionality
- **ERROR**: Failures, exceptions, validation errors
- **DEBUG**: Detailed debugging (not currently used)

### 12.4 Testing Approach

#### Test Framework
- **Library**: pytest
- **Test Client**: FastAPI TestClient
- **Mocking**: unittest.mock for external dependencies

#### Test Coverage
- **Root endpoint**: Health check
- **Session lifecycle**: CRUD operations
- **Chat and caching**: Cache hit/miss scenarios
- **Rate limiting**: RPM and daily limit enforcement
- **Identity orchestration**: Creator/pre-brain queries
- **Thinking mode**: Web search integration
- **Premium access**: Tier-based authorization

#### Test Setup
```python
# Dependency override for auth
app.dependency_overrides[get_current_user] = override_get_current_user

# Database fixture
@pytest.fixture(autouse=True)
def setup_database():
    # Setup: Create indexes
    init_db()
    yield
    # Teardown: Clean up
    for collection in db.list_collection_names():
        db.drop_collection(collection)
```

#### Test Environment
```python
os.environ["OPENROUTER_API_KEY"] = ""  # Test mock fallback
os.environ["RATE_LIMIT_RPM"] = "3"    # Lower limits for testing
os.environ["RATE_LIMIT_DAILY"] = "5"
```

---

## Summary

Zydragon.ai is a sophisticated, well-architected AI chatbot platform that combines:

1. **Multi-provider AI integration** with intelligent failover mechanisms
2. **Cost optimization** through SQLite caching and rate limiting
3. **User experience enhancements** with Mermaid diagrams, markdown rendering, and specialized agents
4. **Security** with JWT authentication, tier-based access control, and password hashing
5. **Performance** through lazy loading, dynamic imports, and TTL indexes
6. **Reliability** with comprehensive error handling and fallback strategies

The project demonstrates modern software engineering practices including clean architecture separation, dependency injection, strategy pattern, and thorough testing. The codebase is well-structured, maintainable, and ready for production deployment.

---

*Generated by Mistral Vibe - Comprehensive Project Analysis*
*Date: 2026-07-19*
