# Outcome Ladder

- Status: `DRAFT`
- Reflects revision:
- Grounding direction:
- Grounding authority:
- Ladder authority:
- Levels cumulative: `YES / NO / MIXED`
- Minimum useful stopping level:
- Refresh condition:

Outcome Ladder represents increasingly strong **observable project success**.

It is not Target authority, a Gap assessment, a Roadmap, task sequence, component decomposition, or execution Definition of Done.

## Authority inheritance

The ladder never has greater authority than its grounding direction.

```text
accepted direction
→ derived ladder under accepted authority

RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL
→ provisional ladder

ladder generation
→ cannot accept Target or authorize work
```

A stronger ladder level means stronger observable outcome, not stronger authority.

## Grounding evidence / constraints

Record accepted or recovered direction evidence, material non-goals, and constraints that bound the ladder.

Repository evidence alone must not create new TO-BE intent.

## Level template

Repeat as needed. A fixed number of levels is not required.

### Level <ID> — <name>

**Outcome statement**

What would be observably true if this level were achieved?

**Observable evidence**

What evidence would let a reviewer recognize that outcome?

**Material constraints / non-goals**

What remains explicitly outside this level?

**What stronger level adds**

State only if a stronger level exists.

## Ladder quality rules

Valid ladder content is outcome-shaped:

```text
A reviewer can use the supported boundary, observe deterministic failure behavior,
and reproduce representative evidence from documented setup.
```

Invalid ladder content is primarily task-shaped:

```text
implement API
add tests
write docs
```

Tasks may later serve an outcome. They are not ladder levels.

## Minimum useful stopping level

Identify the lowest level at which the bounded project can legitimately stop and still be useful.

Do not imply maximal ambition by default.

## Unresolved Target-boundary questions

If a material unresolved Target-boundary question changes the meaning of ladder outcomes, stop before presenting the ladder as stable.

Capability-design and research questions may remain downstream when Target meaning is stable.

## Downstream hand-off

State what later shaping may consume from this ladder.

Do not implement Adaptive Engagement, Strategy Portfolio, Target Skeleton, Executable Target Contract, Roadmap sequencing, or Change planning here.

## Freshness / reuse decision

Refresh only when grounding direction, authority, material constraints/non-goals, or the outcome meaning materially changes.
