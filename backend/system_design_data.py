"""System Design interview preparation curriculum data."""

SYSTEM_DESIGN_PHASES = {
    1: {
        "name": "Fundamentals",
        "tagline": "Lay the Foundation",
        "description": "Master the core networking and web fundamentals that every system design interview builds upon. These concepts are the vocabulary you need before designing any system.",
        "motivation_start": "Every great architect starts with understanding the building materials. These fundamentals will make everything else click.",
        "estimated_days": 5,
    },
    2: {
        "name": "Building Blocks",
        "tagline": "Assemble Your Toolkit",
        "description": "Learn the essential infrastructure components that power modern distributed systems. Load balancers, caches, queues, and storage are the Lego bricks of system design.",
        "motivation_start": "Now that you speak the language, it's time to learn the tools. These building blocks appear in every single system design interview.",
        "estimated_days": 7,
    },
    3: {
        "name": "Design Patterns & Trade-offs",
        "tagline": "Think Like an Architect",
        "description": "Understand the architectural patterns, consistency models, and trade-offs that separate good designs from great ones. This is where you learn to reason about systems.",
        "motivation_start": "You have the tools - now learn when and why to use each one. Interviewers care most about your reasoning and trade-off analysis.",
        "estimated_days": 7,
    },
    4: {
        "name": "Real System Designs",
        "tagline": "Design Like a Pro",
        "description": "Put it all together by designing real-world systems that are commonly asked in FAANG interviews. Practice the full end-to-end design process.",
        "motivation_start": "This is where everything comes together. Each design exercise combines multiple building blocks and patterns you've already learned.",
        "estimated_days": 6,
    },
}

