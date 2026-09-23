# Шпаргалка: веб-хостинг, HTTP, Apache, NGINX и HAProxy

## 1. Request path

~~~text
client
→ DNS
→ TLS/SNI
→ load balancer / proxy / cache
→ web server
→ application server
→ database/backend
→ response
~~~

A real site may combine several roles in one component. NGINX can act as web server, proxy, cache and load balancer.

## 2. HTTP transaction

Request:

~~~text
METHOD path HTTP/version
Headers

Body
~~~

Response:

~~~text
HTTP/version status-code text
Headers

Body
~~~

Important status classes:
- 1xx — processing/information;
- 2xx — success;
- 3xx — redirect/additional action;
- 4xx — client/request error;
- 5xx — server/runtime error.

## 3. HTTP methods

| Method | Chapter semantics |
|---|---|
| GET | get resource |
| HEAD | GET metadata without payload |
| POST | apply request data |
| PUT | replace/update resource; intended idempotent semantics |
| DELETE | delete resource |
| OPTIONS | show supported methods |

Do not assume method semantics alone guarantee safety; application behavior decides the effect.

## 4. URL safety

Web URL:
~~~text
scheme://[user[:password]@]host[:port][/path][?query][#anchor]
~~~

Avoid:
- passwords in URLs;
- sensitive values in query parameters.

Reasons from the chapter:
- URLs are logged;
- can be bookmarked/published;
- may appear in process output.

HTTP default port: 80.
HTTPS default port: 443.

## 5. curl diagnostics

~~~bash
curl -s -v -o /dev/null http://<host>
curl -H "Host: <vhost>" -s -v -o /dev/null <IP>
~~~

Use the second form to test the origin/virtual host independently of DNS.

Download:
~~~bash
curl -O <URL>
~~~

API/JSON example pattern:
~~~bash
curl <API-URL> | jq '.'
~~~

## 6. HTTP/1.1 vs HTTP/2

HTTP/1.1:
- persistent connections reduce TCP setup overhead.

HTTP/2:
- binary framing;
- multiplexes multiple transactions over one connection;
- fewer per-client connection overheads.

## 7. HTTPS and SNI

HTTP itself does not protect data in transit.

TLS adds transport encryption.

SNI sends the desired hostname during TLS setup so a server can select the certificate before HTTP Host is available.

Basic Auth:
- credentials are only encoded, not confidential;
- use only with HTTPS.

## 8. Web stack

~~~text
WAF
→ load balancer
→ cache
→ web server
→ application server
→ database
~~~

Every layer should avoid becoming a single point of failure when availability matters.

## 9. Load balancers

Purposes:
- distribute requests;
- remove unhealthy servers from rotation;
- permit maintenance without full-site downtime;
- optionally terminate TLS.

Algorithms covered:
- round robin;
- least load/connections;
- client-IP/hash affinity.

Health checks should test meaningful application state when possible, not only reachability.

## 10. Caching

Possible layers:
- browser cache;
- forward caching proxy;
- reverse caching proxy;
- CDN edge.

Important inputs:
- Cache-Control;
- ETag;
- Expires;
- response status;
- content characteristics.

Never-cache example:
~~~text
Cache-Control: no-cache, no-store
~~~

Stale-cache diagnosis:
~~~text
query origin directly
→ query reverse proxy/cache
→ query next cache layer
→ compare responses
~~~

Revalidation request:
~~~bash
curl -H "Cache-Control: no-cache" <URL>
~~~

## 11. CDN

CDN:
- places edge servers geographically near users;
- caches content near clients;
- uses DNS to direct users to an edge location;
- reduces latency and origin load.

Traditionally best suited to static assets, although the chapter notes dynamic capabilities as well.

## 12. Cloud hosting

Build yourself:
- maximum control;
- you own OS, patching, tuning, failure handling.

Managed service:
- less administrative work;
- less flexibility.

PaaS:
- deploy application package/code;
- provider manages much of infrastructure;
- shell/admin access may be limited.

Serverless pattern shown:
~~~text
DNS/CDN/static content
+
API Gateway
→ event function
→ database/backend
~~~

## 13. Apache httpd

Process model:
- root master may bind 80/443;
- lower-privilege workers handle requests.

Config:
- global directives;
- VirtualHost;
- Include/module fragments.

Baseline:

~~~bash
httpd -t
apachectl status
~~~

Controlled change:

~~~bash
apachectl graceful
~~~

Graceful reload preserves active connections while moving to new config.

## 14. Apache virtual hosts

Selection uses:
- HTTP Host;
- listening address/port.

Typical site-specific concepts:
- ServerName / aliases;
- DocumentRoot;
- Directory/Location;
- redirects/rewrites;
- logs;
- TLS certificate/key.

## 15. Apache Basic Auth

~~~bash
htpasswd -c /var/www/.htpasswd <user>
chmod 600 /var/www/.htpasswd
~~~

The password file must not be broadly readable.

Basic Auth without HTTPS is unsafe.

## 16. Apache logging

Access log exposes:
- client;
- timestamp;
- request method/path;
- status;
- response size;
- user agent.

Risk:
- high-volume logs can fill disk.

The chapter recommends isolating web logs so growth cannot consume the filesystem used by the rest of the system.

## 17. NGINX model

~~~text
master
→ workers
→ many event-driven connections
~~~

Config hierarchy:

~~~text
main
├─ events
└─ http
   └─ server
      └─ location
~~~

Key directives:
- listen;
- server_name;
- root;
- location;
- proxy_pass;
- include.

Check:
~~~bash
nginx -t
~~~

## 18. NGINX TLS / load balancing

TLS:
- certificate/key;
- TLS protocol selection;
- strong cipher configuration;
- server-side cipher preference.

Load balancing:

~~~text
upstream backend pool
→ proxy_pass
→ health checks
→ remove unhealthy backend
→ restore after successful check
~~~

## 19. HAProxy

Core config split:

~~~text
frontend
→ accepts client traffic
→ default_backend
→ backend
→ server pool
~~~

Health check:
- HTTP 200 means healthy in the simple example;
- non-200 removes server from pool;
- checks continue until recovery.

Stats UI can expose backend state and administrative enable/disable controls.

## 20. Sticky sessions

Preferred architecture:
- put session state in shared persistent storage.

If application state is local to a backend:
- HAProxy can insert a cookie;
- future requests return to the same backend.

Sticky sessions solve affinity, not the underlying state-design limitation.

## 21. TLS termination

~~~text
client HTTPS
→ HAProxy terminates TLS
→ HTTP or HTTPS to backend
~~~

Benefits described:
- offload crypto;
- reduce number of systems holding private key.

Risk:
- proxy-to-backend segment becomes a trust boundary.

## 22. Troubleshooting order

~~~text
1. curl/status/headers
2. DNS and direct-IP virtual-host check
3. TLS/SNI
4. load balancer health
5. cache/origin comparison
6. web-server syntax and logs
7. proxy/routing rules
8. application/backend
~~~

Do not alter several layers at once.

## 23. Rollback boundary

Source-supported inverse/controlled actions exist for some narrow cases, such as Apache module enable/disable.

Universal rollback is not defined for:
- Apache site/TLS changes;
- NGINX config;
- HAProxy config;
- cloud/PaaS/serverless changes.

Mark these [Needs confirmation].
