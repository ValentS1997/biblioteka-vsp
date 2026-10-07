# Source-confirmed design operations and implementation patterns

Scope: chapter 12 RAG only, PDF pages 1058–1109.

This chapter is about engineering methods rather than administration commands. The canonical operational artifact therefore records source-confirmed design actions and code patterns.

| Action / pattern | Type | Source-grounded purpose | Verification |
|---|---|---|---|
| define goals before implementation | design | constrain later architecture choices | goals/non-goals can be stated and tested |
| minimize primitive mechanisms | design | reduce interface and kernel complexity | richer operations can be composed without material loss |
| separate mechanism from policy | design | permit policy replacement | changing policy does not rewrite core mechanism |
| isolate hardware behind HAL-like layer | design | contain platform dependence | upper layer avoids direct device/platform assumptions |
| conditional compilation | build-time | select CPU/word-specific implementation from one source tree | each target builds only its selected branch |
| symbolic configuration constants | implementation | avoid embedded magic values | one configuration change updates all uses |
| indirection tables | implementation | decouple logical identity from physical implementation | remapping does not require caller changes |
| reusable alloc/free routines | implementation | share tested resource-management logic | same numbered-resource abstraction works across uses |
| reentrant procedures | concurrency | permit simultaneous/re-entered execution | shared state is protected or eliminated |
| error checks before resource acquisition | reliability | avoid partial-state cleanup leaks | failed validation leaves resource state unchanged |
| simple linear search for small tables | implementation | favor simplicity when data is small/rarely searched | measured cost stays negligible |
| cache correct results | performance | avoid repeated expensive computation/I/O | every cache hit is valid |
| use hints as untrusted accelerators | performance | retain speed without correctness dependency | hint is always revalidated |
| preserve locality | performance | reduce page/cache/storage costs | measured cache/page/I/O behavior improves |
| optimize common case | performance | put complexity where payoff is highest | common path improves; rare path remains correct |
| profile before optimization | performance | identify real bottlenecks | measurements justify the changed code |

## Source code pattern: orthogonal configuration

The chapter uses separate configuration concepts for CPU type and word length so a new architecture does not require modifying every size-dependent branch.

```c
#if (WORD_LENGTH == 32)
typedef int Register;
#endif

#if (WORD_LENGTH == 64)
typedef long Register;
#endif
```

Exact C type widths are compiler/platform assumptions from the source example and are not generalized beyond that context.

## Source rule: validate first

Preferred control flow:

```text
validate all failure conditions
        ↓
acquire resources
        ↓
perform operation
        ↓
publish success
```

This reduces error-path rollback complexity and prevents slow resource leakage caused by forgotten cleanup.

## Verification

A design change passes this chapter's standard when it reduces complexity or measurable cost without introducing hidden coupling, unrecoverable partial state or unjustified special cases.