SYSTEM_DESIGN_CONCEPTS = [
    # ── Phase 1: Fundamentals ──
    {
        "id": 1,
        "title": "Client-Server Model & HTTP",
        "phase": 1,
        "difficulty": "easy",
        "estimated_minutes": 25,
        "frequency": "very_high",
        "tags": ["networking", "fundamentals", "protocols"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
        "cheat_sheet": "Clients send HTTP requests to servers which return responses. HTTP is stateless, uses methods (GET, POST, PUT, DELETE), and status codes (2xx success, 4xx client error, 5xx server error).",
        "explanation": """## Client-Server Model & HTTP

The **client-server model** is the backbone of the modern internet. A **client** (your browser, mobile app) sends a request to a **server**, which processes it and returns a response. Think of it like ordering at a restaurant: you (client) tell the waiter (HTTP) what you want, the kitchen (server) prepares it, and the waiter brings it back.

**HTTP (HyperText Transfer Protocol)** is the language clients and servers use to communicate. It's **stateless** - each request is independent, and the server doesn't remember previous requests unless you explicitly manage state (via cookies, sessions, or tokens).

### Key HTTP Methods
- **GET**: Retrieve data (read-only, idempotent)
- **POST**: Create new resources
- **PUT**: Update/replace resources (idempotent)
- **DELETE**: Remove resources (idempotent)

### Status Codes
- **2xx**: Success (200 OK, 201 Created)
- **3xx**: Redirect (301 Moved, 304 Not Modified)
- **4xx**: Client error (400 Bad Request, 404 Not Found, 429 Rate Limited)
- **5xx**: Server error (500 Internal, 503 Unavailable)

Understanding HTTP headers, cookies, and connection management (keep-alive, HTTP/2 multiplexing) is essential for designing performant systems.""",
        "key_points": [
            "HTTP is stateless - each request is independent",
            "REST APIs build on HTTP methods for CRUD operations",
            "HTTP/2 introduces multiplexing and server push for performance",
            "HTTPS adds TLS encryption for security",
            "Status codes communicate outcomes: 2xx, 3xx, 4xx, 5xx",
        ],
        "interview_tips": [
            "Always clarify whether the system needs real-time updates (WebSockets) or request-response (HTTP) is sufficient",
            "Mention HTTPS when discussing any user-facing system for security",
            "Know the difference between HTTP/1.1 and HTTP/2 for performance discussions",
        ],
        "common_mistakes": [
            "Forgetting that HTTP is stateless and not accounting for session management",
            "Using POST for idempotent operations where PUT would be more appropriate",
            "Not considering connection overhead when designing high-throughput systems",
        ],
        "youtube_keywords": "HTTP protocol system design fundamentals client server model",
        "diagram_description": "Client (browser/app) sends HTTP request with method, headers, and body to Server via the internet. Server processes request, interacts with database/services, and returns HTTP response with status code, headers, and body.",
        "real_world_examples": [
            "Every website you visit uses HTTP - your browser is the client, the web server returns HTML/CSS/JS",
            "Mobile apps communicate with backend servers using HTTP-based REST or GraphQL APIs",
            "Microservices within Netflix communicate using HTTP/gRPC internally",
        ],
        "related_concepts": [2, 3],
        "practice_questions": [
            "What happens step by step when you type google.com in your browser?",
            "What is the difference between HTTP and WebSockets? When would you use each?",
            "Design a simple REST API for a bookstore with CRUD operations",
        ],
    },
    {
        "id": 2,
        "title": "DNS & Domain Name System",
        "phase": 1,
        "difficulty": "easy",
        "estimated_minutes": 20,
        "frequency": "high",
        "tags": ["networking", "fundamentals", "dns"],
        "companies_asking": ["Google", "Amazon", "Cloudflare", "Microsoft"],
        "cheat_sheet": "DNS translates domain names to IP addresses. Uses hierarchical lookup: browser cache -> OS cache -> recursive resolver -> root -> TLD -> authoritative nameserver. TTL controls caching duration.",
        "explanation": """## DNS & Domain Name System

**DNS** is like the phonebook of the internet. When you type `google.com`, your computer needs to find the actual IP address (like `142.250.80.46`) of Google's servers. DNS handles this translation.

### How DNS Resolution Works
1. **Browser cache**: Check if we've looked this up recently
2. **OS cache**: Check the operating system's DNS cache
3. **Recursive resolver**: Your ISP's DNS server does the heavy lifting
4. **Root nameserver**: Points to the TLD server (`.com`, `.org`)
5. **TLD nameserver**: Points to the authoritative nameserver for `google.com`
6. **Authoritative nameserver**: Returns the actual IP address

### DNS Record Types
- **A record**: Maps domain to IPv4 address
- **AAAA record**: Maps domain to IPv6 address
- **CNAME**: Alias pointing to another domain
- **MX**: Mail server records
- **NS**: Nameserver records

### TTL (Time To Live)
Every DNS record has a TTL that controls how long it's cached. Lower TTL = faster propagation of changes but more DNS lookups. Higher TTL = better performance but slower updates.

DNS is critical in system design for **load balancing** (DNS round-robin), **failover** (updating records to point to healthy servers), and **geo-routing** (returning different IPs based on user location).""",
        "key_points": [
            "DNS is a hierarchical, distributed naming system",
            "TTL controls caching - trade-off between performance and update speed",
            "DNS can be used for basic load balancing via round-robin",
            "DNS propagation delays affect failover time",
            "CNAME records create aliases, A records map to IPs directly",
        ],
        "interview_tips": [
            "Mention DNS as the first step in any request flow diagram",
            "Discuss DNS-based load balancing as a simple first-level distribution strategy",
            "Know that DNS failures can cause widespread outages (mention the 2016 Dyn attack)",
        ],
        "common_mistakes": [
            "Forgetting DNS resolution latency in performance calculations",
            "Not considering DNS caching and TTL when discussing failover strategies",
            "Assuming DNS updates propagate instantly",
        ],
        "youtube_keywords": "DNS system design how DNS works domain name system explained",
        "diagram_description": "Hierarchical DNS resolution flow: User's browser -> Local DNS Cache -> Recursive Resolver -> Root Server (.com) -> TLD Server -> Authoritative Nameserver -> Returns IP address back through the chain.",
        "real_world_examples": [
            "Cloudflare uses DNS to route users to the nearest edge server for faster page loads",
            "AWS Route 53 provides DNS-based health checking and failover for high availability",
            "GitHub uses DNS CNAME records for custom domain support on GitHub Pages",
        ],
        "related_concepts": [1, 5],
        "practice_questions": [
            "How would you design a DNS system that handles billions of lookups per day?",
            "What are the trade-offs of using a low vs high TTL for DNS records?",
            "How does DNS-based geo-routing work?",
        ],
    },
    {
        "id": 3,
        "title": "REST APIs & API Design",
        "phase": 1,
        "difficulty": "easy",
        "estimated_minutes": 30,
        "frequency": "very_high",
        "tags": ["api-design", "fundamentals", "rest"],
        "companies_asking": ["Google", "Amazon", "Meta", "Stripe", "Twilio"],
        "cheat_sheet": "REST uses HTTP methods on resources (nouns, not verbs). Use proper status codes, pagination, versioning. Keep APIs stateless, use consistent naming. Consider rate limiting and authentication.",
        "explanation": """## REST APIs & API Design

**REST (Representational State Transfer)** is the most common architectural style for web APIs. It treats everything as a **resource** identified by a URL, and uses standard HTTP methods to operate on those resources.

### RESTful Design Principles
- **Resources are nouns**: `/users/123`, not `/getUser?id=123`
- **HTTP methods are verbs**: GET (read), POST (create), PUT (update), DELETE (remove)
- **Stateless**: Each request contains all info needed to process it
- **Uniform interface**: Consistent URL patterns and response formats

### Good API Design Practices
```
GET    /api/v1/users          # List users (with pagination)
GET    /api/v1/users/123      # Get specific user
POST   /api/v1/users          # Create user
PUT    /api/v1/users/123      # Update user
DELETE /api/v1/users/123      # Delete user
GET    /api/v1/users/123/orders  # Nested resources
```

### Key Considerations
- **Pagination**: Use cursor-based or offset-based pagination for large collections
- **Versioning**: `/api/v1/` or header-based versioning for backwards compatibility
- **Rate Limiting**: Protect APIs from abuse with request quotas
- **Authentication**: OAuth2, API keys, or JWT tokens
- **Error Handling**: Consistent error response format with meaningful messages

Understanding API design is fundamental because every system design interview involves defining APIs for the system you're building.""",
        "key_points": [
            "Resources should be nouns (URLs), actions should be HTTP methods",
            "APIs must be stateless for horizontal scalability",
            "Pagination is essential for any list endpoint",
            "Versioning prevents breaking changes for existing clients",
            "Rate limiting protects against abuse and ensures fair usage",
        ],
        "interview_tips": [
            "Always define the API interface early in a system design interview",
            "Mention pagination, rate limiting, and authentication proactively",
            "Discuss trade-offs between REST and GraphQL when relevant",
        ],
        "common_mistakes": [
            "Using verbs in URLs instead of nouns (e.g., /getUser instead of /users/:id)",
            "Forgetting pagination for list endpoints that could return millions of results",
            "Not versioning APIs, making it hard to evolve the system",
        ],
        "youtube_keywords": "REST API design best practices system design interview",
        "diagram_description": "Client makes HTTP requests to API Gateway, which routes to backend services. Each service exposes RESTful endpoints following /resource/{id} pattern. Response includes status code, headers, and JSON body.",
        "real_world_examples": [
            "Stripe's API is considered the gold standard of REST API design with excellent documentation",
            "Twitter's API uses REST endpoints for tweets, users, and timelines with OAuth2 authentication",
            "GitHub's REST API allows managing repositories, issues, and pull requests programmatically",
        ],
        "related_concepts": [1, 4],
        "practice_questions": [
            "Design the API for a social media platform's post and comment system",
            "How would you handle API versioning for a public API with millions of users?",
            "Compare REST vs GraphQL - when would you choose each?",
        ],
    },
    {
        "id": 4,
        "title": "Databases: SQL vs NoSQL",
        "phase": 1,
        "difficulty": "medium",
        "estimated_minutes": 35,
        "frequency": "very_high",
        "tags": ["databases", "fundamentals", "storage"],
        "companies_asking": ["Google", "Amazon", "Meta", "Netflix", "Uber"],
        "cheat_sheet": "SQL (relational) for structured data with relationships and ACID guarantees. NoSQL for flexible schemas, horizontal scaling, and high write throughput. Choose based on data model, consistency needs, and scale requirements.",
        "explanation": """## Databases: SQL vs NoSQL

Choosing the right database is one of the most important decisions in system design. The two major categories are **SQL (relational)** and **NoSQL (non-relational)**.

### SQL Databases (PostgreSQL, MySQL, Oracle)
- **Structured data** with predefined schemas and tables
- **ACID transactions**: Atomicity, Consistency, Isolation, Durability
- **Joins**: Efficiently query related data across tables
- **Strong consistency**: Reads always return the latest write
- Best for: Financial systems, user accounts, complex queries with joins

### NoSQL Databases
Several types exist, each optimized for different use cases:

| Type | Examples | Best For |
|------|----------|----------|
| **Key-Value** | Redis, DynamoDB | Caching, sessions, simple lookups |
| **Document** | MongoDB, CouchDB | Flexible schemas, content management |
| **Wide-Column** | Cassandra, HBase | Time-series, high write throughput |
| **Graph** | Neo4j, Amazon Neptune | Social networks, recommendations |

### When to Choose What?
- **Need joins and transactions?** -> SQL
- **Need flexible schemas?** -> Document DB
- **Need massive write throughput?** -> Wide-column
- **Need sub-millisecond lookups?** -> Key-value
- **Need to model relationships?** -> Graph DB

In practice, many systems use **multiple databases** (polyglot persistence) - SQL for core business data, Redis for caching, Elasticsearch for search.""",
        "key_points": [
            "SQL provides ACID guarantees; NoSQL often trades consistency for availability",
            "NoSQL scales horizontally more easily than SQL",
            "Document databases offer flexible schemas for evolving data models",
            "Most real-world systems use multiple database types (polyglot persistence)",
            "Indexing is critical for query performance in both SQL and NoSQL",
        ],
        "interview_tips": [
            "Always justify your database choice with specific trade-offs",
            "Mention that you'd use different databases for different parts of the system",
            "Discuss indexing strategy when mentioning databases",
        ],
        "common_mistakes": [
            "Choosing NoSQL without a clear reason - SQL handles most use cases well",
            "Forgetting about indexing and query patterns when choosing a database",
            "Assuming NoSQL means no schema - you still need to design your data model",
        ],
        "youtube_keywords": "SQL vs NoSQL system design database comparison when to use",
        "diagram_description": "Two-column comparison: Left shows SQL with tables, rows, joins, and ACID. Right shows NoSQL types: key-value pairs, document (JSON), wide-column (row-key based), and graph (nodes+edges).",
        "real_world_examples": [
            "Amazon uses DynamoDB (NoSQL) for shopping cart but PostgreSQL for order processing",
            "Netflix uses Cassandra for viewing history (high writes) and MySQL for billing",
            "Uber uses PostgreSQL for trip data and Redis for real-time driver location caching",
        ],
        "related_concepts": [3, 10, 15],
        "practice_questions": [
            "You're designing a social media platform - which database(s) would you choose and why?",
            "When would you choose Cassandra over PostgreSQL?",
            "How does database indexing work and why is it important?",
        ],
    },
    {
        "id": 5,
        "title": "Caching Fundamentals",
        "phase": 1,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "very_high",
        "tags": ["caching", "fundamentals", "performance"],
        "companies_asking": ["Google", "Amazon", "Meta", "Netflix", "Twitter"],
        "cheat_sheet": "Cache stores frequently accessed data in fast storage (RAM). Eviction policies: LRU, LFU, TTL. Patterns: cache-aside, write-through, write-behind. Watch for cache stampede, consistency issues, and cold starts.",
        "explanation": """## Caching Fundamentals

**Caching** is storing copies of frequently accessed data in a faster storage layer to reduce latency and database load. Think of it like keeping a cheat sheet on your desk instead of going to the library every time.

### Cache Layers
1. **Browser cache**: Static assets (images, CSS, JS)
2. **CDN cache**: Geographically distributed content cache
3. **Application cache**: Redis/Memcached for computed data
4. **Database cache**: Query result caching, buffer pool

### Caching Strategies
- **Cache-aside (Lazy loading)**: App checks cache first, falls back to DB, then populates cache
- **Write-through**: Write to cache and DB simultaneously (consistent but slower writes)
- **Write-behind (Write-back)**: Write to cache first, asynchronously persist to DB (fast but risk of data loss)
- **Read-through**: Cache automatically loads from DB on miss

### Eviction Policies
- **LRU (Least Recently Used)**: Evict the oldest accessed item
- **LFU (Least Frequently Used)**: Evict the least popular item
- **TTL (Time To Live)**: Items expire after a set duration

### Common Pitfalls
- **Cache stampede**: Many requests hit DB simultaneously when cache expires
- **Stale data**: Cache may serve outdated data
- **Cold start**: Empty cache after restart causes DB spike""",
        "key_points": [
            "Cache-aside is the most common pattern - check cache, fallback to DB, populate cache",
            "LRU is the default eviction policy for most use cases",
            "TTL ensures data doesn't become infinitely stale",
            "Cache invalidation is one of the hardest problems in computer science",
            "Multi-level caching (browser -> CDN -> app -> DB) provides defense in depth",
        ],
        "interview_tips": [
            "Always mention caching when discussing read-heavy systems",
            "Discuss cache invalidation strategy proactively - it shows depth",
            "Mention Redis or Memcached as specific technologies",
        ],
        "common_mistakes": [
            "Caching everything without considering which data benefits most from caching",
            "Not planning for cache invalidation when underlying data changes",
            "Ignoring cache stampede scenarios in high-traffic systems",
        ],
        "youtube_keywords": "caching system design cache strategies LRU Redis fundamentals",
        "diagram_description": "Request flow: Client -> Check Cache (Redis) -> Cache Hit returns immediately. Cache Miss -> Query Database -> Store result in Cache -> Return to Client. Shows cache-aside pattern with TTL expiration.",
        "real_world_examples": [
            "Facebook caches user profile data in Memcached, serving billions of requests per day",
            "Netflix caches movie metadata and recommendations in EVCache (built on Memcached)",
            "Twitter uses Redis to cache timelines so home feed loads in milliseconds",
        ],
        "related_concepts": [4, 8],
        "practice_questions": [
            "How would you design a caching strategy for an e-commerce product page?",
            "Explain the cache stampede problem and how to prevent it",
            "When should you NOT use caching?",
        ],
    },
    {
        "id": 6,
        "title": "Scaling: Vertical vs Horizontal",
        "phase": 1,
        "difficulty": "easy",
        "estimated_minutes": 20,
        "frequency": "very_high",
        "tags": ["scaling", "fundamentals", "architecture"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Netflix"],
        "cheat_sheet": "Vertical scaling: bigger machine (more CPU/RAM). Horizontal scaling: more machines. Horizontal is preferred for large systems - needs stateless services, load balancing, and distributed data. Vertical has hard limits.",
        "explanation": """## Scaling: Vertical vs Horizontal

When your system needs to handle more traffic, you have two fundamental approaches:

### Vertical Scaling (Scale Up)
Add more power to your existing machine: more CPU, RAM, faster disks.
- **Pros**: Simple, no code changes needed, no distributed system complexity
- **Cons**: Hardware limits (you can't add infinite RAM), single point of failure, expensive at high end
- **Best for**: Databases (initially), simple applications, quick fixes

### Horizontal Scaling (Scale Out)
Add more machines and distribute the load.
- **Pros**: Nearly unlimited scaling, better fault tolerance, cost-effective with commodity hardware
- **Cons**: Requires stateless design, adds complexity (load balancing, data consistency)
- **Best for**: Web servers, microservices, read-heavy workloads

### Making Systems Horizontally Scalable
1. **Stateless services**: Store session data in external cache (Redis), not in-memory
2. **Load balancing**: Distribute requests across multiple instances
3. **Database sharding**: Split data across multiple database servers
4. **Shared-nothing architecture**: Each node operates independently

In practice, most systems use **both**: vertically scale the database (to a point), and horizontally scale the application layer.""",
        "key_points": [
            "Horizontal scaling is preferred for large-scale systems but adds complexity",
            "Stateless services are a prerequisite for horizontal scaling",
            "Vertical scaling has hard limits but is simpler to implement",
            "Most systems combine both approaches for different tiers",
            "Auto-scaling allows dynamic horizontal scaling based on load",
        ],
        "interview_tips": [
            "Start with vertical scaling for simplicity, then explain when you'd need horizontal",
            "When mentioning horizontal scaling, immediately address state management",
            "Discuss auto-scaling and its trade-offs (cold start latency, cost)",
        ],
        "common_mistakes": [
            "Jumping to horizontal scaling without considering if vertical is sufficient",
            "Forgetting to make services stateless before scaling horizontally",
            "Not addressing how shared state (sessions, locks) works across multiple instances",
        ],
        "youtube_keywords": "horizontal vs vertical scaling system design explained",
        "diagram_description": "Left: Vertical scaling shows single server growing bigger (more CPU/RAM). Right: Horizontal scaling shows multiple identical servers behind a load balancer, with shared database and cache layer.",
        "real_world_examples": [
            "Amazon scales web servers horizontally during Prime Day, adding thousands of instances",
            "Instagram horizontally scales its Django application servers while vertically scaling PostgreSQL",
            "Slack uses horizontal scaling with Kubernetes to handle millions of concurrent WebSocket connections",
        ],
        "related_concepts": [5, 7, 8],
        "practice_questions": [
            "Your application is slowing down under load - walk through your scaling strategy",
            "How do you handle user sessions when scaling horizontally?",
            "What are the trade-offs of auto-scaling?",
        ],
    },
    # ── Phase 2: Building Blocks ──
    {
        "id": 7,
        "title": "Load Balancers",
        "phase": 2,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "very_high",
        "tags": ["load-balancing", "infrastructure", "availability"],
        "companies_asking": ["Google", "Amazon", "Meta", "Netflix", "Microsoft"],
        "cheat_sheet": "Distributes traffic across multiple servers. Algorithms: round-robin, least connections, IP hash, weighted. L4 (transport) is faster, L7 (application) is smarter. Use health checks to avoid sending traffic to dead servers.",
        "explanation": """## Load Balancers

A **load balancer** distributes incoming network traffic across multiple backend servers to ensure no single server becomes a bottleneck. Think of it as a traffic cop directing cars to different lanes.

### Load Balancing Algorithms
- **Round Robin**: Distribute requests sequentially across servers (simple, works well for equal servers)
- **Weighted Round Robin**: Assign weights based on server capacity
- **Least Connections**: Send to the server with fewest active connections
- **IP Hash**: Same client IP always goes to the same server (sticky sessions)
- **Least Response Time**: Route to the fastest responding server

### Layer 4 vs Layer 7
- **L4 (Transport)**: Routes based on IP and port. Very fast, but can't inspect content. (HAProxy, AWS NLB)
- **L7 (Application)**: Routes based on HTTP headers, URLs, cookies. Smarter but slightly slower. (Nginx, AWS ALB)

### Key Features
- **Health checks**: Periodically verify backend servers are alive
- **SSL termination**: Handle HTTPS at the load balancer, reducing backend load
- **Session persistence**: Sticky sessions when needed
- **Auto-scaling integration**: Add/remove backends dynamically

### High Availability
Load balancers themselves can be a single point of failure. Use **active-passive** or **active-active** LB pairs for redundancy.""",
        "key_points": [
            "L7 load balancers can make smarter routing decisions based on request content",
            "Health checks prevent sending traffic to failed servers",
            "SSL termination at the LB reduces computational load on backend servers",
            "Load balancers should be redundant to avoid single points of failure",
            "Consistent hashing is useful for cache-friendly load distribution",
        ],
        "interview_tips": [
            "Always include a load balancer when designing scalable systems",
            "Specify whether you need L4 or L7 based on routing requirements",
            "Mention health checks and failover to show awareness of reliability",
        ],
        "common_mistakes": [
            "Forgetting that the load balancer itself needs to be highly available",
            "Using sticky sessions when stateless design would be better",
            "Not considering SSL termination and its impact on performance",
        ],
        "youtube_keywords": "load balancer system design L4 L7 algorithms explained",
        "diagram_description": "Internet traffic flows to Load Balancer (with health check arrows to each backend). LB distributes requests to Server 1, Server 2, Server 3 using chosen algorithm. Failed server (red X) is bypassed.",
        "real_world_examples": [
            "Netflix uses AWS ELB to distribute traffic across thousands of microservice instances",
            "Google uses Maglev, a custom L4 load balancer handling millions of requests per second",
            "Cloudflare's global load balancer routes users to the nearest healthy data center",
        ],
        "related_concepts": [6, 8, 9],
        "practice_questions": [
            "How would you design a global load balancing solution for a CDN?",
            "When would you choose L4 over L7 load balancing?",
            "How do you handle the load balancer becoming a single point of failure?",
        ],
    },
    {
        "id": 8,
        "title": "Content Delivery Networks (CDN)",
        "phase": 2,
        "difficulty": "medium",
        "estimated_minutes": 25,
        "frequency": "high",
        "tags": ["cdn", "caching", "performance", "infrastructure"],
        "companies_asking": ["Amazon", "Netflix", "Google", "Cloudflare", "Meta"],
        "cheat_sheet": "CDNs cache content at edge servers close to users. Push CDN: origin pushes content. Pull CDN: edge fetches on first request. Reduces latency, bandwidth costs, and origin load. Essential for static assets and streaming.",
        "explanation": """## Content Delivery Networks (CDN)

A **CDN** is a geographically distributed network of servers that caches content closer to users. Instead of everyone hitting your origin server in Virginia, users in Tokyo get content from a nearby edge server.

### How CDNs Work
1. User requests `image.jpg` from your domain
2. DNS resolves to the nearest CDN edge server
3. If the edge has it cached -> return immediately (cache hit)
4. If not -> fetch from origin, cache it, then return (cache miss)

### Push vs Pull CDN
- **Push CDN**: You upload content to the CDN proactively. Good for content you know will be popular.
- **Pull CDN**: CDN fetches from origin on first request. Simpler to manage, but first request is slower.

### What to Cache on a CDN
- Static assets: images, CSS, JavaScript, fonts
- Video content (streaming)
- API responses (for read-heavy, rarely changing data)
- HTML pages (for static or semi-static sites)

### Cache Invalidation
- **TTL-based**: Content expires after a set time
- **Purge**: Manually remove specific content from all edge servers
- **Versioned URLs**: `style.v2.css` or `style.css?v=abc123`""",
        "key_points": [
            "CDNs reduce latency by serving content from geographically closer servers",
            "Pull CDNs are easier to manage; push CDNs give more control",
            "Cache invalidation is the biggest challenge with CDNs",
            "CDNs also protect against DDoS attacks by distributing traffic",
            "Modern CDNs can run edge computing (Cloudflare Workers, Lambda@Edge)",
        ],
        "interview_tips": [
            "Mention CDN for any system serving static content or global users",
            "Discuss cache invalidation strategy for dynamic content",
            "Know the difference between push and pull CDN and when to use each",
        ],
        "common_mistakes": [
            "Caching dynamic, personalized content on CDN without proper cache keys",
            "Setting TTL too high and serving stale content",
            "Forgetting CDN costs scale with bandwidth (egress fees)",
        ],
        "youtube_keywords": "CDN content delivery network system design how CDN works",
        "diagram_description": "Origin server in central location, surrounded by CDN edge servers globally (US, Europe, Asia). User connects to nearest edge. Cache hit returns directly; cache miss fetches from origin then caches.",
        "real_world_examples": [
            "Netflix Open Connect: custom CDN with servers in ISPs, serving 15% of global internet traffic",
            "Cloudflare CDN spans 300+ cities, caching and protecting websites globally",
            "Amazon CloudFront serves static assets for AWS customers with edge locations worldwide",
        ],
        "related_concepts": [5, 7, 2],
        "practice_questions": [
            "How would you design a CDN for a video streaming platform?",
            "What strategies would you use to invalidate cached content across a global CDN?",
            "Should you put API responses behind a CDN? When and how?",
        ],
    },
    {
        "id": 9,
        "title": "Message Queues & Event Streaming",
        "phase": 2,
        "difficulty": "medium",
        "estimated_minutes": 35,
        "frequency": "very_high",
        "tags": ["messaging", "async", "infrastructure", "event-driven"],
        "companies_asking": ["Amazon", "Google", "Meta", "Uber", "LinkedIn"],
        "cheat_sheet": "Queues decouple producers from consumers for async processing. RabbitMQ for task queues, Kafka for event streaming/log. Enables: decoupling, buffering, async processing, fault tolerance. Watch for ordering, exactly-once delivery, and dead letter queues.",
        "explanation": """## Message Queues & Event Streaming

**Message queues** enable asynchronous communication between services. Instead of Service A calling Service B directly (and waiting), Service A puts a message on a queue, and Service B processes it when ready.

### Message Queue (RabbitMQ, SQS)
- **Point-to-point**: One producer, one consumer per message
- **Task queues**: Distribute work among multiple workers
- Messages are **consumed and removed** from the queue
- Great for: background jobs, email sending, image processing

### Event Streaming (Kafka, Kinesis)
- **Pub-sub**: Multiple consumers can read the same event
- Events are **retained** for a configurable period (days/weeks)
- **Ordered within partitions**: Useful for maintaining event sequence
- Great for: real-time analytics, event sourcing, data pipelines

### Key Benefits
1. **Decoupling**: Services don't need to know about each other
2. **Buffering**: Handle traffic spikes without overwhelming downstream services
3. **Reliability**: Messages persist even if consumers are temporarily down
4. **Scalability**: Add more consumers to increase throughput

### Important Concepts
- **Dead letter queue (DLQ)**: Where failed messages go after max retries
- **Ordering guarantees**: Important for some use cases (financial transactions)
- **At-least-once vs exactly-once delivery**: Trade-off between simplicity and correctness""",
        "key_points": [
            "Message queues decouple services and enable asynchronous processing",
            "Kafka retains events and supports multiple consumers; traditional queues don't",
            "Dead letter queues handle messages that can't be processed successfully",
            "Exactly-once delivery is hard; most systems use at-least-once with idempotent consumers",
            "Partitioning enables parallel consumption while maintaining order within partitions",
        ],
        "interview_tips": [
            "Use message queues whenever you have async workflows or need to decouple services",
            "Specify Kafka for event streaming/replay, SQS/RabbitMQ for task queues",
            "Always mention idempotency when discussing at-least-once delivery",
        ],
        "common_mistakes": [
            "Not handling message failures - always discuss retry logic and dead letter queues",
            "Assuming messages are processed in order without using partitioning correctly",
            "Using synchronous communication when async would reduce latency and improve resilience",
        ],
        "youtube_keywords": "message queue Kafka system design event streaming pub sub",
        "diagram_description": "Producer services push messages to Queue/Kafka topic. Multiple consumer instances pull and process messages. Dead letter queue catches failures. Kafka shows partitions with ordered events and consumer groups.",
        "real_world_examples": [
            "Uber uses Kafka for real-time trip event processing and driver matching",
            "LinkedIn processes over 7 trillion messages per day through Kafka",
            "Amazon uses SQS to decouple order placement from order fulfillment",
        ],
        "related_concepts": [7, 14, 17],
        "practice_questions": [
            "When would you choose Kafka over RabbitMQ?",
            "How would you ensure exactly-once processing in a message queue system?",
            "Design an email notification system using message queues",
        ],
    },
    {
        "id": 10,
        "title": "Database Indexing & Query Optimization",
        "phase": 2,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "high",
        "tags": ["databases", "performance", "indexing"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Uber"],
        "cheat_sheet": "Indexes are data structures (B-tree, hash, LSM) that speed up reads at the cost of slower writes and extra storage. Index columns used in WHERE, JOIN, ORDER BY. Composite indexes follow leftmost prefix rule.",
        "explanation": """## Database Indexing & Query Optimization

**Indexes** are like a book's table of contents - they help the database find data without scanning every row. Without an index, a query on 100M rows scans all 100M rows. With an index, it might check only 10.

### How Indexes Work
Most databases use **B-tree** indexes (balanced tree structure):
- Lookups go from O(n) to O(log n)
- Range queries are efficient (BETWEEN, >, <)
- Maintained on every INSERT/UPDATE/DELETE (write overhead)

### Types of Indexes
- **B-tree**: Default, good for range queries and equality
- **Hash index**: O(1) lookups, only for equality (no range)
- **Full-text**: For text search (inverted index)
- **Composite**: Multiple columns, follows leftmost prefix rule
- **Covering**: Index contains all needed columns, avoiding table lookup

### Key Principles
1. **Index columns used in WHERE and JOIN clauses**
2. **Composite index order matters**: (a, b, c) supports queries on (a), (a,b), (a,b,c) but NOT (b) alone
3. **Don't over-index**: Each index costs write performance and storage
4. **Use EXPLAIN/ANALYZE** to understand query execution plans

### Write vs Read Trade-off
More indexes = faster reads, slower writes. For write-heavy systems, be selective with indexes.""",
        "key_points": [
            "B-tree indexes speed up reads from O(n) to O(log n)",
            "Every index adds overhead to write operations",
            "Composite index column order matters (leftmost prefix rule)",
            "EXPLAIN/ANALYZE helps diagnose slow queries",
            "Covering indexes avoid table lookups for maximum read performance",
        ],
        "interview_tips": [
            "When designing a database schema, always discuss which columns to index",
            "Mention the read vs write trade-off of indexing",
            "Know when NOT to index (high-write tables with rarely queried columns)",
        ],
        "common_mistakes": [
            "Indexing every column - this destroys write performance",
            "Wrong composite index order (the leftmost prefix rule)",
            "Not using EXPLAIN to verify queries actually use the index",
        ],
        "youtube_keywords": "database indexing B-tree composite index query optimization explained",
        "diagram_description": "B-tree index visualization: root node with range pointers, internal nodes narrowing the search, leaf nodes pointing to actual data rows. Shows how a query traverses 3-4 levels instead of scanning all rows.",
        "real_world_examples": [
            "Uber indexes (city, timestamp) for efficient trip queries within a city and time range",
            "Amazon indexes (user_id, order_date) for fast order history lookups",
            "Facebook uses composite indexes on (user_id, post_time) for efficient news feed queries",
        ],
        "related_concepts": [4, 15],
        "practice_questions": [
            "You have a query: SELECT * FROM orders WHERE user_id=? AND status=? ORDER BY created_at. Design the optimal index.",
            "When would you use a hash index instead of a B-tree index?",
            "How do you handle indexing for a table with 1 billion rows?",
        ],
    },
    {
        "id": 11,
        "title": "Proxies: Forward & Reverse",
        "phase": 2,
        "difficulty": "easy",
        "estimated_minutes": 20,
        "frequency": "high",
        "tags": ["networking", "infrastructure", "security"],
        "companies_asking": ["Google", "Amazon", "Cloudflare", "Meta"],
        "cheat_sheet": "Forward proxy: sits in front of clients (hide identity, bypass restrictions). Reverse proxy: sits in front of servers (load balancing, SSL, caching, security). Nginx and HAProxy are common reverse proxies.",
        "explanation": """## Proxies: Forward & Reverse

A **proxy** is an intermediary server between clients and servers. There are two types, and they serve very different purposes.

### Forward Proxy
Sits between **clients and the internet**. The server doesn't know who the real client is.
- **VPNs and anonymizers**: Hide client IP address
- **Content filtering**: Corporate firewalls blocking certain sites
- **Caching**: Cache responses for multiple clients (like a shared library)

### Reverse Proxy
Sits between **the internet and your servers**. Clients don't know which backend server handles their request.
- **Load balancing**: Distribute traffic across backends
- **SSL termination**: Handle HTTPS encryption/decryption
- **Caching**: Cache static responses
- **Security**: Hide backend topology, filter malicious requests
- **Compression**: Reduce response sizes

### Common Reverse Proxies
- **Nginx**: High-performance web server and reverse proxy
- **HAProxy**: Specialized for load balancing
- **Envoy**: Modern service mesh proxy (used by Istio)

In system design, when you say "reverse proxy" or "API gateway," you're often referring to the same concept - an entry point that handles cross-cutting concerns before routing to backend services.""",
        "key_points": [
            "Forward proxy represents clients; reverse proxy represents servers",
            "Reverse proxies handle cross-cutting concerns (SSL, caching, rate limiting)",
            "API gateways are essentially reverse proxies with additional features",
            "Nginx is the most popular reverse proxy for web applications",
            "Reverse proxies improve security by hiding backend infrastructure",
        ],
        "interview_tips": [
            "Use 'reverse proxy' or 'API gateway' as the entry point in your system design",
            "Mention SSL termination at the proxy layer to offload backend servers",
            "Discuss rate limiting and authentication at the proxy level",
        ],
        "common_mistakes": [
            "Confusing forward and reverse proxies in discussion",
            "Not using a reverse proxy and exposing backend servers directly",
            "Forgetting that the reverse proxy itself needs to be scalable and redundant",
        ],
        "youtube_keywords": "forward vs reverse proxy system design Nginx API gateway",
        "diagram_description": "Forward proxy: Multiple clients -> Forward Proxy -> Internet -> Server. Reverse proxy: Client -> Internet -> Reverse Proxy (Nginx/HAProxy) -> Multiple backend servers. Reverse proxy handles SSL, caching, rate limiting.",
        "real_world_examples": [
            "Nginx serves as a reverse proxy for over 30% of all websites on the internet",
            "Cloudflare acts as a reverse proxy providing DDoS protection and CDN services",
            "Netflix uses Zuul as an API gateway/reverse proxy for routing and filtering",
        ],
        "related_concepts": [7, 8],
        "practice_questions": [
            "What are the benefits of putting a reverse proxy in front of your application servers?",
            "How does an API gateway differ from a simple reverse proxy?",
            "Design the proxy layer for a microservices architecture",
        ],
    },
    {
        "id": 12,
        "title": "Consistent Hashing",
        "phase": 2,
        "difficulty": "hard",
        "estimated_minutes": 35,
        "frequency": "high",
        "tags": ["distributed-systems", "hashing", "scaling"],
        "companies_asking": ["Google", "Amazon", "Meta", "Netflix", "Uber"],
        "cheat_sheet": "Maps both servers and data to a ring using hash function. Data goes to the next server clockwise. Adding/removing a server only remaps ~1/N of keys (vs all keys with simple modular hashing). Virtual nodes improve balance.",
        "explanation": """## Consistent Hashing

When distributing data across multiple servers (caching, sharding), you need a way to decide which server stores which data. **Simple modular hashing** (`server = hash(key) % N`) breaks when servers are added or removed - almost all keys get remapped.

**Consistent hashing** solves this by mapping both servers and keys onto a circular ring (0 to 2^32).

### How It Works
1. Hash each server name to a position on the ring
2. Hash each data key to a position on the ring
3. Walk clockwise from the key's position until you find a server
4. That server owns the key

### Adding/Removing Servers
- **Add a server**: Only keys between the new server and its predecessor get remapped (~1/N of total)
- **Remove a server**: Only that server's keys get remapped to the next server clockwise

### Virtual Nodes
Real servers may be unevenly distributed on the ring. Solution: assign **multiple virtual nodes** per physical server. A server with more capacity gets more virtual nodes, ensuring balanced distribution.

### Where It's Used
- **Distributed caches**: Memcached, Redis clusters
- **Database sharding**: DynamoDB, Cassandra
- **Load balancing**: Consistent hash-based routing""",
        "key_points": [
            "Only ~1/N keys need remapping when a server is added/removed",
            "Virtual nodes solve the uneven distribution problem",
            "Used in DynamoDB, Cassandra, and distributed caches",
            "Simple modular hashing causes massive remapping on topology changes",
            "The hash ring concept applies to both caching and database sharding",
        ],
        "interview_tips": [
            "Draw the hash ring diagram when explaining consistent hashing",
            "Mention virtual nodes to show you understand the uniformity problem",
            "Connect it to practical systems: cache clusters, database sharding",
        ],
        "common_mistakes": [
            "Using simple modular hashing for distributed systems (doesn't handle server changes well)",
            "Forgetting about virtual nodes, leading to unbalanced data distribution",
            "Not explaining WHY consistent hashing is better than modular hashing",
        ],
        "youtube_keywords": "consistent hashing system design distributed systems hash ring",
        "diagram_description": "Circular hash ring with server positions (S1, S2, S3) and key positions (K1, K2, K3, K4). Arrows show keys mapping to next clockwise server. When S2 is removed, only its keys move to S3.",
        "real_world_examples": [
            "Amazon DynamoDB uses consistent hashing to partition data across nodes",
            "Apache Cassandra uses consistent hashing with virtual nodes for data distribution",
            "Discord uses consistent hashing to route WebSocket connections to specific servers",
        ],
        "related_concepts": [6, 15, 10],
        "practice_questions": [
            "Explain consistent hashing with a diagram. Why is it better than modular hashing?",
            "How do virtual nodes improve consistent hashing?",
            "How would you implement consistent hashing for a distributed cache?",
        ],
    },
    {
        "id": 13,
        "title": "Blob Storage & Object Storage",
        "phase": 2,
        "difficulty": "easy",
        "estimated_minutes": 20,
        "frequency": "high",
        "tags": ["storage", "infrastructure", "media"],
        "companies_asking": ["Amazon", "Google", "Meta", "Netflix", "Dropbox"],
        "cheat_sheet": "Object storage (S3, GCS) stores unstructured data (images, videos, files) as flat key-value blobs. Highly durable (11 nines), scalable, and cheap. Not for frequent updates or database-like queries. Use pre-signed URLs for secure access.",
        "explanation": """## Blob Storage & Object Storage

**Object storage** (also called blob storage) is designed for storing large amounts of unstructured data: images, videos, documents, backups, logs. Unlike file systems or databases, objects are stored in a flat namespace with unique keys.

### Key Characteristics
- **Flat namespace**: No directory hierarchy, just bucket + key
- **Immutable objects**: Write once, read many (updates replace the whole object)
- **Highly durable**: Amazon S3 offers 99.999999999% (11 nines) durability
- **Virtually unlimited scale**: Store petabytes of data
- **Cost-effective**: Tiered storage (hot, warm, cold) for cost optimization

### Common Services
- **Amazon S3**: The industry standard for object storage
- **Google Cloud Storage**: Similar with integrated ML features
- **Azure Blob Storage**: Microsoft's offering

### Access Patterns
- **Pre-signed URLs**: Temporary URLs granting time-limited access to private objects
- **CDN integration**: Serve objects via CDN for global low-latency access
- **Lifecycle policies**: Automatically move objects to cheaper tiers or delete old data

### When to Use Object Storage
- User-uploaded media (profile pictures, post images)
- Video content and streaming assets
- Log files and analytics data
- Backups and archival data
- Static website hosting""",
        "key_points": [
            "Object storage is for unstructured data (media, files, logs)",
            "S3 provides 11 nines of durability - data is essentially never lost",
            "Pre-signed URLs enable secure, temporary access to private objects",
            "Lifecycle policies automate cost optimization by tiering storage",
            "Objects are immutable - updates replace the entire object",
        ],
        "interview_tips": [
            "Use S3/object storage for any media, file, or large data storage needs",
            "Mention pre-signed URLs for secure upload/download without exposing credentials",
            "Discuss CDN in front of object storage for serving static assets",
        ],
        "common_mistakes": [
            "Storing binary files in a SQL database instead of object storage",
            "Not using CDN in front of object storage for frequently accessed content",
            "Ignoring storage tiers and lifecycle policies, leading to unnecessary costs",
        ],
        "youtube_keywords": "blob storage S3 object storage system design AWS",
        "diagram_description": "Client uploads via pre-signed URL to S3 bucket. Bucket stores objects as key-value (key=path, value=blob). CDN layer in front for reads. Lifecycle policy arrows show hot->warm->cold->archive tiers.",
        "real_world_examples": [
            "Instagram stores all user photos and videos in Amazon S3",
            "Netflix stores movie and show content in S3 before distributing via their CDN",
            "Dropbox migrated from S3 to their own blob storage (Magic Pocket) to reduce costs",
        ],
        "related_concepts": [4, 8],
        "practice_questions": [
            "How would you design the storage layer for an image sharing platform?",
            "Explain the difference between object storage and block storage",
            "How would you handle uploading large files (>5GB) to object storage?",
        ],
    },
    # ── Phase 3: Design Patterns & Trade-offs ──
    {
        "id": 14,
        "title": "CAP Theorem & Consistency Models",
        "phase": 3,
        "difficulty": "hard",
        "estimated_minutes": 35,
        "frequency": "very_high",
        "tags": ["distributed-systems", "consistency", "theory"],
        "companies_asking": ["Google", "Amazon", "Meta", "Netflix", "Apple"],
        "cheat_sheet": "CAP: distributed systems can guarantee only 2 of 3: Consistency, Availability, Partition tolerance. Since partitions happen, real choice is CP (consistent, may reject requests) vs AP (available, may serve stale data). Most choose eventual consistency.",
        "explanation": """## CAP Theorem & Consistency Models

The **CAP Theorem** states that a distributed system can only guarantee two of three properties:
- **Consistency**: Every read receives the most recent write
- **Availability**: Every request receives a response (even if it's stale)
- **Partition Tolerance**: System continues operating despite network partitions

### The Real Choice: CP vs AP
Since network partitions are inevitable in distributed systems, the practical choice is:
- **CP (Consistency + Partition tolerance)**: System may become unavailable during partitions but never returns stale data. Example: banking systems, ZooKeeper.
- **AP (Availability + Partition tolerance)**: System stays available but may return stale data during partitions. Example: DNS, Cassandra.

### Consistency Models (from strongest to weakest)
1. **Strong consistency**: Reads always see the latest write (slowest, like a single database)
2. **Linearizability**: Operations appear atomic and ordered (gold standard for distributed)
3. **Sequential consistency**: Operations from each client appear in order
4. **Causal consistency**: Causally related operations appear in order
5. **Eventual consistency**: Given time without new writes, all replicas converge (fastest, most available)

### PACELC Extension
Even when there's **no** partition, there's a trade-off between **Latency** and **Consistency**: Lower latency usually means weaker consistency.""",
        "key_points": [
            "Network partitions are inevitable - the real choice is CP vs AP",
            "Most modern systems choose eventual consistency for availability and performance",
            "Strong consistency requires coordination, which adds latency",
            "PACELC extends CAP: even without partitions, there's a latency vs consistency trade-off",
            "Different parts of a system can make different CAP trade-offs",
        ],
        "interview_tips": [
            "Always discuss CAP trade-offs when designing distributed systems",
            "Specify which consistency model your system needs and why",
            "Different features in the same system can have different consistency requirements",
        ],
        "common_mistakes": [
            "Saying a system is 'CP and AP' - you must choose one during partitions",
            "Always choosing strong consistency without considering the latency impact",
            "Not realizing that even within one system, different data can have different consistency needs",
        ],
        "youtube_keywords": "CAP theorem system design consistency models eventual consistency explained",
        "diagram_description": "Venn diagram with three circles: C (Consistency), A (Availability), P (Partition Tolerance). Overlap areas labeled: CP (ZooKeeper, HBase), AP (Cassandra, DynamoDB), CA (traditional single-node RDBMS).",
        "real_world_examples": [
            "Amazon DynamoDB defaults to AP (eventual consistency) but offers optional strong consistency reads",
            "Google Spanner achieves CP with strong consistency globally using atomic clocks (TrueTime)",
            "Facebook's Cassandra is AP - your friend count might be slightly stale but the system is always available",
        ],
        "related_concepts": [4, 15, 16],
        "practice_questions": [
            "Your e-commerce system needs to handle inventory counts during a sale. Which consistency model do you choose?",
            "Explain the difference between strong and eventual consistency with real examples",
            "What is the PACELC theorem and how does it extend CAP?",
        ],
    },
    {
        "id": 15,
        "title": "Database Sharding & Partitioning",
        "phase": 3,
        "difficulty": "hard",
        "estimated_minutes": 35,
        "frequency": "very_high",
        "tags": ["databases", "distributed-systems", "scaling"],
        "companies_asking": ["Google", "Amazon", "Meta", "Uber", "Pinterest"],
        "cheat_sheet": "Sharding splits data across multiple database instances. Strategies: hash-based (even distribution), range-based (locality), directory-based (lookup table). Challenges: cross-shard queries, rebalancing, hotspots. Avoid sharding until necessary.",
        "explanation": """## Database Sharding & Partitioning

When a single database can't handle your data volume or traffic, **sharding** splits the data across multiple database instances, each holding a subset of the data.

### Sharding Strategies

**1. Hash-based Sharding**
`shard = hash(key) % num_shards`
- Even data distribution
- Hard to do range queries across shards
- Consistent hashing variant handles node changes better

**2. Range-based Sharding**
Split by ranges: users A-M on shard 1, N-Z on shard 2
- Efficient range queries within a shard
- Risk of hotspots (if certain ranges are more popular)

**3. Directory-based Sharding**
A lookup service maps keys to shards
- Most flexible
- Lookup service becomes a single point of failure

### Challenges of Sharding
- **Cross-shard queries**: JOINs across shards are expensive or impossible
- **Rebalancing**: Adding shards requires data migration
- **Hotspots**: Uneven data or traffic distribution
- **Distributed transactions**: Very hard across shards
- **Operational complexity**: More databases to manage

### Best Practices
- **Delay sharding** until vertical scaling and read replicas aren't enough
- Choose shard key carefully - it's very hard to change later
- Plan for rebalancing from the start""",
        "key_points": [
            "Shard key selection is the most critical decision - it determines data distribution and query patterns",
            "Hash-based sharding gives even distribution; range-based enables efficient range queries",
            "Cross-shard queries are expensive - design to keep related data on the same shard",
            "Resharding (changing the shard count) is one of the most painful database operations",
            "Consider read replicas and vertical scaling before resorting to sharding",
        ],
        "interview_tips": [
            "Always justify why sharding is needed - don't jump to it prematurely",
            "Discuss shard key selection with specific trade-offs for the system being designed",
            "Mention consistent hashing as an improvement over simple modular sharding",
        ],
        "common_mistakes": [
            "Sharding too early when vertical scaling or read replicas would suffice",
            "Choosing a shard key that creates hotspots (e.g., sharding by date puts all writes on one shard)",
            "Not planning for cross-shard query needs in the data model",
        ],
        "youtube_keywords": "database sharding partitioning system design horizontal scaling",
        "diagram_description": "Application layer with routing logic sends queries to appropriate shard. Three database shards: Shard 1 (users 1-1000), Shard 2 (users 1001-2000), Shard 3 (users 2001-3000). Hash function determines routing.",
        "real_world_examples": [
            "Instagram shards PostgreSQL by user ID, keeping a user's posts on the same shard",
            "Pinterest shards MySQL by object ID using consistent hashing with virtual nodes",
            "Uber shards trip data by city and time to keep geographically relevant data together",
        ],
        "related_concepts": [4, 12, 14, 16],
        "practice_questions": [
            "How would you shard a social media database where users query their own posts and also see a global feed?",
            "What shard key would you choose for an e-commerce orders table and why?",
            "How do you handle a celebrity user whose shard gets 100x more traffic than others?",
        ],
    },
    {
        "id": 16,
        "title": "Database Replication",
        "phase": 3,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "high",
        "tags": ["databases", "availability", "distributed-systems"],
        "companies_asking": ["Google", "Amazon", "Meta", "Netflix", "Microsoft"],
        "cheat_sheet": "Replication copies data across multiple database nodes. Leader-follower: one writer, multiple readers (common). Leader-leader: multiple writers (conflict resolution needed). Synchronous is consistent but slow; async is fast but may lose data.",
        "explanation": """## Database Replication

**Replication** is maintaining copies of the same data on multiple database nodes. It provides **high availability** (if one node fails, others take over), **improved read performance** (distribute reads across replicas), and **data durability** (multiple copies).

### Replication Strategies

**1. Leader-Follower (Master-Slave)**
- One leader handles all writes
- Followers replicate from the leader and serve reads
- Simple, most common pattern
- Trade-off: follower reads may be slightly stale (replication lag)

**2. Leader-Leader (Multi-Master)**
- Multiple nodes accept writes
- Requires conflict resolution (last-write-wins, manual merge)
- Useful for multi-region deployments
- Complex to manage correctly

**3. Leaderless (Quorum)**
- Any node can accept reads and writes
- Uses quorum: W + R > N for consistency (e.g., write to 2 of 3, read from 2 of 3)
- Used by DynamoDB, Cassandra

### Synchronous vs Asynchronous Replication
- **Synchronous**: Leader waits for follower acknowledgment. Consistent but slower.
- **Asynchronous**: Leader doesn't wait. Faster but followers may lag behind.
- **Semi-synchronous**: One follower is sync, rest are async (compromise).""",
        "key_points": [
            "Leader-follower is the most common pattern - one writer, many readers",
            "Async replication is faster but has replication lag (stale reads possible)",
            "Quorum-based (W+R>N) provides tunable consistency for leaderless systems",
            "Leader election is needed when the primary fails (failover)",
            "Multi-region replication enables disaster recovery but adds latency",
        ],
        "interview_tips": [
            "Use leader-follower replication for read-heavy systems to scale reads",
            "Discuss replication lag and its impact on user experience",
            "Mention automatic failover and leader election for high availability",
        ],
        "common_mistakes": [
            "Assuming followers are always consistent with the leader (replication lag exists)",
            "Not discussing failover mechanism when the leader goes down",
            "Using multi-master without a clear conflict resolution strategy",
        ],
        "youtube_keywords": "database replication leader follower master slave system design",
        "diagram_description": "Leader node receives all writes, replicates to Follower 1 and Follower 2 (async arrows). Read requests distributed across all nodes. When leader fails, follower promoted to new leader (failover).",
        "real_world_examples": [
            "MySQL uses leader-follower replication with binlog for most production deployments",
            "Amazon Aurora replicates writes to 6 copies across 3 availability zones synchronously",
            "Cassandra uses leaderless replication with configurable quorum levels",
        ],
        "related_concepts": [4, 14, 15],
        "practice_questions": [
            "How would you handle a situation where a user writes data and immediately reads it back but hits a stale replica?",
            "Design a multi-region database replication strategy for a global application",
            "What happens during a failover when the leader goes down? Walk through the process.",
        ],
    },
    {
        "id": 17,
        "title": "Microservices Architecture",
        "phase": 3,
        "difficulty": "medium",
        "estimated_minutes": 35,
        "frequency": "very_high",
        "tags": ["architecture", "microservices", "design-patterns"],
        "companies_asking": ["Google", "Amazon", "Netflix", "Uber", "Spotify"],
        "cheat_sheet": "Split monolith into small, independently deployable services, each owning its data. Benefits: independent scaling, deployment, tech choices. Costs: network latency, distributed transactions, operational complexity. Use when team/product is large enough to justify the overhead.",
        "explanation": """## Microservices Architecture

**Microservices** is an architectural pattern where an application is composed of small, independent services that communicate over the network (HTTP/gRPC). Each service is responsible for a specific business capability.

### Key Principles
1. **Single responsibility**: Each service does one thing well
2. **Own your data**: Each service has its own database
3. **Independent deployment**: Deploy services independently without affecting others
4. **Decentralized governance**: Teams choose their own tech stacks
5. **Design for failure**: Services must handle downstream failures gracefully

### Benefits
- Independent scaling (scale only the services that need it)
- Independent deployment (ship features faster)
- Technology diversity (use the best tool for each job)
- Team autonomy (small teams own services end-to-end)

### Challenges
- Network latency between services
- Distributed transactions and data consistency
- Service discovery and load balancing
- Monitoring, tracing, and debugging across services
- Operational overhead (many services to deploy and manage)

### When NOT to Use Microservices
- Small teams (< 10 engineers)
- Simple applications
- When you can't afford the operational overhead
- When strong transactions across domains are critical

Start with a monolith, extract services when clear boundaries emerge.""",
        "key_points": [
            "Each microservice owns its data - no shared databases",
            "Start with a monolith, extract microservices when team/product complexity demands it",
            "Service mesh (Istio/Envoy) handles cross-cutting concerns like auth and tracing",
            "Distributed tracing (Jaeger, Zipkin) is essential for debugging in microservices",
            "Circuit breakers prevent cascading failures when a service is down",
        ],
        "interview_tips": [
            "Don't default to microservices - justify the architecture choice",
            "Discuss service boundaries based on business domains (Domain-Driven Design)",
            "Mention inter-service communication: REST, gRPC, or async messaging",
        ],
        "common_mistakes": [
            "Creating too many tiny services (nano-services) that add complexity without benefit",
            "Sharing databases between services, creating tight coupling",
            "Not implementing proper monitoring and distributed tracing from the start",
        ],
        "youtube_keywords": "microservices architecture system design monolith vs microservices",
        "diagram_description": "API Gateway receives requests, routes to individual microservices: User Service, Order Service, Payment Service, Notification Service. Each has its own database. Services communicate via REST/gRPC and message queues.",
        "real_world_examples": [
            "Netflix has over 1000 microservices powering streaming, recommendations, and billing",
            "Uber evolved from a monolith to microservices to handle different city-level requirements",
            "Amazon's two-pizza team rule led to microservices - each team owns a service",
        ],
        "related_concepts": [9, 11, 18],
        "practice_questions": [
            "When would you choose a monolith over microservices?",
            "How do you handle transactions that span multiple microservices?",
            "Design the service boundaries for an e-commerce platform",
        ],
    },
    {
        "id": 18,
        "title": "Rate Limiting & Throttling",
        "phase": 3,
        "difficulty": "medium",
        "estimated_minutes": 25,
        "frequency": "high",
        "tags": ["security", "api-design", "infrastructure"],
        "companies_asking": ["Google", "Amazon", "Meta", "Stripe", "Cloudflare"],
        "cheat_sheet": "Rate limiting controls request frequency to prevent abuse. Algorithms: token bucket (bursty OK), sliding window (smooth), fixed window (simple). Implement at API gateway or per-service. Return HTTP 429 when limited. Use Redis for distributed rate limiting.",
        "explanation": """## Rate Limiting & Throttling

**Rate limiting** controls how many requests a client can make in a given time window. It protects your system from abuse, prevents resource exhaustion, and ensures fair usage.

### Common Algorithms

**1. Token Bucket**
- Bucket holds tokens, refilled at a steady rate
- Each request consumes a token
- Allows short bursts (up to bucket capacity)
- Most popular algorithm (used by AWS, Stripe)

**2. Sliding Window Log**
- Track timestamp of each request
- Count requests in the sliding window
- Accurate but memory-intensive

**3. Fixed Window Counter**
- Count requests per fixed time window (e.g., per minute)
- Simple but allows burst at window boundaries

**4. Sliding Window Counter**
- Hybrid: weighted average of current and previous window
- Good balance of accuracy and memory

### Implementation
- **Where**: API gateway, reverse proxy, or application layer
- **Storage**: Redis for distributed rate limiting (shared counter across instances)
- **Response**: HTTP 429 Too Many Requests with `Retry-After` header
- **Granularity**: Per user, per IP, per API key, per endpoint

### Rate Limiting Tiers
```
Free tier:    100 requests/minute
Basic tier:   1,000 requests/minute
Pro tier:     10,000 requests/minute
Enterprise:   Custom limits
```""",
        "key_points": [
            "Token bucket is the most popular algorithm - allows bursts within capacity",
            "Use Redis for distributed rate limiting across multiple server instances",
            "Rate limit at multiple levels: per user, per IP, per API endpoint",
            "Always return HTTP 429 with a Retry-After header when rate limited",
            "Different rate limits for different API tiers (free vs premium)",
        ],
        "interview_tips": [
            "Mention rate limiting proactively when designing any public API",
            "Specify the algorithm (token bucket is a safe default) and explain why",
            "Discuss what happens when a user hits the rate limit (graceful degradation)",
        ],
        "common_mistakes": [
            "Not rate limiting at all, leaving the system vulnerable to abuse",
            "Rate limiting only at the application level without gateway-level protection",
            "Not communicating rate limits to clients via headers (X-RateLimit-Remaining)",
        ],
        "youtube_keywords": "rate limiting token bucket algorithm system design API throttling",
        "diagram_description": "Client requests flow through Rate Limiter (checks Redis counter). If under limit: allow through to backend. If over limit: return 429 with Retry-After. Token bucket visualization shows tokens being added at fixed rate and consumed per request.",
        "real_world_examples": [
            "GitHub API limits to 5,000 requests per hour for authenticated users",
            "Stripe uses token bucket rate limiting with different tiers per API key",
            "Cloudflare provides edge-level rate limiting to protect against DDoS attacks",
        ],
        "related_concepts": [3, 11, 17],
        "practice_questions": [
            "Design a distributed rate limiter that works across multiple server instances",
            "Compare token bucket vs sliding window - when would you use each?",
            "How would you rate limit a chat application where users send messages?",
        ],
    },
    {
        "id": 19,
        "title": "Event-Driven Architecture & CQRS",
        "phase": 3,
        "difficulty": "hard",
        "estimated_minutes": 35,
        "frequency": "high",
        "tags": ["architecture", "event-driven", "design-patterns"],
        "companies_asking": ["Amazon", "Google", "Netflix", "Uber", "LinkedIn"],
        "cheat_sheet": "Event-driven: services communicate via events instead of direct calls. CQRS: separate read and write models for different optimization. Event sourcing: store events as source of truth, derive state. Enables eventual consistency, auditability, and temporal queries.",
        "explanation": """## Event-Driven Architecture & CQRS

### Event-Driven Architecture (EDA)
Instead of services calling each other directly, they produce and consume **events**. An event represents something that happened: "OrderPlaced", "PaymentCompleted", "UserRegistered".

**Benefits:**
- Loose coupling between services
- Natural audit trail
- Easy to add new consumers without modifying producers
- Resilient to failures (events are queued)

### CQRS (Command Query Responsibility Segregation)
Separate the **write model** (commands) from the **read model** (queries).
- **Write side**: Optimized for data integrity and business logic
- **Read side**: Optimized for query performance (denormalized views)
- Connected via events: writes produce events, reads consume and build views

### Event Sourcing
Instead of storing current state, store the **sequence of events** that led to the current state.
- State is derived by replaying events
- Complete audit trail
- Can rebuild state at any point in time
- Used with CQRS for complex domains

### When to Use
- Systems with complex business workflows
- When read and write patterns are very different
- When audit trails are required
- When you need temporal queries (what was the state at time X?)""",
        "key_points": [
            "Events are facts about what happened - they're immutable and ordered",
            "CQRS separates read and write models for independent optimization",
            "Event sourcing stores events as the source of truth, not current state",
            "Eventual consistency is inherent in event-driven systems",
            "Event-driven architecture naturally supports adding new consumers",
        ],
        "interview_tips": [
            "Use event-driven architecture for systems with complex workflows",
            "Mention CQRS when read and write patterns differ significantly",
            "Discuss the eventual consistency trade-off with event-driven systems",
        ],
        "common_mistakes": [
            "Using event-driven for simple CRUD applications where it adds unnecessary complexity",
            "Not handling event ordering and idempotency correctly",
            "Forgetting that CQRS read models are eventually consistent with the write model",
        ],
        "youtube_keywords": "event driven architecture CQRS event sourcing system design",
        "diagram_description": "Write side: Command -> Aggregate -> Event Store. Events published to Event Bus (Kafka). Read side: Event Handlers consume events, update denormalized Read Model (optimized views). Queries served from Read Model.",
        "real_world_examples": [
            "LinkedIn uses event sourcing for their messaging system to maintain complete history",
            "Netflix uses event-driven architecture for content ingestion and encoding pipeline",
            "Uber's trip lifecycle is event-driven: trip requested -> driver assigned -> trip started -> trip completed",
        ],
        "related_concepts": [9, 14, 17],
        "practice_questions": [
            "Design an order processing system using event-driven architecture",
            "When would you use CQRS vs a traditional CRUD approach?",
            "How do you handle event ordering in a distributed event-driven system?",
        ],
    },
    {
        "id": 20,
        "title": "API Gateway Pattern",
        "phase": 3,
        "difficulty": "medium",
        "estimated_minutes": 25,
        "frequency": "high",
        "tags": ["architecture", "api-design", "microservices"],
        "companies_asking": ["Amazon", "Google", "Netflix", "Microsoft", "Uber"],
        "cheat_sheet": "Single entry point for all clients. Handles: routing, authentication, rate limiting, request aggregation, protocol translation, SSL termination. Reduces client complexity. Can become a bottleneck - keep it thin. Examples: Kong, AWS API Gateway, Zuul.",
        "explanation": """## API Gateway Pattern

An **API Gateway** is a single entry point for all client requests in a microservices architecture. Instead of clients knowing about dozens of services, they talk to one gateway that routes requests appropriately.

### Responsibilities
1. **Request routing**: Route to the correct backend service
2. **Authentication & authorization**: Validate tokens/API keys
3. **Rate limiting**: Protect backend services from overload
4. **Request aggregation**: Combine multiple service calls into one client response
5. **Protocol translation**: REST to gRPC, WebSocket to HTTP, etc.
6. **SSL termination**: Handle HTTPS at the gateway
7. **Caching**: Cache frequently requested responses
8. **Monitoring & logging**: Centralized request metrics

### Backend for Frontend (BFF)
A variation where each client type (web, mobile, IoT) has its own gateway optimized for its needs. Mobile might need smaller payloads, web might need more data.

### Best Practices
- Keep the gateway thin - business logic belongs in services
- Use circuit breakers for backend service calls
- Implement request/response transformation carefully
- Monitor gateway latency closely (it's on the critical path)""",
        "key_points": [
            "API Gateway provides a single entry point for all clients",
            "Handles cross-cutting concerns: auth, rate limiting, SSL, monitoring",
            "BFF pattern creates client-specific gateways for web, mobile, etc.",
            "Keep the gateway thin - don't put business logic in it",
            "Gateway is on the critical path - its performance matters greatly",
        ],
        "interview_tips": [
            "Include an API gateway when designing microservices architectures",
            "Mention specific responsibilities it handles (auth, rate limiting, routing)",
            "Discuss BFF pattern when the system has different client types",
        ],
        "common_mistakes": [
            "Making the API gateway too fat with business logic",
            "Not making the gateway itself highly available (it's a SPOF)",
            "Not considering the latency overhead of an additional network hop",
        ],
        "youtube_keywords": "API gateway pattern system design microservices BFF",
        "diagram_description": "Web client, Mobile client, IoT device all connect to API Gateway. Gateway handles auth, rate limiting, SSL. Routes requests to User Service, Order Service, Payment Service. Optional BFF layer between gateway and clients.",
        "real_world_examples": [
            "Netflix uses Zuul as its API gateway, handling millions of requests per second",
            "Amazon API Gateway provides managed gateway for serverless and microservice architectures",
            "Kong is an open-source API gateway used by companies like NASA and Nasdaq",
        ],
        "related_concepts": [11, 17, 18],
        "practice_questions": [
            "Design an API gateway for an e-commerce platform with web and mobile clients",
            "What is the BFF pattern and when should you use it?",
            "How do you prevent the API gateway from becoming a bottleneck?",
        ],
    },
    # ── Phase 4: Real System Designs ──
    {
        "id": 21,
        "title": "Design a URL Shortener",
        "phase": 4,
        "difficulty": "medium",
        "estimated_minutes": 45,
        "frequency": "very_high",
        "tags": ["system-design", "interview", "storage", "hashing"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Twitter"],
        "cheat_sheet": "Generate short codes (base62 encoding of auto-increment ID or random). Store mapping in key-value store/SQL. 301 redirect for permanent, 302 for tracking. Handle: collision, custom aliases, analytics, expiration. Scale with caching (most URLs are read-heavy).",
        "explanation": """## Design a URL Shortener (like bit.ly)

This is one of the most popular system design interview questions. Let's walk through the complete design.

### Requirements
- Shorten a long URL to a short URL
- Redirect short URL to original URL
- Custom aliases (optional)
- Analytics (click count, referrer)
- URL expiration
- Scale: 100M URLs created/month, 10B redirects/month (100:1 read:write ratio)

### Short Code Generation

**Approach 1: Base62 Encoding**
Use an auto-incrementing ID, encode to base62 (a-z, A-Z, 0-9).
- 6 characters = 62^6 = 56.8 billion unique URLs
- Pros: No collisions, compact
- Cons: Sequential, predictable

**Approach 2: Random Hash**
Generate random 6-8 character string, check for collision.
- Pros: Unpredictable
- Cons: Collision checking needed

**Approach 3: MD5/SHA256 + Truncate**
Hash the URL, take first 6-8 characters of base62-encoded hash.
- Pros: Deterministic
- Cons: Collisions possible

### Data Model
```
urls table:
  id (PK), short_code (indexed), original_url, user_id, 
  created_at, expires_at, click_count
```

### Architecture
1. **Write path**: Client -> API -> Generate short code -> Store in DB -> Return short URL
2. **Read path**: Client -> short URL -> Load Balancer -> Cache (Redis) -> DB -> 301/302 Redirect
3. **Analytics**: Log clicks asynchronously via message queue -> Analytics service""",
        "key_points": [
            "Read-heavy system (100:1 ratio) - caching is critical",
            "Base62 encoding of auto-increment ID avoids collisions",
            "301 redirect for permanent, 302 for analytics tracking",
            "Cache popular URLs in Redis for sub-millisecond redirects",
            "Async analytics via message queue to not slow down redirects",
        ],
        "interview_tips": [
            "Start with requirements and back-of-envelope calculations",
            "Discuss trade-offs between short code generation approaches",
            "Mention caching strategy given the read-heavy workload",
        ],
        "common_mistakes": [
            "Not estimating scale (storage, QPS) before designing",
            "Using 301 redirect when you need analytics (301 is cached by browsers)",
            "Forgetting about URL expiration and cleanup",
        ],
        "youtube_keywords": "design URL shortener system design interview bit.ly",
        "diagram_description": "Write: Client -> API Server -> ID Generator -> Database (store mapping). Read: Client -> Load Balancer -> Cache (Redis) -> Database -> 302 Redirect. Analytics: Click events -> Kafka -> Analytics Service -> Dashboard.",
        "real_world_examples": [
            "bit.ly handles billions of link clicks per month with global edge caching",
            "TinyURL was one of the first URL shorteners, using a simple database-backed approach",
            "Twitter's t.co shortener wraps every link for click tracking and security scanning",
        ],
        "related_concepts": [5, 12, 4],
        "practice_questions": [
            "Walk through the complete design of a URL shortener from scratch",
            "How would you handle 10 billion redirects per month?",
            "How do you prevent abuse (spam URLs, phishing)?",
        ],
    },
    {
        "id": 22,
        "title": "Design a Chat System",
        "phase": 4,
        "difficulty": "hard",
        "estimated_minutes": 50,
        "frequency": "very_high",
        "tags": ["system-design", "interview", "real-time", "messaging"],
        "companies_asking": ["Meta", "Google", "Amazon", "Microsoft", "Slack"],
        "cheat_sheet": "WebSockets for real-time messaging. Message queue for delivery guarantees. Store messages in time-series optimized DB (Cassandra). Presence service for online status. Push notifications for offline users. Group chat: fan-out on read (small groups) or fan-out on write (large channels).",
        "explanation": """## Design a Chat System (like WhatsApp/Slack)

### Requirements
- 1-on-1 messaging
- Group messaging (up to 500 members)
- Online/offline status (presence)
- Message delivery status (sent, delivered, read)
- Push notifications for offline users
- Media sharing (images, files)
- Message history and search

### Key Components

**1. Connection Management**
- **WebSockets** for real-time bidirectional communication
- Each user maintains a persistent WebSocket connection
- Connection servers handle WebSocket lifecycle
- Use heartbeat to detect disconnections

**2. Message Flow (1-on-1)**
1. User A sends message via WebSocket
2. Chat server receives message, stores in DB
3. If User B is online: push via their WebSocket connection
4. If User B is offline: send push notification, deliver when they reconnect

**3. Group Chat**
- **Small groups (< 500)**: Fan-out on write - copy message to each recipient's inbox
- **Large channels (Slack-style)**: Fan-out on read - store once, recipients fetch on demand

**4. Message Storage**
- Cassandra or similar: optimized for time-series writes
- Partition key: conversation_id
- Clustering key: timestamp (for ordered retrieval)

**5. Presence Service**
- Track user online/offline status
- Use heartbeat (every 30s) to detect disconnections
- Pub-sub for broadcasting status changes to friends""",
        "key_points": [
            "WebSockets are essential for real-time messaging",
            "Fan-out on write for small groups, fan-out on read for large channels",
            "Message queue ensures delivery even if recipient is temporarily offline",
            "Cassandra is ideal for message storage (time-series, high write throughput)",
            "End-to-end encryption requires key exchange between clients (not stored on server)",
        ],
        "interview_tips": [
            "Clarify scope: 1-on-1 only or also group chat? How large are groups?",
            "Discuss WebSocket connection management and scaling",
            "Mention delivery guarantees: at-least-once with client-side deduplication",
        ],
        "common_mistakes": [
            "Using HTTP polling instead of WebSockets for real-time messaging",
            "Not handling the offline user case (message queuing, push notifications)",
            "Using fan-out on write for large groups (too expensive)",
        ],
        "youtube_keywords": "design chat system WhatsApp Slack system design interview",
        "diagram_description": "User A's WebSocket -> Chat Server -> Message Queue. If User B online: Chat Server -> User B's WebSocket. If offline: Push Notification Service. Messages stored in Cassandra. Presence Service tracks online status via heartbeats.",
        "real_world_examples": [
            "WhatsApp uses XMPP protocol variant with Erlang servers handling 2M connections per server",
            "Slack uses WebSockets for real-time messaging with Redis for presence tracking",
            "Discord handles millions of concurrent WebSocket connections using Elixir and Rust",
        ],
        "related_concepts": [9, 14, 4],
        "practice_questions": [
            "Design a 1-on-1 and group chat system from scratch",
            "How would you handle message ordering in a distributed chat system?",
            "Design the presence (online/offline) system for a chat application",
        ],
    },
    {
        "id": 23,
        "title": "Design a News Feed / Timeline",
        "phase": 4,
        "difficulty": "hard",
        "estimated_minutes": 50,
        "frequency": "very_high",
        "tags": ["system-design", "interview", "social-media", "feed"],
        "companies_asking": ["Meta", "Google", "Twitter", "LinkedIn", "Pinterest"],
        "cheat_sheet": "Two approaches: fan-out on write (push model - precompute feeds) or fan-out on read (pull model - compute on demand). Hybrid for celebrities. Feed stored in cache (Redis sorted set). Ranking service for relevance. Handle: celebrity problem, new followers, deletions.",
        "explanation": """## Design a News Feed / Timeline (like Facebook/Twitter)

### Requirements
- Users see posts from people they follow
- Feed should be ranked by relevance (not just chronological)
- Near real-time: new posts appear within seconds
- Scale: 500M daily active users, each following 200 people on average

### Two Fundamental Approaches

**Fan-out on Write (Push Model)**
When a user creates a post, immediately push it to all followers' feed caches.
- Pros: Feed reads are instant (pre-computed)
- Cons: Slow for users with millions of followers (celebrity problem)
- Storage: High (copy to every follower's feed)

**Fan-out on Read (Pull Model)**
When a user opens their feed, fetch latest posts from all followed users.
- Pros: No write amplification, handles celebrities well
- Cons: Slow reads (must query many sources)
- Best for: Users with millions of followers

**Hybrid (What Facebook/Twitter Actually Does)**
- Regular users: Fan-out on write
- Celebrities (>10K followers): Fan-out on read
- Best of both worlds

### Architecture
1. **Post Service**: Store posts in database
2. **Fan-out Service**: Distribute posts to follower feeds (async, via message queue)
3. **Feed Cache**: Redis sorted set per user (score = timestamp or rank)
4. **Ranking Service**: ML model to rank posts by relevance
5. **Feed API**: Paginated feed retrieval from cache""",
        "key_points": [
            "Hybrid fan-out (write for regular users, read for celebrities) is the standard approach",
            "Redis sorted sets are ideal for feed caching (ordered by timestamp/rank)",
            "Feed ranking uses ML models considering engagement, recency, and relationships",
            "Fan-out on write uses message queues for async distribution",
            "Pagination with cursor-based approach for infinite scroll",
        ],
        "interview_tips": [
            "Discuss both push and pull models, then propose hybrid",
            "Address the celebrity/hot user problem explicitly",
            "Mention ranking vs chronological ordering and trade-offs",
        ],
        "common_mistakes": [
            "Only considering one fan-out strategy without discussing trade-offs",
            "Not addressing the celebrity problem (millions of followers)",
            "Forgetting about feed ranking - most modern feeds aren't purely chronological",
        ],
        "youtube_keywords": "design news feed timeline Facebook Twitter system design interview",
        "diagram_description": "User creates post -> Post Service -> Fan-out Service (via Kafka) -> Writes to follower Feed Caches (Redis sorted sets). User opens feed -> Feed API -> Fetch from Redis cache -> Ranking Service reorders -> Return paginated feed.",
        "real_world_examples": [
            "Facebook uses a hybrid push/pull model with a sophisticated ML ranking algorithm",
            "Twitter uses a similar hybrid approach with their home timeline service",
            "Instagram switched from chronological to ML-ranked feed in 2016",
        ],
        "related_concepts": [5, 9, 15],
        "practice_questions": [
            "Design the news feed for a social media platform with 500M users",
            "How do you handle the celebrity problem in a fan-out on write system?",
            "Design a feed ranking system - what signals would you use?",
        ],
    },
    {
        "id": 24,
        "title": "Design a Notification System",
        "phase": 4,
        "difficulty": "medium",
        "estimated_minutes": 40,
        "frequency": "high",
        "tags": ["system-design", "interview", "messaging", "async"],
        "companies_asking": ["Amazon", "Google", "Meta", "Apple", "Uber"],
        "cheat_sheet": "Multi-channel: push, SMS, email. Priority queue for ordering. Template service for content. User preferences for opt-in/out. Rate limiting per user/channel. Retry with exponential backoff. Track delivery status. Use provider abstraction for vendor flexibility.",
        "explanation": """## Design a Notification System

### Requirements
- Multi-channel: Push notifications (iOS/Android), SMS, Email
- Different priority levels (urgent, normal, low)
- User notification preferences (opt-in/out per channel/type)
- Rate limiting (don't spam users)
- Delivery tracking and analytics
- Template management
- Scale: 10M notifications per day

### Architecture

**1. Notification Service (API)**
- Receives notification requests from other services
- Validates, enriches, and routes to appropriate channel

**2. Priority Queue**
- Message queue with priority levels
- Urgent notifications processed first
- Separate queues per channel (push, SMS, email)

**3. Template Service**
- Manages notification templates with variables
- Supports localization (multiple languages)
- A/B testing different message formats

**4. User Preferences Service**
- Stores per-user, per-channel, per-type preferences
- Quiet hours (don't disturb between 10pm-8am)
- Frequency caps (max 5 notifications per hour)

**5. Channel Workers**
- **Push**: APNs (iOS), FCM (Android)
- **SMS**: Twilio, AWS SNS
- **Email**: SendGrid, AWS SES
- Provider abstraction layer for easy switching

**6. Delivery Tracking**
- Track: queued, sent, delivered, opened, clicked
- Store in analytics DB for reporting
- Retry failed deliveries with exponential backoff""",
        "key_points": [
            "Decouple notification intake from delivery using message queues",
            "Priority queues ensure urgent notifications are delivered first",
            "User preferences and rate limiting prevent notification fatigue",
            "Provider abstraction enables switching between SMS/email/push vendors",
            "Retry with exponential backoff for transient delivery failures",
        ],
        "interview_tips": [
            "Cover all channels (push, SMS, email) and how they differ",
            "Discuss user preferences and rate limiting to show user-centric thinking",
            "Mention idempotency - avoid sending duplicate notifications",
        ],
        "common_mistakes": [
            "Not considering user preferences and sending unwanted notifications",
            "No rate limiting, leading to notification spam",
            "Not handling delivery failures with proper retry logic",
        ],
        "youtube_keywords": "design notification system push SMS email system design interview",
        "diagram_description": "Services send notification requests to Notification API. API checks user preferences, selects template, routes to Priority Queue. Channel workers (Push, SMS, Email) consume from queues and send via providers. Delivery tracker logs status.",
        "real_world_examples": [
            "Amazon sends billions of notifications daily across push, email, and SMS channels",
            "Uber sends real-time push notifications for ride updates with priority routing",
            "Slack aggregates notifications to avoid overwhelming users with batched delivery",
        ],
        "related_concepts": [9, 18, 17],
        "practice_questions": [
            "Design a notification system that handles push, SMS, and email at scale",
            "How would you prevent sending duplicate notifications?",
            "Design the user preferences system for notification opt-in/out",
        ],
    },
    {
        "id": 25,
        "title": "Design a Video Streaming Platform",
        "phase": 4,
        "difficulty": "hard",
        "estimated_minutes": 50,
        "frequency": "high",
        "tags": ["system-design", "interview", "streaming", "media"],
        "companies_asking": ["Netflix", "Amazon", "Google", "Meta", "Apple"],
        "cheat_sheet": "Upload: transcode video to multiple resolutions/codecs (async, with queue). Storage: S3 for source + transcoded. Delivery: CDN with adaptive bitrate streaming (HLS/DASH). Client adapts quality to bandwidth. Metadata in SQL/NoSQL. Recommendation engine for discovery.",
        "explanation": """## Design a Video Streaming Platform (like YouTube/Netflix)

### Requirements
- Video upload and processing
- Video streaming with adaptive quality
- Content recommendation
- Scale: 1B daily video views, 500K video uploads per day

### Key Components

**1. Video Upload & Processing Pipeline**
1. Client uploads video to object storage (S3) via pre-signed URL
2. Upload event triggers processing pipeline (via message queue)
3. **Transcoding service** converts to multiple formats:
   - Multiple resolutions: 360p, 480p, 720p, 1080p, 4K
   - Multiple codecs: H.264, H.265, VP9, AV1
   - Thumbnail generation
4. Transcoded files stored back in S3
5. Metadata updated in database when processing complete

**2. Video Streaming (Adaptive Bitrate)**
- **HLS (HTTP Live Streaming)** or **DASH**: Video split into small chunks (2-10 seconds)
- Client requests a manifest file listing available qualities
- Client dynamically switches quality based on bandwidth
- Served via CDN for low latency globally

**3. Content Delivery**
- CDN caches popular videos at edge locations
- Long-tail content served from origin
- Pre-warm CDN cache for anticipated popular content (new releases)

**4. Metadata & Search**
- Video metadata (title, description, tags) in SQL database
- Elasticsearch for video search
- View counts and engagement in separate analytics store

**5. Recommendation Engine**
- Collaborative filtering: users who watched X also watched Y
- Content-based filtering: recommend similar genres/topics
- Real-time signals: watch time, likes, completion rate""",
        "key_points": [
            "Transcoding is CPU-intensive - process asynchronously via message queue",
            "Adaptive bitrate streaming (HLS/DASH) adjusts quality to user's bandwidth",
            "CDN is critical for video delivery - popular content should be cached at edge",
            "Separate hot storage (popular videos on CDN) from cold storage (archive on S3)",
            "Video processing pipeline should be fault-tolerant with retry logic",
        ],
        "interview_tips": [
            "Walk through both upload/processing and streaming/playback flows",
            "Explain adaptive bitrate streaming and why it matters",
            "Discuss CDN strategy for different content popularity (hot vs cold)",
        ],
        "common_mistakes": [
            "Trying to process video synchronously during upload",
            "Not using adaptive bitrate streaming (fixed quality is terrible UX)",
            "Ignoring the CDN strategy for video delivery",
        ],
        "youtube_keywords": "design YouTube Netflix video streaming system design interview",
        "diagram_description": "Upload: Client -> S3 (raw) -> Kafka -> Transcoding Service (parallel workers) -> S3 (transcoded). Playback: Client -> CDN (cached chunks) -> Origin (S3). Manifest file lists available qualities. Client switches quality based on bandwidth.",
        "real_world_examples": [
            "Netflix transcodes every title into 1,200+ different quality/codec combinations",
            "YouTube processes 500+ hours of video uploaded every minute using distributed transcoding",
            "Twitch uses low-latency HLS for live streaming with ~2 second delay",
        ],
        "related_concepts": [8, 9, 13],
        "practice_questions": [
            "Design the video upload and processing pipeline for a streaming platform",
            "How does adaptive bitrate streaming work? Design the playback system.",
            "How would you handle live streaming vs on-demand content differently?",
        ],
    },
    {
        "id": 26,
        "title": "Design a Ride-Sharing Service",
        "phase": 4,
        "difficulty": "hard",
        "estimated_minutes": 50,
        "frequency": "high",
        "tags": ["system-design", "interview", "real-time", "geospatial"],
        "companies_asking": ["Uber", "Lyft", "Google", "Amazon", "Meta"],
        "cheat_sheet": "Geospatial indexing (geohash/quadtree) for nearby drivers. WebSocket for real-time location updates. Matching service pairs riders with drivers. ETA calculation using map data. Surge pricing based on supply/demand. Event-driven trip lifecycle.",
        "explanation": """## Design a Ride-Sharing Service (like Uber/Lyft)

### Requirements
- Riders request rides, matched with nearby drivers
- Real-time location tracking
- ETA and fare estimation
- Surge pricing based on demand
- Trip history and receipts
- Scale: 20M rides per day, 5M concurrent drivers

### Key Components

**1. Location Service**
- Drivers send location updates every 3-5 seconds via WebSocket
- Store in geospatial index (Redis with geohash, or QuadTree)
- Geohash: divide world into grid cells, nearby locations share prefixes

**2. Matching Service**
- Rider requests ride -> find nearby available drivers
- Score drivers by: distance, ETA, rating, acceptance rate
- Send ride request to best driver -> wait for acceptance
- If declined, move to next driver

**3. Trip Service**
- Manages trip lifecycle: REQUESTED -> MATCHED -> PICKUP -> IN_TRIP -> COMPLETED
- Event-driven state machine
- Stores trip data in database

**4. Pricing Service**
- Base fare + per mile + per minute
- **Surge pricing**: multiply base rate when demand > supply in a zone
- Fare estimate before ride confirmation

**5. ETA Service**
- Use map/routing data (Google Maps API or custom)
- Real-time traffic conditions
- Historical data for predictions

### Data Storage
- **Driver locations**: Redis with geospatial commands (GEOADD, GEORADIUS)
- **Trip data**: SQL database (PostgreSQL) for ACID transactions
- **Trip events**: Kafka for event streaming
- **Analytics**: Data warehouse for business intelligence""",
        "key_points": [
            "Geospatial indexing (geohash) enables efficient nearby driver queries",
            "WebSockets for real-time driver location updates (every 3-5 seconds)",
            "Trip lifecycle is an event-driven state machine",
            "Surge pricing balances supply and demand in real-time",
            "Driver matching considers distance, ETA, rating, and acceptance rate",
        ],
        "interview_tips": [
            "Start with the core flow: rider request -> driver matching -> trip lifecycle",
            "Explain geospatial indexing and why simple lat/lng queries don't scale",
            "Discuss the real-time aspects: WebSocket connections, location updates",
        ],
        "common_mistakes": [
            "Not using geospatial indexing (querying all drivers is too slow)",
            "Forgetting about driver-side state management (availability, current trip)",
            "Not handling race conditions in driver matching (two riders requesting same driver)",
        ],
        "youtube_keywords": "design Uber Lyft ride sharing system design interview geospatial",
        "diagram_description": "Rider app -> API Gateway -> Matching Service queries Driver Location Service (Redis geospatial). Best driver receives request via WebSocket. Trip Service manages lifecycle. Pricing Service calculates fare. All events flow through Kafka.",
        "real_world_examples": [
            "Uber uses H3 (hexagonal geospatial index) for efficient location queries",
            "Lyft processes millions of location updates per second using custom geospatial infrastructure",
            "Grab (Southeast Asian ride-sharing) handles 8M rides/day with geospatial sharding by city",
        ],
        "related_concepts": [9, 12, 17],
        "practice_questions": [
            "Design the driver matching system for a ride-sharing platform",
            "How would you implement surge pricing?",
            "Design the real-time location tracking system that handles 5M concurrent drivers",
        ],
    },
]


# ── Helper Functions ──

def get_concept_by_id(concept_id: int):
    """Get a single concept by its ID."""
    for c in SYSTEM_DESIGN_CONCEPTS:
        if c["id"] == concept_id:
            return c
    return None


def get_concepts_by_phase(phase: int):
    """Get all concepts in a given phase."""
    return [c for c in SYSTEM_DESIGN_CONCEPTS if c["phase"] == phase]


def get_concepts_by_tag(tag: str):
    """Get all concepts with a given tag."""
    return [c for c in SYSTEM_DESIGN_CONCEPTS if tag in c["tags"]]


def get_all_tags():
    """Get all unique tags across all concepts."""
    tags = set()
    for c in SYSTEM_DESIGN_CONCEPTS:
        tags.update(c["tags"])
    return sorted(tags)
