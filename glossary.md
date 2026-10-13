---
title: Glossary
description: Plain-language definitions of the Logical Thinking Process terms and acronyms used across Reason Commons — the six trees, the kinds of statement in them, and the method's checks.
---

# Glossary

The [Logical Thinking Process](/ltp) comes with a lot of vocabulary and even more acronyms. You don't need any of it to use Reason Commons, but you will meet it in the guide, in the books, and in what the AI skills write. This page explains each term in a sentence or two. Every term has its own heading, so you can link straight to it — `reasoncommons.com/glossary#current-reality-tree`.

## Acronyms

| Acronym | Stands for |
|---|---|
| CLR | [Categories of Legitimate Reservation](#categories-of-legitimate-reservation) |
| CRT | [Current Reality Tree](#current-reality-tree) |
| CSF | [Critical Success Factor](#critical-success-factor) |
| DE | [Desired Effect](#desired-effect) |
| EC | [Evaporating Cloud](#evaporating-cloud) |
| FRT | [Future Reality Tree](#future-reality-tree) |
| IO | [Intermediate Objective](#intermediate-objective) — or, in "IO Map", the [Goal Tree](#goal-tree) |
| LTP | [Logical Thinking Process](#logical-thinking-process) |
| NBR | [Negative Branch Reservation](#negative-branch) |
| NC | [Necessary Condition](#necessary-condition) |
| PRT | [Prerequisite Tree](#prerequisite-tree) |
| TOC | [Theory of Constraints](#theory-of-constraints) |
| TRT | [Transition Tree](#transition-tree) |
| UDE | [Undesirable Effect](#undesirable-effect) |

## The method

### Theory of Constraints

TOC. A management approach developed by Eliyahu Goldratt from the 1980s. Its starting point: any system's performance is limited by a small number of constraints, so improving anything other than the constraint is mostly wasted effort. The Logical Thinking Process is its toolkit for finding and removing constraints that are policies and beliefs rather than machines.

### Logical Thinking Process

LTP. A set of six linked diagrams — the [trees](#the-six-trees) — for getting from "here is our goal and things are not going well" to "here is what we do on Monday", with every step argued in cause and effect. Codified by H. William Dettmer. See the [guide](/ltp) for an introduction.

### Constraint

The one thing that most limits a system from getting more of its goal. In the LTP it is usually a policy, habit or belief rather than a physical bottleneck, and the [Current Reality Tree](#current-reality-tree) is how you find it.

### Sufficiency logic

"If A, then B." Reading a link as *A is enough to cause B*. Used in the [Current Reality Tree](#current-reality-tree), [Future Reality Tree](#future-reality-tree) and [Transition Tree](#transition-tree). When one cause isn't enough on its own, several are joined with an **AND** (often drawn as an ellipse across the arrows).

### Necessity logic

"In order to have B, we must have A." Reading a link as *B cannot happen without A* — A is required, but not necessarily enough. Used in the [Goal Tree](#goal-tree), [Evaporating Cloud](#evaporating-cloud) and [Prerequisite Tree](#prerequisite-tree).

### Categories of Legitimate Reservation

CLR. The eight standard ways to challenge a link or a statement in a tree: clarity (do I understand it?), entity existence (is it actually true?), causality existence (does A really cause B?), cause insufficiency (is something else also needed?), additional cause (could something else cause B too?), cause–effect reversal (is it the other way round?), predicted effect existence (if A were true, what else would we see?), and tautology (is the effect being used as evidence of its own cause?). They are how a tree gets checked rather than just drawn.

### Negative branch

A chain of cause and effect showing that a proposed change also produces something bad. Raising one is a **Negative Branch Reservation** (NBR). It is built in the [Future Reality Tree](#future-reality-tree) and resolved with a further [injection](#injection) — the method's way of saying "yes, but…" constructively.

### Assumption

The unstated belief behind a link — why someone thinks A leads to B, or that B requires A. Surfacing assumptions is most of the work in an [Evaporating Cloud](#evaporating-cloud): a conflict breaks when one of them turns out to be false.

## The six trees

### Goal Tree

Also the **Intermediate Objectives Map** (IO Map). Shows what success is: the [goal](#goal) at the top, the [critical success factors](#critical-success-factor) beneath it, and the [necessary conditions](#necessary-condition) beneath those. Read with [necessity logic](#necessity-logic). It is the benchmark everything else is measured against. The app calls this view **goal**.

### Current Reality Tree

CRT. Explains why things are the way they are: starts from the [undesirable effects](#undesirable-effect) people can see and traces them back, through [intermediate causes](#intermediate-cause), to a few [root causes](#root-cause). Read with [sufficiency logic](#sufficiency-logic). The app calls this view **problem**; files call it `current_reality`.

### Evaporating Cloud

EC, also the **conflict cloud** or **conflict resolution diagram**. A five-box diagram of a dilemma: a shared objective, two [requirements](#requirement) it depends on, and two [prerequisites](#prerequisite) — the actions each requirement seems to demand — which conflict. Each arrow hides [assumptions](#assumption); finding a false one and an [injection](#injection) that replaces it makes the conflict "evaporate". The app calls this view **conflict**.

### Future Reality Tree

FRT. Tests a proposed change before you make it: starts from one or more [injections](#injection) and follows their effects forward to the [desired effects](#desired-effect), checking along the way for [negative branches](#negative-branch). Read with [sufficiency logic](#sufficiency-logic). The app calls this view **solution**; files call it `future_reality`.

### Prerequisite Tree

PRT. Plans how to make the change real: lists the [obstacles](#obstacle) in the way of an injection and, for each, an [intermediate objective](#intermediate-objective) that gets past it, then puts those objectives in order. Read with [necessity logic](#necessity-logic). The app calls this view **implement**; files call it `prerequisite`.

### Transition Tree

TRT. The step-by-step action plan: each step says what the situation is, why it needs to change, the action someone takes, and the effect they expect. Read with [sufficiency logic](#sufficiency-logic). The app calls this view **task**; files call it `transition`.

## What goes in the trees

### Goal

The single outcome the whole system exists to achieve — the top of the [Goal Tree](#goal-tree).

### Critical Success Factor

CSF. One of a handful of results that must all be true for the [goal](#goal) to hold. Remove any one and the goal fails.

### Necessary Condition

NC. Something a [critical success factor](#critical-success-factor) (or another necessary condition) depends on. The lower levels of the [Goal Tree](#goal-tree).

### Undesirable Effect

UDE (say "oody"). Something happening now that nobody wants, stated as a fact rather than a complaint — "customers wait more than a week for a reply", not "support is bad". The visible symptoms a [Current Reality Tree](#current-reality-tree) sets out to explain. A [Future Reality Tree](#future-reality-tree) may also show new UDEs a change would cause.

### Intermediate cause

A link in the middle of a causal chain in the [Current Reality Tree](#current-reality-tree): it causes something, and is itself caused by something further down.

### Root cause

A cause at the bottom of the [Current Reality Tree](#current-reality-tree) that the analysis doesn't trace any further — usually because it is a policy, belief or condition you could actually change.

### Critical root cause

The root cause (sometimes two or three) that accounts for most of the [undesirable effects](#undesirable-effect). Fixing it is where the leverage is. Close to what TOC means by the [constraint](#constraint).

### Requirement

In an [Evaporating Cloud](#evaporating-cloud), one of two needs that the shared objective depends on. Both are legitimate; the conflict is not between them but between the actions they seem to demand.

### Prerequisite

In an [Evaporating Cloud](#evaporating-cloud), the action one side thinks its [requirement](#requirement) demands. The two prerequisites are what actually conflict — "we must centralise" versus "we must not centralise". (Not to be confused with the [Prerequisite Tree](#prerequisite-tree).)

### Injection

A change you introduce into the system — a new policy, practice or condition — to break a conflict or produce a better future. Injections come out of the [Evaporating Cloud](#evaporating-cloud) and are tested in the [Future Reality Tree](#future-reality-tree).

### Desired Effect

DE. What becomes true once the [injections](#injection) are in place — usually the mirror image of an [undesirable effect](#undesirable-effect). The top of a [Future Reality Tree](#future-reality-tree).

### Obstacle

Something that currently stands in the way of an [injection](#injection) happening. Listed in the [Prerequisite Tree](#prerequisite-tree).

### Intermediate Objective

IO. A milestone that gets past a specific [obstacle](#obstacle) in the [Prerequisite Tree](#prerequisite-tree). (Confusingly, Dettmer also uses "intermediate objectives" for the whole [Goal Tree](#goal-tree) — the IO Map. Context usually tells you which.)

## Reason Commons terms

### Claim tree

Also **issue tree**. A top-level claim or question broken down into sub-claims, which are broken down in turn. It is a stable scaffold: documents come and go, but the tree stays, and evidence accumulates against it. See [claim tree annotation](/claim-tree-annotation).

### Annotation

A fragment quoted from a source document — a paper, a post, a comment thread — attached to the node in a [claim tree](#claim-tree) it bears on, with a link back to where it came from.

### Observation

A statement about the system whose purpose in the argument isn't yet clear. The honest label for a sentence that is clearly relevant but that you can't yet place as a cause, effect or condition.

### Evidence

A measurement or source cited to back up or challenge a statement in a tree.

### View

What a Reason Commons project file calls each of the six trees. A project holds all six views over one shared set of statements, so the same statement can appear in more than one.

### Role

What a statement is doing in a given view — a [goal](#goal), an [undesirable effect](#undesirable-effect), an [injection](#injection), and so on. The full list the project file accepts is in the [ltp-project skill's vocabulary](https://github.com/life-itself/reasoncommons/blob/main/skills/ltp-project/references/vocabulary.md).

## Read more

The [guide](/ltp) walks through a complete worked example, and the [reading list](/library) has the books — Dettmer's *The Logical Thinking Process* is the reference most of these definitions follow.
