---
inclusion: fileMatch
fileMatchPattern: "**/*.java"
---

# Java

Rules for Java services (Spring Boot, Maven/Gradle). Match existing package layout and libraries in the repo before introducing new patterns.

## Naming

| Context | Convention | Example |
| ------- | ---------- | ------- |
| Class, Interface, Enum, Record | PascalCase | `MemberService`, `MemberRepository` |
| Method, variable | camelCase | `getMemberById`, `isActive` |
| Constant (`static final`) | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Package | lowercase segments | `com.company.member.service` |
| Test class | `{Class}Test` or `{Class}Tests` | `MemberServiceTest` |

## Package Layout (Spring Boot)

Typical layers — follow what the repo already uses:

| Layer | Responsibility |
| ----- | -------------- |
| `controller` / `web` | HTTP mapping, status codes, delegation only |
| `service` | Business rules and orchestration |
| `repository` | Persistence (Spring Data JPA, etc.) |
| `dto` / `model` | Request/response and API shapes |
| `entity` / `domain` | Persistence models (when separate from DTOs) |
| `config` | Beans, security, infrastructure wiring |

Do not put business logic in controllers or entities.

## Spring Boot

- Use constructor injection (`@RequiredArgsConstructor` or explicit constructor); avoid field injection for required dependencies.
- Keep `@RestController` methods thin — validate input, call service, return DTO.
- Enable bean validation on request DTOs (`@Valid`, `@NotNull`, `@Size`, …).
- Use `@Transactional` on service methods that write data; keep transactions short.
- Externalize configuration (`application.yml` / env); never hardcode secrets.
- Use `@ControllerAdvice` for consistent exception → HTTP error mapping.

## DTOs and Entities

- Do not expose JPA entities directly from REST APIs — map to DTOs (MapStruct, manual mapper, or repo convention).
- Request and response DTOs are separate types when shapes differ.
- Use `record` for immutable DTOs on Java 16+ when the project already uses records.

## JPA / Hibernate (when the repo uses it)

- Repositories extend Spring Data interfaces; avoid raw `EntityManager` unless necessary.
- Use parameterized queries; never concatenate user input into JPQL/SQL.
- Fetch associations deliberately (`@EntityGraph`, `join fetch`) to avoid N+1.
- Schema changes via Flyway/Liquibase or the repo's migration tool — one logical change per migration.
- Do not modify applied migrations; add a new revision.

## Async and Concurrency

- Use `@Async` or reactive stack (`WebFlux`) only when the project already does.
- For blocking IO, use virtual threads or executor config only if the repo supports it — do not introduce without approval.
- Design scheduled jobs and message consumers to be idempotent.

## Logging and Security

- Use SLF4J (`log.info`, `log.error`); no `System.out.println` in production code.
- Never log passwords, tokens, or PII.
- Reuse existing Spring Security config; do not add parallel auth flows.

## Testing

- Unit tests: JUnit 5 + Mockito; mock repositories and external clients.
- Slice tests (`@WebMvcTest`, `@DataJpaTest`) when the repo uses them.
- Integration tests in a dedicated module/folder; no real external services in unit tests.
- Test method names describe behavior: `shouldRejectExpiredToken`.

## Build

- Match Maven (`pom.xml`) or Gradle (`build.gradle`) already in the repo.
- Pin dependency versions via BOM/parent or version catalog — no open ranges for production deps.
